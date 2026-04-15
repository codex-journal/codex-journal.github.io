[0588:h1] Knots: Source History Beyond Artifacts
[314a:h2] Origin
[cb1f:p]
  [57a8:s] Knots emerged from a concrete failure in AI-assisted theory drafting: agents could generate prose quickly, but the process could not preserve stable structure, source grounding, or intentional edit history well enough to keep a long argument coherent.
  [46ed:s] I hit that failure while drafting the essays that would relaunch Codex Journal, under pressure to turn years of ripe concepts and half-finished pieces into publishable work.
  [2560:s] Knots is the structured source versioning system that emerged in response to that breakdown, built to preserve local addressability, source grounding, replayable change history, and deterministic merge semantics beneath ordinary rendered documents.
[b5f5:p]
  [6638:s] The model usually proposed sentences, and sometimes paragraphs; I split, rewrote, recombined, and folded them back into the draft.
  [902a:s] I was working from my own source material, which was already metabolically dense and knotted: years of concepts, partial arguments, and half-finished pieces that were hard to serialize, complete, and distribute.
  [e7ea:s] The models could help there, not by supplying the concepts, but by absorbing enough of the semantic load to help untie and redistribute them into a workable sequence.
  [b4ec:s] The aim was to keep iterating until the prose broke the slop barrier; some lines were still written or finished by hand where cadence, compression, or conceptual alignment mattered too much to leave to stochastic fluency.
[6219:p]
  [6017:s] Under machine mediation, drafting and editing stop dividing cleanly.
  [45fe:s] Proposal, critique, local rewriting, conceptual recomposition, and acceptance are already collapsing into one structured source process.
  [9cfe:s] The model is not merely drafting and the human is not merely editing; authorship is being redistributed across a field of proposed units whose quality depends less on surface fluency than on how well they hold together structurally.
[a36c:p]
  [abe7:s] One-sentence-per-line was already a sensible technical-writing practice [@groenenOneSentencePerLine; @kreeftmeijerOneSentencePerLine]; once the writing process ran through an agent harness, those sentence boundaries needed stable local identity so the model could point, revise, move, and cite exact units without collapsing back into whole-document churn. That pressure was itself a smell: the problem had already become content-addressed before the tooling was willing to admit it.
[8175:p]
  [169f:s] I call the broader line source engineering: it treats source and artifact dialectically, as phases of a single compilation continuum rather than as separate reified processes.
  [2bfa:s] That occlusion is structural: intellectual property is still secured in part by obscuring derivation itself.
[518b:p]
  [984f:s] Pandoc was already in the background here: I was using it, and its Haskell implementation had already made writing look like a compiler-shaped problem, with source passing through intermediate structure, transforms, and multiple output surfaces [@MacFarlane_Pandoc].
  [9957:s] That also made Haskell feel less incidental than natural, because compiler-shaped and build-system thinking kept orbiting that language and its ecosystem.
[0372:p]
  [b723:s] Steve Yegge's [beads](https://github.com/steveyegge/beads) was already sharpening the engineering side of the same problem: it pulled planning and coordination back into the repository itself through a local-first model rather than a hosted workflow.
  [c7e7:s] JSONL was the durable state, the database was rebuilt as a view, and a custom merge driver let Git's ordinary branching model recede.
  [33c3:s] Remote collaboration still worked without requiring a server, and the whole system was already an attempt to treat model-assisted solo engineering as trackable work rather than mere improvisation.
  [b71a:s] Beads pointed toward a different coordination model: not a dependency graph fixed upstream in plan-driven fashion, and not dependencies pushed outward into process discipline, but a live coordination graph carried inside the repository itself.
  [5df5:s] But beads also exposed an architectural limit: without an explicit event model and with the database still too close to the practical control plane, replay remained secondary and history too soft to serve as the substrate itself.
[877c:p]
  [0829:s] Machine-mediated engineering changes what is scarce: generation becomes cheap, while evaluation, integration, dependency management, and provenance become the harder problem.
  [2ffb:s] That skips past the old waterfall and agile debate without simply resolving it.
  [2176:s] Both still assume planning, implementation, and review can remain partly separated in artifacts or process.
  [f663:s] Machine mediation collapses them into one live source workflow.
  [8164:s] But coordination is still not contradiction, and a repository-native graph is not yet a source process that can preserve conceptual conflict and reorganization as first-class history.
  [e220:s] Writing pressed harder on that limit, because prose does not decompose cleanly into planned units of work: outlines carry too much implicit state, and local revision reorganizes the whole faster than a coordination graph can represent.
  [9505:s] That was also why C. L. R. James's Hegelian use of knots supplied the eventual name [@jamesNotesOnDialectics1948].
  [cda7:s] The problem was not files, nodes, or blocks, but local stabilizations of meaning, reference, and revision hardening out of multiplicity into points of arrest and direction.
[e819:h2] Failure
[6b17:p]
  [e597:s] The problem was not generative throughput; it was that theory collapsed into unreplayable artifact churn, where local edits, source moves, and citation decisions disappeared behind successive draft surfaces.
[9c21:p]
  [dd46:s] The first workable primitive was stable short prefixes on sentence-sized units, but that emerged organically out of drafting pressure rather than from a prior design.
  [1ead:s] I moved to one-sentence-per-line because Git could at least track those units, and I needed stable sentence reference while revising with the model.
  [09e2:s] The model then started hallucinating short prefixes for that purpose, which was useful but brittle: I often wanted to move sentences across files, and duplicated ids immediately created derivation problems.
  [83e4:s] File-level and paragraph-level workflows were too coarse for iterative theory drafting, because they preserved rendered surfaces while obscuring the exact unit of intervention.
  [dce5:s] That wedge was built for theory drafting, but it immediately generalized beyond prose.
  [91dc:s] Any source domain that needs exact local addressability and replayable change can begin from the same move.
[dd40:p]
  [9137:s] The practical difference is that a sentence can be addressed directly, rewritten in place, moved relative to another sentence, or cited as a local source unit without first recovering it from line numbers, paragraph boundaries, or a full-document diff.
  [da1e:s] The rendered paragraph may change, but the operation remains anchored to a stable unit with its own derivation and placement history rather than to a transient textual surface.
[fb72:p]
  [4c5d:s] Recent empirical work on LLM-assisted writing points to the same failure from the artifact side: LLM revision workflows tend to flatten voice, shift stance, and steer distinct essays toward common semantic directions even when the task is framed as assistance rather than wholesale generation [@abdulhai2026llmsdistortwrittenlanguage].
  [7de0:s] That does not prove machine-mediated writing must work this way in principle, but it does show how quickly artifact-surface prompting produces the kind of distortion this system was built to prevent.
  [4976:s] The paper still studies an artifact contract rather than a source model, which is exactly the point: it can observe distortion at the rendered surface, but not preserve or audit the local transformations by which meaning changed.
[bdbb:h2] Substrate
[c834:p]
  [bc05:s] Putting the repository in Postgres [@nesbittGitInPostgres2026; @hoganAgentsPostgresCodebase2026] does not solve deterministic replay, intent-level conflict semantics, or trustworthy reconstruction of historical state.
  [68f7:s] The hard requirement is convergence under distributed writers with explicit causal evidence and replayable contracts, not the mere centralization of blobs in SQL.
  [68be:s] Git already subordinated files to a specialized database, but did so through a partly opaque event and projection model that still remains fundamentally shaped by the file-and-build era it emerged from.
[4747:p]
  [0135:s] The decisive shift is from treating source like a sequence of artifacts to treating it like a structured object graph, with semantic units written directly where that is possible and a separate composition layer preserving the arrangements, views, and editorial surfaces that authoring still requires.
  [542c:s] Language knots together meaning, reference, scope, and order.
  [e7e3:s] Knots exists to make those formations explicit enough to replay, transform, merge, render, and publish without collapsing them back into opaque textual wreckage.
  [d7a0:s] The immediate compatibility irony is that such a substrate still has to compile itself back into files and build directories for legacy toolchains; artifacts become backends rather than the truth.
[ef63:p]
  [bdc2:s] Knots therefore carries source history on explicit axes: `derivation` tracks content evolution, `composition` tracks placement and view, and `links` track reference.
  [338d:s] Those axes are orthogonal enough that collapsing them into one artifact history destroys intent: a `rewrite` changes derivation, a `move` changes composition, and a citation `retarget` changes links.
  [9eaf:s] Replay, merge, and trust all depend on keeping those operations distinct, because content change, arrangement change, and reference change should not masquerade as one another.
[0ea4:p]
  [ed24:s] Obsidian-style file-over-app systems and the ideology of a portable second brain diagnose one thing correctly: people want their notes back from hosted platforms and they want artifacts they can inspect and keep.
  [cbb3:s] But they largely leave the artifact boundary intact, treating markdown files, backlinks, folders, and graph views as the primary unit while relying on human memory and editorial habit to recover structure that is never made explicit enough for deterministic replay or machine-mediated composition.
  [99b1:s] They recover local control without leaving artifact-centricity behind.
[7713:p]
  [70a7:s] A purely content-addressed tree history, of the kind familiar from git or closer semantic relatives like Unison, can preserve committed states very well; what it does less naturally is preserve the fine-grained editorial intent, conflict holding, and replayable transformation semantics needed when source is revised as an active process rather than merely stored as successive snapshots.
  [4401:s] Git names and verifies committed states by Merkle ancestry and derives change from relations among snapshots; knots instead treats authored operations as the canonical historical object and derives state by replay.
  [c121:s] Darcs and later Pijul are closer precedents here than Git, because they treat patches or changes as primary historical objects, reason explicitly about commutation and dependence, and represent conflict as part of the history rather than only as a failed merge against snapshots.^[See Darcs, "Mergers documentation" (https://darcs.net/Theory/MergersDocumentation), Darcs, "Conflictors" (https://darcs.net/Theory/Conflictors), and Pijul, "Why Pijul" (https://pijul.org/manual/why_pijul.html).]
[eaa5:h2] Claims
[909e:p]
  [a19a:s] The durable object is history as a verifiable process; projections are rebuildable, and artifacts are caches.
  [3e0a:s] Conflict handling must classify competing intent against causal basis and preconditions, so sequential edits are not misclassified as concurrent conflicts.
  [f924:s] Publishability and downstream trust depend on explicit contracts for ordering, identity, and replay equivalence.
  [7bf3:s] Without that source discipline, machine-mediated systems become faster engines of irrecoverable confusion.
[b7a8:p]
  [e6ee:s] Merge is therefore not a secondary repair step but the central systems claim: not to abolish it but to make it inspectable, deterministic, and commensurate with the units of authored change.
[b0a0:p]
  [dbde:s] The same pattern appears under conflict: two competing edits to the same unit do not have to collapse into an opaque merge artifact or silent loss.
  [d833:s] Both can remain in recorded history, replay can hold the contested path out of clean state, and later resolution can promote one outcome without pretending the competing intent never existed.
[89de:p]
  [91f3:s] Writing is only the first proving ground.
  [8388:s] That is because conceptual reorganization remains cheapest in language.
  [a65c:s] Any domain in which agents act on structured source eventually becomes a problem of preserving identity while compiling the same underlying object graph into multiple valid views, semantic structures, artifacts, and releases.
[c506:p]
  [bd31:s] Knots therefore treats writing as structured source transformation rather than artifact editing and lets inference proceed compositionally rather than by reconstruction from artifacts.
[558f:p]
  [d800:s] The same logic should eventually reshape the interface itself: model output need not arrive as a flat token stream, but can be emitted as typed, locally addressable units with stable prefixes.
  [6660:s] A terminal or browser client could then expose those visible units with lightweight hinting, so quoting, selection, citation, and reply operate on exact source units instead of awkward textual recapture.
[8e89:p]
  [96b7:s] In the current sentence-prose authoring mode, paragraph replacement is deliberately higher-friction than sentence revision.
  [8fcb:s] That bias is useful: machine-mediated writing needs brakes against over-generation as much as it needs speed, and local sentence-level operations keep revision more accountable and inspectable.
[c534:h2] Program
[d0f9:p]
  [f815:s] The immediate task is to stabilize enough structure for serious writing now while leaving direct semantic writes, richer AST grammars, and the composition or view layer they require for the next phase.
  [81b1:s] Interoperability with git and files remains the adoption boundary, even as the longer path points beyond repository remotes toward a federated source-native network: replicated journals for the write truth, separately scaled read projections for serving and publication, and a forge model co-designed with the replication layer rather than bolted on afterward.
  [9a58:s] The same journal-first model is what makes a serious source server plausible at all: write truth can be replicated once through an append-oriented log while read and query planes scale separately, rather than forcing high-frequency source operations through repository snapshot mechanics.
[69f6:p]
  [ea49:s] The same structure also points toward a more direct knots editor: visible units should become directly selectable and revisable on the surface itself, rather than forcing every refinement back through prompt text or whole-document editing.
  [17c9:s] Where the grammar permits it, those surface edits should lower back into the same source model, so human and model share one structured editing substrate; sentence-prose already makes that direction legible even if it is not part of knots today.
[67d4:p]
  [28f3:s] At that scale, source, serving, and runtime state become distinct but related planes: the source journal remains canonical, read clusters pull context on demand and serve projections from the same underlying layer, and dynamic systems stay tethered to source rather than floating free of it.
  [1d76:s] A globally distributed source history is not a free good, because older regimes of publication stabilized reference partly through friction, latency, and institutional centralization; once those accidental stabilizers disappear, authority, citation stability, and conflict control become harder systems problems rather than inherited conveniences.
  [4cbc:s] Identity, trust boundaries, and artifact normalization then have to be built into the protocol and projection layers themselves if such a network is to remain historically intelligible.
[a89d:h2] Heresy
[f1f6:p]
  [76f8:s] AI-mediated writing has a glass ceiling of slop: it can produce text plausible enough to circulate while remaining too unstable, ungrounded, and unreplayable to sustain serious composition.
  [fa2e:s] Breaking that ceiling is an inference and computational problem, because the system has to preserve structure, provenance, and revision intent strongly enough that serious writing can exceed mere plausibility.
  [c9a1:s] The real ceiling is therefore not fluency but ontology: a system that can only emit plausible local units, but cannot sustain immanent conceptual fields or keep contradictions between totalities alive long enough to reorganize itself around them, will stall quickly whether it is writing prose or producing code.
  [576f:s] Knots is a heresy against that settlement.
  [8a64:s] It assumes trust should come from inspectable source history, replayable structure, and accountable transformations, not from the sacramental aura of toil that literary culture too often mistakes for seriousness.
[8428:p]
  [8305:s] Source engineering names two problems at once.
  [fa96:s] One is the engineering of source substrates themselves.
  [f185:s] The other is the engineering of the conceptual source conditions under which serious production can occur at all: the immanent fields, commitments, and contradictions that have to be sustained long enough for real reorganization to take place.
  [9a53:s] Knots therefore comes into its own less as a throughput engine than as an instrument of dialectical interrogation: a way to preserve local claims, sustain contradictions, and reorganize a developing position without losing the history of its revisions.
  [32a8:s] Theory now has to be pushed hard enough to keep pace with the transformations it is trying to understand, and that opening is part of what source engineering makes possible.
  [4006:s] But the same opening also extends the subsumptive surface itself: once theory, planning, and revision are drawn onto the productive source plane, the mediating layer of conceptual and editorial intelligence becomes more immediately available for capture.
  [e8f3:s] That is a horror for the institutional scholar and a boon for the autologist, and the contradiction should not be denied prematurely; it has to be pushed as far as it can go.
  [b12d:s] What the software engineer experiences as AI value vampirism and the institutional scholar experiences as the collapse of protected theoretical tempo are two faces of the same pressure.^[A concrete software-engineering symptom of this pressure appears in Steve Yegge's "The AI Vampire" (Feb. 11, 2026): https://steve-yegge.medium.com/the-ai-vampire-eda6e4f07163.]
  [d459:s] Both are classic signs of relative surplus value pressure as real subsumption advances into the mediating layer itself.
[1cfe:p]
  [396a:s] History does not become intelligible as a flat continuum. In James's sense it hardens into knots: local formations in which contradiction, reference, and direction are arrested long enough to be worked on. A materialist source system should encode those formations rather than leave them implicit in artifact surfaces.
  [4a09:s] That is also what this framework is for: to preserve, serialize, and distill complex concepts that ordinary social and editorial surfaces struggle to metabolize, without flattening away the tensions that make them worth thinking through in the first place.
[01e7:p]
  [42a2:s] Source cannot simply become the new fixed center either; the term remains overdetermined, naming event, origin, reference, artifact, and derivation at once.
[74e3:p]
  [9e13:s] By transumption I mean the case in which machine-mediated production begins to turn toward machine-facing outputs and recursively machine-conditioned development.
  [1431:s] Any domain with ready-made, verifiable outputs, stable evaluation harnesses, and little need for ontological innovation is correspondingly easier to transume; much of machine learning research now points in that direction.
  [b85b:s] Karpathy's autoresearch^[An overview of the project is available at https://deepwiki.com/karpathy/autoresearch.] is an especially legible emblem of that direction: not because it settles the model, but because his proof-of-concept repos reliably crystallize the discourse and infrastructure that capital is then likely to build around.
  [6cc4:s] Knots did not emerge from that case, but from the opposite one: theory and writing where contradiction, historical intelligibility, and ontological reorganization remain load-bearing, even if the same emphasis on replay, provenance, build, and verification could later prove useful in transumable domains as well.
[af50:h2] Opening
[72ff:p]
  [cd92:s] Access should open in phases rather than all at once.
  [e6b1:s] The right near-term model is invited inspection and a small circle of design partners: interested readers can inspect the repository, run the system, and help validate invariants, merge behavior, and implementation choices before the project opens more widely.
  [e62a:s] This is not scarcity theater; the code is still raw, the implementation still lags the spec, and the project still needs a first reduction pass on the agent-grown codebase.
[c165:p]
  [5056:s] Knots remains a research system rather than finished infrastructure.
  [76e1:s] Git remains a compatibility transport rather than a native journal protocol, canonical event arbitration still leans on ULID, and code-repository projection, branch or view semantics, identity, and forge or replication design remain incomplete.
  [4afe:s] These are not cosmetic gaps; they are part of the substantive program, including how a native source journal should coexist with classical databases serving the query path rather than becoming the truth themselves.
  [deb9:s] For now, knots should be understood as a working local authoring and sync system, not yet a complete forge or general-purpose version-control substrate.
[c639:p]
  [7e5c:s] Outside help should initially bias toward spec review, regression tests, replay and sync correctness, migration boundaries, and hot-path performance rather than broad stylistic cleanup.
  [fb3b:s] The current codebase is bloated, structurally rough, and in places clearly transitional because correctness, recoverability, and actual use were prioritized ahead of reduction, architectural cleanup, and non-functional polish.
  [2fa4:s] A wider public contribution model makes sense only after the first reduction pass, when the codebase is tighter, contribution boundaries are named, and the core contracts are legible enough that external patches do not dissolve the architecture into improvised local fixes.
[6974:p]
  [2fb3:s] Knots does not yet solve the full problem it has exposed.
  [215e:s] But it already makes one decisive shift real: writing can be organized against inspectable, replayable source history rather than against opaque artifact surfaces alone.
  [380e:s] That is enough to open a different editorial and computational horizon, even while the larger source engineering program remains unfinished.
[dcbd:h2] Contact
[6746:p]
  [1de7:s] For now, access is best handled directly.
  [9fc6:s] Email: [codexjournalinquiries@gmail.com](mailto:codexjournalinquiries@gmail.com). Instagram: [\@codexjournal](https://instagram.com/codexjournal). X: [\@sourceaware](https://x.com/sourceaware). GitHub: [codex-journal](https://github.com/codex-journal).
  [2031:s] Readers who want to inspect the code, try knots in its current state, or discuss the source engineering line are welcome to reach out there.
