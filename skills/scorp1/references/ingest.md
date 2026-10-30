# Step 5: Take the audio back

## Find the run

- `/scorp1 render` with no folder: `python <skill-dir>/scripts/scorp1.py latest --phase awaiting-audio`. If several businesses are waiting, list them (`latest` without `--phase`, or look in `scorp1-output/*/*/scorp1.json`) and ask which one.
- Read its `scorp1.json` and `plan/plan.json`, then load the style skill again; the render needs its look.

## Check the files

`scorp1.py status <run>` lists what arrived, what is missing and what didn't match. Common fixes:
- ElevenLabs names files after the text or the date. Rename them to `VO01.mp3`, ... in `audio-in/` (or ask the person which file is which if you can't tell from the length).
- One long file: name it `voiceover.mp3`; `ingest` splits it into lines.
- A missing custom sound or custom music is fine, since the fallback is used. A missing voice line is not: ask for it, or run `ingest --allow-missing` and say that line will be silent.

## Ingest

`scorp1.py ingest <run>`, per voice file:
1. trims silence at both ends (keeping 60 ms),
2. levels it to −16 LUFS (true peak −1.5 dB) as 48 kHz mono WAV in `audio/VOnn.wav`,
3. transcribes it for word timings (`npx hyperframes transcribe`, Parakeet or whisper),
4. compares what was heard with the script and prints a match score.

Below 75% match, the file is probably the wrong line, or the read drifted from the script. Listen to the transcript it heard (in `audio/manifest.json`), and either rename, ask for a regeneration, or update the line's `text` in `plan.json` to what was actually said (captions show the script's words at the heard times, so the script must match the read).

## Retime

`scorp1.py retime <run>`:
- places each scene and line: a scene starts at the previous scene's end minus its `overlap`, its first line starts `lead_in` later, lines follow each other with `gap`, and the scene ends `tail` after its last line (at least `min`);
- places every sound effect on its anchor (scene, line or spoken word), snapped to the music if asked, trimmed to the sound's real length;
- builds the music duck: full level, down to `duck_to` under every stretch of voice, back up between;
- copies every sound into `composition/assets/audio/` and writes the `<audio>` tags to `plan/audio-clips.html`;
- writes `timing.json`, the single source of truth for every time in the edit.

Read its printout. Handle every warning (a word anchor not heard, a missing file, music shorter than the video). If the total is far from the target, shorten or lengthen scene `min`, `tail` and `lead_in`, or ask for a shorter read; don't speed up the voice in the edit.

Platform limits to keep in mind: Instagram Reels and TikTok ads run best under 30s, WhatsApp Status cuts at 60s and YouTube bumpers at 6s.

## Captions

If the style or the person wants captions: `scorp1.py captions <run>` writes `captions.srt` (for upload) and `plan/caption-groups.json` (groups of up to six words, broken at sentence ends, each with its words' start and end times for word-by-word highlights, for burning in). Captions show the script's spelling (or the line's `caption`, such as `stavore.com`) at the times the speech model heard, so a misheard brand name doesn't reach the screen. Read the groups once before composing.
