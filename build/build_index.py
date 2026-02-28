#!/usr/bin/env python3
"""Generate index.html and feeds.html from templates + essay registry + feed sources."""

import argparse
import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = PROJECT_ROOT / "build" / "index-template.html"
DEFAULT_ESSAYS = PROJECT_ROOT / "_data" / "essays.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "index.html"
DEFAULT_FEEDS_CONFIG = PROJECT_ROOT / "_data" / "feeds.json"
DEFAULT_FEEDS_TEMPLATE = PROJECT_ROOT / "build" / "feeds-template.html"
DEFAULT_FEEDS_OUTPUT = PROJECT_ROOT / "feeds.html"


def load_essays(path):
    if not path.exists():
        print(f"Warning: {path} not found, using empty essay list", file=sys.stderr)
        return []
    with open(path) as f:
        data = json.load(f)
    return data.get("essays", [])


def load_feeds_config(path):
    if not path.exists():
        print(f"Warning: {path} not found, using empty feed list", file=sys.stderr)
        return []
    with open(path) as f:
        data = json.load(f)
    return [f for f in data.get("feeds", []) if f.get("active", True)]


def normalize_date(date_str):
    """Handle ISO 8601 (Atom) and RFC 822 (RSS) date formats -> YYYY-MM-DD."""
    if not date_str:
        return ""
    # Try ISO 8601 first (Atom feeds)
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass
    # Try "YYYY-MM-DD HH:MM:SS UTC" (GitHub Atom feeds)
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %Z")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass
    # Try RFC 822 (RSS feeds)
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        pass
    return date_str


def parse_atom(xml_data):
    """Parse Atom feed XML, return (feed_title, site_url, [entries])."""
    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    feed_title_el = root.find("atom:title", ns)
    feed_title = feed_title_el.text.strip() if feed_title_el is not None and feed_title_el.text else ""
    site_url = ""
    for link_el in root.findall("atom:link", ns):
        if link_el.get("rel", "alternate") == "alternate":
            site_url = link_el.get("href", "")
            break
    entries = []
    for entry in root.findall("atom:entry", ns):
        title_el = entry.find("atom:title", ns)
        link_el = entry.find("atom:link", ns)
        published_el = entry.find("atom:updated", ns)
        title = title_el.text if title_el is not None else ""
        link = link_el.get("href", "") if link_el is not None else ""
        published = published_el.text if published_el is not None else ""
        entries.append({"title": title, "link": link, "published": published})
    return feed_title, site_url, entries


def parse_rss(xml_data):
    """Parse RSS 2.0 feed XML, return (feed_title, site_url, [entries])."""
    root = ET.fromstring(xml_data)
    channel = root.find("channel")
    feed_title = ""
    site_url = ""
    if channel is not None:
        title_el = channel.find("title")
        feed_title = title_el.text.strip() if title_el is not None and title_el.text else ""
        link_el = channel.find("link")
        site_url = link_el.text.strip() if link_el is not None and link_el.text else ""
    entries = []
    for item in root.iter("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        pub_el = item.find("pubDate")
        title = title_el.text if title_el is not None else ""
        link = link_el.text if link_el is not None else ""
        published = pub_el.text if pub_el is not None else ""
        entries.append({"title": title, "link": link, "published": published})
    return feed_title, site_url, entries


def fetch_feed(config, timeout=10):
    """Fetch one feed, auto-detect Atom vs RSS, apply filters, return entries.

    Returns (resolved_name, [entries]). Feed title is extracted from the XML;
    config 'name' is used only as fallback.
    """
    url = config["url"]
    max_items = config.get("max_items", 10)
    filter_terms = [t.lower() for t in config.get("filter_exclude", [])]
    source_id = config["id"]
    fallback_name = config.get("name", source_id)

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "build_index/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml_data = resp.read()
    except Exception as e:
        print(f"Warning: failed to fetch feed {source_id}: {e}", file=sys.stderr)
        return fallback_name, []

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"Warning: failed to parse feed {source_id}: {e}", file=sys.stderr)
        return fallback_name, []

    # Auto-detect format from root tag
    tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
    if tag == "feed":
        feed_title, site_url, raw_entries = parse_atom(xml_data)
    elif tag == "rss":
        feed_title, site_url, raw_entries = parse_rss(xml_data)
    else:
        print(f"Warning: unknown feed format for {source_id}: <{root.tag}>", file=sys.stderr)
        return fallback_name, []

    source_name = feed_title or fallback_name

    entries = []
    for entry in raw_entries:
        title = entry.get("title", "")
        if filter_terms and any(term in title.lower() for term in filter_terms):
            continue
        entry["published"] = normalize_date(entry["published"])
        entry["source_id"] = source_id
        entry["source_name"] = source_name
        entry["source_site"] = site_url
        entries.append(entry)
        if len(entries) >= max_items:
            break

    return source_name, entries


def fetch_all_feeds(configs, timeout=10):
    """Fetch all active feeds, return ({feed_id: [entries]}, {feed_id: resolved_name})."""
    entries_by_id = {}
    names_by_id = {}
    for config in configs:
        name, entries = fetch_feed(config, timeout)
        entries_by_id[config["id"]] = entries
        names_by_id[config["id"]] = name
    return entries_by_id, names_by_id


def render_essay_entries(essays):
    if not essays:
        return ""
    parts = []
    for essay in essays:
        title = essay.get("title", "[Title]")
        link = essay.get("link", "#")
        author = essay.get("author", "")
        version = essay.get("current_version", "")
        date = essay.get("published_date", "")
        meta_parts = [p for p in [author, version, date] if p]
        meta = " &middot; ".join(meta_parts)
        parts.append(
            f'            <div class="essay-entry">\n'
            f'                <p class="essay-entry-title">\n'
            f'                    <a href="{link}">{title}</a>\n'
            f"                </p>\n"
            f'                <p class="essay-entry-meta">{meta}</p>\n'
            f"            </div>"
        )
    return "\n\n".join(parts)


def _site_label(url):
    """Extract a short label from a URL, e.g. 'https://nesbitt.io/foo' -> 'nesbitt.io'."""
    if not url:
        return ""
    from urllib.parse import urlparse
    host = urlparse(url).hostname or ""
    if host.startswith("www."):
        host = host[4:]
    return host


def render_activity_entry(entry, show_source=False):
    """Render a single activity entry div."""
    title = entry.get("title", "")
    link = entry.get("link", "")
    published = entry.get("published", "")
    source_name = entry.get("source_name", "")
    source_site = entry.get("source_site", "")
    meta_parts = [published]
    if show_source and source_name:
        meta_parts.append(source_name)
    site_label = _site_label(source_site)
    if site_label:
        meta_parts.append(site_label)
    meta = " &middot; ".join(p for p in meta_parts if p)
    return (
        f'            <div class="activity-entry">\n'
        f'                <p class="activity-entry-title">\n'
        f'                    <a href="{link}">{title}</a>\n'
        f"                </p>\n"
        f'                <p class="activity-entry-meta">{meta}</p>\n'
        f"            </div>"
    )


def render_activity_preview(all_entries, max_preview=5):
    """Merged timeline for index page, inside a collapsible <details>."""
    merged = []
    for entries in all_entries.values():
        merged.extend(entries)
    merged.sort(key=lambda e: e.get("published", ""), reverse=True)
    merged = merged[:max_preview]

    if not merged:
        return ""

    items = [render_activity_entry(e, show_source=True) for e in merged]
    entries_html = "\n\n".join(items)
    return (
        f'        <details class="activity-feed">\n'
        f'            <summary><span class="activity-feed-label">Feeds</span><span class="activity-feed-toggle"></span></summary>\n\n'
        f"{entries_html}\n\n"
        f'            <p class="activity-more"><a href="/feeds.html">more &rarr;</a></p>\n'
        f"        </details>\n"
    )


def render_feeds_sections(feeds_by_id, feeds_config, names_by_id):
    """Per-source sections for the feeds page, grouped by 'group' field."""
    from collections import OrderedDict
    groups = OrderedDict()
    for config in feeds_config:
        feed_id = config["id"]
        group = config.get("group", names_by_id.get(feed_id, feed_id))
        feed_name = names_by_id.get(feed_id, feed_id)
        entries = feeds_by_id.get(feed_id, [])
        if group not in groups:
            groups[group] = []
        groups[group].append((feed_name, entries))

    sections = []
    for group_name, feed_list in groups.items():
        items_parts = []
        for feed_name, entries in feed_list:
            if not entries:
                items_parts.append(f'            <p class="feed-empty">No entries available.</p>')
                continue
            # Show feed title as subtitle when multiple feeds in a group
            if len(feed_list) > 1:
                items_parts.append(
                    f'            <p class="feed-subtitle">{feed_name}</p>'
                )
            items_parts.extend(render_activity_entry(e) for e in entries)
        items_html = "\n\n".join(items_parts)

        sections.append(
            f'        <section class="feed-source">\n'
            f'            <p class="feed-source-label">{group_name}</p>\n\n'
            f"{items_html}\n"
            f"        </section>\n"
        )
    return "\n".join(sections)


def render_template(template, essay_html, activity_html):
    result = template.replace("{{ESSAY_ENTRIES}}", essay_html)
    result = result.replace("{{ACTIVITY_SECTION}}", activity_html)
    return result


def write_output(html, path):
    if path.exists():
        existing = path.read_text()
        if existing == html:
            print(f"No changes to {path}", file=sys.stderr)
            return False
    path.write_text(html)
    print(f"Wrote {path}", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate index.html and feeds.html")
    parser.add_argument("--no-feed", action="store_true", help="Skip all feed work")
    parser.add_argument("--feeds-config", type=Path, default=DEFAULT_FEEDS_CONFIG,
                        help="Feed registry JSON path")
    parser.add_argument("--feeds-output", type=Path, default=DEFAULT_FEEDS_OUTPUT,
                        help="Feeds page output path")
    parser.add_argument("--feeds-template", type=Path, default=DEFAULT_FEEDS_TEMPLATE,
                        help="Feeds page template path")
    parser.add_argument("--max-preview", type=int, default=5,
                        help="Max items in index activity preview")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Index output path")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="Index template path")
    parser.add_argument("--essays", type=Path, default=DEFAULT_ESSAYS, help="Essays JSON path")
    args = parser.parse_args()

    template = args.template.read_text()
    essays = load_essays(args.essays)
    essay_html = render_essay_entries(essays)

    if args.no_feed:
        activity_html = ""
        html = render_template(template, essay_html, activity_html)
        write_output(html, args.output)
        return

    # Fetch all feeds once
    feeds_config = load_feeds_config(args.feeds_config)
    feeds_by_id, names_by_id = fetch_all_feeds(feeds_config)

    # Render index with preview
    activity_html = render_activity_preview(feeds_by_id, args.max_preview)
    html = render_template(template, essay_html, activity_html)
    write_output(html, args.output)

    # Render feeds page
    feeds_template = args.feeds_template.read_text()
    feeds_section_html = render_feeds_sections(feeds_by_id, feeds_config, names_by_id)
    feeds_html = feeds_template.replace("{{FEEDS_SECTION}}", feeds_section_html)
    write_output(feeds_html, args.feeds_output)


if __name__ == "__main__":
    main()
