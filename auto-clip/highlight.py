"""
auto-clip/highlight.py -- the LLM "moment selector": rank transcript spans into standalone shorts.

Reads a transcribe.py JSON, asks an LLM to pick the best ~20-60s self-contained clips
(strong hook + ONE complete idea), snaps each window to clean segment boundaries, sorts by
score, and writes a ranked highlights JSON that reframe.py + the caption-engine consume.
This is the engine's core "brain" -- the piece that did NOT already exist in the hub / abc wrap.

Default provider is the Anthropic API (needs ANTHROPIC_API_KEY). --provider ollama routes to a
local model (http://localhost:11434) for zero-cost / fully-offline runs.

Usage:
  python highlight.py data/<stem>.transcript.json [--n 5] [--model claude-sonnet-4-6] [--provider anthropic|ollama]
Writes:
  data/<stem>.highlights.json   [{rank,start,end,duration,title,hook,score,reason}]
"""
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent


def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:  # Windows cp1252 console chokes on emoji/smart-quotes/arrows
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)


SYSTEM = (
    "You are a world-class short-form video editor. Given a timestamped transcript of a long "
    "video, select the strongest self-contained moments to cut as vertical shorts "
    "(Reels/TikTok/YouTube Shorts). Each clip MUST: open with a scroll-stopping hook, contain "
    "exactly ONE complete idea, and stand alone without the rest of the video. Prefer 20-60s. "
    "Favor concrete payoffs (numbers, secrets, bold claims). Return STRICT JSON only, no prose."
)


def build_prompt(segments, n):
    lines = [f"[{i}] {s['start']:.1f}-{s['end']:.1f}  {s['text']}" for i, s in enumerate(segments)]
    return (
        "Transcript segments (index, start-end seconds, text):\n"
        + "\n".join(lines)
        + f"\n\nReturn the top {n} clips as a JSON array. Each item: "
        '{"start_seg": <int index>, "end_seg": <int index, inclusive>, "title": <str>, '
        '"hook": <the opening line>, "score": <0-100 short-form potential>, "reason": <one sentence>}. '
        "start_seg/end_seg index into the list above. JSON array only."
    )


def call_anthropic(model, prompt):
    from anthropic import Anthropic  # pip install anthropic

    client = Anthropic()  # reads ANTHROPIC_API_KEY from env
    msg = client.messages.create(
        model=model, max_tokens=2000, system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def call_ollama(model, prompt):
    import urllib.request

    body = json.dumps(
        {"model": model, "system": SYSTEM, "prompt": prompt, "stream": False, "format": "json"}
    ).encode()
    req = urllib.request.Request(
        "http://localhost:11434/api/generate", data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["response"]


def extract_json(text):
    m = re.search(r"\[.*\]", text, re.DOTALL)
    return json.loads(m.group(0)) if m else json.loads(text)


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        log("FATAL: usage: python highlight.py data/<stem>.transcript.json [--n 5] [--provider anthropic|ollama]")
        sys.exit(1)

    tpath = Path(args[0]).resolve()
    if not tpath.exists():
        log(f"FATAL: transcript not found: {tpath}")
        sys.exit(1)

    def opt(flag, d):
        return args[args.index(flag) + 1] if flag in args else d

    n = int(opt("--n", "5"))
    provider = opt("--provider", "anthropic")
    model = opt("--model", "claude-sonnet-4-6" if provider == "anthropic" else "llama3.1")

    data = json.loads(tpath.read_text(encoding="utf-8"))
    segments = data.get("segments") or []
    if not segments:
        log("FATAL: transcript has no segments")
        sys.exit(1)

    prompt = build_prompt(segments, n)
    log(f"selecting top {n} clips via {provider}/{model} over {len(segments)} segments ...")
    try:
        raw = call_anthropic(model, prompt) if provider == "anthropic" else call_ollama(model, prompt)
    except Exception as e:
        log(f"FATAL: LLM call failed ({e}). anthropic -> set ANTHROPIC_API_KEY; ollama -> run `ollama serve`.")
        sys.exit(1)

    picks = extract_json(raw)
    clips = []
    for p in picks:
        a = max(0, min(int(p["start_seg"]), len(segments) - 1))
        b = max(a, min(int(p["end_seg"]), len(segments) - 1))
        start, end = segments[a]["start"], segments[b]["end"]
        clips.append({
            "start": round(start, 2), "end": round(end, 2), "duration": round(end - start, 1),
            "title": p.get("title", "").strip(), "hook": p.get("hook", "").strip(),
            "score": int(p.get("score", 0)), "reason": p.get("reason", "").strip(),
        })
    clips.sort(key=lambda c: c["score"], reverse=True)
    for i, c in enumerate(clips, 1):
        c["rank"] = i

    out_path = tpath.parent / (Path(data["media"]).stem + ".highlights.json")
    out_path.write_text(json.dumps(clips, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"wrote {out_path}  ({len(clips)} clips)")
    for c in clips:
        log(f"  #{c['rank']} [{c['score']}] {c['start']:.0f}-{c['end']:.0f}s ({c['duration']:.0f}s)  {c['title']}")


if __name__ == "__main__":
    main()
