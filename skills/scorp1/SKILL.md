---
name: scorp1
description: Turn any business into an advert video. Give it the business's website or social pages; Scorp1 researches what the business does and how it shows up online, writes the advert in the chosen style (launch, product spotlight, offer, brand story, social proof, how-to, or a custom style skill), hands back a voiceover script and sound prompts to generate in ElevenLabs (or makes the voice itself with VoiceStudio or Kokoro), then edits and renders the full video to that audio with music, sound effects, captions and share copy. Use when someone says "/scorp1", "$scorp1", "make an advert for this business", "promo video for this website/Instagram", or "render the scorp1 video".
---

# Scorp1

A video editor for businesses. The style skill decides how the advert feels; this skill runs the edit.

Two stops are built in, because the voice is made outside:

1. **Brief** (`/scorp1 <url>`): research, storyboard, script, and an audio pack for ElevenLabs. Stop.
2. **Render** (`/scorp1 render`): take the audio back, time everything to it, build, preview, render. Stop for approval before the final render unless the person asked for no stops.

`<skill-dir>` is the folder holding this file. Run the helper as `python <skill-dir>/scripts/scorp1.py <command>`; it handles run folders, the audio pack, audio cleanup, timing and captions, so never do that maths by hand. Templates are in `<skill-dir>/templates/`, bundled music and sound effects in `<skill-dir>/assets/`.

## Invocation

```
/scorp1 <website and/or social URLs> [options] [free-text direction]
/scorp1 render            continue the newest run waiting for audio (or name the run folder)
/scorp1 status            where every run in ./scorp1-output stands
/scorp1 styles            list the style skills installed
```

| Option | Values | Default |
|---|---|---|
| `--style` | `launch`, `product`, `offer`, `story`, `proof`, `howto`, or any installed `scorp1-<name>` style | recommended from research |
| `--format` | `landscape` 16:9, `vertical` 9:16, `square` 1:1, `portrait` 4:5 | the style's default |
| `--duration` | seconds | the style's default |
| `--product` | the product, service or offer to feature | none |
| `--voice` | `elevenlabs` (you generate it), `voicestudio` (the local VoiceStudio app, automatic), `kokoro` (local, automatic), `none` (music only) | `elevenlabs` |
| `--captions` | `on`, `off` | the style's default |
| `--lang` | voiceover language code | `en` |
| `--no-stops` | skip approval stops (the audio stop stays unless `--voice` is `voicestudio`, `kokoro` or `none`) | off |

Codex users type `$scorp1` instead of `/scorp1`. Free text after the options is creative direction ("make it feel like a Sunday morning", "Sheng is fine", "aim at university students"): keep it in the plan.

## Before anything

- Needs `ffmpeg`, `node`/`npx` and `python` on PATH, plus the HyperFrames skills (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`). If any skill is missing: `npx hyperframes skills update`.
- Word timings need a speech model: `npx hyperframes models list`; if Parakeet is not installed, run `npx hyperframes models install parakeet` once (whisper also works where it is built).
- Output goes under `./scorp1-output/<business-slug>/<style>-<timestamp>/` in the current folder: the **run folder**. Its layout is in [references/run-folder.md](references/run-folder.md).

## Stage 1: Brief

### 1. Research the business
**Read:** [references/research.md](references/research.md)

`python <skill-dir>/scripts/scorp1.py init --business "<name>" --style <style-or-tbd> --format <f> --duration <d> --voice <v> --source <url> ...` creates the run folder; use what it prints for every later step.
Read the website and every social link, collect real media, and write `research/business-profile.md`.
**Gate:** the profile answers every question in the research rubric, with sources, and real media is saved in `research/media/`.

### 2. Choose the style
**Read:** [references/styles.md](references/styles.md)

If `--style` was given, use it. Otherwise recommend one from the profile, with one line on why, and ask (skip asking under `--no-stops`). Then load the style skill (`scorp1-<style>`; how to find it is in styles.md) and follow it for everything it covers: structure, pacing, voice, visuals, effects, transitions, music, sound effects, captions and CTA. This skill decides how the work is done; the style decides how it looks and sounds.
**Gate:** the style skill is loaded, and its format and duration defaults are applied wherever the person didn't set one.

### 3. Storyboard, script and sound
**Read:** [references/plan.md](references/plan.md)

Write `plan/storyboard.md` (for people) and `plan/plan.json` (for the helper; template `templates/plan.example.json`). Then run `scorp1.py estimate <run>` and adjust lines and scene minimums until the estimate is within about 10% of the target length.
**Gate:** `estimate` prints no `note:` and no warnings, and every scene shows something real from the business.

### 4. Audio pack, then stop
**Read:** [references/audio-pack.md](references/audio-pack.md)

`scorp1.py pack <run>` writes `audio-pack/`: the step-by-step `README.md`, one paste-ready text file per line, the whole read as `transcript.txt`, the script with directions and pronunciations, the sound design cue sheet, and prompts for any custom sounds or music.
- `--voice elevenlabs`: show the storyboard in short form, the script lines, and the path to `audio-pack/README.md`. Say: generate the files, put them in the run's `audio-in/` folder, then run `/scorp1 render`. **Stop here.**
- `--voice voicestudio`: make each line in VoiceStudio (a free local ElevenLabs alternative, http://localhost:3900), then go on to stage 2:
  1. `curl -s -m 5 http://localhost:3900/health` (in PowerShell type `curl.exe`, since `curl` there is another command). No answer: tell the person to open VoiceStudio and wait about 4 minutes for it to start, and stop; the audio pack still works for ElevenLabs.
  2. One line at a time, same voice for every line:
     ```
     curl -s -m 900 -X POST http://localhost:3900/generate -F "text=<<run>/audio-pack/lines/VOnn.txt" -F engine=kittentts -F preset_voice=<voice> -F language=English -F speed=<speed> -o <run>/audio-in/VOnn.wav
     ```
     `text=<file` reads the line from the file, so quotes in the script can't break the command. Defaults: `expr-voice-2-f` at speed 1.12 for a female narrator, `expr-voice-2-m` at 1.05 for a male one; the person's direction wins. A cloned voice: `-F engine=pockettts -F profile_id=<id>` instead (ids from `GET /profiles`). Never the OmniVoice engine: it can take minutes a line on a CPU. KittenTTS is English only; for other languages use the person's choice of engine or `--voice elevenlabs`.
  3. Expect 15-40 seconds a line (the first one loads the model, about a minute and a half). Record the engine and voice in `plan.json` under `voice.voicestudio` and in `credits.txt`.
- `--voice kokoro`: generate each line with `npx hyperframes tts <lines/VOnn.txt> --voice <id> --output <run>/audio-in/VOnn.wav` (see `/media-use` for voices and setup), then go on to stage 2.
- `--voice none`: go straight to stage 2.

## Stage 2: Render

### 5. Take the audio back
**Read:** [references/ingest.md](references/ingest.md)

Find the run (`scorp1.py latest --phase awaiting-audio`, or the folder the person named), run `scorp1.py status <run>`, and fix any naming problems with the person. Then run `scorp1.py ingest <run>` (it trims, levels and transcribes), then `scorp1.py retime <run>` (it times every scene, line and sound, writes `timing.json`, copies the audio into the composition and writes `plan/audio-clips.html`), then `scorp1.py captions <run>` if captions are on.
**Gate:** no line with a low script match is left unexplained, no warning from `retime` is left unhandled, and the total is within the platform limits of the format.

### 6. Build the edit
**Read:** the `hyperframes` skill (its contract, `references/format.md`, `references/motion.md`), `hyperframes-cli`, `hyperframes-registry`. Scorp1 replaces their storyline, SPEC and REVIEW steps: the storyboard and timing.json are the spec, and `check` is the gate.
**Read:** [references/compose.md](references/compose.md)

Build `composition/` as a HyperFrames project. Scene hosts take their start and duration from `timing.json`, and the audio tags are pasted from `plan/audio-clips.html` as they are. Visual moments land on the narrator's words (use the word times in `timing.json`). The style skill sets the look, the effects and the transitions.
**Gate:** `npx hyperframes check --json` shows zero errors and every warning weighed; snapshots of every scene's midpoint look right.

### 7. Preview, approve, deliver
**Read:** [references/deliver.md](references/deliver.md)

Open the Studio preview and render a draft; show both and wait for approval (skip under `--no-stops`). Then render the final video, pick and bake the poster frame, and write `captions.srt`, `share-copy.md` (a caption per platform) and `credits.txt`.
**Gate:** `video.mp4`, `poster.jpg`, `share-copy.md` and `credits.txt` are in the run folder, and the video's length, size, frames and loudness are checked.

Use `scorp1.py mark <run> <phase>` as you move between steps, so `/scorp1 status` stays true.

## Laws of the edit

- **Real over invented.** Show the business's own logo, products, photos, screens, prices and words. Generate or draw only what doesn't exist, and never invent reviews, prices, awards or claims. A testimonial is only used if it is public and attributed.
- **The voice leads.** Picture changes and sound effects land on the narrator's words and on the music's beats, never at arbitrary times.
- **One idea per scene.** Every on-screen line holds long enough to read (about 0.3 seconds a word, never under 0.8 seconds).
- **The first two seconds sell it.** A product, a face, a bold claim or the offer, never a slow logo fade.
- **End on the action.** The last scene says exactly what to do and where: WhatsApp number, website, shop location, handle.
- **Speak like the customer.** Use the business's own words and their customers' language, not "elevate your experience".
- **Credit the music.** Bundled tracks are CC BY 4.0 and need the credit line in `credits.txt` and the post caption.
