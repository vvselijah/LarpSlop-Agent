# The Name-Search Plan: Building a Real Online Story (and a Google Knowledge Panel) for Elijah Sullivan & Tanner Carlson — the Cheapest Legitimate Way

*Deep-research plan · drafted 2026-06-29 · for Elijah Sullivan (@elijahaifl, ~104.7k) & Tanner Carlson (Clarity Digital Development / archetypeindex.com)*

> **The job, in Elijah's own words (from the vault):** *"Figure out a way to start building Actual SEO around my name, Elijah Sullivan and Tanner's name Tanner Carlson because there's other people with our names that have Actual SEO when you search Our names… getting published articles about us and things that we've done and things we've created… when people look either of us up… it comes up with only our information and data. I feel like published articles from high credibility sources will be the best route."*
>
> This document is the answer to that note. You two have **real** credibility (shipped products, a live company, a 100k+ audience, an NYU CS background, genuine accolades). You have almost **zero** structured online footprint. The whole point of what follows is to close that gap honestly — and because you have real credibility to protect, doing it the fake way is more dangerous for you than for a nobody.

---

## 1. TL;DR — the honest big picture

**A Google Knowledge Panel is not a thing you buy, build, or "claim into existence." It is the *visible output* of Google becoming confident it understands you as an entity.** You engineer the entity; the panel is downstream. Anyone who sells you "a guaranteed Knowledge Panel" is selling a scam (or a manipulation Google later strips).

The good news, and the single most important myth to correct: **there is NO fame/notability bar in Google's Knowledge Graph.** Unlike Wikipedia, Google "just wants to understand everything." An ordinary founder or creator absolutely can earn a panel — the gate is **data clarity and consistency across enough corroborating sources,** not celebrity. You two qualify on substance; you're just invisible to the machine right now.

The realistic path is a corroboration loop:

1. **Pick and own one "Entity Home"** — a single page you control that Google accepts as the source of truth about each of you (best case: an About page on a personal-name domain). Mark it up with `schema.org/Person` + a `sameAs` array linking every profile you control.
2. **Make every profile say the *same thing*** — identical name spelling, bio, headshot, links back to the Entity Home. Consistency is the #1 driver of Google's confidence; conflicting data is the #1 reason no panel appears.
3. **Build ~20 consistent third-party corroborations** — Wikidata, Crunchbase, podcast/interview bios, guest bylines, real press — all stating the same facts, reciprocally linked.
4. **Wait & monitor**, then **claim** the panel once it appears.

**Timeline:** ~3 weeks to ~3 months *after* the corroboration work is done, sometimes faster, longer if your name is ambiguous (and "Elijah Sullivan" / "Tanner Carlson" are common — namesakes already outrank you, exactly as the vault notes, so expect the slower end and plan extra corroboration). Long-term stability is built over years of staying consistent.

**Cost:** the entire core can be done for **~$10–20/year** (a domain you probably already half-own via `claritydigital.dev`) plus your time. Everything that actually moves the needle is free or near-free. Paid tiers (a budget press release, a podcast-matching sub) are optional accelerants, not requirements. No legitimate vendor can guarantee a panel.

**What's already in your favor (the substance bank in §7):** a live company (Clarity Digital Development), multiple shipped products (Archetype Index/archetypeindex.com, ClipWith.ai, Artifacial, Infinet), a 104.7k-follower verified IG account with reels hitting 100k–215k shares, an NYU CS co-founder, and a genuine self-made arc. That's more than enough raw material — it just needs to be made legible and corroborated.

---

## 2. How it actually works (entity → Knowledge Graph → panel)

Two hurdles, in order (Jason Barnard / Kalicube's framing, the recognized authority here):

- **UNDERSTANDING** gets you *into* the Knowledge Graph. Google has to be able to answer: who is this, what do they do, who do they serve, how do they relate to other *known* entities (companies, schools, products, people)?
- **CONFIDENCE** keeps you there and surfaces the panel. Google must be confident enough in that understanding — and confident the searcher means *you* and not your namesake — to show a panel.

**The Knowledge Graph** is Google's database of entities (people, places, things) and the facts linking them. A person panel appears only once Google (a) has an entity for you, (b) understands it, and (c) trusts it. You can't target the panel; you raise Google's confidence in the entity and the panel emerges.

**The Entity Home** is the master lever: ONE page you own that Google treats as the authoritative description of you. Ranked best-to-worst:
1. An "About me" page on your **own personal-name domain** (best).
2. The homepage of your personal site.
3. An About page on your company site (e.g. a `/team/elijah-sullivan` page on `claritydigital.dev` — a strong, realistic option for you two since the company is your shared anchor).
4. A social profile (LinkedIn/X) — last resort.

**Critical warning:** if you don't *define* your Entity Home, Google picks one for you — often a random social profile you don't fully control — and **changing Google's chosen Entity Home later is exceptionally slow, costly, and frustrating.** Decide it deliberately, now, before Google guesses.

**The corroboration loop** (this is the whole mechanism):
- On the Entity Home, describe yourself clearly and add `Person` schema with a `sameAs` array (every official profile). *Verified by Google's own docs:* `sameAs` is the recognized way to declare "all these profiles are the same entity (me)" and help Google disambiguate you. Frame it honestly — it's an **identity/disambiguation signal, not a magic ranking switch and not a guaranteed panel.**
- Get authoritative third parties to state the **same facts.** Third-party corroboration outweighs anything you say about yourself. Kalicube's working number is **~20 consistent corroborating sources** (fewer if they're high-authority).
- Link reciprocally: Entity Home links out to corroborators; they link back. Google reads that self-confirming web as verification.

**On Wikipedia and Wikidata (myth-correction, verified):**
- A Wikipedia page is **NOT required.** Kalicube's data: the share of person-entities sourced from Wikipedia dropped from ~41% (Jun 2023) to ~12% (Sep 2023); ~87.6% of person entities have **no** Wikipedia page. Most founder panels are not Wikipedia-based. (A *legitimate* Wikipedia page, if you ever truly qualify, roughly halves the corroboration count you need — but it's a downstream effect of real notability, never a starting move.)
- **Wikidata** is the highest-leverage *structured* source you can touch yourself — but with a **verified caveat:** you *can* create an item (there's no Wikipedia-style fame bar; meeting one of three criteria is enough), **but only if you can cite serious, independent third-party references.** An item sourced only to your own site/socials, or created by a single-purpose self-promo account, gets flagged and deleted. And it's **one input among many, not a switch** — a Wikidata item alone rarely conjures a panel. Treat it as a cheap, worthwhile *supporting* node **once you have a few independent references to cite** (so it slots best at the end of Phase 1 / into Phase 2, not day one).

**Claiming ≠ creating.** You can only claim a panel that *already exists*. Claiming is verification/management. Even after a verified claim you **cannot directly edit facts** — you can only *suggest* changes (Google decides; verified suggestions get priority). To change a hard fact, you change it at the source and let it propagate. (Verified against Google's official docs — accurate.)

---

## 3. The phased plan

> **Standing rule baked into every phase:** nothing is auto-published. Drafts, container-creation, and profile setup are fine; the final publish/post click is Elijah's, per the hub's #1 rule. And public-facing bios use **only the public, verifiable accomplishments** in §7 — the sensitive private beats stay out (see §5/§7).

### Phase 0 — Own your properties (the foundation; do this first, ~1–2 weeks part-time, ~$0–20)

Nothing else works until this exists. This is ~80% of the value and ~5% of the cost.

| Step | Who | Cost | Effort | Outcome |
|---|---|---|---|---|
| **0.1 Build the canonical "identity kit"** for each person: exact name spelling, one short bio, one high-res headshot, primary URL, full list of profile links. Reuse verbatim everywhere. | Both (each their own) | Free | 1–2 hrs each | The single source that keeps every profile consistent — the thing that makes you legible to Google. |
| **0.2 Lock the Entity Home.** Decide deliberately. Recommended: dedicated person pages on the shared company site — `claritydigital.dev/team/elijah-sullivan` and `/team/tanner-carlson` (you control it, it ties both names to shipped products, and the company is your strongest existing credibility node). Optional upgrade later: `elijahsullivan.com` / `tannercarlson.dev` personal domains as the *true* best-case homes. | Tanner builds (engineer); Elijah supplies copy | $0 (existing domain) to ~$20/yr if you add personal domains | Half a day | The one page Google will treat as truth — chosen by you, not guessed by Google. |
| **0.3 Add `schema.org/Person` + `ProfilePage` JSON-LD** to each Entity Home: `name`, `image`, `jobTitle`, `worksFor` (Clarity Digital Development), `knowsAbout` (AI software, video, real estate, etc. — drives topical/AI-search understanding), `alumniOf` (NYU for Tanner), `award` (only real ones), and a **`sameAs` array** of every profile. Validate at Google's Rich Results Test. | Tanner | Free | 1–2 hrs | "Google's native language" — declares these profiles are one entity and where to corroborate. |
| **0.4 Verify each Entity-Home domain in Google Search Console** (DNS TXT). | Tanner | Free | 30–60 min | The **most reliable** future route to *claim* the panel (the "globe icon" path). Also lets you request indexing. |
| **0.5 Optimize LinkedIn for name-search** (each person): custom vanity URL = your name; keyword-rich headline (≤220 chars); front-load the first ~300 chars of About with name + what you do + who you serve; complete the profile. | Each | Free | ~1 hr each | LinkedIn's ~98 domain authority near-guarantees a page-one slot for your name — the highest-ROI single profile after your site. |
| **0.6 Standardize name + headshot + bio across ALL existing profiles** (IG, YouTube, X, LinkedIn, GitHub, beacons.ai). One spelling, one photo, one bio, link back to the Entity Home. Fix/kill conflicting or stale listings. | Each | Free | 1–2 days grind | Consistency = confidence. This is the most common self-inflicted wound; fixing it is pure upside. |
| **0.7 Stand up cheap aggregator nodes:** Gravatar + About.me (free), wired into each `sameAs`. | Each | Free | 1–2 hrs | More page-one real estate + more identity-triangulation spokes pointing at the hub. |

**Phase 0 outcome:** each of you has a controlled Entity Home, machine-readable identity, a verified domain, an optimized LinkedIn, and a consistent profile web. This alone often starts displacing namesakes on page one within weeks.

### Phase 1 — Structured entities (the free, self-serve corroboration layer; ~1–2 weeks, ~$0)

Each profile you legitimately hold becomes another `sameAs` node corroborating who you are.

| Step | Who | Cost | Effort | Outcome |
|---|---|---|---|---|
| **1.1 Crunchbase person profiles** (any socially-authenticated user; name only required) — link to Clarity Digital Development, Archetype Index, ClipWith. | Each | Free | 30–60 min | A trusted structured node Google ingests; ties names → ventures. |
| **1.2 Crunchbase / company entity for Clarity Digital Development** (and list the products as ventures). | Tanner | Free | 1 hr | Strengthens the shared anchor both names hang off. |
| **1.3 GitHub profiles polished** — real name, bio, link to Entity Home; the `clarity-digital-development` org made presentable (it hosts the live TOI/archetypeindex.com app). | Tanner (Elijah's optional) | Free | 1 hr | A genuine, verifiable "they actually build things" signal. |
| **1.4 Claim only what you truly qualify for, with evidence:** ORCID (free, if either does any research/writing/innovation worth an ID); IMDb **only** if a real film/TV/web credit exists (it's verified and declined otherwise — do not fabricate); Muck Rack only if genuinely a working journalist (you're not — skip). | Each, selectively | Free | Varies | Each legit node = another corroboration. Do **not** invent credits — fabrication poisons the whole web. |
| **1.5 Wikidata items** — *only after* you have a few independent references to cite (so do this near the end of Phase 1 or alongside Phase 2). Cleanest path: have a third party create it (an editathon, a collaborator) and then maintain it; if you self-create, disclose any paid relationship and source **every** claim. Add `instance of: human`, occupation, `worksFor`, official site, and external-ID links (Crunchbase, ORCID, GitHub). | Each | Free | 1–2 hrs + learning curve | The externally-verifiable structured layer that feeds the Knowledge Graph — a real supporting signal, not a guaranteed lever. Will be deleted if under-sourced, so gate it on having sources. |

**Phase 1 outcome:** 4–8 high-trust structured nodes per person, all cross-linked, all saying the same thing.

### Phase 2 — Cheap authoritative mentions (earned third-party corroboration; ongoing, ~$0–50/mo)

This is the part that actually builds *Google's confidence* and human credibility, because it's other people describing you. Ranked by credibility-per-dollar (full ladder in §4).

| Step | Who | Cost | Effort | Outcome |
|---|---|---|---|---|
| **2.1 Set up the FREE journalist-query stack** and pitch it like a habit. Verified 2026 state: **HARO is back and free** (Featured.com reacquired and relaunched it April 2025 as a free email newsletter); **Source of Sources (sourceofsources.com)** — Peter Shankman's free, no-paywall successor — is the one most lists miss; **MentionMatch** (ex–Help a B2B Writer) is free and great for SaaS/tech. Featured.com and Qwoted have usable free tiers but are effectively freemium (real volume is paid). **Connectively is dead — do not sign up.** | Elijah (and Tanner for technical/B2B queries) | Free | 2–3 hrs setup; 20–40 min/day pitching | Quotes/mentions in real outlets. ~30% of relevant pitches convert; speed (<1 hr) + a specific data point win. **Accept nofollow placements** — in AI search the brand mention itself is the asset (Semrush 2025: nofollow and dofollow correlate near-identically with AI-search visibility). |
| **2.2 Podcast-guesting engine.** Free start on RadioGuestList + MatchMaker.fm (free/trial) to bank 2–3 credits, then optionally PodMatch (~$6–38/mo). Elijah's the natural on-camera guest; Tanner can do technical/founder shows. **Never pay a host to appear; don't cold-email shows.** | Elijah lead; Tanner selectively | Free–$38/mo | Profile setup ~3–4 hrs; ~1 hr/booking | Each appearance = a bio page (corroboration) + clippable content. One operator hit 30+ in 3 months. |
| **2.3 Repurpose every appearance/quote** into owned proof: clip episodes with the hub's `auto-clip`/`caption-engine` pipeline → Reels/Shorts; "I joined [show] to talk about X" on LinkedIn + IG; maintain an honest "as featured in" strip on the Entity Home. | Elijah (hub pipeline) | Free | 1–2 hrs/appearance | One booking → weeks of content + a permanent trust signal. This is where credibility compounds. |
| **2.4 Owned bylines** on LinkedIn Articles + Medium + (optionally) a Substack as a portfolio, then pitch 2–3 niche industry blogs/month (DR 40–60, tight topical overlap, personalized to the editor) for real guest bylines. | Each, in their lane | Free | 2–4 hrs/article | Self-published = portfolio (borrowed credibility); an earned byline on a recognized site = transferred authority + another corroboration. |
| **2.5 The progress + AI-news blog on `archetypeindex.com`** — Elijah's own recorded idea, and the hub's prior recommendation. A documented build log + AI-news commentary on the owned domain, with author pages for both names linking to shipped products. Drafts auto-generated, **Elijah approves each post** (respects the publish gate + $0-API constraint). | Tanner builds; Elijah approves | Free (owned domain); API cost only if auto-drafted | Moderate dev (fits the TOI/Next.js stack) | Compounds name SEO + product SEO + a fresh-content magnet — a self-owned "ultimate portfolio with our names and data," exactly as the vault note describes. *(Note: a `docs/plans/2026-06-28-ai-news-progress-blog.md` plan is referenced in memory but isn't in this worktree — read it from the main hub copy before building so you extend it, not duplicate it.)* |
| **2.6 (Optional, sparingly) ONE budget press release** via EIN Presswire (~$149) or NewswireJet (~$129) tied to a *real* milestone (a launch, a data study, a partnership). Skip premium wires ($350–3,000+) entirely. | Either | $129–149 once | 2–3 hrs to write | A credibility "floor" you can reference — **not** earned coverage. Lowest credibility-per-dollar of the legit options; use only around genuine news. |

**Phase 2 outcome:** a steadily growing pile of consistent, independent mentions — the fuel for Google's confidence and for human trust.

### Phase 3 — Notability, Wikipedia, and claiming the panel (the long horizon; months, ~$0)

| Step | Who | Cost | Effort | Outcome |
|---|---|---|---|---|
| **3.1 Monitor.** Search each name in an incognito window weekly. Watch page-one ownership climb and watch for a panel to appear. | Either | Free | 5 min/week | Early signal of when to claim. |
| **3.2 Earn genuine notability** (the real Wikipedia prerequisite): significant coverage in *multiple independent reliable* outlets. Press releases, interviews, self-published posts, and councils do **not** count toward notability. Keep a citation tracker of every genuinely independent mention. | Both | Free (your time) | Ongoing, this is the hard part | The only honest road to a Wikipedia article and a more durable panel. |
| **3.3 Wikipedia — only if/when you genuinely qualify.** Then post a neutral request at Articles for Creation / Requested Articles with a conflict-of-interest disclosure and let an independent editor write it. **Never** self-write or pay for it (see §5). | Whoever qualifies first (likely Tanner via NYU + shipped products + any press) | Free | Long-horizon | Roughly halves the corroboration needed; a strong (not required) panel anchor. |
| **3.4 Claim the panel once it exists.** Sign into Google → search your name → "Claim this knowledge panel" → verify via a **linked official account** (YouTube/X — fastest) or **Search Console domain ownership** (most reliable; needs the Entity-Home "globe icon" on the panel — which is why Phase 0.4 matters). | Each | Free | 15–30 min if a profile/SC is already linked | Verified management of your own panel. |
| **3.5 Manual claim if no auto route.** The live form requires: your relationship to the entity, the panel link, **screenshots proving admin access to 2–5 official profiles that rank on your panel's SERP**, and a **selfie holding your government photo ID** (Google's help page omits the ID/selfie step, but the live form requires it). Prep these before starting. | Each | Free | 30–60 min; review days–weeks | Verification when the easy path isn't offered. |
| **3.6 Manage it.** Use the Feedback button to *suggest* corrections (verified suggestions get priority). You can most readily influence the featured image; you generally **cannot** edit the subtitle, any Wikipedia-sourced text, or "People also search for." To change a fact, fix the source and let it propagate. | Each | Free | Light, ongoing | Honest, durable control. |

---

## 4. The cost ladder (ranked by credibility-per-dollar)

### Tier $0 — do ALL of this; it's where the real leverage is
- Entity Home page on the existing `claritydigital.dev` (or free host) + `Person`/`ProfilePage` schema + `sameAs`.
- Google Search Console verification.
- LinkedIn optimization (vanity URL, headline, About).
- Name/headshot/bio consistency across every profile.
- Gravatar, About.me, GitHub, Crunchbase (person + company), ORCID (if applicable).
- Wikidata item (free — gated on having real independent references to cite).
- Free journalist queries: **HARO (relaunched), Source of Sources, MentionMatch**; free tiers of Featured.com & Qwoted.
- Free podcast matching: RadioGuestList, MatchMaker.fm (free/trial).
- Owned bylines: LinkedIn Articles, Medium, Substack.
- The progress/AI-news blog on `archetypeindex.com` (owned).
- Monitoring + claiming + managing the panel.

**This tier alone can produce a Knowledge Panel.** Everything below is an *optional accelerant.*

### Tier cheap (~$10–50/mo or one-off) — only if you want speed
- Personal-name domains `elijahsullivan.com` / `tannercarlson.dev` (~$10–20/yr each) — upgrades the Entity Home from company-page to the true best-case.
- PodMatch (~$6–38/mo) — more/better podcast bookings once you have credits.
- IMDbPro (~$20/mo) — *only* if there's a real credit to manage (optional even then).
- ONE budget press release, EIN Presswire (~$149) / NewswireJet (~$129) — tied to genuine news, used rarely.

### Tier optional paid (later, eyes open) — lowest credibility-per-dollar
- A *legitimate* publicist/PR firm that pitches journalists for **earned** (non-guaranteed) coverage: ~$2k–$10k+/mo. The bottleneck this solves is the corroboration grind, not the concept. **A guarantee is the tell it's a scam.**
- Kalicube / a reputable entity-SEO specialist to run the whole entity build for you (premium; no one can guarantee a panel).
- **Avoid entirely:** paid "councils" (Forbes/Entrepreneur/Newsweek, ~$2,500–7,400/yr), premium press wires, and anything "guaranteed." See §5 for why these are *worse* than nothing for people with real credibility.

---

## 5. What to AVOID (and why it's *more* dangerous for you, specifically)

**The asymmetry that should govern every decision here:** a person with *zero* real credibility who fakes a presence risks little — if exposed, they just return to zero. **You two have real credibility, so the same fakes are far more dangerous:** the discerning people you want to reach (investors, serious partners, fellow operators) actively pattern-match for bought signals, and *one* exposed fake makes them re-weight *all* your genuine wins as possibly also fake. The fakes don't even fool the audience that matters — they fool no one and burn the trust that does.

**Radioactive — never do these:**
1. **"Guaranteed Knowledge Panel" vendors** ($2k–$15k). No legitimate paid path exists. Best case wasted money; worst case Google strips the manufactured signals and you're flagged. The standard scam plays: hidden paid Wikipedia edits, mass low-quality press-release syndication, fake database entries, or outright theft (a screenshot from a manipulated logged-in Google session as "proof"). Any **guarantee, money-back promise, or "back-end access"** offer is the tell.
2. **Paid Wikipedia articles.** *Verified nuance:* paid editing isn't banned outright — **undisclosed** paid editing is what violates Wikipedia's Terms of Use, and it's how commercial "write your page" services operate (concealment, sockpuppets). Such articles get deleted for failing notability or for promotional tone, and exposure draws negative press and leaves a permanent public record on the talk page (see Wiki-PR 2013, Operation Orangemoody 2015: ~381 accounts banned, 200+ articles deleted; the Ramaswamy 2023 paid-editor blowup). For people with a real reputation, this is a permanent, searchable stain.
3. **Buying followers / engagement / reviews.** Now an **FTC civil-penalty offense** (Fake Reviews & Testimonials Rule, in force Oct 2024; up to ~$53k/violation; first warning letters already issued). Detectable by the brand audits Elijah's deals will increasingly require, suppresses reach, and one exposure retroactively taints your genuine 104.7k-and-real-shares numbers — which are your actual leverage.
4. **Pay-to-play "as seen on Forbes/Entrepreneur/Newsweek" councils & guest-post packages.** Sophisticated audiences increasingly read a wall of media-logo badges as a *red flag*, not a green one ("anyone with a credit card can join"; Newsweek and Fortune paused theirs; documented BuzzFeed-style exposures where outlets quietly pulled the articles). Low signal, real downside, and the Oct-2025 Google spam update specifically targets the AI-guest-post-farm / paid-link versions (penalties up to de-indexation; Forbes ended its contributor program partly over this).
5. **Third-party "get verified" services** (IG/Meta blue check). Pure scam/phishing. The only real paths are the free in-app request or the official Meta Verified subscription ($7.99 mobile / $14.99 web). False info during verification can disable the account.
6. **AI-spun fake bylines / fake-expert personas** (AI headshots, fabricated bios). When exposed it reads as deliberate deception. *Honest line:* AI-assisted drafting in your **own voice under your real byline** is fine; manufacturing a fake expert is the trap.

**Safe-ish gray zone (fine, with honest framing):** AI-assisted writing under your real byline; soliciting reviews/testimonials from *real* customers/collaborators; hiring a real publicist for *earned* (non-guaranteed) media; the official Meta Verified subscription; ORM that surfaces *true* positive info. **The line is always: is it TRUE and attributable, or manufactured to look organic?**

---

## 6. START-HERE checklist (the first 5–10 concrete actions, this month)

Ordered for momentum — early wins, no spend.

1. **Write both identity kits** (name spelling, one bio, one headshot, primary URL, profile-link list). *Owner: Elijah for his, Tanner for his. ~1 hr each. Free.* — this governs everything else.
2. **Decide & build the two Entity Homes** as person pages on `claritydigital.dev/team/...` (and grab `elijahsullivan.com` / `tannercarlson.dev` if you want the upgrade). *Owner: Tanner builds, Elijah supplies copy. Half a day. ~$0–20.*
3. **Add `Person` + `ProfilePage` JSON-LD with `sameAs`** to both pages; validate at Rich Results Test. *Owner: Tanner. 1–2 hrs. Free.*
4. **Verify both Entity-Home domains in Google Search Console.** *Owner: Tanner. <1 hr. Free.* — unlocks the reliable claim route later.
5. **Optimize both LinkedIn profiles** (vanity URL, headline, first-300-char About). *Owner: each. ~1 hr each. Free.* — fastest page-one win.
6. **Run the consistency sweep** across IG, YouTube, X, GitHub, beacons.ai: one name, one headshot, one bio, link back to Entity Home; kill stale listings. *Owner: each. ~half a day. Free.*
7. **Create Crunchbase person profiles + a Clarity Digital Development company entity**, and stand up Gravatar + About.me; wire all into `sameAs`. *Owner: each + Tanner for company. ~2 hrs. Free.*
8. **Register the free journalist stack** (HARO, Source of Sources, MentionMatch; free tiers of Featured & Qwoted) and write the reusable expert bio + headshot. *Owner: Elijah lead. ~2–3 hrs. Free.* — then pitch 3–5 quality answers/day.
9. **Set up MatchMaker.fm + RadioGuestList podcast profiles.** *Owner: Elijah. ~3 hrs. Free.* — book the first 2–3 appearances.
10. **Update `team/profile.md`** to the live **104,719** follower count (it still says ~99.7k) and note top reels hit **100k–215k shares**, so every generated bio cites the correct, current figure. *Owner: whoever's in the hub next. 2 min. Free.*

*(Defer to next month: Wikidata items once you've banked a few independent references; the `archetypeindex.com` progress blog; the optional budget press release.)*

---

## 7. Substance bank — the real material for bios, articles, and profiles

> **Use only the public, verifiable items below in cold third-party profiles and pitches.** Keep the sensitive/private beats (flagged at the end) OUT — they're powerful *content* narrative but liabilities for credibility pieces, and exposing them could undercut the whole effort.

**Shared anchor**
- **Clarity Digital Development** (`claritydigital.dev`) — the company tying both names together; GitHub org `clarity-digital-development` hosts the live **archetypeindex.com** app (Next.js 16 / Prisma 7 / Clerk). The strongest existing credibility node — build everything off it.

**Elijah Sullivan — public, verifiable**
- Founder/creator; **@elijahaifl on Instagram, 104,719 followers** (live, 2026-06-29), 123 posts; based in Jacksonville, FL; business contact `Elijah@claritydigital.dev`.
- **Content track record (hard numbers):** share-driven account; **top reels have hit 100k–215k shares**; ships ~200 videos/month; Money/Finance content ~4.15M views from 20 posts in a recent 30-day window (~207k/post).
- **Ventures (real, usable):** **ClipWith / ClipWith.ai** (AI video editor, "first fully agentic prompt-to-edit," built on TwelveLabs, co-built with Tanner, 1,000+ waitlist); **Archetype Index / archetypeindex.com** (AI personality classifier + automated report + courses, co-built with Tanner); **Artifacial / artifacial.io** (AI video product, ~$ couple-grand/month); **Infinet / infinetai.org** (LLM platform on Venice.ai); **Cruncrr** & **Labeltrust** (consumer-safety scanner apps, co-founded with Rebecca Santos); **FlipOps** (proptech SaaS, supportive role). Plus real-estate development, a jewelry business, music, and a podcast (first guest Derwin Scott / @dsdpaintings).
- **Narrative spine (public-safe):** self-made entrepreneur from Jacksonville; began flipping/hustling young; built across shoes → jewelry/cars → crypto → real estate → software; "financially free by 21"; philosophy of leverage/OPM, reps over ideas, reputation as startup capital, 50/50 partnerships. *(Correction to keep accurate: his DOGE position at 17 was ~$100k and "the start of everything serious" — NOT "made him rich"; he held too long. Don't repeat the inflated version.)*

**Tanner Carlson — public, verifiable**
- **NYU computer science**; full-stack + AI engineer; **technical co-founder.** Runs **Clarity Digital Development** and the `clarity-digital-development` GitHub org. Contact `tanner@claritydigital.dev`.
- Previously at **Tiffany & Co** (where he and Elijah met and started building together).
- **Builds:** ClipWith, Archetype Index (the live TOI/archetypeindex.com app), FlipOps (technical co-founder, with Mason on GTM). Persona: the "silent technical builder."

**Keep OUT of cold third-party profiles (vault-flagged sensitive/private):** the ~$680k loss + the firearm/self-harm moment, any drug history, sensitive family detail, and Tanner's marijuana-trafficking conviction. These are flagged "decide consciously before any public use" — great owned-content beats, but not for credibility/knowledge-panel material.

---

## 8. Sources

**Knowledge Graph, panels, entity home, claiming (primary + expert):**
- Google Knowledge Panel Help — Get verified: support.google.com/knowledgepanel/answer/7534902 ; Submit feedback: /answer/7534842
- Google Search Central — ProfilePage structured data; sameAs guidance (developers.google.com/search/docs/appearance/structured-data/profile-page)
- Google Search Quality Rater Guidelines (E-E-A-T, updated Sept 11 2025): services.google.com/fh/files/misc/hsw-sqrg.pdf
- Jason Barnard / Kalicube — "How to Trigger a Personal Knowledge Panel"; "Building Google's Confidence in Your Entity"; "Knowledge Panel for a Company Founder"; "How Do I Claim a Knowledge Panel"; Wikipedia-decline data (jasonbarnard.com; kalicube.com)
- ReputationX — knowledge-panel sources & claiming (reputationx.com/blog/knowledge-panel-sources; /claim-google-knowledge-panel)
- 2026 claim/verify walkthroughs incl. selfie/ID step: pradeepsingh.com/verified-google-knowledge-panel ; anupsarker.com ; instantpress.co (real process & the scam version)

**Structured entities (Wikidata / Wikipedia / sameAs):**
- Wikidata:Notability; Wikidata:Autobiography; Property:P2671 (Google Knowledge Graph ID): wikidata.org
- Wikipedia:Notability (people); Conflict-of-interest editing; Orangemoody editing: en.wikipedia.org ; Wikimedia Foundation 2015 paid-advocacy block: wikimediafoundation.org/news/2015/08/31
- schema.org `sameAs`; entity-SEO guides: schemavalidator.org; highervisibility.com/seo/learn/entity-seo; rankmath.com/kb/sameas-schema
- Self-serve profiles: support.crunchbase.com; info.orcid.org; help.imdb.com; muckrack.com/criteria

**Cheap earned media (2026 state):**
- HARO relaunch (free, Featured.com, Apr 2025): backlinkbuilding.io/insight/haro-is-back ; Connectively shutdown: octivdigital.com
- Source of Sources (sourceofsources.com); MentionMatch / Help a B2B Writer (helpab2bwriter.com); HARO alternatives: prezly.com/academy/the-best-haro-alternatives
- Journalist-platform test data: buzzstream.com/blog/journalist-request-platform-study ; visibilitystack.ai/academy/.../best-journalist-query-platforms
- Nofollow vs dofollow in AI search (Semrush via): serpreach.com/haro-link-building
- Podcast guesting: edwardsturm.com/articles/get-on-podcasts-as-guest-2026 ; talks.co/p/podcast-matching-platform
- Guest posting 2026: backlinko.com/the-definitive-guide-to-guest-blogging ; searchengineland.com/guest-post-outreach-proven-scalable-process-473497
- Press-release pricing: pressonify.ai/blog/press-release-distribution-pricing-comparison-2026 ; einpresswire.com/pricing

**Scams / what to avoid:**
- "Buy a Knowledge Panel" scam anatomy: instantpress.co/blog/buy-google-knowledge-panel-scam
- Paid-Wikipedia risk: en.wikipedia.org/wiki/Wikipedia:Conflict_of_interest ; reputationx.com/blog/wikipedia-core-policies
- Forbes/Council pay-to-play: buzzfeednews.com (Jayson DeMers/AudienceBloom); alloycrew.com/resources/forbes-council-wont-make-you-a-thought-leader ; stanventures.com/news/forbes-ends-freelance-contributions-1509
- Google spam policies / site-reputation abuse: developers.google.com/search/docs/essentials/spam-policies ; /blog/2024/11/site-reputation-abuse ; imarkinfotech.com Oct-2025 link-spam update
- FTC Fake Reviews & Testimonials Rule: ftc.gov/news-events/news/press-releases/2024/08/... ; ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers
- Meta Verified (official only): meta.com/meta-verified ; help.instagram.com/461238577687001
- AI-byline deception cases: cnn.com/2024/05/30/media/ai-bylines-local-news-hoodline

**Internal (substance bank + prior intent):**
- `obsidian/Elijah's vault/40-Projects/LarpSlop/What I need to do or start with the ai agent team.md` (the original SEO/credibility goal, quoted in §intro)
- `team/profile.md`, `team/memory.md`; `obsidian/Elijah's vault/30-People/Tanner.md`; vault `CLAUDE.md` Active-ventures block
- instagram MCP `get_profile_info` (live 2026-06-29: 104,719 followers)

---

### One-paragraph bottom line
You can't buy a Google Knowledge Panel, and for two people with *real* credibility, trying to fake one is the single most dangerous move available — it fools no one who matters and taints the genuine wins. But you don't need to fake anything: there's **no fame bar in Google's Knowledge Graph,** only a clarity-and-consistency bar, and you clear the substance test easily. Spend ~$0 and a few weeks doing Phase 0 (own one Entity Home per name on `claritydigital.dev`, mark it up with `Person`/`sameAs`, verify it in Search Console, fix LinkedIn and every profile to say the same thing), then keep stacking free structured nodes (Crunchbase, Wikidata-when-sourced) and *earned* cheap mentions (relaunched HARO, Source of Sources, podcasts, real bylines, your own `archetypeindex.com` progress blog). In ~3 weeks–3 months after the corroboration work lands, the panel tends to emerge on its own — and then you claim it. Cheapest legitimate path, full stop.
