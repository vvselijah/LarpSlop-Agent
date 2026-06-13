"""
auto-clip/highlight.py -- the "moment selector": rank transcript spans into standalone shorts.

Reads a transcribe.py JSON, picks the best ~20-60s self-contained clips (strong hook + ONE
complete idea), snaps each window to clean segment boundaries, sorts by score, and writes a
ranked highlights JSON that reframe.py + the caption-engine consume. This is the engine's core
"brain" -- the piece that did NOT already exist in the hub / abc wrap.

Providers (how the selection gets made):
  anthropic  (default)  -- Anthropic API, needs ANTHROPIC_API_KEY in env.
  ollama                -- local model at http://localhost:11434 (zero-cost / fully offline).
  agent                 -- NO key, NO install: the Claude Code agent IS the selector. Runs in two
                           steps so the deterministic seg->time mapping stays in Python:
                             1) python highlight.py <transcript> --provider agent
                                -> writes data/<stem>.agent-prompt.json and stops.
                             2) the agent reads that, writes data/<stem>.picks.json, then re-run:
                                python highlight.py <transcript> --provider agent --from-picks data/<stem>.picks.json
                                -> validates/sorts/writes the final highlights JSON.
                           The `auto-clip` skill drives this loop automatically; use it for
                           interactive runs through Claude Code (no API key or Ollama needed).

Usage:
  python highlight.py data/<stem>.transcript.json [--n 5] [--model ...]
                      [--provider anthropic|ollama|agent] [--from-picks <picks.json>]
Writes:
  data/<stem>.highlights.json   [{rank,start,end,duration,title,hook,score,reason}]
"""
import json
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

# The exact pick schema both the LLM providers and the agent provider must emit.
PICK_SCHEMA = (
    '{"start_seg": <int index>, "end_seg": <int index, inclusive>, "title": <str>, '
    '"hook": <the opening line>, "score": <0-100 short-form potential>, "reason": <one sentence>}'
)


def build_prompt(segments, n):
    lines = [f"[{i}] {s['start']:.1f}-{s['end']:.1f}  {s['text']}" for i, s in enumerate(segments)]
    return (
        "Transcript segments (index, start-end seconds, text):\n"
        + "\n".join(lines)
        + f"\n\nReturn the top {n} clips as a JSON array. Each item: "
        + PICK_SCHEMA
        + ". start_seg/end_seg index into the list above. JSON array only."
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


def write_highlights(picks, segments, media, out_dir):
    """Map agent/LLM picks (segment indices) -> clean clip windows, sort by score, rank, write."""
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
    out_path = out_dir / (Path(media).stem + ".highlights.json")
    out_path.write_text(json.dumps(clips, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path, clips


def emit_agent_prompt(tpath, data, n, prompt):
    """Write a self-contained brief the Claude Code agent uses to make the selection (no API key)."""
    stem = Path(data["media"]).stem
    picks_out = tpath.parent / f"{stem}.picks.json"
    bundle = {
        "instructions": (
            "AGENT MODE - you are the moment selector for auto-clip. Read SYSTEM + prompt below, "
            f"pick the top {n} self-contained clips, and WRITE your picks as a JSON array to "
            f"picks_out. Each pick is exactly: {PICK_SCHEMA}. start_seg/end_seg index into the "
            "numbered segments inside prompt. Then re-run: "
            f"python highlight.py {tpath.name} --provider agent --from-picks {picks_out.name}"
        ),
        "n": n,
        "system": SYSTEM,
        "prompt": prompt,
        "picks_out": str(picks_out),
        "highlights_out": str(tpath.parent / f"{stem}.highlights.json"),
    }
    apath = tpath.parent / f"{stem}.agent-prompt.json"
    apath.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    return apath, picks_out


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        log("FATAL: usage: python highlight.py data/<stem>.transcript.json [--n 5] "
            "[--provider anthropic|ollama|agent] [--from-picks <picks.json>]")
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

    # --- agent provider: the Claude Code agent is the selector (no key, no install) ---
    if provider == "agent":
        from_picks = opt("--from-picks", None)
        if from_picks:
            picks = json.loads(Path(from_picks).resolve().read_text(encoding="utf-8"))
            out_path, clips = write_highlights(picks, segments, data["media"], tpath.parent)
            log(f"wrote {out_path}  ({len(clips)} clips from agent picks)")
            for c in clips:
                log(f"  #{c['rank']} [{c['score']}] {c['start']:.0f}-{c['end']:.0f}s ({c['duration']:.0f}s)  {c['title']}")
            return
        apath, picks_out = emit_agent_prompt(tpath, data, n, prompt)
        log(f"AGENT MODE -- wrote brief {apath}")
        log(f"  next: agent selects -> writes {picks_out.name} -> re-run with --from-picks {picks_out.name}")
        return

    # --- automated providers (unattended / scheduled runs) ---
    log(f"selecting top {n} clips via {provider}/{model} over {len(segments)} segments ...")
    try:
        raw = call_anthropic(model, prompt) if provider == "anthropic" else call_ollama(model, prompt)
    except Exception as e:
        log(f"FATAL: LLM call failed ({e}). anthropic -> set ANTHROPIC_API_KEY; "
            "ollama -> run `ollama serve`; or use --provider agent (no key needed).")
        sys.exit(1)

    picks = extract_json(raw)
    out_path, clips = write_highlights(picks, segments, data["media"], tpath.parent)
    log(f"wrote {out_path}  ({len(clips)} clips)")
    for c in clips:
        log(f"  #{c['rank']} [{c['score']}] {c['start']:.0f}-{c['end']:.0f}s ({c['duration']:.0f}s)  {c['title']}")


if __name__ == "__main__":
    main()
