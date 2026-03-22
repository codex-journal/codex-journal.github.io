# Knots: Source History Beyond Artifacts

## Origin

Knots emerged from a concrete failure in AI-assisted theory drafting:
agents could generate prose quickly, but the process could not preserve
stable structure, source grounding, or intentional edit history well
enough to keep a long argument coherent. The failure surfaced while I
was drafting an essay advancing what I am calling source engineering,
which made the writing system itself evidence for the larger thesis.
Knots is the structured source versioning system that emerged in
response to that breakdown, built to preserve local addressability,
source grounding, replayable change history, and deterministic merge
semantics beneath ordinary rendered documents.

I call the broader line of work source engineering: parsing,
normalization, linkage, verification, and release become phases of one
compilation problem concerned with historical intelligibility rather
than artifacts alone.

Pandoc [@MacFarlane_Pandoc] was a direct source of inspiration here: it
made writing legible as a compilation and build pipeline with
intermediate structure, transforms, and multiple output surfaces. That
also made Haskell feel like a plausible implementation language for
knots, given Pandoc's own ecosystem and the typed, compiler-shaped
character of the problem.

The theory was diagnosing the breakdown of artifact-centric intellectual
production at the same time that multi-agent drafting made that
breakdown operationally intolerable.

The drafting workflow was neither autonomous generation nor solitary
hand composition: agents usually proposed sentences, and sometimes
paragraphs, which were then split, rewritten, recombined, and folded
back into the draft. The aim was to keep iterating until the prose broke
the slop barrier; some lines were still written or finished by hand
where cadence, compression, or conceptual alignment mattered too much to
leave to stochastic fluency.

This workflow does not divide cleanly into drafting and editing.
Proposal, critique, local rewriting, conceptual recomposition, and
acceptance are already collapsing into one structured source process.
The model is not merely drafting and the human is not merely editing;
authorship is being redistributed across a field of proposed units whose
quality depends less on surface fluency than on how well they hold
together structurally.

Before knots existed, the pressure was already visible in the raw draft
form itself: One-sentence-per-line was already a sensible
technical-writing practice
[@groenenOneSentencePerLine; @kreeftmeijerOneSentencePerLine]; once the
writing process ran through an agent harness, those sentence boundaries
needed stable local identity so the model could point, revise, move, and
cite exact units without collapsing back into whole-document churn. That
pressure was itself a smell: the problem had already become
content-addressed before the tooling was willing to admit it.

``` text
[f8fb] Contemporary capital's machine intelligence stack recovers information in spite of history, not because of it.
[d5a5] History must be normalized before it can be subsumed.
[20ec] The transformer is architecturally historicidal: it systematically murders history to produce information.
[0d3c] Historical knowledge is not contained in artifacts alone; it is reproduced through apperception, the unifying act by which a subject synthesizes heterogeneous sources into a coherent judgment.
```

The problem was that this structure was real, but the surrounding
toolchain still treated it as a flat artifact.

Steve Yegge's [beads](https://github.com/steveyegge/beads) supplied a
more concrete architectural influence: it pulled planning and
coordination back into the repository itself through a local-first model
rather than a hosted workflow. JSONL was the durable state, the database
was rebuilt as a view, and a custom merge driver let Git's ordinary
branching model recede. Remote collaboration still worked without
requiring a server, and the whole system was already an attempt to treat
model-assisted solo engineering as trackable work rather than mere
improvisation. Beads pointed toward a different coordination model: not
a dependency graph fixed upstream in plan-driven fashion, and not
dependencies pushed outward into process discipline, but a live
coordination graph carried inside the repository itself. But beads also
exposed an architectural limit: without an explicit event model and with
the database still too close to the practical control plane, replay
remained secondary and history too soft to serve as the substrate
itself.

Machine-mediated engineering changes what is scarce: generation becomes
cheap, while evaluation, integration, dependency management, and
provenance become the harder problem. That skips past the old waterfall
and agile debate without simply resolving it. Both still assume
planning, implementation, and review can remain partly separated in
artifacts or process. Machine mediation collapses them into one live
source workflow. But coordination is still not contradiction, and a
repository-native graph is not yet a source process that can preserve
conceptual conflict and reorganization as first-class history. Writing
pressed harder on that limit, because prose does not decompose cleanly
into planned units of work: outlines carry too much implicit state, and
local revision reorganizes the whole faster than a coordination graph
can represent.

The eventual name came through C. L. R. James's Hegelian use of knots:
formations that harden out of multiplicity into points of arrest and
direction. Knots was closer to the problem than files, nodes, or blocks
because the system needed to preserve those local stabilizations of
meaning, reference, and revision.

## Failure

The problem was not generative throughput; it was that theory collapsed
into unreplayable artifact churn, where local edits, source moves, and
citation decisions disappeared behind successive draft surfaces.

The first workable primitive was stable short hash prefixes on
sentence-sized units: an agent could point to a specific sentence,
rewrite it, move it, or cite it without diff-hunting through whole
files. File-level and paragraph-level workflows were too coarse for
iterative theory drafting, because they preserved rendered surfaces
while obscuring the exact unit of intervention. That wedge was built for
theory drafting, but it immediately generalized beyond prose. Any source
domain that needs exact local addressability and replayable change can
begin from the same move.

The practical difference is that a sentence like \[dd46:s\] can be
addressed directly, rewritten in place, moved relative to another
sentence, or cited as a local source unit without first recovering it
from line numbers, paragraph boundaries, or a full-document diff. The
rendered paragraph may change, but the operation remains anchored to a
stable unit with its own derivation and placement history rather than to
a transient textual surface.

## Substrate

Putting the repository in Postgres
[@nesbittGitInPostgres2026; @hoganAgentsPostgresCodebase2026] does not
solve deterministic replay, intent-level conflict semantics, or
trustworthy reconstruction of historical state. The hard requirement is
convergence under distributed writers with explicit causal evidence and
replayable contracts, not the mere centralization of blobs in SQL. Git
already subordinated files to a specialized database, but did so through
a partly opaque event and projection model that still remains
fundamentally shaped by the file-and-build era it emerged from.

The decisive shift is from treating source like a sequence of artifacts
to treating it like a structured object graph, with semantic units
written directly where that is possible and a separate composition layer
preserving the arrangements, views, and editorial surfaces that
authoring still requires. Language knots together meaning, reference,
scope, and order. Knots exists to make those formations explicit enough
to replay, transform, merge, render, and publish without collapsing them
back into opaque textual wreckage. The immediate compatibility irony is
that such a substrate still has to compile itself back into files and
build directories for legacy toolchains; artifacts become backends
rather than the truth.

A purely content-addressed tree history, of the kind familiar from git
or closer semantic relatives like Unison, can preserve committed states
very well; what it does less naturally is preserve the fine-grained
editorial intent, conflict holding, and replayable transformation
semantics needed when source is revised as an active process rather than
merely stored as successive snapshots. Git names and verifies committed
states by Merkle ancestry and derives change from relations among
snapshots; knots instead treats authored operations as the canonical
historical object and derives state by replay. Darcs and later Pijul are
closer precedents here than Git, because they treat patches or changes
as primary historical objects, reason explicitly about commutation and
dependence, and represent conflict as part of the history rather than
only as a failed merge against snapshots
[@darcsMergersDocumentation; @darcsConflictors; @pijulWhyPijul].

## Claims

The durable object is history as a verifiable process; projections are
rebuildable, and artifacts are caches. Conflict handling must classify
competing intent against causal basis and preconditions, so sequential
edits are not misclassified as concurrent conflicts. Publishability and
downstream trust depend on explicit contracts for ordering, identity,
and replay equivalence. As source production becomes increasingly
agentic, inspectable state and rebuildable history stop being luxuries
and become the minimum condition for trust; otherwise higher write
velocity merely turns opaque control planes into faster engines of
irrecoverable confusion.

Merge is therefore not a secondary repair step but the central systems
claim: not to abolish it but to make it inspectable, deterministic, and
commensurate with the units of authored change.

The same pattern appears under conflict: two competing edits to the same
unit do not have to collapse into an opaque merge artifact or silent
loss. Both can remain in recorded history, replay can hold the contested
path out of clean state, and later resolution can promote one outcome
without pretending the competing intent never existed.

Writing is only the first proving ground. That is because conceptual
reorganization remains cheapest in language. Any domain in which agents
act on structured source eventually becomes a problem of preserving
identity while compiling the same underlying object graph into multiple
valid views, semantic structures, artifacts, and releases.

Knots therefore treats writing as structured source transformation
rather than artifact editing and lets inference proceed compositionally
rather than by reconstruction from artifacts.

The same logic should eventually reshape the interface itself: model
output need not arrive as a flat token stream, but can be emitted as
typed, locally addressable units with stable prefixes. A terminal or
browser client could then expose those visible units with lightweight
hinting, so quoting, selection, citation, and reply operate on exact
source units instead of awkward textual recapture.

In the current sentence-prose authoring mode, paragraph replacement is
deliberately higher-friction than sentence revision. That bias is
useful: machine-mediated writing needs brakes against over-generation as
much as it needs speed, and local sentence-level operations keep
revision more accountable and inspectable.

## Scope

This memo is scoped to knots as a systems response to the breakdown of
artifact-level writing workflows. It asks why knots exists, which
guarantees it must provide, and which failures it has to prevent.

This memo stays inside one narrow wedge of that argument: prose exposed
the problem first, but the machinery is grammar-agnostic by design, even
though code-repository projection, forge semantics, and branch or view
mechanics are not yet complete. Review and promotion semantics, fuller
branching, build-system integration, and networked source infrastructure
belong to the larger line, but not to this memo.

Obsidian-style file-over-app systems and the ideology of a portable
second brain diagnose one thing correctly: people want their notes back
from hosted platforms and they want artifacts they can inspect and keep.
But they largely leave the artifact boundary intact, treating markdown
files, backlinks, folders, and graph views as the primary unit while
relying on human memory and editorial habit to recover structure that is
never made explicit enough for deterministic replay or machine-mediated
composition. They recover local control without leaving
artifact-centricity behind.

The broader inquiry reaches beyond prose tooling into build systems,
archives, normalization, and verification, including inherited artifacts
such as OCRed sources; it asks how historical intelligibility can be
made public, reproducible, and forkable under machine-mediated
production.

Knots remains a research system rather than finished infrastructure,
because the underlying problems it is trying to solve are still open.
Git remains a compatibility transport rather than a native journal
protocol, canonical event arbitration still leans on ULID, and
code-repository projection, branch or view semantics, identity, and
forge or replication design all remain incomplete. These are not
cosmetic gaps; they are part of the substantive program, including how a
native source journal should coexist with classical databases serving
the query path rather than becoming the truth themselves.

Its current architecture is transitional but already sufficient for real
editorial workflows, and a larger re-architecture remains possible,
including structured migration, without fundamentally changing the
user-facing mode of work. Knots should presently be understood as a
working local authoring and sync system, not yet a complete forge or
general-purpose version-control substrate.

## Program

The immediate task is to stabilize enough structure for serious writing
now while leaving direct semantic writes, richer AST grammars, and the
composition or view layer they require for the next phase.
Interoperability with git and files remains the adoption boundary, even
as the longer path points beyond repository remotes toward a federated
source-native network: replicated journals for the write truth,
separately scaled read projections for serving and publication, and a
forge model co-designed with the replication layer rather than bolted on
afterward. The same journal-first model is what makes a serious source
server plausible at all: write truth can be replicated once through an
append-oriented log while read and query planes scale separately, rather
than forcing high-frequency source operations through repository
snapshot mechanics.

The same structure also points toward a more direct knots editor:
visible units should become directly selectable and revisable on the
surface itself, rather than forcing every refinement back through prompt
text or whole-document editing. Where the grammar permits it, those
surface edits should lower back into the same source model, so human and
model share one structured editing substrate; sentence-prose already
makes that direction legible even if it is not part of knots today.

At that scale, source, serving, and runtime state become distinct but
related planes: the source journal remains canonical, read clusters pull
context on demand and serve projections from the same underlying layer,
and dynamic systems stay tethered to source rather than floating free of
it. A globally distributed source history is not a free good, because
older regimes of publication stabilized reference partly through
friction, latency, and institutional centralization; once those
accidental stabilizers disappear, authority, citation stability, and
conflict control become harder systems problems rather than inherited
conveniences. Identity, trust boundaries, and artifact normalization
then have to be built into the protocol and projection layers themselves
if such a network is to remain historically intelligible.

ATproto is a useful adjacent response to the post-platform internet
because it federates identity and records through a shared protocol
rather than leaving them trapped inside platforms. Knots asks the
analogous question for historical source: not how to federate social
presence after platforms, but how to federate source, projection, and
trust once artifacts stop being an adequate unit of the network.

## Heresy

AI-mediated writing has a glass ceiling of slop: it can produce text
plausible enough to circulate while remaining too unstable, ungrounded,
and unreplayable to sustain serious composition. Breaking that ceiling
is an inference and computational problem, because the system has to
preserve structure, provenance, and revision intent strongly enough that
serious writing can exceed mere plausibility. The real ceiling is
therefore not fluency but ontology: a system that can only emit
plausible local units, but cannot sustain immanent conceptual fields or
keep contradictions between totalities alive long enough to reorganize
itself around them, will stall quickly whether it is writing prose or
producing code. Knots is a heresy against that settlement. It assumes
trust should come from inspectable source history, replayable structure,
and accountable transformations, not from the sacramental aura of toil
that literary culture too often mistakes for seriousness. Source cannot
simply become the new fixed center either; the term remains
overdetermined, naming event, origin, reference, artifact, and
derivation at once.

Source engineering names two problems at once. One is the engineering of
source substrates themselves. The other is the engineering of the
conceptual source conditions under which serious production can occur at
all: the immanent fields, commitments, and contradictions that have to
be sustained long enough for real reorganization to take place. Knots
therefore comes into its own less as a throughput engine than as an
instrument of dialectical interrogation: a way to preserve local claims,
sustain contradictions, and reorganize a developing position without
losing the history of its revisions. Theory now has to be pushed hard
enough to keep pace with the transformations it is trying to understand,
and that opening is part of what source engineering makes possible. But
the same opening also extends the subsumptive surface itself: once
theory, planning, and revision are drawn onto the productive source
plane, the mediating layer of conceptual and editorial intelligence
becomes more immediately available for capture. That is a horror for the
institutional scholar and a boon for the autologist, and the
contradiction should not be denied prematurely; it has to be pushed as
far as it can go. What the software engineer experiences as AI value
vampirism and the institutional scholar experiences as the collapse of
protected theoretical tempo are two faces of the same pressure.[^1] Both
are classic signs of relative surplus value pressure as real subsumption
advances into the mediating layer itself.

By transumption I mean the case in which machine-mediated production
begins to turn toward machine-facing outputs and recursively
machine-conditioned development. Any domain with ready-made, verifiable
outputs, stable evaluation harnesses, and little need for ontological
innovation is correspondingly easier to transume; much of machine
learning research now points in that direction. Karpathy's
autoresearch[^2] is an especially legible emblem of that direction: not
because it settles the model, but because his proof-of-concept repos
reliably crystallize the discourse and infrastructure that capital is
then likely to build around. Knots did not emerge from that case, but
from the opposite one: theory and writing where contradiction,
historical intelligibility, and ontological reorganization remain
load-bearing, even if the same emphasis on replay, provenance, build,
and verification could later prove useful in transumable domains as
well.

## Opening

Access should open in phases rather than all at once. The right
near-term model is invited inspection and a small circle of design
partners: interested readers can inspect the repository, run the system,
and help validate invariants, merge behavior, and implementation choices
before the project opens more widely. This is not scarcity theater; the
code is still raw, the implementation still lags the spec, and the
project still needs a first reduction pass on the agent-grown codebase.

Outside help should initially bias toward spec review, regression tests,
replay and sync correctness, migration boundaries, and hot-path
performance rather than broad stylistic cleanup. The current codebase is
bloated, structurally rough, and in places clearly transitional because
correctness, recoverability, and actual use were prioritized ahead of
reduction, architectural cleanup, and non-functional polish. A wider
public contribution model makes sense only after the first reduction
pass, when the codebase is tighter, contribution boundaries are named,
and the core contracts are legible enough that external patches do not
dissolve the architecture into improvised local fixes.

Knots does not yet solve the full problem it has exposed. But it already
makes one decisive shift real: writing can be organized against
inspectable, replayable source history rather than against opaque
artifact surfaces alone. That is enough to open a different editorial
and computational horizon, even while the larger source engineering
program remains unfinished.

## Contact

For now, access is best handled directly. Email:
[email](mailto:codexjournalinquiries@gmail.com). Instagram:
[codexjournal](https://instagram.com/codexjournal). X:
[sourceaware](https://x.com/sourceaware). GitHub:
[codex-journal](https://github.com/codex-journal). Readers who want to
inspect the code, try knots in its current state, or discuss the source
engineering line are welcome to reach out there. The software is already
usable, but the repository and contribution surface are still being
reduced and clarified before a fuller public release.

[^1]: A concrete software-engineering symptom of this pressure appears
    in Steve Yegge's "The AI Vampire" (Feb. 11, 2026):
    https://steve-yegge.medium.com/the-ai-vampire-eda6e4f07163.

[^2]: An overview of the project is available at
    https://deepwiki.com/karpathy/autoresearch.
