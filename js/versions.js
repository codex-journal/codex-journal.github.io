(function() {
  var path = location.pathname.replace(/\/index\.html$/, '/');
  var parts = path.split('/').filter(Boolean);
  var essayRoot = '/' + parts[0] + '/';
  var currentVersion = parts.length > 1 ? parts[1] : null;

  fetch(essayRoot + 'versions.json')
    .then(function(r) { return r.ok ? r.json() : null; })
    .then(function(data) {
      if (!data || !data.versions || data.versions.length < 2) return;
      var nav = document.getElementById('essay-versions');
      if (!nav) return;

      // Find current version label
      var current = currentVersion || data.versions[0].version;

      // Build dropdown
      var html = '<details class="version-dropdown">' +
        '<summary class="version-toggle">' + current + '</summary>' +
        '<ul class="version-list">';
      data.versions.forEach(function(v) {
        var active = v.version === current;
        html += '<li><a href="' + v.link + '"' +
                (active ? ' class="version-current"' : '') + '>' +
                '<span>' + v.version + '</span>';
        if (v.published_at) {
          html += ' <span class="version-date">' + v.published_at.split('T')[0] + '</span>';
        }
        html += '</a></li>';
      });
      html += '</ul></details>';
      nav.innerHTML = html;
    })
    .catch(function() {});
})();
