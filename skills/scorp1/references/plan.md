# Step 3: Storyboard, script and sound

Follow the loaded style skill's structure. This file covers how to write it down so the helper can time it.

## `plan/storyboard.md` (for people)

One block per scene:

```
## 2. The cakes  (min 4s, after VO02 ends +0.5s)
Picture:  three real cake photos (research/media/ruracio.jpg, bento-pink.jpg, wedding-3tier.jpg) pop into circles
On screen: Birthdays · Weddings · Bento
Voice:    VO02 "Birthdays, weddings, little bento cakes. Every one baked to order."
Effects:  circle mask pop-in, one per word as she names it; slow push-in on the middle photo
Sound:    card-place on the first circle, on the beat
Into next: whip-pan left
```

Then a short **Sound** section: music track and why, the level and duck, every sound effect with its moment, and any custom sound or music prompt for ElevenLabs.

## `plan/plan.json` (for the helper)

Start from `templates/plan.example.json`. Fields:

| Field | Meaning |
|---|---|
| `business` | `name`, `slug`, `url`, `socials`, `one_liner` |
| `style` | the style name |
| `target_duration` | seconds the advert should run |
| `format` | `aspect` (`landscape`, `vertical`, `square`, `portrait`), `width`, `height`, `fps` (30) |
| `voice.mode` | `elevenlabs`, `kokoro` or `none` |
| `voice.language` | `en`, `sw`, ... (sets transcription) |
| `voice.voice_brief` | who the narrator is, in one sentence (age, accent, warmth, energy) |
| `voice.voice_library_search` | what to type into ElevenLabs' Voice Library |
| `voice.model` | `eleven_multilingual_v2` (steady, the default), `eleven_v3` (most expressive, takes audio tags), `eleven_flash_v2_5` (fast) |
| `voice.settings` | `stability`, `similarity`, `style`, `speed`, `speaker_boost`, from the style skill |
| `voice.wps` | words a second for estimates (2.4 calm, 2.6 normal, 2.9 brisk) |
| `voice.gap` | seconds of silence between lines in the same scene |
| `music` | `source` (`bundled`, `custom`, `elevenlabs`, `none`), `file`, `cues`, `mood`, `prompt` (for ElevenLabs Music), `fallback` (bundled file if theirs never arrives), `volume`, `duck_to` (fraction kept under the voice), `fade_out` |
| `scenes[]` | in order: `id`, `title`, `min` (shortest it may run), `lead_in` (seconds before its first line), `tail` (seconds held after its last line), `overlap` (seconds it starts before the previous scene ends, for transitions), `visual`, `on_screen_text`, `effects`, `transition_out`, `vo[]` |
| `scenes[].vo[]` | `id` (`VO01`, `VO02`, ... in reading order across the whole advert), `text` (exactly what is spoken), `direction` (how to say it), `tags` (Eleven v3 audio tags such as `excited`, used only with `eleven_v3`), `pronounce` (`{"word": "how to say it"}`), `gap_after` (overrides `voice.gap`) |
| `sfx[]` | `id`, `file` (library path such as `assets/sfx/interface/drop_001.ogg`) **or** `custom` (`filename` such as `SFX01`, `prompt`, `duration`) with a `fallback` file, `volume`, `anchor`, `why` |
| `sfx[].anchor` | when it plays. `{"scene": "outro", "offset": 0.6}` (from the scene's start; add `"at": "end"` for its end), `{"vo": "VO03", "word": "WhatsApp", "offset": -0.05}` (on a spoken word), `{"vo": "VO03", "at": "end"}`, or `{"time": 4.2}`. Add `"snap": "beat"` or `"snap": "cue"` to pull it onto the music within `snap_window` (0.3s) |
| `captions` | `enabled`, plus the style's caption look |
| `cta` | `text` and the exact `url`, handle, number or place shown at the end |

A scene's length is worked out, not typed: it runs from its start until its last line ends plus `tail`, and never less than `min`. Scenes without voice run for exactly `min`. With `--voice none`, every scene runs for `min`.

## Writing the voiceover

- Write for the ear. One idea per line, one line per scene where possible; a line is one to two sentences.
- Write numbers, prices and symbols the way they should be said: "two thousand five hundred shillings", "K-S-H" only if they say it that way, "W-W-W dot" never; say "faithpastries dot co dot ke" or show the address on screen and say "link in bio". Put anything that will be said oddly in `pronounce`.
- Keep the business's own language: if they post in Sheng or mix Swahili and English, the voice can too (set `voice.language` to the main language).
- The narrator says what the picture can't. Don't read the on-screen text word for word, except in the CTA, where repeating it helps.
- About 2.6 words a second. A 30-second advert holds about 55–65 spoken words with room for music to breathe.
- Directions are for a voice actor ("smiling, unhurried", "drop the energy, almost a secret"). For `eleven_v3`, put up to two audio tags per line in `tags` (`excited`, `warmly`, `whispers`, `laughs softly`, `confident`), never inside `text`.

## Sound

Choose from [sound-library.md](sound-library.md). The style skill sets the music mood, how many effects, and which families. Effects follow the picture: a tap gets a click, a card landing gets a card sound, a reveal gets one soft impact. Anchor them to the words that cause them. Under a voice, fewer effects is better.

When nothing in the library fits a moment that matters (an oven ding for a bakery, a camera shutter for a photographer, a wave for a beach bar), add a `custom` sound with an ElevenLabs Sound Effects prompt and a library `fallback`. At most three custom sounds per advert.

Music: use the style's pick from the bundled tracks, or set `source: "elevenlabs"` with a `prompt` and a bundled `fallback` when the mood needs something the library doesn't have (an emotional piano for a founder story, Afrobeats energy for a club night). A custom track needs a beat map for snapping: once it arrives, run `npx hyperframes beats <file> --json` (see `/media-use`), save it next to the track, and point `music.cues` at it.

## Check the length

`python <skill-dir>/scripts/scorp1.py estimate <run>` prints each scene's start and end from word counts. Adjust until the total is within about 10% of `target_duration`, then mark the phase `plan`.
