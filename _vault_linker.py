#!/usr/bin/env python3
"""
Vault connector: creates a few missing HUB notes + appends a `## Related` section
of [[wikilinks]] to under-linked notes. ADDITIVE ONLY — never edits frontmatter,
never edits existing prose, never deletes. Skips any note that already has a
`## Related` heading. Backed up at obsidian/_vault-backup-link-pass-2026-06-26.zip.
"""
import os, glob, re

VAULT = r"C:\Users\elija\OneDrive\Desktop\ai agent team\obsidian\Elijah's vault"

# ── 1) HUB notes to create (only if missing). Frontmatter copies the template keys. ──
HUBS = {
 r"30-People\Tanner.md": """---
type: person
name: Tanner
role: Technical co-founder
company:
status: active
follower_count:
follower_tier:
last_contact:
next_contact:
owe_reply: false
owe_value: false
intro_needed:
services: []
rates:
contact_email:
contact_phone:
contact_ig:
contact_linkedin:
location:
how_we_met: Met at 19 (he worked at Tiffany & Co, NYU comp sci); started selling jewelry together, then building software.
tags: [co-founder]
---

## Who they are
Elijah's primary technical collaborator and co-founder. Camera-shy "silent builder" — the technical half to Elijah's face/voice/hype. Co-builds [[ClipWith]], [[40-Projects/Archetype-Index/To do|Archetype Index]], and is technical co-founder on FlipOps.

## Why they matter to me
The engine behind the products. The co-founder story itself is content (see [[Co-Founder Content Ideas Tanner In Town - 2026-06-23]], the "me and tanner cooking" event ideas).

## What they can do / offer
Full-stack / AI engineering. The "doesn't do camera" technical builder character.

## What I can do / offer them
Face, voice, distribution, brand.

## Notes & history
Appears across [[Longform — Real Answers & Talking Points (2026-06-18)]], [[Longform content ideas]], [[Tanner and I]], [[Hosting In person events]], [[Meet your cofounder]], [[ideas for us going live]].
""",
 r"40-Projects\ClipWith\ClipWith.md": """---
type: project
status: active
owner: Elijah
co_owners: [Tanner]
stage:
priority:
started_at:
target_ship:
tags: []
---

## Mission
AI video editor built on TwelveLabs — the first fully agentic, prompt-to-edit model. Co-built with [[Tanner]].

## Current focus
The "Introducing ClipWith" launch reel (script: [[Tanner and I]]).

## Active threads
Launch content with [[Tanner]] — see [[Co-Founder Content Ideas Tanner In Town - 2026-06-23]].

## Blockers


## Decisions log link


## Bug log link


## Recent wins

""",
 r"40-Projects\Artifacial\Artifacial.md": """---
type: project
status: active
owner: Elijah
co_owners: []
stage:
priority:
started_at:
target_ship:
tags: []
---

## Mission
AI video / face-swap product (AI Character & Video Studio).

## Current focus


## Active threads
Promo via [[Champagne lance]]; content ideas in [[Ai videos for infinetai.org]] sibling format.

## Blockers


## Decisions log link


## Bug log link


## Recent wins

""",
 r"40-Projects\Infinet\Infinet.md": """---
type: project
status: active
owner: Elijah
co_owners: []
stage:
priority:
started_at:
target_ship:
tags: []
---

## Mission
Uncensored LLM platform built on Venice.ai.

## Current focus
Video content for infinetai.org — see [[Ai videos for infinetai.org]].

## Active threads


## Blockers


## Decisions log link


## Bug log link


## Recent wins

""",
 r"40-Projects\Labeltrust\Labeltrust.md": """---
type: project
status: active
owner: Elijah
co_owners: [Rebecca Santos]
stage:
priority:
started_at:
target_ship:
tags: []
---

## Mission
Product / label safety scanner — input a product or URL, get safety info. "Crunchy mom" health-conscious feel. Co-founded with Rebecca Santos (related to the Cruncrr baby/child safety scanner).

## Current focus
Quality pass (less vibe-coded), URL/product input — see [[upgrades and ideas or fixes]].

## Active threads
[[Rebecca's ideas or advice]] · security hardening [[Things to make sure are handled]].

## Blockers


## Decisions log link


## Bug log link


## Recent wins

""",
}

# ── 2) Related-link map: relpath -> [(target, reason)]. target may be "Name" or "path|Alias". ──
AI = "40-Projects/Archetype-Index/To do|Archetype Index — To do"
AR = "40-Projects/Artifacial/To do|Artifacial — To do"
LINKS = {
 r"20-Content\Hooks\How to get your first 100 users supposedly.md": [
    ("How I'd Start a Business From Zero — the Backwards Version","launch/growth playbook"),
    ("2026 Content Idea Bank","turn tactics into content")],
 r"20-Content\Ideas\Different cool video ideas.md": [
    ("2026 Content Idea Bank","master idea bank"),("Quick funnies","goofy bits"),
    ("Longform content ideas","more video ideas")],
 r"20-Content\Ideas\Longform content ideas.md": [
    ("Longform — The 5 Secrets to Success","the 5 secrets script"),
    ("What Success Before 21 Cost Me","the cost script"),
    ("Longform — Question Bank (2026-06-18)","the question prompts"),
    ("Tanner","meeting Tanner = origin"),("How I'd Start a Business From Zero — the Backwards Version","SaaS/business angle")],
 r"20-Content\Ideas\Quick funnies.md": [
    ("Different cool video ideas","more video ideas"),("Yaptalks","opinion/comedy bits"),
    ("2026 Content Idea Bank","content bank")],
 r"20-Content\Ideas\Quick talking videos.md": [
    ("Cool repos to checkout","the 'top repos' video"),("2026 Content Idea Bank","content bank"),
    ("YouTube summary in the new way to win with Instagram in 2026 content algorithm","content myths"),
    ("Quick funnies","more quick bits")],
 r"20-Content\Ideas\Trial reel methods.md": [
    ("2026 Content Idea Bank","content strategy"),
    ("How I Grew to 100k — the Data, Not Vibes","data-driven testing"),
    ("YouTube summary in the new way to win with Instagram in 2026 content algorithm","IG 2026 data")],
 r"20-Content\Ideas\Yaptalks.md": [
    ("Flock camera research","flock cameras / surveillance"),("Creating zombie gpt","AI-opinion bits"),
    ("Quick funnies","comedy/opinion bits"),("2026 Content Idea Bank","content bank")],
 r"20-Content\Scripts\Tanner and I.md": [
    ("ClipWith","the product being launched"),("Tanner","co-founder / co-star"),
    ("Co-Founder Content Ideas Tanner In Town - 2026-06-23","co-founder content set"),
    ("Stop Vibe Coding - tworkflow Carousel","same co-founder/AI-build theme")],
 r"30-People\Champagne lance.md": [
    ("Artifacial","promo reactions on Artifacial"),("Infinet","promo on Infinet"),("Labeltrust","promo on Labeltrust")],
 r"30-People\Derwin Scott\Epoxy man @dsdpaintings.md": [
    ("ABC wrap","Derwin Scott podcast edit lives here")],
 r"40-Projects\Archetype-Index\To do.md": [
    ("Full self built community website","the archetype-index community site"),
    ("In the moment ideas","course/program structure")],
 r"40-Projects\Artifacial\To do.md": [
    ("Artifacial","project hub"),("Champagne lance","promo plan")],
 r"40-Projects\Infinet\Video ideas\Ai videos for infinetai.org.md": [
    ("Infinet","project hub"),("2026 Content Idea Bank","content bank"),
    ("Claude Runs Your Instagram - AI Dashboard Carousel","mentions Infinet")],
 r"40-Projects\Labeltrust\Rebecca’s ideas or advice.md": [
    ("Labeltrust","project hub"),("Things to make sure are handled","security checklist"),
    ("upgrades and ideas or fixes","upgrade backlog")],
 r"40-Projects\Labeltrust\Things to make sure are handled.md": [
    ("Labeltrust","project hub"),("Rebecca’s ideas or advice","Rebecca's input"),
    ("upgrades and ideas or fixes","upgrade backlog"),("Cool repos to checkout","repos that may help labeltrust")],
 r"40-Projects\Labeltrust\upgrades and ideas or fixes.md": [
    ("Labeltrust","project hub"),("Rebecca’s ideas or advice","Rebecca's input"),
    ("Things to make sure are handled","security checklist"),
    ("Stop Vibe Coding - tworkflow Carousel","'less vibe-coded' theme")],
 r"40-Projects\LarpSlop\ABC wrap.md": [
    ("Working on","what's live in the hub"),
    ("What I need to do or start with the ai agent team","hub roadmap"),
    ("Epoxy man @dsdpaintings","Derwin Scott edit"),("insta360 editing","editing refs")],
 r"40-Projects\LarpSlop\Color-Grading-Masterclass\Screenshot index.md": [
    ("00 - Color Grading Masterclass (index)","the masterclass index"),
    ("Color Engine (colorkit)","the engine the masterclass grounds")],
 r"40-Projects\LarpSlop\Cool repos to checkout.md": [
    ("What I need to do or start with the ai agent team","hub roadmap"),
    ("Working on","current hub work"),
    ("Things to make sure are handled","repos for labeltrust"),
    ("Quick talking videos","the 'top repos' video")],
 r"40-Projects\LarpSlop\What I need to do or start with the ai agent team.md": [
    ("Working on","what's live now"),("What I have so far","current capabilities"),
    ("Completed — master log","what's done"),("Cool repos to checkout","repos to add"),
    ("2026 Content Idea Bank","content engine output")],
 r"60-Life\Dumb shit\Creating zombie gpt.md": [
    ("Yaptalks","AI-opinion content"),("Infinet","uncensored-LLM angle")],
 r"60-Life\Personal masterclasses\Color grading, color correction, and color theory.md": [
    ("00 - Color Grading Masterclass (index)","the full written masterclass"),
    ("insta360 editing","editing learning"),("Color Engine (colorkit)","the engine")],
 r"60-Life\Personal masterclasses\insta360 editing.md": [
    ("Color grading, color correction, and color theory","color learning"),
    ("00 - Color Grading Masterclass (index)","grading masterclass"),("ABC wrap","video editing project")],
 r"60-Life\To do general\Clipping.md": [
    ("ABC wrap","the clipping/auto-clip pipeline"),
    ("2026 Content Idea Bank","content/repurposing"),("What I have so far","hub capabilities")],
 r"60-Life\To do general\Full self built community website.md": [
    (AI,"archetype-index tasks"),("In the moment ideas","program structure")],
 r"60-Life\To do general\Quick.md": [
    ("What I need to do or start with the ai agent team","hub roadmap"),
    ("What I have so far","meta ads/IG bot already wired"),
    ("Claude Runs Your Instagram - AI Dashboard Carousel","IG automation")],
 r"60-Life\To do general\Upload all my music again.md": [
    ("write song with Overlord Scooch","music / features")],
 r"60-Life\To do general\write song with Overlord Scooch.md": [
    ("Upload all my music again","music distribution")],
 r"Brainstorming\Pocket ai recorder.md": [
    ("Pocket - DIY Voice-Capture Device Research","the full research on this device")],
 r"Brainstorming\me and tanner cooking\Hosting In person events.md": [
    ("Meet your cofounder","the event format"),("ideas for us going live","the live-grading idea"),
    ("Co-Founder Content Ideas Tanner In Town - 2026-06-23","co-founder content"),("Tanner","co-host")],
 r"Brainstorming\me and tanner cooking\Meet your cofounder.md": [
    ("Hosting In person events","the in-person event"),("ideas for us going live","go-live plan"),
    ("Co-Founder Content Ideas Tanner In Town - 2026-06-23","co-founder content"),("Tanner","co-host")],
 r"Brainstorming\me and tanner cooking\ideas for us going live.md": [
    ("Hosting In person events","in-person version"),("Meet your cofounder","event format"),
    ("Tanner","co-host"),("Co-Founder Content Ideas Tanner In Town - 2026-06-23","co-founder content")],
 r"Research\Flock camera research.md": [
    ("Yaptalks","the flock-camera / surveillance take")],
 r"Research\Pocket - DIY Voice-Capture Device Research.md": [
    ("Pocket ai recorder","the original brainstorm")],
 r"Research\YouTube summary about the best six things to know for the new Meta ads Andromeda.md": [
    ("What I have so far","meta ads MCP wired"),("2026 Content Idea Bank","content/ads"),
    ("How I'd Start a Business From Zero — the Backwards Version","ads/leverage")],
 r"Research\YouTube summary about the most potable ai side hustle.md": [
    ("How I'd Start a Business From Zero — the Backwards Version","one-person AI business"),
    ("2026 Content Idea Bank","content/build-in-public"),
    ("What I need to do or start with the ai agent team","the AI agent hub")],
 r"Research\YouTube summary in the new way to win with Instagram in 2026 content algorithm.md": [
    ("2026 Content Idea Bank","the 2026 content strategy"),
    ("How I Grew to 100k — the Data, Not Vibes","data-not-vibes growth"),
    ("Trial reel methods","testing methods")],
 r"Repeated Claude Prompts\Compact Audit & Handoff Generator.md": [
    ("Citation URL Research & Verification Workflow","sister claude-prompt")],
}

def slug(t):  # link target -> the note NAME used for resolution check
    return (t.split("|")[0]).replace("\\", "/").split("/")[-1]

def main():
    md = [p for p in glob.glob(os.path.join(VAULT,"**","*.md"), recursive=True) if ".obsidian" not in p]
    names = {os.path.splitext(os.path.basename(p))[0] for p in md}
    created = []
    for rel, content in HUBS.items():
        full = os.path.join(VAULT, rel)
        if os.path.exists(full):
            print(f"  hub exists, skip: {rel}"); continue
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full,"w",encoding="utf-8").write(content)
        names.add(os.path.splitext(os.path.basename(rel))[0]); created.append(rel)
        print(f"  CREATED hub: {rel}")

    # validate targets
    missing = set()
    for rel, lst in LINKS.items():
        for tgt,_ in lst:
            if slug(tgt) not in names: missing.add(f"{slug(tgt)}  (in {rel})")
    if missing:
        print("\n!! UNRESOLVED LINK TARGETS (fix before run):")
        for m in sorted(missing): print("   -", m)
        return

    added = skipped = 0
    for rel, lst in LINKS.items():
        full = os.path.join(VAULT, rel)
        if not os.path.exists(full):
            print(f"  !! note missing, skip: {rel}"); continue
        txt = open(full,encoding="utf-8").read()
        if re.search(r"(?mi)^##+\s*Related\b", txt):
            print(f"  has Related, skip: {os.path.basename(rel)}"); skipped += 1; continue
        block = "\n\n## Related\n" + "".join(f"- [[{t}]] — {r}\n" for t,r in lst)
        if not txt.endswith("\n"): block = "\n" + block
        open(full,"a",encoding="utf-8").write(block)
        added += 1; print(f"  +Related ({len(lst)}): {os.path.basename(rel)}")

    print(f"\n=== DONE: {len(created)} hubs created, {added} notes linked, {skipped} skipped (already had Related) ===")

if __name__ == "__main__":
    main()
