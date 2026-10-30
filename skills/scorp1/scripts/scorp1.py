#!/usr/bin/env python3
"""Scorp1 run helper: the deterministic half of the editor.

The agent writes the creative plan (plan/plan.json). This script turns it into
files and numbers: the ElevenLabs audio pack, the cleaned voice files, and the
exact timing of every scene, voice line, sound effect and music duck.

Standard library only, plus ffmpeg/ffprobe on PATH and `npx hyperframes` for
word timings. Run `python scorp1.py <command> --help` for each command.

  init      create a run folder and its state file
  latest    print the newest run folder under ./scorp1-output
  status    show where a run is and what it is waiting for
  mark      set a run's phase
  pack      build audio-pack/ (scripts and prompts for ElevenLabs) from the plan
  estimate  time the plan from word counts (before any audio exists)
  ingest    clean, measure and transcribe the files dropped in audio-in/
  retime    time the plan from the real voice files -> timing.json
  captions  write captions.srt from timing.json
  styles    list the style skills installed
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHASES = [
    "research",        # reading the business
    "plan",            # storyboard + plan.json
    "awaiting-audio",  # audio pack delivered, waiting for the user's files
    "ingested",        # audio cleaned and timed
    "composing",       # Hyperframes composition being built
    "preview",         # Studio preview / draft render shown
    "delivered",       # final render, poster, captions, share copy
]
AUDIO_EXT = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac", ".opus", ".webm"}
FORMATS = {
    "landscape": (1920, 1080),
    "vertical": (1080, 1920),
    "square": (1080, 1080),
    "portrait": (1080, 1350),
}
V3_MODELS = {"eleven_v3"}
DEFAULT_WPS = 2.6


# ---------------------------------------------------------------- helpers

def die(msg: str) -> None:
    print(f"scorp1: {msg}", file=sys.stderr)
    sys.exit(1)


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"missing {path}")
    except json.JSONDecodeError as e:
        die(f"{path} is not valid JSON: {e}")


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "business"


def r3(x: float) -> float:
    return round(float(x), 3)


def snap_frame(t: float, fps: int) -> float:
    return round(round(t * fps) / fps, 4)


def tool(name: str) -> str:
    found = shutil.which(name)
    if not found:
        die(f"{name} not found on PATH")
    return found


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def probe_duration(path: Path) -> float:
    out = run([tool("ffprobe"), "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nw=1:nk=1", str(path)])
    try:
        return float(out.stdout.strip())
    except ValueError:
        die(f"ffprobe could not read {path}: {out.stderr.strip()[:300]}")


def loudness(path: Path) -> dict:
    out = run([tool("ffmpeg"), "-hide_banner", "-nostats", "-i", str(path),
               "-af", "volumedetect", "-f", "null", "-"])
    mean = re.search(r"mean_volume:\s*(-?[\d.]+)", out.stderr)
    peak = re.search(r"max_volume:\s*(-?[\d.]+)", out.stderr)
    return {"mean_db": float(mean.group(1)) if mean else None,
            "peak_db": float(peak.group(1)) if peak else None}


def words_of(text: str) -> list[str]:
    text = re.sub(r"\[[^\]]*\]", " ", text)  # drop ElevenLabs v3 audio tags
    return re.findall(r"[\w'’-]+", text.lower())


def run_dir_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument("run", type=Path, help="run folder (holds scorp1.json)")


def load_state(run_dir: Path) -> dict:
    return read_json(run_dir / "scorp1.json")


def save_state(run_dir: Path, state: dict) -> None:
    state["updated"] = dt.datetime.now().isoformat(timespec="seconds")
    write_json(run_dir / "scorp1.json", state)


def load_plan(run_dir: Path) -> dict:
    plan = read_json(run_dir / "plan" / "plan.json")
    problems = validate_plan(plan)
    if problems:
        die("plan.json problems:\n  - " + "\n  - ".join(problems))
    return plan


def vo_lines(plan: dict) -> list[dict]:
    lines = []
    for scene in plan["scenes"]:
        for line in scene.get("vo", []):
            lines.append({**line, "scene": scene["id"]})
    return lines


def voice_mode(plan: dict) -> str:
    return plan.get("voice", {}).get("mode", "elevenlabs")


def validate_plan(plan: dict) -> list[str]:
    problems = []
    for key in ("business", "style", "format", "scenes"):
        if key not in plan:
            problems.append(f"missing '{key}'")
    if problems:
        return problems
    if plan["format"].get("aspect") not in FORMATS:
        problems.append(f"format.aspect must be one of {sorted(FORMATS)}")
    seen_scenes, seen_vo, seen_sfx = set(), set(), set()
    for s in plan["scenes"]:
        sid = s.get("id")
        if not sid or sid in seen_scenes:
            problems.append(f"scene id missing or repeated: {sid!r}")
        seen_scenes.add(sid)
        if not isinstance(s.get("min", 0), (int, float)):
            problems.append(f"scene {sid}: 'min' must be seconds")
        for line in s.get("vo", []):
            vid = line.get("id", "")
            if not re.fullmatch(r"VO\d{2}", vid) or vid in seen_vo:
                problems.append(f"scene {sid}: voice line id must be VO01, VO02, ... and unique (got {vid!r})")
            seen_vo.add(vid)
            if not line.get("text", "").strip():
                problems.append(f"{vid}: empty text")
            if re.search(r"\[[^\]]*\]", line.get("text", "")):
                problems.append(f"{vid}: put ElevenLabs audio tags in 'tags', not in 'text'")
    for sfx in plan.get("sfx", []):
        xid = sfx.get("id")
        if not xid or xid in seen_sfx:
            problems.append(f"sfx id missing or repeated: {xid!r}")
        seen_sfx.add(xid)
        if not sfx.get("file") and not sfx.get("custom"):
            problems.append(f"sfx {xid}: needs 'file' (library) or 'custom' (ElevenLabs prompt)")
        a = sfx.get("anchor", {})
        if "scene" in a and a["scene"] not in seen_scenes:
            problems.append(f"sfx {xid}: anchor scene {a['scene']!r} does not exist")
        if "vo" in a and a["vo"] not in seen_vo:
            problems.append(f"sfx {xid}: anchor voice line {a['vo']!r} does not exist")
        if not any(k in a for k in ("scene", "vo", "time")):
            problems.append(f"sfx {xid}: anchor needs 'scene', 'vo' or 'time'")
    return problems


# ---------------------------------------------------------------- init / latest / status / mark

def cmd_init(a) -> None:
    root = Path(a.root)
    slug = slugify(a.business)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M")
    run_dir = root / slug / f"{a.style}-{stamp}"
    if run_dir.exists():
        die(f"{run_dir} already exists")
    for sub in ("research/media", "plan", "audio-pack/lines", "audio-in", "audio", "composition"):
        (run_dir / sub).mkdir(parents=True, exist_ok=True)
    w, h = FORMATS[a.format]
    state = {
        "schema": "scorp1.state/1",
        "created": dt.datetime.now().isoformat(timespec="seconds"),
        "business": {"name": a.business, "slug": slug, "sources": a.source},
        "style": a.style,
        "options": {"format": a.format, "width": w, "height": h, "duration": a.duration,
                    "voice": a.voice, "product": a.product, "extra": a.extra},
        "phase": "research",
    }
    save_state(run_dir, state)
    write_text(run_dir / "audio-in" / "DROP-AUDIO-HERE.txt",
               "Put your ElevenLabs files here (VO01.mp3, VO02.mp3, ... or one voiceover.mp3),\n"
               "plus any custom sound effects (SFX01.mp3, ...) and music.mp3 if the pack asked for them.\n"
               "Then run /scorp1 render (Claude Code) or $scorp1 render (Codex).\n")
    print(run_dir.resolve())


def find_runs(root: Path) -> list[Path]:
    return sorted((p.parent for p in root.glob("*/*/scorp1.json")),
                  key=lambda p: (p / "scorp1.json").stat().st_mtime, reverse=True)


def cmd_latest(a) -> None:
    runs = find_runs(Path(a.root))
    if a.phase:
        runs = [r for r in runs if load_state(r).get("phase") == a.phase]
    if not runs:
        die(f"no runs under {a.root}" + (f" in phase {a.phase}" if a.phase else ""))
    print(runs[0].resolve())


def expected_audio(plan: dict) -> dict:
    exp = {"voice": [], "sfx": [], "music": None}
    if voice_mode(plan) != "none":
        exp["voice"] = [l["id"] for l in vo_lines(plan)]
    for sfx in plan.get("sfx", []):
        if sfx.get("custom"):
            exp["sfx"].append(sfx["custom"].get("filename", sfx["id"]))
    m = plan.get("music", {})
    if m.get("source") in ("custom", "elevenlabs"):
        exp["music"] = "music"
    return exp


def scan_audio_in(run_dir: Path) -> dict:
    found = {"voice": {}, "single": None, "sfx": {}, "music": None, "unmatched": []}
    for f in sorted((run_dir / "audio-in").iterdir()):
        if f.suffix.lower() not in AUDIO_EXT:
            continue
        stem = f.stem
        m = re.search(r"(?i)(?<![a-z])vo[\s_-]*0*(\d{1,2})(?!\d)", stem)
        s = re.search(r"(?i)(?<![a-z])sfx[\s_-]*0*(\d{1,2})(?!\d)", stem)
        if m:
            found["voice"].setdefault(f"VO{int(m.group(1)):02d}", f)
        elif s:
            found["sfx"].setdefault(f"SFX{int(s.group(1)):02d}", f)
        elif re.search(r"(?i)^(voice[\s_-]*over|narration|vo|full)", stem):
            found["single"] = found["single"] or f
        elif re.search(r"(?i)^music", stem):
            found["music"] = found["music"] or f
        else:
            found["unmatched"].append(f)
    return found


def cmd_status(a) -> None:
    run_dir = a.run
    state = load_state(run_dir)
    print(f"Run:    {run_dir.resolve()}")
    print(f"Brand:  {state['business']['name']}   Style: {state['style']}   Phase: {state['phase']}")
    plan_path = run_dir / "plan" / "plan.json"
    if not plan_path.exists():
        print("Next:   research the business and write plan/plan.json")
        return
    plan = load_plan(run_dir)
    exp = expected_audio(plan)
    found = scan_audio_in(run_dir)
    missing = []
    if exp["voice"]:
        if found["single"] and not found["voice"]:
            print(f"Voice:  single take {found['single'].name} (will be split into {len(exp['voice'])} lines)")
        else:
            missing += [v for v in exp["voice"] if v not in found["voice"]]
    missing += [x for x in exp["sfx"] if x not in found["sfx"]]
    if exp["music"] and not found["music"]:
        missing.append("music")
    have = list(found["voice"]) + list(found["sfx"]) + (["music"] if found["music"] else [])
    print(f"Have:   {', '.join(have) or 'nothing yet'}")
    print(f"Needs:  {', '.join(missing) or 'nothing - ready to ingest'}")
    if found["unmatched"]:
        print("Unmatched files (rename to VO01 / SFX01 / music): " + ", ".join(f.name for f in found["unmatched"]))


def cmd_mark(a) -> None:
    if a.phase not in PHASES:
        die(f"phase must be one of {PHASES}")
    state = load_state(a.run)
    state["phase"] = a.phase
    save_state(a.run, state)
    print(f"{a.run}: phase = {a.phase}")


# ---------------------------------------------------------------- pack

def est_seconds(text: str, wps: float) -> float:
    return len(words_of(text)) / wps + 0.35


def spoken_line(line: dict, model: str) -> str:
    text = line["text"].strip()
    tags = line.get("tags", [])
    if model in V3_MODELS and tags:
        return " ".join(f"[{t.strip('[]')}]" for t in tags) + " " + text
    return text


def cmd_pack(a) -> None:
    run_dir = a.run
    plan = load_plan(run_dir)
    state = load_state(run_dir)
    # the plan wins over init's guesses (init may have run with --style tbd)
    fmt = plan["format"]
    state["style"] = plan["style"]
    state["options"].update(format=fmt.get("aspect"), width=fmt.get("width"), height=fmt.get("height"),
                            duration=plan.get("target_duration"), voice=voice_mode(plan))
    pack = run_dir / "audio-pack"
    voice = plan.get("voice", {})
    model = voice.get("model", "eleven_multilingual_v2")
    wps = voice.get("wps", DEFAULT_WPS)
    lines = vo_lines(plan) if voice_mode(plan) != "none" else []
    for old in (pack / "lines").glob("*.txt"):
        old.unlink()

    # 1. one paste-ready file per line, and the whole read as one take
    for line in lines:
        write_text(pack / "lines" / f"{line['id']}.txt", spoken_line(line, model) + "\n")
    take = "\n\n".join(spoken_line(l, model) for l in lines)
    if lines:
        write_text(pack / "transcript.txt", take + "\n")

    # 2. the script, readable
    rows = ["| Line | Scene | Say this | Direction | ~sec |", "|---|---|---|---|---|"]
    for l in lines:
        direction = l.get("direction", "")
        if l.get("tags"):
            direction = (" ".join(f"[{t.strip('[]')}]" for t in l["tags"]) + " " + direction).strip()
        rows.append(f"| {l['id']} | {l['scene']} | {l['text']} | {direction} | {est_seconds(l['text'], wps):.1f} |")
    est_total = sum(est_seconds(l["text"], wps) for l in lines)
    pron = {}
    for l in lines:
        pron.update(l.get("pronounce", {}))
    pron_md = "\n".join(f"- **{k}**: say it as \"{v}\"" for k, v in pron.items()) or "- Nothing unusual."
    write_text(pack / "voiceover-script.md",
               f"# Voiceover script: {plan['business']['name']} ({plan['style']})\n\n"
               f"{len(lines)} lines, about {est_total:.0f} seconds of speech at {wps} words a second.\n\n"
               + "\n".join(rows) + "\n\n## Pronunciation\n\n" + pron_md + "\n")

    # 3. sound design cue sheet
    music = plan.get("music", {})
    sfx_rows = ["| Sound | File / source | When | Why |", "|---|---|---|---|"]
    custom = []
    for s in plan.get("sfx", []):
        src = s.get("file") or f"custom: {s['custom'].get('filename', s['id'])}.mp3"
        sfx_rows.append(f"| {s['id']} | `{src}` | {describe_anchor(s.get('anchor', {}))} | {s.get('why', '')} |")
        if s.get("custom"):
            custom.append(s)
    music_md = (f"- Track: `{music.get('file', 'music.mp3 (you provide)')}` ({music.get('source', 'bundled')})\n"
                f"- Level: {music.get('volume', 0.3)}, ducked to {int(music.get('duck_to', 0.35) * 100)}% under the voice, "
                f"fade out {music.get('fade_out', 1.5)}s\n"
                f"- Mood: {music.get('mood', '')}\n")
    write_text(pack / "sound-design.md",
               f"# Sound design: {plan['business']['name']}\n\n## Music\n\n{music_md}\n## Sound effects\n\n"
               + "\n".join(sfx_rows) + "\n\nTimes are worked out from your real voice files when you render.\n")

    # 4. README: the step-by-step the user follows in ElevenLabs
    write_text(pack / "README.md", pack_readme(plan, lines, custom, est_total))

    state["phase"] = "awaiting-audio" if (lines or custom or expected_audio(plan)["music"]) else "ingested"
    save_state(run_dir, state)
    print(f"Wrote {pack.resolve()}  ({len(lines)} voice lines, {len(custom)} custom sounds, ~{est_total:.0f}s speech)")


def describe_anchor(a: dict) -> str:
    off = a.get("offset", 0)
    sign = f" {'+' if off >= 0 else '-'} {abs(off)}s" if off else ""
    if "word" in a:
        return f'on the word "{a["word"]}" in {a["vo"]}{sign}'
    if "vo" in a:
        return f"{'end' if a.get('at') == 'end' else 'start'} of {a['vo']}{sign}"
    if "scene" in a:
        return f"{'end' if a.get('at') == 'end' else 'start'} of scene {a['scene']}{sign}"
    return f"{a.get('time', 0)}s"


def pack_readme(plan: dict, lines: list, custom: list, est_total: float) -> str:
    v = plan.get("voice", {})
    st = v.get("settings", {})
    model = v.get("model", "eleven_multilingual_v2")
    model_name = {"eleven_v3": "Eleven v3", "eleven_multilingual_v2": "Eleven Multilingual v2",
                  "eleven_flash_v2_5": "Eleven Flash v2.5", "eleven_turbo_v2_5": "Eleven Turbo v2.5"}.get(model, model)
    music = plan.get("music", {})
    out = [f"# Audio pack: {plan['business']['name']}",
           "",
           f"Style: **{plan['style']}**. Everything below is what Scorp1 needs from ElevenLabs. "
           "When the files are in `audio-in/`, run `/scorp1 render` (Claude Code) or `$scorp1 render` (Codex) "
           "from the same folder and Scorp1 times the whole video to your audio.",
           ""]
    step = 1
    if lines:
        out += [f"## {step}. Voiceover ({len(lines)} lines, about {est_total:.0f} seconds)", "",
                f"**Voice.** {v.get('voice_brief', 'Pick a warm, clear narrator.')}",
                f"In ElevenLabs open *Voices > Voice Library* and search: `{v.get('voice_library_search', 'warm narrator')}`. "
                "Use the same voice for every line.", "",
                f"**Model:** {model_name}  ",
                f"**Settings:** stability {st.get('stability', 0.5)}, similarity {st.get('similarity', 0.75)}, "
                f"style {st.get('style', 0.2)}, speed {st.get('speed', 1.0)}, speaker boost "
                f"{'on' if st.get('speaker_boost', True) else 'off'}. "
                "If your screen shows different names, use the closest match.", ""]
        if model in V3_MODELS:
            out += ["Words in square brackets such as `[warmly]` are Eleven v3 audio tags: paste them as they are; "
                    "they set the delivery and are not spoken.", ""]
        pron = {}
        for l in lines:
            pron.update(l.get("pronounce", {}))
        if pron:
            out += ["**Pronunciation.** Listen for these. If the voice says one wrong, change the spelling in the "
                    "pasted text to the sound-alike (for example `JOO-jah`) and regenerate that line; Scorp1 still "
                    "matches it to the script:", ""]
            out += [f"- {k}: \"{v}\"" for k, v in pron.items()]
            out.append("")
        out += ["**Option A, recommended: one file per line.** For each file in `lines/`, paste its text, generate, "
                "and download. Name the downloads to match:", ""]
        out += [f"- `{l['id']}.mp3`: \"{l['text']}\"" for l in lines]
        out += ["",
                "**Option B: one take.** Paste `transcript.txt` as one generation and save it as `voiceover.mp3`. "
                "Scorp1 transcribes it and cuts it into the lines itself. Option A gives more control over timing.",
                "",
                "Download as MP3 (44.1 kHz, 128 kbps or better) or WAV. Don't worry about silence at the start "
                "or end; Scorp1 trims it and evens out the loudness.", ""]
        step += 1
    if custom:
        out += [f"## {step}. Custom sound effects (optional)", "",
                "These moments get their own sound. In ElevenLabs open *Sound Effects*, paste the prompt, "
                "set the duration, and save with the file name shown. Skip any of them and Scorp1 uses its "
                "built-in library instead.", ""]
        for s in custom:
            c = s["custom"]
            out.append(f"- `{c.get('filename', s['id'])}.mp3` ({c.get('duration', 2)}s): {c['prompt']}")
        out.append("")
        step += 1
    if music.get("source") in ("custom", "elevenlabs"):
        out += [f"## {step}. Music", "",
                "Generate a music bed in ElevenLabs *Music* (or bring your own licensed track) and save it as "
                "`music.mp3`.", "", f"Prompt: {music.get('prompt', music.get('mood', ''))}",
                f"Length: at least {int(plan.get('target_duration', 30)) + 5} seconds, instrumental, no vocals.", ""]
        step += 1
    else:
        out += [f"## {step}. Music", "",
                f"Nothing to do: Scorp1 uses `{Path(music.get('file', '')).name or 'a bundled track'}`. "
                "To use your own, drop it in `audio-in/` as `music.mp3`.", ""]
        step += 1
    out += [f"## {step}. Hand it back", "",
            "Put every file in this run's `audio-in/` folder, then run `/scorp1 render`. "
            "`/scorp1 status` shows what is still missing.", "",
            "Other files here: `voiceover-script.md` (the script with directions and pronunciations), "
            "`sound-design.md` (every sound and when it plays), `transcript.txt` (the whole read).", ""]
    return "\n".join(out)


# ---------------------------------------------------------------- timing

def align_script(text: str, heard: list[dict]) -> list[dict]:
    """The script's words with the heard timings, so captions and anchors spell names as written."""
    toks = text.split()
    if not heard or not toks:
        return heard

    want, want_of = "", []
    for i, t in enumerate(toks):
        k = "".join(words_of(t))
        want += k
        want_of += [i] * len(k)
    got, got_t = "", []  # every heard letter gets its slice of its word's time
    for w in heard:
        k = "".join(words_of(w["text"])) or "_"
        step = (w["end"] - w["start"]) / len(k)
        got += k
        got_t += [(w["start"] + step * n, w["start"] + step * (n + 1)) for n in range(len(k))]
    # letter-level alignment survives split words ("short-stay"), merged ones ("stavore dot com" heard
    # as "stavor.com") and misspelled names
    spans = {}
    for a, b, n in difflib.SequenceMatcher(None, want, got, autojunk=False).get_matching_blocks():
        for x in range(n):
            i, (s, e) = want_of[a + x], got_t[b + x]
            spans[i] = (min(spans.get(i, (s, e))[0], s), max(spans.get(i, (s, e))[1], e))
    out = [{"text": t, "start": spans[i][0] if i in spans else None,
            "end": spans[i][1] if i in spans else None} for i, t in enumerate(toks)]
    for i, o in enumerate(out):  # a script word nobody heard sits in the gap between its neighbours
        if o["start"] is None:
            prev = next((out[k]["end"] for k in range(i - 1, -1, -1) if out[k]["end"] is not None), heard[0]["start"])
            nxt = next((out[k]["start"] for k in range(i + 1, len(out)) if out[k]["start"] is not None), heard[-1]["end"])
            o["start"], o["end"] = prev, max(prev, nxt)
    return out


def resolve_timing(plan: dict, vo_info: dict, estimated: bool, music_cues: dict) -> dict:
    """vo_info: id -> {"duration": s, "file": str|None, "words": [{text,start,end}] relative}"""
    fps = plan["format"].get("fps", 30)
    voice = plan.get("voice", {})
    gap = voice.get("gap", 0.25)
    cursor = 0.0
    scenes_out, vo_out = [], []
    prev = None
    for scene in plan["scenes"]:
        overlap = scene.get("overlap", 0.0) if prev else 0.0
        start = max(0.0, cursor - overlap)
        t = start + scene.get("lead_in", 0.4)
        vo_ids = []
        last_end = None
        for line in scene.get("vo", []):
            info = vo_info.get(line["id"])
            if not info:
                continue
            vstart = snap_frame(t, fps)
            dur = info["duration"]
            def timed(text):
                return [{"text": w["text"], "start": r3(vstart + w["start"]), "end": r3(vstart + w["end"])}
                        for w in align_script(text, info.get("words", []))]
            words = timed(line["text"])
            vo_out.append({"id": line["id"], "scene": scene["id"], "file": info.get("file"),
                           "start": r3(vstart), "duration": r3(dur), "end": r3(vstart + dur),
                           "text": line["text"], "words": words})
            if line.get("caption"):  # written form for the screen ("stavore.com" for "stavore dot com")
                vo_out[-1].update(caption=line["caption"], caption_words=timed(line["caption"]))
            vo_ids.append(line["id"])
            last_end = vstart + dur
            t = last_end + line.get("gap_after", gap)
        end = start + scene.get("min", 2.0)
        if last_end is not None:
            end = max(end, last_end + scene.get("tail", 0.5))
        end = snap_frame(end, fps)
        scenes_out.append({"id": scene["id"], "start": r3(snap_frame(start, fps)), "end": r3(end),
                           "duration": r3(end - snap_frame(start, fps)), "vo": vo_ids})
        cursor = end
        prev = scene
    total = snap_frame(cursor, fps)

    by_scene = {s["id"]: s for s in scenes_out}
    by_vo = {v["id"]: v for v in vo_out}
    sfx_out, warnings = [], []
    for s in plan.get("sfx", []):
        a = s.get("anchor", {})
        t = None
        if "time" in a:
            t = a["time"]
        elif "scene" in a:
            sc = by_scene[a["scene"]]
            t = sc["end"] if a.get("at") == "end" else sc["start"]
        elif "vo" in a:
            v = by_vo.get(a["vo"])
            if v is None:
                warnings.append(f"{s['id']}: voice line {a['vo']} has no audio; sound skipped")
                continue
            t = v["end"] if a.get("at") == "end" else v["start"]
            if "word" in a:
                target = words_of(a["word"])
                hit = next((w for w in v["words"] if words_of(w["text"])[:1] == target[:1]), None)
                if hit:
                    t = hit["start"]
                elif estimated:
                    idx = next((i for i, w in enumerate(words_of(v["text"])) if w == target[0]), 0) if target else 0
                    n = max(1, len(words_of(v["text"])))
                    t = v["start"] + v["duration"] * idx / n
                else:
                    warnings.append(f"{s['id']}: word {a['word']!r} not heard in {a['vo']}; used line start")
        t += a.get("offset", 0.0)
        grid = music_cues.get(a.get("snap", ""), [])
        if grid:
            near = min(grid, key=lambda c: abs(c - t))
            if abs(near - t) <= a.get("snap_window", 0.3):
                t = near
        t = max(0.0, snap_frame(t, fps))
        sfx_out.append({"id": s["id"], "file": s.get("file"), "custom": bool(s.get("custom")),
                        "start": r3(t), "volume": s.get("volume", 0.45)})

    music = plan.get("music", {})
    music_out = None
    if music and music.get("source") != "none":
        music_out = {"file": music.get("file"), "volume": music.get("volume", 0.3),
                     "fade_out": music.get("fade_out", 1.5), "start": 0, "duration": total,
                     "automation": duck_automation(vo_out, music.get("duck_to", 0.35), total)}
    return {"schema": "scorp1.timing/1", "estimated": estimated, "fps": fps,
            "width": plan["format"].get("width"), "height": plan["format"].get("height"),
            "total": total, "scenes": scenes_out, "vo": vo_out, "sfx": sfx_out,
            "music": music_out, "warnings": warnings}


def duck_automation(vo: list[dict], duck: float, total: float) -> dict | None:
    """A Hyperframes volume lane: full level, down under every voice run, back up after."""
    if not vo or duck >= 1:
        return None
    runs = []
    for v in sorted(vo, key=lambda x: x["start"]):
        if runs and v["start"] - runs[-1][1] < 0.9:  # short breath: stay ducked
            runs[-1][1] = v["end"]
        else:
            runs.append([v["start"], v["end"]])
    pts = [{"t": 0, "v": 1}]
    for s, e in runs:
        down0, down1 = max(0.0, s - 0.35), max(0.0, s - 0.05)
        up0, up1 = e + 0.15, min(total, e + 0.6)
        if down0 > pts[-1]["t"]:
            pts.append({"t": r3(down0), "v": 1})
        pts.append({"t": r3(max(down1, pts[-1]["t"])), "v": duck})
        pts.append({"t": r3(up0), "v": duck})
        pts.append({"t": r3(up1), "v": 1})
    return {"version": 1, "lanes": [{"target": "volume", "points": pts}]}


PLUGIN_ROOT = Path(__file__).resolve().parent.parent  # skills/scorp1


def resolve_asset(path: str | None, run_dir: Path) -> Path | None:
    """A plan path is absolute, relative to the run folder, or relative to skills/scorp1."""
    if not path:
        return None
    p = Path(path)
    if p.is_absolute():
        return p if p.exists() else None
    for base in (run_dir, PLUGIN_ROOT):
        if (base / p).exists():
            return (base / p).resolve()
    return None


def _times(raw) -> list[float]:
    out = []
    for c in raw or []:
        if isinstance(c, (int, float)):
            out.append(float(c))
        elif isinstance(c, dict):
            for k in ("time", "t", "seconds", "start"):
                if k in c:
                    out.append(float(c[k]))
                    break
    return sorted(out)


def load_cues(plan: dict, run_dir: Path) -> dict:
    """{"cue": strong cues, "beat": every beat}, from a brag-style cue preset or `hyperframes beats` JSON."""
    p = resolve_asset(plan.get("music", {}).get("cues"), run_dir)
    if not p:
        return {"cue": [], "beat": []}
    data = json.loads(p.read_text(encoding="utf-8"))
    strong = _times(data.get("strongCues") or data.get("strong_cues") or data.get("cues") or data.get("downbeats"))
    beats = _times(data.get("beats")) or strong
    return {"cue": strong or beats, "beat": beats}


def cmd_estimate(a) -> None:
    plan = load_plan(a.run)
    wps = plan.get("voice", {}).get("wps", DEFAULT_WPS)
    info = {}
    if voice_mode(plan) != "none":
        for l in vo_lines(plan):
            info[l["id"]] = {"duration": est_seconds(l["text"], wps), "file": None, "words": []}
    timing = resolve_timing(plan, info, True, load_cues(plan, a.run))
    # catch wrong library paths now, not at render time
    music = plan.get("music", {})
    checks = [("music", music.get("file") if music.get("source") == "bundled" else music.get("fallback"))]
    checks += [("music cues", music.get("cues"))] if music.get("cues") else []
    checks += [(s["id"], s.get("file") or s.get("fallback")) for s in plan.get("sfx", [])]
    for name, path in checks:
        if path and not resolve_asset(path, a.run):
            timing["warnings"].append(f"{name}: file not found ({path})")
        elif not path and name != "music":
            timing["warnings"].append(f"{name}: custom sound has no library fallback")
    write_json(a.run / "plan" / "timing.estimate.json", timing)
    print_timing(timing, plan)


def print_timing(timing: dict, plan: dict) -> None:
    tag = "ESTIMATE" if timing["estimated"] else "FROM AUDIO"
    print(f"[{tag}] total {timing['total']:.2f}s (target {plan.get('target_duration', '?')}s)")
    for s in timing["scenes"]:
        print(f"  {s['id']:<14} {s['start']:6.2f} -> {s['end']:6.2f}  ({s['duration']:.2f}s)  {' '.join(s['vo'])}")
    for w in timing["warnings"]:
        print(f"  warning: {w}")
    target = plan.get("target_duration")
    if target and abs(timing["total"] - target) > max(2.0, 0.12 * target):
        print(f"  note: {timing['total']:.1f}s is far from the {target}s target; trim lines or scene minimums")


# ---------------------------------------------------------------- ingest

def clean_audio(src: Path, dst: Path) -> None:
    """Trim silence at both ends (keeping 60 ms), level to -16 LUFS, 48 kHz mono wav."""
    trim = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,"
            "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse")
    af = f"{trim},loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000"
    out = run([tool("ffmpeg"), "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
               "-af", af, "-ac", "1", "-c:a", "pcm_s16le", str(dst)])
    if out.returncode != 0:
        die(f"ffmpeg could not clean {src.name}: {out.stderr.strip()[:400]}")


def transcribe(path: Path, plan: dict) -> list[dict]:
    """Word timings via `npx hyperframes transcribe` -> [{text,start,end}] relative to the file."""
    # Engine "auto" uses Parakeet when installed (`npx hyperframes models install parakeet`), else whisper.
    lang = plan.get("voice", {}).get("language", "en")
    model = plan.get("voice", {}).get("whisper_model") or ("small.en" if lang == "en" else "small")
    with tempfile.TemporaryDirectory(prefix="scorp1-tx-", ignore_cleanup_errors=True) as tmp:
        cmd = [tool("npx"), "--yes", "hyperframes", "transcribe", str(path.resolve()),
               "--dir", tmp, "--model", model, "--json"]
        if lang != "en":
            cmd += ["--language", lang]
        out = run(cmd, timeout=900)
        words = []
        try:
            result = json.loads(out.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            result = {}
        if result.get("transcriptPath") and Path(result["transcriptPath"]).exists():
            words = parse_words(Path(result["transcriptPath"]).read_text(encoding="utf-8"))
        if not words:
            words = parse_words(out.stderr) or parse_words(out.stdout)
        if not words:
            why = result.get("reason") or out.stderr.strip()[-300:]
            hint = " (run: npx hyperframes models install parakeet)" if "unavailable" in str(why) else ""
            print(f"  warning: no word timings for {path.name}: {why}{hint}")
        return words


def parse_words(text: str) -> list[dict]:
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        # --json may print other lines; take the last JSON value
        for line in reversed((text or "").splitlines()):
            try:
                data = json.loads(line)
                break
            except json.JSONDecodeError:
                continue
        else:
            return []

    def walk(d):
        if isinstance(d, list) and d and isinstance(d[0], dict) and {"start", "end"} <= set(d[0]) \
                and ("text" in d[0] or "word" in d[0]):
            return d
        if isinstance(d, dict):
            for k in ("words", "transcript", "result", "data", "segments"):
                if k in d:
                    found = walk(d[k])
                    if found:
                        return found
            for v in d.values():
                found = walk(v)
                if found:
                    return found
        if isinstance(d, list):
            flat = []
            for item in d:
                if isinstance(item, dict) and "words" in item:
                    flat += walk(item["words"]) or []
            return flat or None
        return None

    raw = walk(data) or []
    return [{"text": str(w.get("text", w.get("word", ""))).strip(), "start": float(w["start"]), "end": float(w["end"])}
            for w in raw if str(w.get("text", w.get("word", ""))).strip()]


def similarity(expected: str, words: list[dict]) -> float:
    # letters only, so "every one baked" and "everyone bake" still count as the same read
    heard = "".join(t for w in words for t in words_of(w["text"]))
    want = "".join(words_of(expected))
    return difflib.SequenceMatcher(None, want, heard, autojunk=False).ratio() if heard else 0.0


def split_single_take(src: Path, plan: dict, out_dir: Path) -> dict:
    """Cut one long voiceover into VO01..VOnn by aligning its transcript to the script."""
    lines = vo_lines(plan)
    print(f"  transcribing single take {src.name} ...")
    words = transcribe(src, plan)
    if not words:
        die("could not transcribe the single take; generate one file per line instead (Option A)")
    heard = [(i, t) for i, w in enumerate(words) for t in words_of(w["text"])[:1]]
    heard_tokens = [t for _, t in heard]
    script_tokens, owner = [], []
    for li, l in enumerate(lines):
        for t in words_of(l["text"]):
            script_tokens.append(t)
            owner.append(li)
    sm = difflib.SequenceMatcher(None, script_tokens, heard_tokens, autojunk=False)
    first_word = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            li = owner[blk.a + k]
            first_word.setdefault(li, heard[blk.b + k][0])
    starts = []
    for li in range(len(lines)):
        if li not in first_word:
            die(f"could not find {lines[li]['id']} (\"{lines[li]['text'][:40]}...\") in the single take; "
                "check the read matches the script, or use one file per line")
        starts.append(first_word[li])
    if starts != sorted(starts):
        die("the single take reads the lines in a different order than the script")
    dur = probe_duration(src)
    cuts = []
    for li, wi in enumerate(starts):
        if li == 0:
            cuts.append(max(0.0, words[wi]["start"] - 0.15))
        else:
            prev_end = words[wi - 1]["end"]
            cuts.append((prev_end + words[wi]["start"]) / 2)
    cuts.append(dur)
    result = {}
    for li, l in enumerate(lines):
        piece = out_dir / f"{l['id']}.raw.wav"
        out = run([tool("ffmpeg"), "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
                   "-ss", f"{cuts[li]:.3f}", "-to", f"{cuts[li + 1]:.3f}", "-c:a", "pcm_s16le", str(piece)])
        if out.returncode != 0:
            die(f"ffmpeg could not cut {l['id']}: {out.stderr[:300]}")
        result[l["id"]] = piece
    return result


def cmd_ingest(a) -> None:
    run_dir = a.run
    plan = load_plan(run_dir)
    state = load_state(run_dir)
    found = scan_audio_in(run_dir)
    exp = expected_audio(plan)
    audio = run_dir / "audio"
    audio.mkdir(exist_ok=True)
    manifest = {"schema": "scorp1.audio/1", "voice": {}, "sfx": {}, "music": None, "warnings": []}

    sources = dict(found["voice"])
    if exp["voice"] and not sources and found["single"]:
        sources = split_single_take(found["single"], plan, audio)
    missing = [v for v in exp["voice"] if v not in sources]
    if missing and not a.allow_missing:
        die(f"missing voice files: {', '.join(missing)} (in {run_dir / 'audio-in'}). "
            "Add them, or pass --allow-missing to time those lines silent.")
    by_id = {l["id"]: l for l in vo_lines(plan)}
    for vid in exp["voice"]:
        if vid not in sources:
            continue
        src = sources[vid]
        dst = audio / f"{vid}.wav"
        clean_audio(src, dst)
        dur = probe_duration(dst)
        words = [] if a.no_words else transcribe(dst, plan)
        sim = similarity(by_id[vid]["text"], words) if words else None
        entry = {"file": f"audio/{vid}.wav", "source": src.name, "duration": r3(dur),
                 "loudness": loudness(dst), "match": None if sim is None else round(sim, 2), "words": words}
        manifest["voice"][vid] = entry
        flag = ""
        if sim is not None and sim < 0.75:
            flag = "  <- does not sound like the script line; check the file name"
            manifest["warnings"].append(f"{vid}: heard text matches the script only {sim:.0%}")
        print(f"  {vid}: {dur:5.2f}s  match {'-' if sim is None else f'{sim:.0%}'}{flag}")
        if src.name.endswith(".raw.wav"):
            src.unlink(missing_ok=True)

    for name, src in found["sfx"].items():
        dst = audio / f"{name}{src.suffix.lower()}"
        shutil.copyfile(src, dst)
        manifest["sfx"][name] = {"file": f"audio/{dst.name}", "duration": r3(probe_duration(dst))}
        print(f"  {name}: {manifest['sfx'][name]['duration']:.2f}s (custom sound)")
    for name in exp["sfx"]:
        if name not in found["sfx"]:
            manifest["warnings"].append(f"{name}: custom sound not provided; use the library fallback")
    if found["music"]:
        dst = audio / f"music{found['music'].suffix.lower()}"
        shutil.copyfile(found["music"], dst)
        manifest["music"] = {"file": f"audio/{dst.name}", "duration": r3(probe_duration(dst))}
        print(f"  music: {manifest['music']['duration']:.1f}s (custom)")
    elif exp["music"]:
        manifest["warnings"].append("music: custom track not provided; fall back to the bundled track in plan.music.fallback")

    write_json(audio / "manifest.json", manifest)
    for w in manifest["warnings"]:
        print(f"  warning: {w}")
    state["phase"] = "ingested"
    save_state(run_dir, state)
    print(f"Wrote {(audio / 'manifest.json').resolve()}")


def cmd_retime(a) -> None:
    run_dir = a.run
    plan = load_plan(run_dir)
    manifest_path = run_dir / "audio" / "manifest.json"
    manifest = read_json(manifest_path) if manifest_path.exists() else {"voice": {}, "sfx": {}, "music": None}
    info = {vid: {"duration": v["duration"], "file": v["file"], "words": v.get("words", [])}
            for vid, v in manifest["voice"].items()}
    timing = resolve_timing(plan, info, False, load_cues(plan, run_dir))
    # custom sounds and music the user supplied take over from the library
    specs = {x["id"]: x for x in plan.get("sfx", [])}
    for s in timing["sfx"]:
        spec = specs[s["id"]]
        if spec.get("custom"):
            got = manifest["sfx"].get(spec["custom"].get("filename", spec["id"]))
            s["file"] = got["file"] if got else spec.get("fallback")
    if timing["music"] and manifest.get("music"):
        timing["music"]["file"] = manifest["music"]["file"]
    elif timing["music"] and plan.get("music", {}).get("source") in ("custom", "elevenlabs"):
        timing["music"]["file"] = plan["music"].get("fallback")

    kept = []
    for s in timing["sfx"]:
        src = resolve_asset(s.get("file"), run_dir)
        if not src:
            timing["warnings"].append(f"{s['id']}: no sound file ({s.get('file')}); left out")
            continue
        s["source_path"] = str(src)
        s["duration"] = r3(min(probe_duration(src), max(0.05, timing["total"] - s["start"])))
        kept.append(s)
    timing["sfx"] = kept
    for v in timing["vo"]:
        src = resolve_asset(v["file"], run_dir)
        v["source_path"] = str(src) if src else None
    if timing["music"]:
        src = resolve_asset(timing["music"]["file"], run_dir)
        if src:
            timing["music"]["source_path"] = str(src)
            timing["music"]["media_duration"] = r3(probe_duration(src))
            if timing["music"]["media_duration"] < timing["total"]:
                timing["warnings"].append("music is shorter than the video; loop it or pick a longer track")
        else:
            timing["warnings"].append(f"music file not found ({timing['music']['file']}); no music bed")
            timing["music"] = None

    if not a.no_stage:
        stage_audio(run_dir, timing)
    write_json(run_dir / "timing.json", timing)
    print_timing(timing, plan)
    print(f"Wrote {(run_dir / 'timing.json').resolve()}")


def stage_audio(run_dir: Path, timing: dict) -> None:
    """Copy every sound into composition/assets/audio and write the <audio> tags for index.html."""
    dest = run_dir / "composition" / "assets" / "audio"
    dest.mkdir(parents=True, exist_ok=True)

    def place(src: str, name: str) -> str:
        target = dest / name
        shutil.copyfile(src, target)
        return f"assets/audio/{name}"

    tags = ["<!-- Scorp1 audio: generated by `scorp1.py retime` from timing.json. Re-run retime instead of hand-editing times. -->"]
    m = timing.get("music")
    if m:
        m["src"] = place(m["source_path"], "music" + Path(m["source_path"]).suffix.lower())
        auto = ""
        if m.get("automation"):
            auto = ' data-automation="' + json.dumps(m["automation"], separators=(",", ":")).replace('"', "&quot;") + '"'
        tags.append(f'<audio id="music" class="clip" data-start="0" data-duration="{timing["total"]}" '
                    f'data-track-index="10" data-volume="{m["volume"]}" data-fade-out="{m["fade_out"]}"'
                    f'{auto} src="{m["src"]}"></audio>')
    for v in timing["vo"]:
        if not v.get("source_path"):
            continue
        v["src"] = place(v["source_path"], f"{v['id']}.wav")
        tags.append(f'<audio id="{v["id"].lower()}" class="clip" data-start="{v["start"]}" '
                    f'data-duration="{v["duration"]}" data-track-index="30" data-volume="1" '
                    f'src="{v["src"]}"></audio>')
    for i, s in enumerate(timing["sfx"]):
        s["src"] = place(s["source_path"], f"{s['id']}{Path(s['source_path']).suffix.lower()}")
        tags.append(f'<audio id="{s["id"]}" class="clip" data-start="{s["start"]}" data-duration="{s["duration"]}" '
                    f'data-track-index="{11 + i}" data-volume="{s["volume"]}" src="{s["src"]}"></audio>')
    write_text(run_dir / "plan" / "audio-clips.html", "\n".join(tags) + "\n")
    print(f"Staged {len(tags) - 1} sounds into {dest.resolve()} (tags in plan/audio-clips.html)")


# ---------------------------------------------------------------- captions

def srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def caption_groups(timing: dict, max_words: int = 6, max_len: float = 2.6) -> list[dict]:
    groups = []
    for v in timing["vo"]:
        text = v.get("caption") or v["text"]
        words = v.get("caption_words") or v["words"] or [
            {"text": t, "start": v["start"] + v["duration"] * i / max(1, len(text.split())),
             "end": v["start"] + v["duration"] * (i + 1) / max(1, len(text.split()))}
            for i, t in enumerate(text.split())]
        cur = []
        for k, w in enumerate(words):
            cur.append(w)
            nxt = words[k + 1]["text"] if k + 1 < len(words) else ""
            too_long = len(cur) >= max_words or cur[-1]["end"] - cur[0]["start"] >= max_len
            end_here = ((too_long and not re.search(r"[.!?]$", nxt))  # never strand a sentence's last word
                        or re.search(r"[.!?]$", w["text"])
                        or (len(cur) >= 3 and re.search(r"[,;:]$", w["text"])))
            if end_here:
                groups.append(cur)
                cur = []
        if cur:
            groups.append(cur)
    return [{"start": g[0]["start"], "end": g[-1]["end"], "text": " ".join(w["text"] for w in g),
             "words": [[w["start"], w["end"]] for w in g]} for g in groups]


def cmd_captions(a) -> None:
    timing = read_json(a.run / "timing.json")
    groups = caption_groups(timing, a.max_words, a.max_len)
    out = []
    for i, g in enumerate(groups, 1):
        out.append(f"{i}\n{srt_time(g['start'])} --> {srt_time(g['end'])}\n{g['text']}\n")
    write_text(a.run / "captions.srt", "\n".join(out))
    write_json(a.run / "plan" / "caption-groups.json", groups)
    print(f"Wrote {(a.run / 'captions.srt').resolve()} ({len(groups)} captions)")


# ---------------------------------------------------------------- styles

def style_dirs() -> list[Path]:
    home = Path.home()
    return [Path.cwd() / ".scorp1" / "styles", home / ".claude" / "skills", home / ".agents" / "skills",
            PLUGIN_ROOT.parent]


def cmd_styles(a) -> None:
    seen = {}
    for base in style_dirs():
        for skill in sorted(base.glob("scorp1-*/SKILL.md")):
            name = skill.parent.name[len("scorp1-"):]
            if name in seen:
                continue
            text = skill.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"^description:\s*(.+)$", text, re.M)
            seen[name] = (skill, (m.group(1).strip() if m else "")[:160])
    if not seen:
        die("no style skills found")
    for name, (path, desc) in seen.items():
        print(f"{name:<12} {desc}")
        if a.paths:
            print(f"{'':<12} {path}")


# ---------------------------------------------------------------- main

def main() -> None:
    p = argparse.ArgumentParser(prog="scorp1", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create a run folder")
    s.add_argument("--business", required=True)
    s.add_argument("--style", required=True)
    s.add_argument("--format", default="landscape", choices=sorted(FORMATS))
    s.add_argument("--duration", type=float, default=30)
    s.add_argument("--voice", default="elevenlabs", choices=["elevenlabs", "kokoro", "none"])
    s.add_argument("--product", default=None)
    s.add_argument("--source", action="append", default=[], help="website or social URL (repeatable)")
    s.add_argument("--extra", default=None, help="free-text direction")
    s.add_argument("--root", default="scorp1-output")
    s.set_defaults(fn=cmd_init)

    s = sub.add_parser("latest", help="print the newest run folder")
    s.add_argument("--root", default="scorp1-output")
    s.add_argument("--phase", default=None)
    s.set_defaults(fn=cmd_latest)

    for name, fn, hlp in (("status", cmd_status, "where a run is"),
                          ("pack", cmd_pack, "build the ElevenLabs audio pack"),
                          ("estimate", cmd_estimate, "time the plan from word counts")):
        s = sub.add_parser(name, help=hlp)
        run_dir_arg(s)
        s.set_defaults(fn=fn)

    s = sub.add_parser("retime", help="time the plan from the real audio and stage it in the composition")
    run_dir_arg(s)
    s.add_argument("--no-stage", action="store_true", help="only write timing.json")
    s.set_defaults(fn=cmd_retime)

    s = sub.add_parser("mark", help="set a run's phase")
    run_dir_arg(s)
    s.add_argument("phase")
    s.set_defaults(fn=cmd_mark)

    s = sub.add_parser("ingest", help="clean, measure and transcribe audio-in/")
    run_dir_arg(s)
    s.add_argument("--no-words", action="store_true", help="skip transcription (no word anchors or captions)")
    s.add_argument("--allow-missing", action="store_true", help="time missing voice lines as silence")
    s.set_defaults(fn=cmd_ingest)

    s = sub.add_parser("styles", help="list installed style skills")
    s.add_argument("--paths", action="store_true")
    s.set_defaults(fn=cmd_styles)

    s = sub.add_parser("captions", help="write captions.srt from timing.json")
    run_dir_arg(s)
    s.add_argument("--max-words", type=int, default=6)
    s.add_argument("--max-len", type=float, default=2.6)
    s.set_defaults(fn=cmd_captions)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
