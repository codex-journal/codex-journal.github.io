# Knots: Source History Beyond Artifacts

## Origin

Knots emerged from a concrete failure in AI-assisted theory drafting:
agents could generate prose quickly, but the process could not preserve
stable structure, source grounding, or intentional edit history well
enough to keep a long argument coherent. I hit that failure while
drafting the essays that would relaunch Codex Journal, under pressure to
turn years of ripe concepts and half-finished pieces into publishable
work. Knots is the structured source versioning system that emerged in
response to that breakdown, built to preserve local addressability,
source grounding, replayable change history, and deterministic merge
semantics beneath ordinary rendered documents.

The model usually proposed sentences, and sometimes paragraphs; I split,
rewrote, recombined, and folded them back into the draft. I was working
from my own source material, which was already metabolically dense and
knotted: years of concepts, partial arguments, and half-finished pieces
that were hard to serialize, complete, and distribute. The models could
help there, not by supplying the concepts, but by absorbing enough of
the semantic load to help untie and redistribute them into a workable
sequence. The aim was to keep iterating until the prose broke the slop
barrier; some lines were still written or finished by hand where
cadence, compression, or conceptual alignment mattered too much to leave
to stochastic fluency.

Under machine mediation, drafting and editing stop dividing cleanly.
Proposal, critique, local rewriting, conceptual recomposition, and
acceptance are already collapsing into one structured source process.
The model is not merely drafting and the human is not merely editing;
authorship is being redistributed across a field of proposed units whose
quality depends less on surface fluency than on how well they hold
together structurally.

One-sentence-per-line was already a sensible technical-writing practice
[@groenenOneSentencePerLine; @kreeftmeijerOneSentencePerLine]; once the
writing process ran through an agent harness, those sentence boundaries
needed stable local identity so the model could point, revise, move, and
cite exact units without collapsing back into whole-document churn. That
pressure was itself a smell: the problem had already become
content-addressed before the tooling was willing to admit it.

I call the broader line source engineering: it treats source and
artifact dialectically, as phases of a single compilation continuum
rather than as separate reified processes. That occlusion is structural:
intellectual property is still secured in part by obscuring derivation
itself.

Pandoc was already in the background here: I was using it, and its
Haskell implementation had already made writing look like a
compiler-shaped problem, with source passing through intermediate
structure, transforms, and multiple output surfaces
[@MacFarlane_Pandoc]. That also made Haskell feel less incidental than
natural, because compiler-shaped and build-system thinking kept orbiting
that language and its ecosystem.

Steve Yegge's [beads](https://github.com/steveyegge/beads) was already
sharpening the engineering side of the same problem: it pulled planning
and coordination back into the repository itself through a local-first
model rather than a hosted workflow. JSONL was the durable state, the
database was rebuilt as a view, and a custom merge driver let Git's
ordinary branching model recede. Remote collaboration still worked
without requiring a server, and the whole system was already an attempt
to treat model-assisted solo engineering as trackable work rather than
mere improvisation. Beads pointed toward a different coordination model:
not a dependency graph fixed upstream in plan-driven fashion, and not
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
can represent. That was also why C. L. R. James's Hegelian use of knots
supplied the eventual name [@jamesNotesOnDialectics1948]. The problem
was not files, nodes, or blocks, but local stabilizations of meaning,
reference, and revision hardening out of multiplicity into points of
arrest and direction.

## Failure

The problem was not generative throughput; it was that theory collapsed
into unreplayable artifact churn, where local edits, source moves, and
citation decisions disappeared behind successive draft surfaces.

The first workable primitive was stable short prefixes on sentence-sized
units, but that emerged organically out of drafting pressure rather than
from a prior design. I moved to one-sentence-per-line because Git could
at least track those units, and I needed stable sentence reference while
revising with the model. The model then started hallucinating short
prefixes for that purpose, which was useful but brittle: I often wanted
to move sentences across files, and duplicated ids immediately created
derivation problems. File-level and paragraph-level workflows were too
coarse for iterative theory drafting, because they preserved rendered
surfaces while obscuring the exact unit of intervention. That wedge was
built for theory drafting, but it immediately generalized beyond prose.
Any source domain that needs exact local addressability and replayable
change can begin from the same move.

The practical difference is that a sentence can be addressed directly,
rewritten in place, moved relative to another sentence, or cited as a
local source unit without first recovering it from line numbers,
paragraph boundaries, or a full-document diff. The rendered paragraph
may change, but the operation remains anchored to a stable unit with its
own derivation and placement history rather than to a transient textual
surface.

Recent empirical work on LLM-assisted writing points to the same failure
from the artifact side: LLM revision workflows tend to flatten voice,
shift stance, and steer distinct essays toward common semantic
directions even when the task is framed as assistance rather than
wholesale generation [@abdulhai2026llmsdistortwrittenlanguage]. That
does not prove machine-mediated writing must work this way in principle,
but it does show how quickly artifact-surface prompting produces the
kind of distortion this system was built to prevent. The paper still
studies an artifact contract rather than a source model, which is
exactly the point: it can observe distortion at the rendered surface,
but not preserve or audit the local transformations by which meaning
changed.

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

Knots therefore carries source history on explicit axes: `derivation`
tracks content evolution, `composition` tracks placement and view, and
`links` track reference. Those axes are orthogonal enough that
collapsing them into one artifact history destroys intent: a `rewrite`
changes derivation, a `move` changes composition, and a citation
`retarget` changes links. Replay, merge, and trust all depend on keeping
those operations distinct, because content change, arrangement change,
and reference change should not masquerade as one another.

Obsidian-style file-over-app systems and the ideology of a portable
second brain diagnose one thing correctly: people want their notes back
from hosted platforms and they want artifacts they can inspect and keep.
But they largely leave the artifact boundary intact, treating markdown
files, backlinks, folders, and graph views as the primary unit while
relying on human memory and editorial habit to recover structure that is
never made explicit enough for deterministic replay or machine-mediated
composition. They recover local control without leaving
artifact-centricity behind.

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
only as a failed merge against snapshots.[^1]

## Claims

The durable object is history as a verifiable process; projections are
rebuildable, and artifacts are caches. Conflict handling must classify
competing intent against causal basis and preconditions, so sequential
edits are not misclassified as concurrent conflicts. Publishability and
downstream trust depend on explicit contracts for ordering, identity,
and replay equivalence. Without that source discipline, machine-mediated
systems become faster engines of irrecoverable confusion.

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

History does not become intelligible as a flat continuum. In James's
sense it hardens into knots: local formations in which contradiction,
reference, and direction are arrested long enough to be worked on. A
materialist source system should encode those formations rather than
leave them implicit in artifact surfaces. That is also what this
framework is for: to preserve, serialize, and distill complex concepts
that ordinary social and editorial surfaces struggle to metabolize,
without flattening away the tensions that make them worth thinking
through in the first place.

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
protected theoretical tempo are two faces of the same pressure.[^2] Both
are classic signs of relative surplus value pressure as real subsumption
advances into the mediating layer itself.

By transumption I mean the case in which machine-mediated production
begins to turn toward machine-facing outputs and recursively
machine-conditioned development. Any domain with ready-made, verifiable
outputs, stable evaluation harnesses, and little need for ontological
innovation is correspondingly easier to transume; much of machine
learning research now points in that direction. Karpathy's
autoresearch[^3] is an especially legible emblem of that direction: not
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

Knots remains a research system rather than finished infrastructure. Git
remains a compatibility transport rather than a native journal protocol,
canonical event arbitration still leans on ULID, and code-repository
projection, branch or view semantics, identity, and forge or replication
design remain incomplete. These are not cosmetic gaps; they are part of
the substantive program, including how a native source journal should
coexist with classical databases serving the query path rather than
becoming the truth themselves. For now, knots should be understood as a
working local authoring and sync system, not yet a complete forge or
general-purpose version-control substrate.

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
<codexjournalinquiries@gmail.com>. Instagram:
[@codexjournal](https://instagram.com/codexjournal). X:
[@sourceaware](https://x.com/sourceaware). GitHub:
[codex-journal](https://github.com/codex-journal). Readers who want to
inspect the code, try knots in its current state, or discuss the source
engineering line are welcome to reach out there.

# References {#bibliography .unnumbered}

[^1]: See Darcs, "Mergers documentation"
    (https://darcs.net/Theory/MergersDocumentation), Darcs,
    "Conflictors" (https://darcs.net/Theory/Conflictors), and Pijul,
    "Why Pijul" (https://pijul.org/manual/why_pijul.html).

[^2]: A concrete software-engineering symptom of this pressure appears
    in Steve Yegge's "The AI Vampire" (Feb. 11, 2026):
    https://steve-yegge.medium.com/the-ai-vampire-eda6e4f07163.

[^3]: An overview of the project is available at
    https://deepwiki.com/karpathy/autoresearch.
