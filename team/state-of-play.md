# 2026 State of Play — @elijahaifl

> The strategic synthesis the agent reads before any content/business planning, alongside
> `profile.md` (who he is), `stats.md` (live numbers), and `memory.md` (learnings). This file
> is **decisive on purpose**: it says what to do, when, and why — and tags every load-bearing
> claim with its evidence tier so we never relay marketer math as platform fact.
>
> **Tiers:** `[platform-official]` = the platform/regulator/institution said it ·
> `[well-documented]` = cross-confirmed across independent named sources ·
> `[marketer-claim]` = single agency/SEO blog, directional only — verify on his own data ·
> `[unverified]` = forecast/anecdote, treat as a bet.
>
> **The hub rule that governs this whole file:** use the DIRECTION, never quote a marketer
> MAGNITUDE as fact, and backtest the number against his own 300-post history (`metrics2026.py` +
> `self-improve/grade.py`). Almost every percentage and multiplier in 2026 creator research is
> third-party; his own data is the only ground truth.
>
> Last synthesized: **2026-06-24**. Live numbers from `stats.md` (2026-06-23).

---

## 0. The one-paragraph picture

Elijah is a 21-year-old AI/tech + money/business creator at **~102.7k followers (+2,570/30d)** whose
account is **~99.5% reels** (672/675 over 6 months) and **share-driven, not like-driven** — his top
reels pull **100k–215k SHARES**. The data is blunt: **Money/Finance is the runaway reach leader**
(owns his single biggest reel at 3.9M views), **AI/Tech is the strongest strategic niche** (best
retention, highest saves, feeds his ventures, #1 by 6-month total) **but executes ~13× worse than
Money on equal post counts** — that gap is his single biggest fixable problem. **Motivation/Life is
over-supplied** (most-posted, lowest views-per-post — cut it), and two formats sit **completely
untapped in front of him: carousels (he runs ~zero) and long-form/YouTube (scripts written, pivot
active).** The single most important re-frame this year: **stop optimizing for likes/views and
optimize for SENDS-per-reach and WATCH-TIME** — those are the two signals Instagram itself names as
what pushes a reel to strangers `[platform-official]`. **And the strategic seat nobody at scale owns:
young (Gen-Z) + actually-ships-AI-software + money/contrarian operator + faith anchor — his bio
already claims it; the field splits cleanly around him.** Everything below is downstream of those two
facts. The **three highest-leverage zero-cost moves** that fall straight out of this: (1) ship his
first **carousels** + a per-clip **branded cover** (§2, §21); (2) stand up ONE free **Broadcast Channel**
as the owned-audience spine that survives a deplatforming (§23); (3) **pivot Archetype's course into a
recurring AI agent** (§24) — and pin everything to his own 300-post data, never a marketer magnitude.

---

## 1. The 2026 signal model (what "good" actually means now)

This is the spine. Every format and idea below is a delivery vehicle for one of these signals.

- **Instagram's own "Ranking Explained" names the top Reels predictions: reshare (send), watch-all-the-way-through, like, and audio-page taps.** For **Explore / non-follower discovery** the named signals are **likes, saves, and shares.** The Feed-recs system also names a NEGATIVE predictor: **"how likely you are to watch less than three seconds of a reel."** `[platform-official]` (about.instagram.com/blog/announcements/instagram-ranking-explained + transparency.meta.com)
- **Mosseri's creator guidance: the three metrics to watch are watch time (#1), sends-per-reach (DM shares), and likes-per-reach** — with his own split: **likes weigh more for reaching FOLLOWERS, sends weigh more for reaching NON-followers.** `[platform-official]`
- **Sends are "the most heavily weighted signal for distribution" for Reels** because short-form is symbiotic with friend-to-friend sharing (Mosseri, via Buffer relaying the Colin & Samir interview). `[platform-official]`
- **~half of Instagram video is watched WITHOUT sound** (Mosseri, approximate/verbal — treat as "roughly half," not an exact stat). `[platform-official]` → the hook must land on-mute (text in frame 1).
- **Mosseri publicly DEBUNKED the "link in bio kills reach" myth** (July 2025, verbatim: it "will not affect your reach one way or another"). Reach drops blamed on links are weak standalone content, not a link penalty. `[platform-official]` **Justify any comment-keyword funnel on intent-capture + the sends signal, NOT on a link-suppression myth.**
- **"Go to the audio page" is one of the FOUR named Reels predictions** — Meta's Transparency Center spells out the exact model inputs for "how likely you are to USE the audio from a reel you're viewing": (a) viewing reels >15s, (b) how many times you've clicked the audio link, (c) how many times you've clicked "Use audio." The audio-reuse prediction **also appears in Feed Recommendations** (cross-surface). `[platform-official]` **This makes original audio he authors an OFFENSE lever, not just the §7 constraint — see §19.**
- **The specific magnitudes are NOT official.** "Sends weighted 3–5× a like," "saves ~3× a like," "1.4× carousel reach," "DM-share >2–3% triggers a harder push," "10+ reposts/30d = Explore exclusion" — all appear **only in agency/SEO blogs with no Meta citation.** `[marketer-claim]` **Use the direction; never quote the multiplier as fact.**
- **Instagram normalizes for account size** (connected vs unconnected reach), and Mosseri says **engagement RATE matters more than raw reach** — a smaller account with high send-rate can out-perform a larger one on a given post `[well-documented]`. Magnitude of the normalization is unquantified (direction solid).

**Operating rule for the hub:** score and report on **sends/reach, watch-time, saves/reach** — NOT raw likes/views. `metrics2026.py` already ingests skip/share/save rates; the open follow-up is surfacing **sends-per-reach and avg-watch-time as first-class columns** and grading posts on those.

---

## 2. Format strategy — which / when / why

### Reels — the discovery engine (60–70% of output)
**When:** default top-of-funnel for every idea. **Why:** reels are injected to non-followers via Explore/recommendations and rank on watch-time + sends; **Buffer (4M+ posts): reels get 1.36× the reach of carousels and 2.25× the reach of single images** `[well-documented]`. **Metricool (24.4M posts): reels = 4× the interactions of single images** `[well-documented]`.
- **Reels up to 3 minutes are now recommended to non-followers**, gated by **retention, not length** `[platform-official]` — a 15s reel at high completion beats a 3-min reel at low completion. **Avg watch time roughly doubled YoY to ~8.5s** (Metricool) `[well-documented]`.
- **This unlocks 60–120s mini-explainers that previously only reached followers** — repurpose podcast/interview segments (Derwin edit via auto-clip facetrack) into retention-engineered long reels, not just 15s cuts.
- **Recommendation-eligibility gate** (must clear to reach non-followers): original content, no third-party watermarks (TikTok logos etc.), includes audio, ≤3 min, reasonably high quality, not recycled/aggregated `[platform-official]`. **NOTE:** "9:16 required" and "hook in first 3s" are NOT formal eligibility gates — 9:16 is the standard export spec; the 3s hook is a retention best-practice, not a rule.
- **Account-level originality enforcement is a TAILWIND for him:** "If your account primarily posts unoriginal reels/photos/carousels you didn't create or edit in a material way, your account may not be seen in recommendations to new audiences"; eligibility returns when most recent posts are original over a 30-day window `[platform-official]`. His original voice removes low-effort reposters from the pool. **The exact failure mode for his auto-clip pipeline: enforce per-clip distinctiveness (unique hook, self-contained idea, clean no-watermark export) so near-duplicate slices of one video don't read as aggregated.**

### Carousels — the save/convert engine, and HIS #1 UNTAPPED LEVER (20–30% of output)
**When:** turn every proven reel into a saveable reference deck. **Why:** he runs **ZERO carousels today** (`stats.md` tracks no carousel category) = pure upside, and carousels are the verified saves format. `carousel-builder` exists and has **never run in production.**
- **Metricool: carousels = 9× the saves of single images** `[well-documented]`. **Buffer: carousels deliver 2.09× the engagement rate of reels** and the highest median engagement-rate-of-reach **(6.90% vs reels 3.31%)** `[well-documented]`.
- **Socialinsider (35M posts): at 100k–1M-follower accounts, carousels out-VIEW reels** (35,370 vs 16,035 avg views) — partly mechanical: **Instagram re-serves unseen slides as "new content," resuming from the first slide the viewer hadn't reached** `[well-documented]`, giving one post multiple distribution chances. **Caveat:** those are 2025 values labeled 2026; directional, not his numbers.
- **Explore explicitly weights likes, SAVES, and SHARES** `[platform-official]` — AI/money reference decks (tool lists, prompt libraries, pricing breakdowns, playbooks) hit two of the three named Explore signals at once.
- **Build spec** `[well-documented]`: **8–12 slides** (12–20 only for deep guides); **Slide 1 = cover** (promise + specificity + pattern-interrupt, headline **<12 words**, must stop the scroll alone) → **Slide 2 = credibility/roadmap** → **Slides 3+ = one point per slide** (flashcard) → **final = CTA**. Portrait **1080×1350**, body text **24–30pt min**, 2–3 fonts, consistent palette. **Because the re-serve resumes from any unseen slide, design every body slide to stand alone as a mini-cover — no dead slides.** Carousels now support **up to 20 slides** `[platform-official]` (don't default to 20; reserve for deep guides).
- **Concrete hook devices** `[well-documented]`: **half-reveal** (split a headline across the slide 1→2 seam to force the swipe), open-loop/"wait for it" payoff on the final slide, a **progress indicator** ("1 of 8"), and the single most save-worthy asset (framework/checklist/number) on its own slide.
- **High-save formats** (Krumzi, verified the FOUR): step-by-step tutorials · "things I wish I knew" · **Myth vs Fact** (one real debunk per slide — triggers emotion + shares) · quick-tips/cheat-sheets. ("Case study with real numbers" is widely recommended but NOT in this source — separately sourced.) `[well-documented]`
- **Dual CTA standard** (cheap, targets both top signals): a **save CTA** ("Save this for the next time you build with X") AND a **send CTA** ("Send this to the founder still doing X manually") `[marketer-claim]` on wording, but maps cleanly onto Mosseri's saves-vs-sends.
- **Swipe cues** (arrows, "swipe →", progress dots) — pineable reports only ~5% of carousels use them and a small lift `[marketer-claim]`; cheap edge. **Do NOT promise an "Explore boost from completion %" — that claim is unsubstantiated.**
- **Audio-carousel hybrid (adding music to push a carousel into the Reels feed): UNVERIFIED agency claim, NOT a Mosseri statement** `[marketer-claim]` — A/B it on his account, don't rely on it.

### Long-form / YouTube — the active pivot, where loyalty + CPM live (build now)
**When:** his flagship content (age-14 testimony, the "5 Secrets" 30-min, the Derwin podcast). **Why:** the platform's money and distribution are tilting here.
- **YouTube is the #1 US streaming-watchtime platform ~3 years running (Nielsen); paid $100B+ to creators over 4 years; 2026 strategy = TV-screen, episodic "seasons & shows," long-form; Shorts now ~200B daily views** `[platform-official]`. The pivot **swims with the platform's incentives.**
- **Ranking weights watch time by SATISFACTION** (surveys, returns, session continuation, shares) — long-form ≠ "pad to 20 min"; **value density beats raw length** (Todd Beaupre, YouTube Sr. Director of Growth & Discovery) `[well-documented]`. **The viral "April 2026 YouTube killed watch-time / 3-min beats 20-min" framing is a marketer DRAMATIZATION, not an official announcement** `[marketer-claim]` — never relay that date as fact.
- **First 30s is a hard gate** ("Intros" metric = % still watching after 30s; YouTube tells creators to experiment with the first 30s) `[platform-official]`. Front-load the payoff; use the retention chart's dips/spikes to cut weak segments and clone what spikes.
- **Per-video reach, not channel size:** "whether your channel has 500 subscribers or 500,000… every video earns its own reach now" (Gillian Perkins) `[well-documented]` — a brand-new low-sub long-form channel is NOT gated; one well-packaged, well-targeted video can break out.
- **Shorts → long-form is the funnel:** Shorts and long-form are **two separate ranking models**; Shorts convert to subs at **<10% the rate of long-form** but work as a cheap hook-test `[well-documented]`. Use Shorts to test topics, build winners into long-form. **>57% of YouTube minutes watched in 2025 came from 20+-min videos** (Tubular Labs via Bloomberg) `[marketer-claim]` — long-form compounds for years vs short-form's ~24–48h shelf life.
- **His lane sits in the top CPM tiers** (vidIQ estimates, ordering reliable, dollars ballpark): AI finance $15–25, B2B/SaaS automation $15–28, AI tutorials/reviews $10–28 — **faceless AI automation is the LOWEST tier ($4–12)** `[marketer-claim]`. The finance long-form RPM band is **~$10–25/1k AFTER YouTube's 45% cut, vs ~$0.03–0.10 RPM for the same content as a Short** (third-party benchmark) `[well-documented]` — an order-of-magnitude gap that is the core argument for staffing YouTube long-form. Avoid the faceless floor.
- **Packaging is the gate** `[well-documented]`: **title-first, THEN script.** Titles <60 chars, front-load first 3–5 words, specific/odd numbers beat vague, a bracket tag "[2026 Update]" boosts CTR, write different titles for Shorts (<40 chars) vs long-form. Build **evergreen, undated** titles ("How I Automate X with AI") so views compound; reserve dated titles for genuine AI-news roundups only.
- **Interview/podcast is a 2026-FAVORED format** he already shoots (Derwin edit) — 30–60-min talk formats now pull millions, and **audio quality is "non-negotiable"** `[well-documented]`. Invest in audio before more visual polish (high-leverage given his Insta360 + edit pipeline).
- **AI as production partner, not product:** YouTube's Inauthentic-Content policy demonetizes pure TTS-over-stock and templated batch uploads; **human input (real research/commentary/demo/POV) is required** `[well-documented]`. His face + live tool demos ARE the moat.

### Stories — warm-lead / reply engine, NOT a reach play (daily, light)
**When:** daily, to convert existing followers. **Why:** Mosseri positions Feed/Stories for "friends, family, those they're closest to" `[platform-official]`; **Story replies rose 88% YoY** (Metricool) `[well-documented]`. Run poll/Q&A/quiz stickers on AI-tool & money topics to manufacture the reply signal, then route engaged repliers toward DMs (via comment-triage's draft→approve flow). Judging Stories by reach is the wrong frame.

### Static single images — AVOID as a standalone reach play
**Metricool single-image YoY: reach −21.96%, interactions −25.41%, engagement −45.98%** `[well-documented]`. When a static asset exists, **wrap it as slide 1 of a carousel** so it gets the re-serve + saves treatment instead of dying as a one-shot.

### Recommended mix (synthesized, not a single-source stat)
~**60–70% Reels** (discovery via watch-time + sends) · ~**20–30% carousels** built for saves · **Stories daily** for replies · **1 long-form/week** as the pillar repurposed into the week's reels. He is at **~6.7 posts/week with 0% carousels** — over-supplying reels, skipping the entire save/convert engine.

---

## 3. Niche playbook — lean-in vs avoid (his live data)

Live category mix, last 30d (`stats.md`, 2026-06-23):

| Niche | 30d posts | 30d views | ~views/post | Verdict |
|---|---|---|---|---|
| **Money / Finance** | 20 | 4,097,687 | **~205k** | **LEAN IN for reach** (skip-risk — tighten hooks/depth) |
| **Other** (reaction/personality) | 63 | 1,558,163 | ~25k | **Sleeper — keep mining his comedic voice** |
| **Founder / Business** | 31 | 549,194 | ~18k | **LEAN IN — his most shareable identity lane** |
| **Motivation / Life** | 47 | 380,268 | **~8.1k** | **DEPRIORITIZE — over-supplied, lowest return** |
| **AI / Tech** | 20 | 315,900 | ~16k | **GROW — strongest strategic niche; ~13× worse than Money on equal posts = his #1 fixable gap** |
| **Child Safety / PSA** | 12 | 153,166 | ~12.8k | **Mission + lean-in arbitrage bet (out-performs Motivation/post)** |
| **Faith** | 8 | 79,906 | ~10k | **Identity anchor — conviction, not metrics** |

- **Money/Finance** owns the single biggest reel (**3,949,336 views, 2026-05-28**) and a 6-mo 5.6M reel that pulled **215k shares**. **But it rides REACH not retention** (skip-rate risk, lowest watch-time hold) — lean in for reach, AND apply the **money-retention fix (§10)** to convert that reach into watch-time and sends.
- **AI/Tech** is the **#1 niche by 6-month total (19.8M, incl. a 10.0M Feb reel)**, holds attention best (**~17.5s vs Motivation's 8.3s**), and is his **highest save-rate niche (~3.6%, utility content)** — yet it gets **~13× fewer views than Money on equal 20-post counts (315,900 vs 4,097,687).** This is the niche to grow because it's his identity moat AND it feeds his ventures; the gap is **execution, not positioning** (see §10 the AI-content fix).
- **Motivation/Life** was the **most-posted niche over 6 months (168×) for only 6.6M views** — the clearest "redeploy this volume into Money + AI/Tech" signal.
- **"Other"** (the "ain't no way…" comedic-reaction voice) is an unplanned sleeper that **travels far on shares** (829,758-view breakout) — keep it as a natural-voice release valve, don't over-engineer it. His viral hits ARE contrarian hooks; he just isn't applying that pattern systematically to his AI/builder content where it's absent.

---

## 4. Biggest trending themes that actually fit him

These are the news/format waves where his AI-builder + money positioning lets him **own the credible middle** vs the hype crowd. All have built-in shareability. (Reactive items go stale — re-pull weekly via the intel engines.)

1. **"Why did the US government turn OFF the best AI model?"** — Claude Fable 5 / Mythos 5 **suspended worldwide June 12, 2026** under a Commerce export-control directive barring foreign-national access; Anthropic pulled both for ALL users and publicly disagreed; Opus 4.8 unaffected; launch pricing $10/M in + $50/M out `[platform-official]`. Stick to that verified spine; **skip the unverified "100+ experts petitioned" / "SK Telecom China-risk" sub-claims.** Tie to: *depending on one AI model is now a business risk.*
2. **"GitHub Copilot just 10×–50×'d people's bills overnight"** — moved to usage-based token billing June 1, 2026; real screenshotted bills jumped $29→$750, $50→$3,000 `[platform-official]`. **Load-bearing caveat: code completions stay FREE — only chat/agent/review meter.** Relatable money-pain → high comments. Teach how not to get wrecked.
3. **"AI isn't taking your job — here's what's actually happening"** (contrarian myth-bust) — ~27,600 of 2026 cuts explicitly AI-cited (~13%, up from ~5%); tech layoffs ~142,000 amid a ~$700B buildout; **but a 750-CFO survey pins ACTUAL AI-attributable role loss at ~0.4%, and Altman/Andreessen both call AI a layoff "excuse"** `[well-documented]`. Lead with the firm 0.4% / 60%-of-managers numbers; avoid the deleted 123k/50k/14% specifics. **Under-saturated contrarian seat.**
4. **The AI bubble / "circular financing" debate** — Michael Burry called the Nvidia→Valor(VCI)→xAI GPU-financing loop "fugazi" (Nvidia put ~$1.9B into the buyer of its own $5.4B of chips); SEC filing confirms **Anthropic pays xAI ~$1.25B/month** for Colossus `[well-documented]`. **CRITICAL FRAMING: Burry is NOT alleging fraud — say "here's the deal structure, you decide," never "it's fraud."** Pair with verified concentration (top 10 ≈ 37% of S&P weight; Alphabet alone >20% of YTD return; **Fed June-17 FOMC removed its 2026 rate-cut, raised PCE forecast to 3.6%**) for a bull-vs-bear series. **Do NOT use the deleted "83% of gains" / "SOX +70%" stats.**
5. **"Sora is dead — here's what I actually use now"** — OpenAI killed the consumer Sora app (~Apr 2026; API runs to ~Sept 2026); **Grok Imagine 1.5 is the BUDGET pick (~$4.20/min, ~86% below Sora 2 Pro); Veo 3.1 is PREMIUM (4K + synced audio, ~$9–24/min, NOT cheap); LTX-2.3 open-weights** `[well-documented]`. **Be accurate: Grok is the bargain, Veo is the premium tier** (source originally had this backwards).
6. **"Your AI coding agent can be hijacked" — agentjacking** — malicious instructions hidden in error-tracking output (fake Sentry reports) get executed by Claude Code / Cursor; Tenet recorded **~85% test success** and **2,388 orgs whose Sentry DSNs accepted injected events** `[well-documented]`. **Say clearly: 2,388 = DSNs that accepted events, NOT 2,388 breaches.** Near-zero competition among money/tech creators = pure authority builder. Mitigation: human review between tool output and agent execution.
7. **"I priced out running a business on AI agents for a month"** — the $300–$500/mo solo-operator agent stack vs the salaries it could replace `[marketer-claim]` on the dollar figures. **Show YOUR own stack; caveat the inflated ROI numbers on-screen (drop the "340%").** Most on-brand money angle he has.
8. **Talent-war + market-shift combo** — Noam Shazeer (transformer co-author) left Google for OpenAI (June 18, ~22 months after the ~$2.7B 2024 CharacterAI poach); **ChatGPT fell below 50% AI-assistant share for the first time (46.4%; Gemini 27.7%, Claude 10.3%)**; SpaceX bought Cursor's parent Anysphere for **$60B all-stock** (largest VC-backed acquisition ever) `[well-documented]`. **Add that ChatGPT still leads at 1B MAU so the "losing" chart stays honest.**
9. **"You're overpaying for AI" — open models** — GLM-5.2 (MIT-licensed, ~62.1 vs GPT-5.5's 58.6 on SWE-Bench Pro) as a free/cheap frontier coding model `[well-documented]`. **Verify the exact cost multiple before stating a number on camera** (the per-token pair was unverified). **"MIT named generative/AI coding a 2026 Breakthrough Technology" is the accurate authority hook — NOT "vibe coding"** (MIT's official label is generative coding; "vibe coding" is Karpathy's colloquial term) `[platform-official]`.
10. **The named money-trend block** — "No-Buy 2026" / "little-treat crackdown" grounded in **verified Intuit numbers (59% cutting small purchases, 49% mindful spending, 54% have 2025 regrets)** `[well-documented]` and **BofA's shame/accountability data (41% weekly money guilt, 42% loud-budgeting, 42% paycheck-to-paycheck, 34% no longer get family help)** `[platform-official]`. Make it ownable: *"I automated my no-buy with an AI spend-tracker."*

**Recurring series to own** (turns "what do I post" into filling buckets):
- **"The Model Flood"** — weekly "what dropped + which model wins for [task]." The late-May→June cadence (Opus 4.8, Fable 5, GPT-5.6, Gemini 3.5 Pro) means he never runs out.
- **"X Clearly Explained (and how to use it)"** — Greg Isenberg's CONFIRMED highest-frequency format `[well-documented]`; one episode per new model/tool drop, near-zero idea cost. Wire to `intel/news-radar.py`. (The "you're using X wrong"/"banned" news-jack variant is plausible but unverified — test, don't assume.)
- **"AI Builder's 6-Pack"** — Isenberg's CONFIRMED fixed-slot digest (one idea / trend / tool / framework / news-debate / product) as a single carousel or reel — turns "what to post" into filling predictable buckets, maximizes saves `[well-documented]`.
- **"Building [an AI tool] from $0"** numbered public series across Reels + LinkedIn, each episode on a real number, ending on an open loop.
- **"Rebuild This"** — vibe-code a better version of one widely-disliked app per week (Riley Brown / Isenberg angle) — content AND product R&D. **The specific "hated app / $10M" framing is a creator-claim** `[marketer-claim]` — own it in honest terms.
- **"AI Slop Teardown" / "Grade My Software"** — grade other AI tools/content on-camera against a fixed rubric (the `live-software-review` skill) — rides the documented anti-slop sentiment and positions him as the trusted human curator (see §11).

---

## 5. What works for HIM (his proven mechanics)

- **SHARES are the engine, not likes.** Top reels pull 100k–215k shares. **Every concept should end on an implicit "send this to ___"** (e.g. "send this to your co-founder"). Optimize for shareability first.
- **Disbelief / audacity / contrarian hooks in the first 3 seconds.** His winners: *"ain't no way…"*, *"I still can't even believe the audacity of this fool. Absolutely mindblowing 🤯"*, *"Wait… we were all just exit liquidity the whole time 😳."* These ARE contrarian hooks (verified in his `stats.md` captions) — the pattern already driving 3.95M views; systematize it across ALL niches, especially AI/builder where it's absent.
- **Outcome-first hook as default for AI/tech demos** — open frame 1 on the finished result (the tool doing the impressive thing), THEN reveal the how. This is the **#1 data-backed hook type in the verified 34,635-clip OpusClip study (~2× the lowest-ranked type)** `[well-documented]` and suits demo content natively.
- **The 5-hook rotation** (a menu, NOT a ranked leaderboard): Outcome Showcase · Expert Explainer · Contrarian · Specific Odd Number · Imperative `[well-documented]`. A/B against his own history.
- **The curiosity-loop:** state an unresolved question/promised payoff in the first 3s, resolve it only at the end — the cheapest retention lever for longer "explain the agent team" content, feeding watch-time (the #1 signal).
- **Mute-survival:** burn the value-promise into on-screen text in frame 1 — ~half watch without sound. Text overlays reportedly retain ~25% more viewers than audio-only `[well-documented, single-source]` — A/B it.
- **His most distinctive, un-copyable long-form assets:** the **age-14 testimony** (the devil's soul-bargain he refused — sensitivity gate: drug/police-beating detail + a self-harm disclosure are HIS call on detail level), the **"7 bets that looked stupid"** arc, and **"build software FOR agents, not people"** with the hard line *"I'll go all-in on AI, I won't put it in my body."* These anchor the YouTube pivot.
- **Build-in-public of his OWN SaaS portfolio** (Artifacial/Infinet/ClipWith/Archetype) — content + product-marketing + the most authentic proof-of-builder content NO money-creator can copy (most have no product; Riley Brown has one, Elijah has four).
- **Format experiments already validated/exploring:** trial-reel A/B; **Trial Reels as a free pre-publish A/B** (publish to non-followers first, promote winners) `[platform-official]` — the official version of the proposed audience-sim hook-ranker; episodic open-loop mini-series; the **faceless co-founder/Tanner CHARACTER series** (text-on-screen, nature-doc VO, "tag your co-founder").
- **Voice:** high-energy, plain-spoken, direct second-person "you," CAPS for emphasis, emoji-forward; 21-year-old contrarian operator (credit-and-leverage over cash, "build software for agents not people," willing to look stupid and never stop) — **blunt conviction, never corporate.** Faith ("Jesus is how") woven in naturally and literally, never preachy. Long-form goes raw and testimonial.

---

## 6. Lean-into vs avoid (the decisive list)

**LEAN INTO**
- **Carousels** — his single biggest untapped lever (zero today). Ship 1–2/week, optimized for SAVES first, with dual save+send CTAs. Turn the 3.95M "exit liquidity" reel into a saveable "AI + money breakdown" deck — pure additive whitespace, no new filming.
- **Long-form/YouTube** — the active pivot, with the platform's incentives. Title-first, real demos, first-30s gate, invest in audio.
- **Own the triple-intersection** — "AI-builder who talks money like a 21-yo operator." Riley owns AI-builder, Codie owns contrarian-money, Iman owns young-founder-money; **nobody owns all three.** Position every reel at the overlap: *"I built [real AI feature] this week — here's the money math."* (See §9.)
- **Sends-first design** — a deliberate "send this to ___" trigger on every reel and carousel.
- **AI/Tech as the growth niche** (fix the execution gap) + **Money/Finance for reach** (apply §10) + **Founder/Business for shares.**
- **Outcome-first hooks** on AI demos; **disbelief/audacity/contrarian hooks** on everything else.
- **The "Other" comedic-reaction voice** as a natural-voice release valve (it travels on shares).
- **Stories daily** as a reply/warm-lead engine (poll/Q&A/quiz stickers).
- **Owned audience** — start a beehiiv newsletter + comment→DM email capture now to hedge algorithm risk (§13).
- **Faith as the un-copyable 4th differentiator** — not preachy, but as the value-system frame on money/AI takes ("why I build differently"); none of his named rivals carry it.

**AVOID / DEPRIORITIZE**
- **Motivation/Life volume** — over-supplied, lowest return. Redeploy into Money + AI/Tech.
- **Standalone static images** for reach — wrap as carousel slide 1 instead.
- **Hashtag clumps** — Metricool: posts with hashtags saw **−31.70% views / −33.89% interactions** vs platform average `[well-documented]`. (Use a question in the caption instead: **+36.70% comments**; comment-focused CTAs **+202.78% comments** `[well-documented]`.)
- **Faceless TTS-over-stock long-form** — lowest CPM tier AND demonetization risk under YouTube's Inauthentic-Content policy.
- **Fully-automated/AI-only content with no human** — the actual penalty trigger on both Meta (deception) and YouTube (inauthentic). AI for craft/b-roll/ideation, NEVER AI for fake proof (§11).
- **Quoting marketer magnitudes as fact** — the 3–5× sends weight, 1.4× carousel reach, 70% completion thresholds, 22% save lift, etc. are all `[marketer-claim]`. **Use the direction; verify the number on his 300-post history.**

---

## 7. Hard guardrails (non-negotiable, govern every output)

- **API-published reels CANNOT use licensed/trending audio** (IG API limit) → API-publish **only voice-only / original-audio** reels; **any trend-audio reel goes out manually / in-app (Edits)** `[platform-official]` (account rule, verified). **Account-classification caveat:** only BUSINESS accounts are restricted to the Meta Sound Collection (~14k cleared tracks); CREATOR accounts keep the larger licensed catalog — **verify whether @elijahaifl is Business vs Creator**, since it determines whether the manual trend-audio path is even fully available. The Edits-sharing reach nudge is **real but small + temporary** (one A/B ≈ 0.4%) — use Edits for **quality/audio/originality**, never as a secret multiplier. For process content, **tactile Foley + original audio** is the on-brand workaround.
- **NEVER publish, post, comment, or DM without explicit per-action confirmation from Elijah.** Drafts and container-creation are fine; the final publish click is always his.
- **DRAFT-ONLY output.** This run proposes and drafts; it never auto-posts, never creates/edits/pauses an ad, never spends. **Meta Ads = read/report freely, confirm before ANY write.**
- **Vault notes follow the property contract** in `obsidian/Elijah's vault/CLAUDE.md` exactly — lowercase snake_case names, copy the matching `_templates/` block, never invent property names. Idea notes → `20-Content/Ideas/`.
- **Secrets only in Windows env vars (setx), never in files** — the whole tree syncs to OneDrive.
- **Sensitivity gate on the flagship testimony** — drug/police-beating detail and the self-harm disclosure are HIS call on detail level (monetization + duty-of-care).
- **FTC disclosure is LAW, not optional** (§12) — any sponsored/affiliate content needs disclosure IN the video (spoken + on-screen), not buried in a caption hashtag clump; the IG Paid Partnership label does NOT satisfy the FTC on its own. `[platform-official]`
- **EU AI Act Art. 50 transparency obligations apply 2 Aug 2026** — build the AI-disclosure + authenticity habit now, not retrofit later (§11). `[well-documented]`
- **Pre-flight bulk reel publishing with `get_content_publishing_limit`** — quota is a non-issue (~0/100) but **the audio rule is the real binding constraint.**

---

## 8. Posting cadence — is 3.6/day over-posting? (his open question, answered)

- **There is NO algorithmic frequency penalty.** Mosseri: "Posting often generally helps with reach, but it's important not to burn out" / "the more you post, the more people you'll reach" — each post is judged on its own engagement. `[platform-official]` Buffer's 2.1M-post study: posting MORE correlates with MORE reach per post (+24% at 10+/week vs 1–2/week) AND monotonically higher follower-growth. `[well-documented]`
- **BUT the data only goes to ~1.4/day (the top "10+/week" bucket).** Elijah at ~3.6/day is **~2.5× beyond where any large study measured**, and Buffer itself flags diminishing returns past 3–5/week. The likely cost of his volume is **lower AVERAGE per-post reach + fatigue, NOT a reach cap** `[unverified — depends on his own data]`.
- **The one real mechanism that hurts: intra-account competition.** Instagram "can't promote all videos simultaneously — it picks those with the best initial metrics," so stacking reels close together splits his warm audience across each post's early window. Practitioner minimum: **~3–4h between reels** `[marketer-claim]`.
- **The one real volume-related Meta penalty is ORIGINALITY/aggregation, not count** `[marketer-claim on magnitude, platform-official on direction]` — near-duplicate slices of one video read as low-originality. Enforce per-clip distinctiveness.

**Decisive moves (all use his own data):**
1. **Run the self-cannibalization test** — regress his 300-post reach/watch-time/skip-rate vs (a) posts-that-day and (b) hours-since-previous-post. The ONLY way to know if 3.6/day is over-posting FOR HIM. Add a panel to `metrics2026.py`.
2. **Enforce ~3–4h+ spacing** in the publishing layer — distribute reels across the day, don't batch-drop.
3. **Per-post quality gate** — route every auto-clip output through the virality score; below a floor, it doesn't post. **Ship 1–2 gated reels/day over 4 ungated.**
4. **Shift the scoreboard** from posts/day → **average reach-per-post and watch-time-per-post.** Run a 2–3 week A/B: alternate weeks of ~3.6/day vs ~1.5/day (gated), compare per-post reach + follower growth.

---

## 9. Competitive whitespace — the seat nobody owns

His **live baseline:** ~102.7k followers, 300 posts tracked, AI/Tech executing ~13× worse than Money, **zero carousels** `[platform-official, from stats.md]`.

| Rival | Scale | Owns | Gap he exploits |
|---|---|---|---|
| **Riley Brown** (@realrileybrown) | ~1.5M cross-platform, 635k TikTok; Vibecode ($9M raised) | AI-builder / vibe-coding screen-records | Almost no money/contrarian/faith; tutorial-led, not reaction-led `[well-documented]` |
| **Greg Isenberg** (@gregisenberg) | 128k IG | "AI startup ideas," fixed-slot digests | Older VC-founder, podcast-led, not raw/young `[well-documented]` |
| **Codie Sanchez** | 1.5M+, 100k+ email | "contrarian / boring businesses" | Skews 30–45 cash-buyers; no software; polished not raw `[well-documented]` |
| **Iman Gadzhi** (age 26) | Dominant young-founder money creator | course-funnel, polished | Just NOW moving into AI-growth-marketing (confirms the battleground); over-polished course-seller = the contrast wedge. Net worth ~$25–40M, NOT $100M+ `[marketer-claim]` |
| **AI-agent educators** (Matthew Berman ~49k IG vs 336k YT, Wes Roth, David Ondrej) | YouTube-primary, sub-100k IG | deep AI-agent expertise | **Biggest structural gap: deepest AI-agent expertise has NOT translated to IG short-form — Elijah already out-scales them on IG** `[well-documented]` |

**The whitespace, stated plainly:** no creator at scale occupies Elijah's **triple-intersection — young/Gen-Z + actually-ships-AI-software + money/contrarian operator** — and his **faith anchor is a 4th differentiator none of them carry.** The field splits cleanly: AI-builders don't do money/contrarian; money-operators don't ship software and are polished-not-raw; AI-educators are weak on IG. **The problem is execution, not positioning** — his bio already claims a multi-venture operator identity no single rival matches.

**Moves:** (1) position every reel at the triple-overlap; (2) **fix the AI-content gap** by stealing Riley's screen-record-build format + ADDING his face + a money/contrarian hook ("Everyone's paying $X for this AI tool — I built it in an afternoon"); (3) **launch carousels now** (rivals + benchmark both say it's the under-supplied lane); (4) **build-in-public of his 4 SaaS products** (no money-creator can copy); (5) **own a named contrarian series** at the AI+money seam (e.g. "Build, Don't Buy" as the Gen-Z answer to Codie's buy-boring-businesses); (6) **repackage AI-agent depth as punchy face-on IG reels** to capture the audience YouTube-primary educators can't reach; (7) **add Riley/Greg/Codie/Iman/Berman to `intel/viral-radar.py`** so the hub auto-surfaces their breakouts weekly and he reaction-counters while hot (his speed advantage over their produced content).

---

## 10. The Money-niche retention fix (his #1 fixable problem)

Money rides reach but "leaks watch-time" (lowest hold, skip-risk). The fix is concentrated in the FRONT and the PAYOFF, not the whole video.

- **Skip rate = % who scroll past in the FIRST 3 SECONDS** (Metricool's definition; he already ingests `reels_skip_rate`) `[well-documented]` — so flagged skip-risk is a **first-3-second hook problem.**
- **Open-loop hook with a NUMBER in the first ~2.5s** (a number raises credibility + curiosity at once): direct/measurable promise ("This one move saved me $4k in tax"), specific-pain question ("Why is your high-yield savings actually losing you money?"), or contrarian pattern-interrupt ("I made more money after I stopped posting daily"). `[well-documented]`
- **Plan the hook FIRST, then deliver on it** — a weak/delayed payoff is a named retention killer; **don't bury the dollar result or split it into a "part 2."** His Money reels' "high reach + flat payoff" is the textbook signature of high-reach/low-completion. `[well-documented]`
- **Add a beat at the ~15s drop** (new visual / data beat / narrative turn) — finance is information-dense, so beat cadence matters more. (The "every 5–7s" cadence is an unverified rule of thumb; the ~15s cliff IS sourced.) `[marketer-claim]`
- **Lean INTO length: 45–90s** for finance (it earns credibility through depth and total watch time compounds) — **don't shorten to chase completion %; raise the HOLD curve.** `[marketer-claim]`
- **Caption density for finance:** move OFF fast 200–240 WPM kinetic captions toward **2–4 word chunks held 600–900ms**, hook text ~80–120px on the 1080×1920 canvas; pin literal dollar figures as their own held chunks for the ~70–85% sound-off majority. `[well-documented on the numbers]`
- **Native save/share triggers:** "save this before your next paycheck," "send to whoever you split bills with" — finance is one of the few niches where the ask feels natural. (Treat the 3–5×/3× weightings as unverified estimates.)
- **BACKTEST FIRST:** correlate skip-rate vs hook-type (number-in-first-3s vs not) and watch-time vs caption-speed on his OWN Money reels via `grade.py` — replace every marketer "completion benchmark" with HIS numbers. Build a vault "Money reel retention template" with every numeric target marked "pending backtest."

---

## 11. AI-slop / authenticity — turn the handle's liability into a moat

The **@elijahaifl handle pre-discloses AI on every impression**, and there's a measured, peer-reviewed "trust penalty" for disclosed AI (Journal of Interactive Advertising, 13 experiments; consumer preference for AI-creator content fell from 60%→26%, Billion Dollar Boy 'Muse', `[marketer-claim]` on the survey). So he pays a trust cost on cold audiences by default and must **actively buy trust back.**

- **The penalty is gated on DECEPTION, not AI use.** Meta demotes realistic AI depictions of real people/events/results presented as real; YouTube's "inauthentic content" policy terminated 16 channels (~35M subs, ~4.7B views, trade-aggregated) for faceless TTS-over-stock with no human input. **AI-ASSISTED content with genuine human commentary is fine.** `[platform-official on mechanism, well-documented on the wave]`
- **The market shifted to an "authenticity premium"** — real-face / real-screen presence is now a scarce, defensible asset (Digiday; Mosseri's "who's posting" authenticity push). `[well-documented]`
- **The IG "AI Creator" label is NOT cleanly reach-neutral** — disclosed-AI content still must clear the skip/watch-time bar; don't treat the badge as a free pass. `[well-documented]`

**Moves:** (1) **real-face cold open** (first ~1.5s is his actual face before any AI b-roll) to front-load proof-of-personhood; (2) **lead with on-screen receipts** (real dashboard / Stripe / IG-insights screen-records, real before/after) — verifiable real results are both SAFE and the scarce trust signal slop can't fake; (3) **pin an "I use AI, I am not made of AI" credo reel** ("every result I show is real and on my screen; AI helps me make it, it doesn't fake it"); (4) codify the **deceptive-AI third rail** in the content SOP; (5) run the **"AI slop teardown"** series (`live-software-review`) as the trusted human curator above the slop.

---

## 12. Sponsorship / brand-deal economics (when offers come)

- **Price off ACTUAL data, not follower-band quotes.** At ~102k with strong watch-time he can credibly open **Reel negotiations at $4,000–$6,000 and carousels at $3,000–$4,000**, defended with retention/skip-rate numbers most creators can't show. His **finance + AI/SaaS niche commands a ~2–3× premium** (Influee, `[marketer-claim]`). Build a one-page rate card from `ig-dashboard` views × a Reel CPM (~$45 starting benchmark, then calibrate).
- **Default every deal to HYBRID:** flat fee (covers his time win-or-lose) + an affiliate/recurring tail on the AI tool. **Decline affiliate-ONLY offers** unless a flat floor is included. AI/SaaS programs with lifetime-recurring commissions compound monthly (verify each vendor's current rate). `[well-documented]`
- **Charge separately for usage rights / Partnership-Ads whitelisting (+20–50%) and exclusivity (+25–50%, up to ~2× at 90+ days).** When a sponsor wants to "boost" his reel as an IG Partnership Ad, that's a paid right — quote it, don't give it away. `[marketer-claim]`
- **Inbound flywheel:** add "AI tools + business | partnerships: [email]" to bio, auto-generate a media kit from `ig-dashboard` stats (brands request one before deciding), post 1–2 authentic "tools I actually use" reels/carousels that double as soft pitches to those exact vendors.
- **FTC is LAW** `[platform-official]`: disclosure mandatory for ANY material connection (incl. free product); must be IN the video (spoken + on-screen `#ad`/"sponsored" near the FRONT of the caption), never buried in a hashtag clump or behind "more"; the IG label alone does NOT satisfy the FTC; forbidden words: "sp/spon/collab/ambassador" alone. The Oct-2024 reviews rule makes unsubstantiated/incentivized claims separately illegal at **$51,744 per violation** — keep a "claims he can personally substantiate" guardrail. The label does NOT suppress reach; bad creative does — score sponsored reels against the same skip/watch-time bar as organic.

---

## 13. The view→revenue funnel + owned audience (the structural hedge)

His owned audience is **~0 today** — the single biggest strategic gap. Borrowed IG reach dies in a deplatforming; an owned list survives it.

- **One top-of-funnel → parallel ladders, not 7 disconnected funnels.** Reel (engineered for sends) → **comment keyword** → **2-step DM** (question first in the single Private Reply, link second AFTER they reply inside the 24h window — Meta allows ONE private reply per comment within 7 days `[platform-official]`) → lead magnet/quiz capturing email + ONE qualifying question → the answer **ROUTES** the lead to the right venture's ladder.
- **Offer ladder per venture:** Free (quiz/template) → $9–49 tripwire → $100–2,000 core (host on **Whop**, ~5.7% all-in fee + community gating + recurring) → $5k+ high-ticket 1:1/done-for-you. `[well-documented]`
- **Platform picks** (verified pricing): newsletter base = **beehiiv** (free Launch tier: 2,500 subs + custom domain + 0% revenue cut; Scale $43/mo annual unlocks ad network/automations) `[platform-official]`; money/checkout page = **Stan Store** (0% txn fee on paid plans) or Whop direct, NOT Beacons (9% on free/low tiers); community/product layer = **Whop** (~6–7% blended, not the lowest variable but lowest fixed). `[platform-official / well-documented]`
- **Lead magnets from assets he ALREADY has** (near-zero marginal cost): "The AI-Tool Stack I Use," "prompts behind my viral reels," a Notion "AI Content OS," the live-review "Software Grading Scorecard," a hooks swipe file, a **quiz** ("What's your AI/money archetype?") that converts AND segments leads toward the right venture.
- **Compliance guardrails** `[platform-official + well-documented]`: official Graph API only (ManyChat-class, never browser bots); user-initiated triggers only (no cold DM); first DM = a question (no link); rotate 3+ message variants; **200 automated DMs/hour cap** (cut from ~5,000 in Oct 2024) — must throttle/queue; keep link-in-bio live in PARALLEL as a silent-outage fallback (his comment→DM tool died Nov 2025 for ~11h on a Meta webhook failure).
- **Activate the ALREADY-BUILT Telegram bridge bot (@Elijahclaudebot)** as a first owned channel (blocked on the Anthropic-credit unblock noted in memory) + beehiiv. The first marginal email/Telegram subscriber is worth disproportionately more than the next 1,000 IG followers because it survives a deplatforming.

---

## 14. Cross-platform repurposing — one shoot → N platforms

He already owns most of the engine in-house. `auto-clip` IS the OpusClip layer (highlight + facetrack + tighten + word-pop captions), and `platform-exporter` renders per-platform specs (IG Reels / TikTok / Shorts / YouTube-long / LinkedIn). **The only gap vs the commercial stack is auto-distribution scheduling — which the no-auto-publish rule means we WANT to keep manual anyway.** Design = a draft-to-N-format batch landing in `out/`, never auto-posting. `[well-documented, verified in-repo]`

- **Each platform pays off on a different axis:** TikTok = top-of-funnel reach + Gen-Z discovery; **Instagram = his monetization home base**; **YouTube = deepest trust + by far the highest ad RPM** + the only place a video compounds for years; X = real-time AI-news authority to other builders; LinkedIn = B2B credibility + lead-gen to highest-LTV buyers. `[marketer-claim on the role-split]`
- **Highest-ROI second front = YouTube** (Shorts as near-free repurpose of existing 9:16 outputs → 1–2 long-form/week; finance long-form RPM is the only short-form-adjacent channel where ad revenue alone is material). **TikTok = cheap #2 reach add** — **correction: TikTok does NOT bar AI from Creator Rewards**; AI content IS eligible if labeled + original + 60s+, so add the AI label to keep eligibility. `[well-documented]`
- **Free authority layer off the SAME transcript:** auto-draft a 5–7-tweet X thread + a LinkedIn native-video post per long-form, gated for his approval — no extra shoot.
- **LinkedIn is mid-2026's most-improved B2B platform** (Creator Marketplace + BrandWorks launched June 2026, invite-only alpha; BrandLink ad-rev-share). **Value it as lead-gen to high-LTV buyers, not a per-view check (revenue-share % undisclosed).** On LinkedIn specifically, **carousels/documents win reach (~1.39×) and native video reach is BELOW median (~0.86×)** — segment advice by platform (opposite of IG/TikTok). `[well-documented / platform-official]`

---

## 15. Audience quality — who actually engages (his real composition)

His follower base and his ENGAGED audience are NOT the same audience — a fact the dashboard collapses today.

- **His ENGAGED audience is measurably YOUNGER than his followers** (inversion): followers skew 25–34 + a 35+ tail; this month's ENGAGED audience is **18–24-dominant (~44%)**, ~84% under 35. Older followers are largely passive/legacy; current content resonates with a Gen-Z-heavy set. `[platform-official metric, operator-reported values]`
- **Gender skew widens with intent:** followers ~54% M; engaged ~64% M (roughly 3:1–6:1 male among classified engagers, though a ~25% "unknown" bucket widens the error bars). **Design offers/casting/copy/ad-targeting for a predominantly male 18–34 audience.** `[platform-official metric]`
- **Premium geography:** ~72.7% US, then GB/CA/AU ahead of any non-English country; tier-1 cities (NYC/LA/London/Houston/Chicago/Toronto/Melbourne/Sydney). His reach concentrates in **high-purchasing-power English markets** — raises monetizable value per follower and makes US/UK/CA/AU ad lookalikes + a media-kit selling point. `[platform-official metric]`
- **The intent funnel leaks at the bottom:** high reach → ~10% accounts-engaged → ~2.7% profile views → single-digit link taps. **The bottleneck is the bio/Beacons funnel, NOT reach.** Engagement is strong but mostly vanity-viewer attention. `[platform-official metrics]`
- **Two-track strategy:** Gen-Z-tuned reels for reach, but deliberately route the high-ticket OFFER at the higher-spend 25–44 follower cohort that engagement under-serves. Validate the offer-cohort assumption against his own conversion data (the external disposable-income figures were unverified).

**Hub move:** add `engaged_audience_demographics` to `refresh.py` (confirmed official, same code path) and build a "follower vs engaged delta" panel; treat `reached_audience_demographics` as a GUARDED add (returned live but NOT in Meta's current reference — wrap in try/except). Wire `follows_and_unfollows` (confirmed churn metric) + daily snapshots into a churn tracker annotated against viral-reel days, to measure REAL retention instead of trusting aggregator churn benchmarks.

---

## 16. Platform survival / account security (existential, Elijah-gated)

A 100k+ AI/money account is exactly the "valuable account" profile attackers farmed in the **June-2026 Meta-AI-chatbot takeover wave** (Obama White House, Sephora, OG usernames seized by asking Meta's AI support to attach an attacker email, then running password recovery — no technical exploit). **Critical: the attack generally FAILED against accounts with MFA, even SMS 2FA.** `[well-documented]`

- **Hardening order** `[platform-official]`: (1) switch IG 2FA to an **authenticator app** (Instagram says it's the most secure; SMS is SIM-swappable, but any 2FA beats none); (2) save backup codes offline; (3) audit/remove stale recovery emails (the exact vector abused); (4) confirm a clean recovery phone.
- **Meta Verified** = the only documented path to a human agent (24/7 chat/email; "request a call" on Max) when the AI-support failure mode strands you, plus impersonation takedowns. Standard $14.99/mo mobile is high-ROI insurance for a one-account business. `[platform-official]`
- **Continuity tripwire:** Account Status panel (Settings → Account Status) is the only OFFICIAL recommendation-suppression signal — **check it weekly.** Add a `refresh.py`/`metrics2026.py` daily tripwire on non-follower-reach share (self-calibrated 7-day vs prior-30, NOT a hardcoded band). `[platform-official]`
- **Pre-stage an "IG zero-day runbook"** (in `HANDOFF.md`/a `SECURITY.md`): in-app "I can't access my account" → video selfie in bright even light, ONE careful submission (retries trigger cooldowns), ~2 business-day review; Meta Verified escalation; never share codes/PINs. `[well-documented]`
- **The structural fix is owned audience (§13)** — so an IG event costs reach but not the business.

---

## 17. Ventures (what content should feed)

- **Artifacial** — AI video / face-swap; needs daily fresh ad content + an ad per workshop tool (`artifacial-ad-ideator` skill).
- **Infinet** — uncensored LLM platform (infinetai.org, on Venice.ai); AI-concept video ads.
- **ClipWith** — AI video editor on TwelveLabs, co-built with Tanner.
- **Archetype Index** — personality classifier + courses; migrating OFF Kajabi → self-built (Whop is the pick); the quiz lead-magnet (§13) routes leads here.
- **Cruncrr** — baby/child-safety scanner, co-founded with Rebecca Santos (ties to the Child Safety/PSA lane).
- **FlipOps** — proptech SaaS (Tanner technical, Mason GTM; Elijah supportive).
- Real estate development; jewelry (VVS); podcast (first guest: Derwin Scott, @dsdpaintings). **Long-form YouTube is the active pivot.**

---

## 18. Open hub follow-ups this State of Play implies (Elijah-gated)

1. **Surface sends-per-reach + avg-watch-time as first-class columns** in `refresh.py`/`metrics2026.py` and grade on them, not likes. (Verify the IG API exposes a `sends`/reshare field before promising the breakdown.)
2. **Ship the first carousels** via `carousel-builder` (AI-tool teardown / money-playbook / Myth-vs-Fact decks) and backtest his carousels vs reels by save-rate + send-rate once a few exist — replace borrowed marketer numbers with first-party truth.
3. **Run the §8 self-cannibalization + §10 money-retention backtests** on his 300-post history via `self-improve/grade.py`, and add the panels to `metrics2026.py`.
4. **Add `engaged_audience_demographics` + a follower-vs-engaged panel + a churn tracker** to the dashboard (§15).
5. **Wire "X Clearly Explained" + "AI Builder's 6-Pack" to `news-radar.py`** so each model/tool drop auto-drafts an episode; add the 5 named rivals to `viral-radar.py` (§9).
6. **Start a `yt-retention` reader** (analogous to metrics2026) to close the predict→observe loop on long-form once he has uploads.
7. **Stand up beehiiv + the comment→DM email-capture funnel + activate @Elijahclaudebot** (§13), and bake a capture CTA into the `content-intel-2026` / `weekly-content-plan` skills.
8. **Build a "Rising Sound Radar"** (sibling to `trend-radar.py`) + the API-vs-manual decision flowchart, and **mint 2–3 signature original "sonic hooks"** — use original audio as OFFENSE (audio-page taps are a named Reels signal `[platform-official]`) (§7, §19).
9. **One-time security hardening + Meta Verified + an IG zero-day runbook** (§16).
10. **Schedule the engines** — the level-up finding stands: 7 validated engines run on no schedule. Propose a `Weekly Agent Refresh.bat` so the measure/generate loop doesn't go stale.
11. **Add `auto-clip/cover.py`** (branded 1080×1920 grid-safe cover per clip) + the hook/loop/pacing QA gates into `viral-shortform-2026` (§20, §21).
12. **Stand up ONE Broadcast Channel + a `broadcast-draft` skill** as the always-on owned-audience spine + giveaway backstop (§23).
13. **Pivot Archetype Index course → recurring "Archetype Agent"** and ship one flagship "sell-executions" bot (Grade-My-Software / Viral-Hook-Grader) (§24).
14. **Re-scope `comment-triage` to a thread-engine** (5th "thread-seed" bucket, repeat-commenter ledger, pinned-first-comment seeding) (§25).
15. **Build ONE living AEO comparison hub wired to `news-radar.py`** + fix crawlability (robots.txt for GPTBot/PerplexityBot/ClaudeBot, `llms.txt`) (§26).
16. **Build the `newsjack-or-skip` decision layer** (story-type-aware half-life in `news-radar.py` + viral-radar saturation join) and run the engines more than daily during AI-drop windows (§28).
17. **Caption-SEO:** optimize the display NAME field + front-load first-125-char keywords + fill alt text + run the `trial_ab.py` SEO-caption test (his real lever is caption SUBSTANCE: word-count ~ reach +0.42, hashtags ~ noise) (§22).

---

## 19. Audio as OFFENSE — not just the API constraint

§7 treats audio only as a limitation. The bigger move is the offense: **a tappable original sound feeds a confirmed top-tier Reels signal.**

- **"Go to the audio page" is one of Instagram's FOUR named Reels predictions** (reshare, watch-through, like, audio-page tap — "a proxy for whether you might be inspired to make your own reel"). The model inputs are spelled out in Meta's Transparency Center, and the audio-reuse prediction appears in **Feed Recommendations too** (cross-surface). `[platform-official]`
- **Original audio is an attributable, discoverable ASSET:** it gets its own audio page, shows his username on every reel that uses it, and (public account) lets others reuse it — every external creator who taps "Use audio" on his sound fires the reuse signal back toward his handle. `[well-documented]` So a voice-only / original-audio API reel **mints a named audio asset rather than forfeiting the audio lever.**
- **Trending audio is NOT among the named CORE signals** (watch-time / sends / likes are) and is at most a modest secondary boost; original content out-distributes reposts. `[well-documented]` So the API voice-only path **loses almost nothing on ranking** in the typical case.

**The decision rule (one-screen flowchart):**
- **DEFAULT = API voice-only original-audio reel** — fast, automatable, attributable, safe, loses ~nothing on the core signals.
- **OVERRIDE to a MANUAL in-app trend-audio post ONLY when ALL of:** (a) the sound is genuinely rising, (b) the audio page/feed is itself the discovery vector for that piece, (c) the sound is cleared for his account classification (Meta Sound Collection or licensed — see §7 Business-vs-Creator caveat), (d) the format is built to RIDE the sound, not decorate it. Anything failing a–d ships via API.

**Moves:** (1) **mint 2–3 signature "sonic hooks"** (recognizable intro sting / catchphrase / "AI just did X" stinger) via ElevenLabs/compose-music so clips are tappable; (2) use a recognizable/curiosity sound in the **first 3s** to suppress the platform-official "watch <3s" negative predictor; (3) build a **"Rising Sound Radar"** (sibling to `trend-radar.py`) that scans TikTok Discover for sounds not yet crossed to IG and confirms via the real platform surfaces (trending-arrow + Professional Dashboard "Trending Audio") — **do NOT hardcode the unverified use-count/saturation thresholds** (the "1,000–10,000 uses," "5–7 day saturation," "first-48-hours" rules are all marketer rules-of-thumb with no source); (4) add audio-page-taps / plays-from-audio to `metrics2026` where the API exposes them.

---

## 20. Hook + editing craft layer (the per-clip QA gates)

Every craft rule here is a lever on the **platform-official** watch-time signal (Instagram weighs BOTH relative % watched AND absolute seconds; Explore tracks "finishing a video / 95%+"). `[platform-official]` Wire these as gates in `viral-shortform-2026` + the `auto-clip` pipeline.

- **Multi-layer hook = three SIMULTANEOUS layers in the first ~1s**, not three sequential seconds: (1) VISUAL interrupt — open on the payoff/result, never the windup; (2) on-screen TEXT hook ~3–7 words (sound-off); (3) VERBAL hook ~5–10 words. When all three reinforce ONE promise, the viewer "gets it" before the first syllable finishes. `[well-documented; word counts are vidiq's heuristic, not law]`
- **Design for a ~1s human keep-or-swipe decision inside a ~3s algorithmic read.** The strongest visual+text+first-word should land by frame ~24–30. The ~3s mark stays real as the algorithm's early-retention read (a >30% drop in the first 3s reads as a failed hook). `[marketer-claim on the exact 1s; direction sound]`
- **Pacing QA gate (the stopwatch test — codeable):** a visual change every **1.5–2s** for sub-60s clips, i.e. **5–7 changes per 10s** — where a "visual change" = hard cut / camera move / text-overlay swap / zoom / LUT shift / reveal. Flag spans below 4 (slow) or above 8 (noise). Hold two SANCTIONED exceptions longer (3–4s): a visual payoff and the loop-closing frame. `[marketer-claim — labeled 2026 editorial standard, not Meta data]`
- **The intentional LOOP** (high-leverage on short clips): cut so the last ~0.5s composition resolves back into frame 1 so viewers replay before realizing it restarted — manufacturing rewatches + inflating both absolute and relative watch-time. Construction: split the clip at midpoint, move the back half to the front, cross-dissolve the seam, match first/last frames. **Gate `loop_eligible` to short clips (~≤15s soft heuristic) OR tight visual-process beats — do NOT force a loop on a 40–60s talking-head** (the loop tax of sacrificing a clean verbal ending outweighs the gain). `[well-documented on construction; the exact ≤15s cutoff is a heuristic to A/B]`
- **Mid-clip re-hook for clips >~30s:** defend the mid-video sag (~40–60% mark — the only source-supported drop point) with a pivot / new visual / question; ensure `tighten.py` leaves no dead-air cliff there. **DELETE the fabricated 8s/15s/30s cliff stack** — those timestamps were not in any source.
- **Dual-length output:** auto-clip should emit BOTH a tight loop-eligible micro-cut (~≤15s, optimizes rewatch + relative WT) AND a complete-idea cut (~30–60s, optimizes absolute WT) from strong moments, then let his data decide which wins per niche — **don't hard-code one target length.** This directly exploits the platform-official "both relative and absolute watch time" signal. `[well-documented]`
- **Creator-fit note:** his AI/money content is concept-heavy (numbers, claim cards), not action-heavy — so build the loop on a **TEXT/graphic match** (same card position frame 1 = frame last), easier to make seamless than a motion match, and fits his carson-raps/infographic style. Same circular idea ships as a save carousel.
- **Add a SHARE lever to the craft, not just rewatch:** since sends-per-reach is a co-equal top signal, engineer share-worthiness too — a screenshot-able stat card, a "send this to someone who…" beat, a quotable claim.

---

## 21. Reel cover / grid thumbnail — a confirmed pipeline GAP

The grid changed and `auto-clip` has **no cover step** — verified by code inspection (modules are transcribe/highlight/reframe/facetrack/tighten/caption/broll_planner/color/colorkit/library; no cover/poster/thumbnail module). The pipeline ends at a finished `.mp4` and never emits a branded cover. `[well-documented, verified in-repo]`

- **The 2026 grid is 3:4, not 1:1.** Jan 2025 Mosseri moved the profile-grid preview from 1:1 to a taller **3:4** crop, and IG added native 3:4 (1080×1440) upload. **The brief's "1:1 + 4:5 safe zone" framing is OUTDATED.** `[platform-official]`
- **Binding design constraint:** on a 1080×1920 cover, keep ALL critical content (title text, face, logo) inside the **centered 1080×1440 (3:4) box** — that's what the GRID shows AND it survives the separate 4:5 (1080×1350) feed crop. The full 9:16 displays uncropped only in the Reels tab. Keep text off ~top-250px (username/audio) and ~bottom-340px (action UI), ~60px left / ~120px right margins (these pixel margins are third-party guide values — validate against the live UI). `[platform-official on 3:4; well-documented on margins]`
- **The cover is a first-class editable asset** (custom upload, pick any in-video frame, adjust grid crop, AND edit cover AFTER posting). `[platform-official]`
- **The "custom thumbnails get 65% more plays" stat is UNVERIFIABLE marketing lore** — attributed to "internal Instagram research" with no Meta source. **Do NOT relay the 65%.** Test it instead via official **Trial Reels** (same reel + same caption, change ONLY the cover, ~1,000-follower eligibility, space variants). `[marketer-claim deleted; Trial Reels is platform-official]`

**Moves:** (1) **add `auto-clip/cover.py`** — per ranked clip, generate a branded 1080×1920 cover PNG (face frame from facetrack + short hook line in brand type, all inside the 1080×1440 box) and emit alongside the `.mp4` in `out/` (DRAFT artifact, no publish); (2) standardize ONE branded cover TEMPLATE (fixed font/position, 3:4 guide baked in) so the grid reads as one cohesive AI/money brand; (3) **retro-fit covers on the back catalog** (covers are editable post-publish — DRAFT images for him to apply in-app); (4) for his niche, **bias the cover hook toward the NUMBER or AI-tool name** ("$0→$4k with this agent," "I let Claude run my IG") since profile visitors judge legitimacy off the grid.

---

## 22. Caption SEO + search/Google discovery — and his RECOMPUTED first-party truth

Captions are a discovery-surface (Explore, Search, Google) lever, NOT a core feed-ranking signal. Two corrections matter here, both from re-checking his own data.

- **He is NOT hashtag-heavy** (the premise to "fix" doesn't exist): recomputed live on `store.json` — hashtags per caption **max=5, median=5, ZERO posts over 5.** The real lever in HIS data is caption **SUBSTANCE**: caption **word-count ~ reach = +0.42 / ~ views = +0.40** (Spearman, n=300), while **hashtag-count ~ reach = −0.11** (essentially noise/slightly negative, NOT the "+0.17" originally claimed). `[well-documented, first-party recomputed]` → the test is "keyword-dense vs his current looser captions," not "keywords vs hashtags."
- **The "30% more reach / 2× likes for keyword captions" stat is an orphan citation-loop** — absent from the live Hootsuite article, repeated uncited downstream. **Do NOT relay 30%/2×.** Only the DIRECTION (keywords aid discovery, hashtags deprioritized) is supported. `[marketer-claim]`
- **Google indexes public IG content (official, July 10 2025):** public posts/reels from professional 18+ accounts are Google/Bing-indexable (retroactive to Jan 1 2020), ON by default, opt-out at Settings → Privacy. **Stories/highlights/bio are EXCLUDED.** His back catalog is Google-discoverable — a keyword-rich caption gains a second, evergreen Google-search audience that compounds. `[well-documented]`
- **Instagram DOES read audio + visuals** ("signals about the content within the video such as the audio track or visuals") — verbatim official. So put the core keyword/topic in the SPOKEN script + clean on-screen cover text. (Alt text being searchable is a Later/third-party claim, NOT on the Meta page — fill it anyway, near-zero cost.) `[platform-official on audio/visuals]`
- **Following hashtags was removed (Dec 2024); Mosseri: "hashtags are not a way to get more reach."** Hashtags now categorize, not distribute. `[well-documented]` Keyword-STUFFING actively hurts (Later: "doesn't help SEO and hurts readability").

**Moves:** (1) optimize the **display NAME field** (not the @handle) with keywords ("AI Automation | Business") — Later says it carries similar SEO weight, costs nothing; (2) **front-load the first ~125 chars** of every caption with the exact phrase a viewer would TYPE (it's the pre-"more" preview, the in-app search-match zone, AND the Google SERP snippet); (3) write **evergreen keyword captions** on cornerstone reels for compounding Google long-tail; (4) **always fill alt text** with a natural keyword sentence; (5) the gold-standard test uses official **Trial Reels** ("SEO caption" vs normal, matched reels, non-follower reach) — infra `trial_ab.py` already exists; the retrospective test needs a small `refresh.py` upgrade (per-post `views` with `breakdown=follow_type`, the exact pattern `sync_daily` already uses at line 264); (6) set the RIGHT success metric — **non-follower reach share + Search/Explore-sourced reach, NOT total likes.**

---

## 23. On-platform owned audience — Broadcast Channels FIRST

Before (or alongside) the off-platform owned audience in §13, IG has a free on-platform push surface he isn't using.

- **Broadcast Channels = a one-to-many DM feed where ONLY he sends** (followers react/vote in polls). First message triggers a one-time join notification to ALL followers; supports text/photo/video/voice/polls. `[platform-official]` It is **NOT governed by the 200/hr Graph-API automated-DM cap** (different surface; "no DOCUMENTED limit" ≠ guaranteed unlimited). At ~102k Creator/US he's comfortably eligible (the old 10k gate is gone); **setup is IN-APP ONLY — no Graph-API path**, so the hub drafts and he pastes.
- **This is the highest-leverage, lowest-cost owned-audience move:** it fixes the §13 funnel wound (comment→DM dies at ~200/hr and failed silently for ~11h in Nov 2025). A Broadcast Channel pushes a free DM to his whole opted-in audience as the always-on spine for every reel/long-form drop, feature ship, and giveaway link — **and a redundant delivery rail behind every "comment WORD" campaign.**
- **Subscriptions (paid, recurring) — DON'T launch yet.** Eligibility = 10k+/Creator/18+/clean-policy (he clears it), but it's invite/wave-based, and the real trap is economics: **"0% Meta commission" is true-but-incomplete** — in-app (iOS/Android) subscribers lose ~30% to the app-store layer; **only WEB checkout keeps ~98%.** `[well-documented]` And it's recurring content-DEBT: mobile-sub churn averages ~9%/mo `[well-documented, NOT IG-creator-specific]`. **Pre-condition: prove he can ship a subscriber-only deliverable every week for 8 weeks via the FREE Broadcast Channel first**, then convert that cadence to a paid web-checkout sub (best fit = Archetype Index, see §24).
- **Gifts (Stars) = the weakest of the three** for him — a flat ~$0.01/Star tip rail (~500-follower floor), monetizes attention spikes not relationships. His audience expects software/value over tipping.

**Moves:** (1) **stand up ONE Broadcast Channel this week** (not one per venture) as the distribution spine; (2) build a hub **`broadcast-draft` skill** (drafts the per-drop message + poll in his voice, staged for him to paste — the API can't post anyway, so it respects no-auto-publish by construction); (3) track channel join-rate and the sends-per-reach it drives against `metrics2026`.

---

## 24. Course → AI-agent productization (the monetization pivot)

The static-course business is decaying and the survivable unit is an **interactive, accountable, outcome-defined** product — most powerfully an AI agent that delivers the outcome 24/7.

- **The course isn't dead — it survives ONLY as the cohort/accountability WRAPPER around an outcome, never a standalone video library:** self-paced courses complete at ~10–20%; **cohort courses with a schedule + live sessions + peer accountability complete at 85–95% AND command 3–5× higher prices.** `[well-documented, cross-confirmed]` (Udemy cut its instructor subscription-payout share 25%→15% over 2023–2026 — a 40% cut — proxy evidence the model is decaying. `[well-documented]`)
- **The post-course stack:** free quiz/lead-magnet → paid **CHALLENGE** (time-boxed outcome sprint, the cold-to-paid converter) → **AGENT** (the scale layer that delivers the outcome 24/7) → paid **GROUP/community** (retention). The agent is the SCALE layer, not the front door. `[marketer-claim on the exact 4-layer prices — single source; validate before scaling]`
- **Agent pricing in 2026 is HYBRID by default** (base + usage ± outcome): seat-based pricing is declining for autonomous agents (21%→15% of SaaS firms in 12 months); hybrid surged (27%→41%) and is associated with higher growth/retention. Outcome-framing converts at a premium where the result is verifiable (Intercom Fin $0.99/resolution scaled $1M→$100M+ ARR). `[well-documented on the structural shift]`
- **The proven SOLO primitive: "sell executions"** — wrap ONE piece of trusted expertise as an input→output bot, free tier feeding paid. Works ONLY when the audience already trusts his methodology (NoteSmith: built in ~40h, ~$5k ANNUALIZED run-rate in week one off existing audience trust — a run-rate anecdote, not guaranteed cash). `[marketer-claim, single self-reported case]`
- **Marketplaces are DISCOVERY, not the revenue home** (correction: the GPT Store DOES have a live, US, engagement-based builder payout, but it's undisclosed/low; Poe pays per-message + a share of a referred user's first sub). Always drive the paid tier to his OWN Whop/Stripe checkout. `[well-documented]`

**Product-by-product call** (pricing = synthesis, mark every $ "pending A/B on his audience"):
- **Archetype Index = the #1 move:** do NOT rebuild it as a course on Whop. Convert the personality classifier into a recurring **"Archetype Agent"** (~identity-based monthly sub), fronted by a free quiz that doubles as the §13 email lead-magnet; retire the static course, keep a short live "build your archetype" CHALLENGE as the converter.
- **Artifacial** = HYBRID (base + per-render credit overage), not a course.
- **ClipWith** = usage/per-execution + base tier (classic hybrid SaaS).
- **Infinet** = already usage/subscription SaaS — leave as-is.
- **Cruncrr** = outcome/per-scan consumer utility ("one scan = one peace-of-mind check").

**Move:** ship ONE flagship "sell executions" bot to prove the model fast — a **"Grade My Software" agent** (the live-review rubric) or a **"Viral Hook Grader"** trained on his 300-post winners; free tier → paid → his checkout. Make "I turned my course into an agent" the build-in-public CONTENT itself.

---

## 25. The comment flywheel — comment-triage from spam-defense to THREAD-engine

Replies build the account-to-account relationship graph that biases future delivery — re-scope `comment-triage` accordingly.

- **The interaction-history graph is REAL and Instagram-official:** "Your history of interacting with someone" is a named ranking signal across **Feed, Explore, AND Reels** — every back-and-forth reply thickens the edge between his account and that commenter, biasing future delivery toward them. `[platform-official]`
- **Replying to comments produces a measured +21% engagement lift on Instagram** (Buffer, ~700k IG posts, within-account fixed-effects). **CRITICAL caveat: that's a CURRENT-post lift — the study does NOT establish carryover to FUTURE posts, and does NOT isolate first-hour vs later replies.** `[well-documented]`
- **The brief's "reply to 50%+ in the first hour → ~23% higher engagement on FUTURE posts" does NOT verify** — no primary source states it (it's a conflation of Buffer's +21% current-post with an unconfirmed DM-reply stat). Treat first-hour + future-post carryover as **hypotheses to A/B on his own data.** `[unverified]`
- **Comment DEPTH beats COUNT in 2026:** single-emoji "nice!" is discounted (post-2024 anti-pod); multi-sentence comments + back-and-forth threads carry more weight and lengthen dwell time (the official "time spent" Feed signal). `[well-documented on direction; magnitudes unknown]`

**Moves:** (1) add a **5th `comment-triage` bucket — "thread-seed"** = a real comment worth a 2–3-turn conversation; for these, **draft a reply that ENDS WITH A QUESTION back** (cheapest way to manufacture the depth 2026 weights); (2) add a **first-hour priority pass** (when run within ~60 min of a post, rank that post's comments to the top) — framed HONESTLY as a hypothesis since "first hour" is unverified; (3) **no bare-emoji replies** rule — default to substantive; (4) build a **repeat-commenter ledger** (log handles + counts to `memory.md`, always personally reply to 2+-time commenters) to deliberately thicken the official interaction-history edges; (5) **seed the thread at post time** — extend `carousel-builder`/`content-intel-2026` to draft a pinned first-comment question he pins on posting; (6) mine deep threads for DM-share-worthy lines + next-content ideas into `content-intel-2026`; (7) **BACKTEST the first-hour/future-post hypothesis** via `grade.py` before believing any "23%" number; keep the spam-hide path as hygiene, but make "threads seeded + repeat-commenter edges strengthened" the new north-star.

---

## 26. Answer-Engine Optimization — get cited by ChatGPT/Perplexity/AI-Overviews

A new compounding distribution surface his model-flood cadence is uniquely built to win.

- **There's no single "AI search" — engines cite from low-overlap source pools** (~11% domain overlap ChatGPT↔Perplexity). **Perplexity cites sources far more than ChatGPT** (~13% vs ~0.6% of responses), so a named creator is roughly an order of magnitude more "winnable" on Perplexity near-term; ChatGPT is the long-game. `[well-documented]`
- **What mechanically lifts citation (Princeton/GA-Tech/Allen-AI GEO paper, KDD 2024, 10K queries):** Quotation Addition +27.8%, Statistics Addition +25.9%, Cite Sources +24.9%, Authoritative +21.8% — **Keyword Stuffing is the WORST tactic.** His native output (benchmark numbers, direct model-card quotes, cited primary sources) is exactly the shape LLMs over-extract. `[well-documented — peer-reviewed]`
- **Freshness premium is real and large:** AI-cited URLs are ~25.7% fresher than organic (Ahrefs, 17M citations); ChatGPT cites URLs ~393 days newer than Google's top results. **Cadence is the moat** a static blog can't match. `[well-documented]`
- **CRITICAL counter-signal: plain "best X" listicles are LOSING citations** (ChatGPT listicle citations fell ~30% MoM, Seer) — EXCEPT those with fresh/"2026" content, comprehensive coverage, and **disclosed methodology** (accelerating fastest). So the play is NOT a thin "best AI tools" roundup but a **methodology-transparent, benchmark-backed, frequently-updated COMPARISON HUB.** `[well-documented]`
- **Off-page corroboration outweighs owned content:** unlinked brand MENTIONS correlate ~0.664 with AI visibility vs ~0.218 for backlinks (~3×, Ahrefs 75k brands). LLMs trust corroborated mentions over self-published claims. `[well-documented]`

**Moves:** (1) **build ONE living comparison hub** per high-traffic decision ("Best AI Video Tools (Updated {Month} 2026)," "Claude vs GPT vs Gemini for {task}," AI-tool pricing tracker) — comprehensive, disclosed scoring methodology, HIS benchmark numbers + direct quotes + cited primaries, visible "Last updated"; (2) **wire `news-radar.py` to auto-refresh it** on every model drop (append a dated cited entry, bump the year in title/H1) — operationalizes the freshness premium for free; (3) **3-surface distribution loop per update** (YouTube companion clip → AI-Overviews; Reddit/LinkedIn post with his named entity → ChatGPT+Perplexity; fast index → Perplexity same-day); (4) seed off-page corroboration (3–5 third-party roundups/quarter, speak tool names clearly so transcripts are accurate, pursue a Wikipedia/vertical-DB presence); (5) **FIX THE FREE WIN — crawlability:** allow GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended in robots.txt, server-render, add `llms.txt`; (6) instrument an AI-citation tracker (Perplexity = near-term KPI, ChatGPT inclusion = long-game).

---

## 27. Faith as an economic asset (not just identity)

§5/§6 frame faith as the un-copyable differentiator; the data says it's also an engagement + retention + trust lever — IF expressed as identity, never preached.

- **PEER-REVIEWED mechanism:** a ~54,400-post study of Christian influencers found **religious (shared-identity) cues INCREASE engagement while promotional (commercial-intent) cues DECREASE it.** Lead with identity/shared-meaning, soft-pedal "buy this." `[well-documented — peer-reviewed]`
- **Cold-audience trust is contracting, shared values are a hedge:** Edelman 2026 (33k+ respondents) — ~7 in 10 are "insular," hesitant to trust those with different values; the creator economy is an "attachment economy" where trust is borrowed from a creator the audience already holds close. A values-anchored creator captures trust a neutral one structurally can't. `[well-documented]`
- **The craft rule (converges with the data): SHOW values through actions/standards** (integrity, generosity, stewardship, how he prices) rather than TELL through doctrine — no proselytizing, no attacking other beliefs (which activates the ~70% out-group reflex AND triggers persuasion-resistance). `[marketer-claim, converges with verified data]`
- **The real risk vector is COMBATIVE framing, not the faith itself** — faith-as-identity (warm, stewardship-framed) is rewarded; faith-as-culture-war risks both suppression and the out-group reflex. (A faith-specific algorithmic penalty is widely asserted but NOT confirmed in any platform doc — `[unverified]`; the guardrail is safe either way.)

**Moves:** (1) anchor on ONE repeatable value-line (stewardship / "multiply what you're given to bless others") and NEVER preach it — express it only through HOW the money/AI content is done (radical cost transparency, refusing hype/scammy plays, free high-value teardowns); (2) recruit **faith-ALIGNED** affiliate/brand partners (stewardship/budgeting apps, ethical-finance, Christian-owned SaaS — verified-joinable, rates ~4.5–20% tier-dependent) where shared values pre-warm the audience; (3) make the lead-magnet a CONCRETE stewardship/AI-income deliverable; (4) **run a tasteful A/B on his OWN 300-post history first** — tag past reels values-cue vs pure-tactical and check skip/save/watch-time deltas via `metrics2026` + `self-improve` before trusting any external magnitude.

---

## 28. Newsjacking velocity — the two-clock react system

The §4 reactive themes need a decision LAYER, because two distinct clocks govern a newsjack and the engines already hold the machinery.

- **CLOCK A (story decay — the binding constraint on WHEN):** X tweet half-life ~80 min, ~95% dead by 24h (peer-reviewed, ICWSM 2023); YouTube news-video 24h half-life ~7h (2–15h range, peer-reviewed). Short-form story decay is measured in HOURS. `[well-documented]`
- **CLOCK B (YOUR post's distribution decay — Graffius 2026, 5.6M+ posts):** Instagram **18.27h**, X 52 min, Facebook 1.43h, YouTube 10.6 days. `[well-documented]` **Consequence: a same-day reel shipped inside a ~7h-half-life story window is NOT "too late"** — the IG post itself distributes for ~18h.
- **React-window gate (directional, NOT measured):** newsjack practitioner rule is "react within hours, inside a <24h window" (David Meerman Scott). GREEN = act now if the story is hours-old and inside its half-life; YELLOW = react only with a contrarian/novel angle as it ages; RED/SKIP = breaking event older than ~24h. **The original "0–2h optimal / 6–24h diminishing" hour thresholds are UNSUPPORTED by the cited source — treat all hour boundaries as tunable heuristics.** `[marketer-claim]`
- **Story-TYPE routing:** event-pegged decays fast (dated/named hook: "Gemini 3.1 just dropped — here's the catch"); evergreen compounds (timeless title from the same spark: "How to tell if an AI benchmark is lying to you") — so a model-drop spawns BOTH a perishable reel (ships today) and a banked evergreen reel.
- **The engines already hold the machinery** `[platform-official — verified in code]`: `news-radar.py` has decay built in (`RECENCY_HALFLIFE_H = 36.0` at line 60; `recency_score()` at 264–269; `score_story()` at 288–297) but uses ONE fixed global half-life. `viral-radar.py` supplies the "is this story ALREADY saturated?" signal (ranks competitor posts + captures captions).

**Moves:** (1) build a thin **`newsjack-or-skip` decision layer** that JOINS the two engines — classify each story by type, score against a type-specific half-life, cross-check viral-radar's recent competitor captions for saturation, emit a one-line verdict (**NEWSJACK-NOW / CONTRARIAN-ANGLE / EVERGREEN-EXPLAINER / SKIP**); (2) make `news-radar.py`'s half-life story-type-aware (a `HALFLIFE_BY_TYPE` dict + keyword classifier — a ~30-line additive change; seed values from the verified anchors but mark them tunable); (3) wire a same-day DRAFT-in-minutes path (NEWSJACK-NOW → `content_angle` hook → carousel-builder OR voice-only reel script, publish click stays his); (4) **schedule the engines more than daily** during the binding window (AI drops cluster on weekday US mornings/conference days) — closes the level-up "engines on no schedule" gap; (5) **log every newsjack decision + outcome** to `self-improve` and backtest whether faster react actually correlates with better held-out performance on HIS data (the "speed wins" / "first-hour velocity" claims are unverified — only his data confirms them).

---

## 29. Long-form funnel + membership math (model it correctly before staffing)

When the YouTube pivot gets real, model the funnel on the verified mechanics — and avoid the subscriber-as-reach error.

- **Recommendations drive more viewership than subscriptions or search (YouTube-official).** So **do NOT build a subscriber→reach loop into the model** — each video is independently distributed on its own clicks × satisfaction-weighted retention; subscribers are a downstream RESULT + a monetization floor, not the growth lever. `[platform-official]`
- **The ranking objective is "valued watch time"** — only time on videos a viewer would rate 4–5 stars counts (YouTube trains an ML model on post-watch surveys to score the ~99% who never answer). **Lead with valued watch time, not a fixed 30–60 min:** a tight ~15–22 min video that satisfies beats a padded 40-min one. `[platform-official]`
- **Shorts→sub is RELATIVE, not absolute:** Perkins' "<10%" means Shorts viewers subscribe at under one-tenth the rate of long-form viewers (absolute Shorts→sub is ~0.05–0.5% of views). **Budget Shorts as ~zero-revenue acquisition** whose ROI is realized only downstream in long-form conversion + RPM. `[marketer-claim — validate on his first 30–60 days]`
- **Niche RPM strongly favors his lane:** US finance long-form RPM ~$10–29 (CPM ~$15–50), tech mid-high-teens, vs gaming ~$3–7 and Shorts ~$0.05–0.30; **8+ min unlocks mid-roll.** Long-form-led with Shorts as feeders. `[well-documented; corrected DOWN from the inflated "$28–40" the original draft carried]`
- **Memberships:** YouTube takes 30% (creator nets 70%; iOS in-app loses an ADDITIONAL Apple cut). `[platform-official]` Conversion/churn bands (0.5–3% sub→member, 5–10% monthly churn) are **marketer estimates — treat as a wide tunable band, model churn as the key drag, validate on his channel.** `[marketer-claim]`
- **New-channel reality:** every upload is seed-tested with a small audience; early videos looking small (hundreds of views) is EXPECTED, not failure — budget **10–20+ long-form uploads as a seeding phase.** (The "48h window / 8%→4–5% CTR" benchmarks are observational, never YouTube-confirmed.) `[well-documented mechanic; numbers are planning priors]`

**Pillar mapping** (the 3 candidate pillars → their jobs):
- **MODEL-FLOOD ("I built/tested X with the newest model") = the compounding VOLUME engine** — highest evergreen + suggested demand + concrete payoff = strongest Shorts→long-form bridge. Front-load evergreen search-anchored titles so the back-catalog compounds for months.
- **BUILD-IN-PUBLIC = the membership/community engine** (members come disproportionately from parasocial build-in-public followers) — recurring numbered series, gate behind-the-scenes/templates/actual agent prompts as a higher tier.
- **AGE-14 TESTIMONY = the flagship identity anchor** (one or two high-production origin/documentary videos + milestone updates) — lowest search demand but maximal emotional satisfaction + the strongest "why subscribe to ME" hook. Pin it; make it the channel trailer. NOT the volume engine.

**Move:** model two decoupled stages — Stage 1 (reach) = Shorts + long-form CTR × satisfaction → impressions, subs as OUTPUT; Stage 2 (revenue) = long-form viewers → ad RPM ($10–29 finance) + memberships (70% net, conversion a wide band, churn a drag). Run conservative vs aggressive scenarios before staffing, and **validate the <10% Shorts→sub, membership conversion/churn, and 48h-CTR numbers on his OWN first 30–60 days** (none are primary data). Stand up a `yt-retention` reader (analogous to `metrics2026`) to close the predict→observe loop.

---

> **Profile note for Elijah:** `profile.md` line 9 still says "~99.7k followers" while live `stats.md` says **102,675**. This State of Play uses the live number — refresh that line in your profile when you get a chance.
