# Trial-reel A/B method — generate the overlay×image matrix + track which combos win — build & feasibility research

- **Candidate id:** `trial-reel-ab-method`
- **Date:** 2026-06-14
- **Source of the ask:** roadmap STILL-TO-RESEARCH → Content-ops (`docs/plans/2026-06-14-overnight-roadmap.md` line 92) + vault `obsidian/Elijah's vault/20-Content/Ideas/Trial reel methods.md`.
- **The vault note, in full (2 lines):** "Posting the same successful text overlay on multiple different pictures" / "Posting different trial overlays on the same successful picture." That is the whole idea — a deliberate overlay×image A/B grid run as **trial reels** (IG's non-follower test surface), with a winner picked on data.

---

## Verdict: ADD-NOW — but build ONLY the MEASURE half; the GENERATE+PUBLISH half is ADD-LATER and Elijah-gated

**One-line:** The genuinely cheap, high-leverage, gate-free slice is a **scorer/tracker** — group the trial reels Elijah already runs into A/B experiments (by a tag in the caption or a tiny sidecar file), score each variant on the *correct 2026 signals* via the just-built `ig-dashboard/metrics2026.py`, and declare a winner with an n-floor honesty check. That closes the loop the metric engine was built for, adds **zero new dependencies**, is **read-only over the official API**, and writes a vault idea note — pure hub-native plumbing. The **matrix-generation** half (rendering N overlay×image variants) and the **publish-as-trial** half are a separate, later, Elijah-gated track because (a) generation is real image-compositing work and (b) API-publishing collides with Standing Rule 1 and the original-audio API constraint.

**The decisive feasibility facts (this is what makes the measure-half ADD-NOW):**

1. **Trial reels expose the SAME insights endpoint as regular reels.** Metrics (views, reach, likes, comments, shares, saves, watch-time, completion) come back from `GET /{ig-media-id}/insights` for a trial reel exactly as for a normal reel — confirmed by PostFast ("you get the same metrics and graduation options") and Phyllo. **This means `metrics2026.py` already works on trial reels unchanged** — no new metric code, the 2026 rate/score/gate contract just applies.
2. **`media_product_type` is the field that distinguishes a trial reel** (Meta docs: "request its `media_product_type` field" to determine reel type), so `refresh.py` can *tag* trial reels and the scorer can *filter* to them. (Caveat below — needs a live probe to confirm the exact returned value; the literature does not pin the string.)
3. **Trial reels are fully API-publishable** via `trial_params: { "graduation_strategy": "MANUAL" | "SS_PERFORMANCE" }` on the `media_type=REELS` container (Meta official docs + Postproxy). So the *publish* half is technically possible later — it's gated by policy (Standing Rule 1) and the audio constraint, not by capability.

**Two honest corrections to the candidate's framing:**

- **The audio constraint does NOT block this candidate** (it would block a "trending-audio trial" idea, but not this one). The hub rule is: API-published reels are **original-audio / voice-only** — no Instagram music-library tracks via API ("No trending sounds, no catalogue music… must be embedded in the video file before upload"). This candidate's A/B variable is **overlay text × cover image**, with audio *held constant* by design. So the constraint is irrelevant to the experiment — in fact a held-constant original-audio track is *correct* experimental hygiene. Don't let the audio rule scare you off this one.
- **"Generate the matrix" is the expensive, lower-value half; "track which combos win" is the cheap, high-value half.** Generating overlay×image variants is image compositing (Pillow, or Higgsfield/HyperFrames) — doable but it's craft work that competes with the editing suite Elijah already has, and rendering the wrong variants fast is not the bottleneck. The bottleneck Elijah actually has is **measuring fairly on the right signals** — which is exactly what the metric engine unlocked yesterday and what nothing currently does.

**Why ADD-NOW (the measure half):** (a) zero new deps — pure stdlib over `store.json` + a one-field add to `refresh.py`, same shape as `metrics2026.py` and the intel scripts; (b) read-only official API, no scraping, no writes, no new token scope; (c) it's the **literal payoff the metric engine was built to enable** — "score the A/B combos on skip/share/save instead of likes, closing the loop"; (d) trial reels are the single best lever for a creator chasing non-follower reach, and Elijah is at 100k chasing exactly that.

**Rough effort:** Measure half — Phase 0 ≈ 1–2 hrs (group + score + winner from existing data); Phase 1 ≈ ½-day (tag trial reels in `refresh.py` + experiment sidecar + vault idea-note writer). Generate+publish half (ADD-LATER) — Phase 2 ≈ ½–1 day for a Pillow variant-renderer that stops at files; the publish step is Elijah-gated and per-action-confirmed, never automated.

---

## What it actually is / what it does

A **trial reel** is Instagram's native, built-in A/B test surface: a reel shown **only to non-followers**, never on your feed, so you can test cold-reach performance before committing to a real post (Meta launched it Dec 2024; public accounts, 1,000+ followers — Elijah qualifies at ~100k). After ~24h you see views/likes/comments/shares; after ~72h you can **graduate** it to followers manually, or let IG auto-share if it performs (the `SS_PERFORMANCE` strategy). **Instagram explicitly allows running multiple trials simultaneously "for A/B testing: same topic, different hook or format, see which drives higher engagement rate before committing"** (inro.social) — i.e. the platform *designed in* exactly the matrix the vault note describes.

The candidate turns that native capability into a measured, repeatable hub workflow:

| Vault method | Variable held constant | Variable swept | What it isolates |
|---|---|---|---|
| Same overlay × N images | text overlay (a proven hook) | the cover/background image | which **visual** wins for a known-good hook |
| Same image × N overlays | the image (a proven visual) | the text overlay / hook line | which **hook** wins for a known-good visual |

The winning signal must be the **2026 priority order**, not likes: for trial reels specifically, the field-recommended North Stars are **average watch time + share rate** ("Likes feel good but tell you very little"; "Watch time tells you the algorithm wants to keep showing this; shares tell you viewers want others to see it" — socialchamp / fliki). That is precisely the `metrics2026.py` model (skip-gate → share > like > save), so the scorer is a *consumer* of the metric engine, not new logic.

### What the candidate is NOT
- It is **not** a new model or scraper. The metrics already exist; the work is grouping + relative scoring + an honesty floor.
- It is **not** a publishing bot. The hub never auto-publishes; this stops at "here is the winner, here's the draft note" and (later) "here are the rendered variants in `out/`."

---

## Windows + OneDrive feasibility + dependency weight

**Measure half — GREEN across the board (same profile as `metrics2026.py`):**
- **Dependencies:** none. Pure stdlib (`json`, `statistics`) reusing `metrics2026.rates()/score_2026()/build_distributions()`. No torch, no cv2, no cloud, no paid API, no model download.
- **OneDrive:** safe — small modules that `import`, no heavy imports that hang on the synced disk.
- **Secrets:** none new — reuses `INSTAGRAM_ACCESS_TOKEN`; the only API delta is adding `media_product_type` (and, if exposed, a trial flag) to the fields `refresh.py` already requests. Read-only, rides the existing token + `CALL_SLEEP` rate budget.
- **Scheduled task:** none new — folds into the existing daily `refresh.py` run / `Daily Agent Refresh.bat`.

**Generate+publish half — YELLOW, and deliberately deferred:**
- **Variant rendering** is light if done with **Pillow** (pure-Python image compositing; MIT-equivalent HPND license; ~3MB wheel, no torch/cv2) — overlay text on a cover image is exactly Pillow's wheelhouse and is OneDrive-safe. *Or* reuse the existing Higgsfield/HyperFrames/`caption-engine` suite (already wired) for richer variants — but that's heavier and not needed for a static cover-card A/B. **Recommend Pillow** for the cheap path.
- **Publishing** is the only real friction and it is **policy, not tech**: API publish needs a **public `video_url`** (a trial reel is still a reel container, so it needs a hosted video, not a still — see Risks), API reels are **original-audio only**, and **Standing Rule 1 forbids the publish click without per-action confirmation**. So publishing stays manual/confirmed; the hub's job ends at rendered files + a checklist.

---

## Integration sketch — how it composes with the hub

**Composes tightest with the thing built yesterday: `ig-dashboard/metrics2026.py`.** The scorer is a thin consumer of it. Nothing here re-implements a metric.

### New file: `ig-dashboard/trial_ab.py` (the scorer/tracker — the ADD-NOW artifact)
Pure-ish, reads `store.json` (read-only) + an experiment sidecar, imports `metrics2026`:

```python
import metrics2026 as m   # reuse the 2026 contract verbatim

# An "experiment" = a group of posts that share an experiment id and a swept var.
# Source of the grouping (cheapest first):
#   (a) a tag Elijah puts in the caption, e.g. "#abx_hookA_img3" -> parsed, OR
#   (b) a sidecar ig-dashboard/experiments.json mapping experiment_id -> [permalinks]
# Each variant carries: which_held (overlay|image), variant_label, is_trial flag.

def score_experiment(posts_in_group, distributions):
    """Rank the variants of ONE A/B experiment by the 2026 score, with an
    n-floor + reach-floor honesty gate so we don't crown noise."""
    ranked = m.rank_posts(posts_in_group, distributions)   # reuses metric engine
    # honesty: a trial reel's non-follower reach is structurally small/slow
    # (a trial may pull ~180 views where a normal reel pulls ~3000 day 1),
    # so require a minimum reach per variant before declaring a winner.
    return annotate_with_confidence(ranked, MIN_REACH=500)

def winner(ranked):
    """Top variant IF it clears MIN_REACH and beats #2 by a margin; else
    'inconclusive — keep running'. Compares share_rate + watch-time first
    (the trial-reel North Stars), score_2026 as the tiebreak composite."""
```

**Data shapes:** input is the exact post dicts `refresh.py` stores (`{insights:{reach,shares,saved,...}, like_count, comments_count, media_product_type, ...}`) plus a tiny grouping. Output is `{experiment_id, held, variants:[{label, score, rates, skip_grade, reach, confidence}], winner|inconclusive}`. No schema migration — it reads what's already stored, exactly like `metrics2026.py`.

### Wiring (smallest blast radius first)
1. **`ig-dashboard/refresh.py`** — add `media_product_type` to the media-fields request (so each post carries its reel-type) and, if a live probe confirms a trial flag is exposed, capture it. This is a one-line field add — the same pattern as the metric engine's `reels_skip_rate` add. *(Probe first; if trials are NOT distinguishable in the API list, fall back to caption-tag grouping — see Risks.)*
2. **`ig-dashboard/experiments.json`** (new, tiny, hand- or skill-written) — `experiment_id -> {held, variants:[{permalink, label}]}`. This is the durable record of "these N posts were one A/B grid." Cheap, human-editable, version-friendly.
3. **`trial_ab.py` CLI** — `python trial_ab.py` prints each active experiment's ranked variants + winner/inconclusive; matches the `metrics2026.py --n` CLI style and the intel scripts' report style.
4. **Vault idea-note writer** — on a decisive winner, write/update a note in `20-Content/Ideas/` using `_templates/idea.md` **verbatim** (`type: idea`, `domain: content`, `stage: raw`, `status: open`) — body holds "winner = overlay A on image 3, +X% share-rate vs #2, n=… reach=…". Never invent a property; never a new `type`. This is the same vault-write discipline `news-update-system` and `carousel-builder` already follow.
5. **Skills that consume it:** `weekly-content-plan` (Step-3 arbitrage gains a "proven winners to scale to a full post" input — a trial winner is the strongest possible signal to graduate); `reel-analytics` (reports A/B results in 2026 terms); `niche-intel` (optional — feed winning hooks back to the swipe file). `carousel-builder` is a natural downstream (a winning hook → carousel).

### Generate+publish half (ADD-LATER) — `trial_ab_render.py`
- Pillow composites the swept variants (text overlay on cover image, or N covers under one overlay) into `out/` as still cards → but a **trial reel is still a video container**, so a still must be wrapped to a short video (ffmpeg, already on the box) before it can be published as a reel. Stops at files in `out/`.
- A printed **publish checklist** (not an action): "to run this as a trial grid, in-app or via confirmed API call set `trial_params.graduation_strategy=MANUAL`, original audio only, then confirm each publish." **No automated publish, ever** (Standing Rule 1).

---

## Phased build sketch

**Phase 0 — the scorer over EXISTING data (≈1–2 hrs). THE ADD-NOW WIN.**
- Write `ig-dashboard/trial_ab.py`: `score_experiment()`, `winner()`, confidence/honesty gate, all built on `metrics2026.rank_posts()`. Read grouping from a hand-made `experiments.json` (even one real past grid, or a synthetic one) + caption-tag fallback parser.
- Tiny inline `--self-test` over a couple hand-made experiment dicts (matches `metrics2026.py` style, no test framework).
- **Done = given a group of variants, the hub names the 2026-correct winner (or honestly says "inconclusive, n too low"), with zero new deps.** This is the metric engine's payoff made concrete.

**Phase 1 — tag trial reels + write the vault note (≈½-day). THE LOOP CLOSED.**
- Probe the live API for whether a trial reel is distinguishable (run `refresh.py`-style call with `media_product_type`; inspect a real trial reel if Elijah has one, else document the caption-tag path as primary).
- Add `media_product_type` to `refresh.py`'s media fields; capture a trial flag if exposed.
- Wire the `20-Content/Ideas/` idea-note writer (template verbatim) on a decisive winner.
- Add one bullet to `weekly-content-plan` Step 3: "graduate proven trial winners to full posts."
- **Done = run a trial grid → next dashboard refresh tags + scores it → a winner note lands in the vault for Elijah to graduate. Fully read-only, no publish.**

**Phase 2 (ADD-LATER, Elijah-gated) — variant renderer (≈½–1 day).**
- `trial_ab_render.py` with Pillow: generate the overlay×image grid into `out/` (+ ffmpeg still→short-video wrap so they're reel-publishable). Stops at files + a manual publish checklist.
- **Gate:** only worth it once Elijah confirms he wants the hub generating variants rather than hand-making them in the editing suite; and only after he's run ≥1 trial grid by hand so the measure-half has proven useful.

**Non-goals:** no automated publishing of any kind; no "trending-audio" trial path (API can't, and it's out of scope); no predicted-winner forecasting (that's the unproven audience-sim track — this scores *observed* variants only).

---

## Risks & honest caveats

- **Standing Rule 1 hard-walls the publish step.** Trial reels are API-publishable, but the publish click is Elijah's, per-action. The hub stops at "winner identified" (Phase 0–1) and "variants rendered to `out/` + checklist" (Phase 2). Never wire an auto-publish, even with `SS_PERFORMANCE` graduation — graduation is a *publish*.
- **Trial-reel detection in the API is not confirmed-by-source.** Meta says use `media_product_type` to classify reels, but the literature does **not** pin the exact string a trial reel returns (and trial reels may not even appear in the normal `/media` edge until graduated, since they're feed-hidden). **Mitigation:** make caption-tag grouping (`#abx_…`) the *primary* grouping mechanism and treat any API trial flag as a bonus. A live probe in Phase 1 settles it. Do not block Phase 0 on this — Phase 0 works purely off `experiments.json` + tags.
- **Small-n is the real statistical trap.** Non-follower trial reach is structurally small and slow (a trial may pull ~180 views where a normal reel pulls ~3,000 on day 1 — socialchamp/fliki). Declaring "overlay A wins" off 150 vs 180 views is noise. **Mitigation:** the `winner()` honesty gate requires a reach floor + a margin over #2, and otherwise returns "inconclusive — keep running." Be loud about this in the report; an over-confident winner is worse than none.
- **Confounding if more than one variable moves.** The whole value is *one* swept variable (overlay XOR image) with everything else — audio, length, posting time, caption — held constant. **Mitigation:** the experiment record stores `held` explicitly and the renderer (Phase 2) enforces a single swept axis; flag any experiment where variants differ on >1 axis as "not a clean A/B."
- **Audio constraint (clarified, not a blocker here):** API reels are original-audio/voice-only. This candidate holds audio constant, so it's fine — but if Elijah ever wants to A/B *trending audio*, that cannot be API-published (must be done in-app), and that's a different idea.
- **Don't double-count vs the in-app trial comparison.** Instagram already shows "how this trial compares to previous trials" in-app. The hub's added value is the **2026-correct scoring** (skip/share/save, relative to his 300-post distribution) and the **vault paper trail / graduation hand-off**, not re-deriving raw counts. If Elijah only ever reads the in-app screen, Phase 0's value is the durable, queryable record + the right metric; say so honestly.
- **ToS / ban risk: none for the measure half.** Read-only over the official API with the existing token, arithmetic on owned data, vault writes. Trial reels are a first-party Meta feature and API-publishing them via `trial_params` is documented and supported — no scraping, no automation-of-engagement, no shadow-ban surface. The only risk surface is the publish step, which stays manual + confirmed.

---

## Sources

- **Trial reels overview, eligibility (1k+ followers, Dec-2024 launch), A/B / multi-trial design, North-Star metrics (watch time + share rate over likes):** https://www.socialchamp.com/blog/instagram-trial-reels/ · https://fliki.ai/blog/trial-reels-instagram · https://www.inro.social/blog/what-is-a-reel-trial-and-how-does-it-work · https://hiketop.com/en/blog/instagram-trial-reels-explained
- **Official Meta docs — trial reels are API-publishable via `trial_params` (`graduation_strategy` MANUAL / SS_PERFORMANCE); use `media_product_type` to classify reels; 100 API publishes / 24h:** https://developers.facebook.com/docs/instagram-platform/content-publishing/ · https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media/
- **Trial reels expose the SAME insights + graduation via API (the fact that makes `metrics2026.py` apply unchanged):** PostFast — https://postfa.st/blog/instagram-trial-reels · Metricool — https://metricool.com/instagram-trial-reels/ · Instagram for Creators — https://creators.instagram.com/blog/instagram-trial-reels
- **Reels insights field set (plays/reach/likes/saves/comments/shares/completion) on `GET /{ig-media-id}/insights`:** https://www.getphyllo.com/post/a-complete-guide-to-the-instagram-reels-api · https://www.getphyllo.com/post/real-time-reels-analytics-using-instagram-reels-api-iv
- **API publishing details + the original-audio-only constraint (no music library via API) + `trial_params` JSON shape + 24h limit:** https://postproxy.dev/blog/instagram-reels-api-publishing-guide/
- **Scheduling/publishing trial reels via third-party tools (confirms it behaves like a native trial, same metrics + graduation):** https://postfa.st/blog/instagram-trial-reels · https://metricool.com/instagram-trial-reels/
- **Hub code this composes with:** `ig-dashboard/metrics2026.py` (the 2026 rate/score/skip-gate contract — verified on disk, 300 reels, keyed on `store.json`), `ig-dashboard/refresh.py` (stores `media_product_type`, `insights{views,reach,saved,shares,...}`, `like_count`, `comments_count` per post), `intel/competitor-radar.py` (engine/report style template), `obsidian/Elijah's vault/_templates/idea.md` (verbatim vault contract), `weekly-content-plan` / `reel-analytics` / `niche-intel` / `carousel-builder` skills. Companion plan: `docs/plans/2026-06-14-ig-2026-algorithm-metric-engine-research.md`.
