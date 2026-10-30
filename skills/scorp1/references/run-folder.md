# Run folder

`scorp1.py init` creates one per advert: `./scorp1-output/<business-slug>/<style>-<YYYYMMDD-HHMM>/`.

```
scorp1.json               state: business, style, options, phase (scorp1.py keeps it)
research/
  business-profile.md     what the business is, sells, says, and how it uses each platform
  sources.md              every URL read, with what was taken from it
  capture/                `npx hyperframes capture` output for the website
  inbox/                  screenshots or exports the person drops in (social pages that need a login)
  media/                  real images, logo and clips chosen for the video (with where each came from)
plan/
  storyboard.md           the advert for people: scenes, words, visuals, sound
  plan.json               the advert for the helper (schema: templates/plan.example.json)
  timing.estimate.json    `estimate` output from word counts
  audio-clips.html        `retime` output: every <audio> tag, ready to paste
  caption-groups.json     `captions` output for on-screen captions
audio-pack/               what the person takes to ElevenLabs (`pack`)
  README.md               step by step
  lines/VO01.txt ...      one paste-ready line each
  transcript.txt          the whole read as one take
  voiceover-script.md     lines, directions, pronunciations, estimated lengths
  sound-design.md         music and every sound effect, with when and why
audio-in/                 the person drops the generated files here
audio/                    cleaned voice (VOnn.wav), custom sounds, music, manifest.json (`ingest`)
timing.json               exact times for scenes, voice, words, sound effects and the music duck (`retime`)
composition/              the HyperFrames project (index.html, compositions/, assets/)
video.mp4                 final render, poster baked as frame 0
poster.jpg                best frame
captions.srt              subtitles for platforms that take a file
share-copy.md             post captions per platform
credits.txt               music and media credits
```

## File names in `audio-in/`

The helper matches loosely, so most ElevenLabs downloads work once the line number is in the name:

| Put in | Matches | Examples |
|---|---|---|
| Voice line | `VO` + number | `VO01.mp3`, `vo-2 final.wav`, `ElevenLabs_VO3.mp3` |
| One take | name starts with `voiceover`, `narration`, `vo` or `full` | `voiceover.mp3` |
| Custom sound | `SFX` + number | `SFX01.mp3` |
| Music | name starts with `music` | `music.mp3` |

Anything else is listed as unmatched by `scorp1.py status`.

## Phases

`research` → `plan` → `awaiting-audio` → `ingested` → `composing` → `preview` → `delivered`. `pack` sets `awaiting-audio`, `ingest` sets `ingested`; set the others with `scorp1.py mark <run> <phase>`.
