# Scorp1

**Give it a business. Get back an advert video.**

Scorp1 is a skill-driven video editor for Claude Code and Codex. Point it at a business's website or social pages. It researches what the business does and how it uses each platform, writes the advert in the style you choose, and gives you the voiceover script and sound prompts to generate in ElevenLabs. When you hand the audio back, it edits and renders the whole video to your voice, with music, sound effects, captions, a poster frame and post captions.

The **style skills** decide what kind of advert it is: structure, pacing, voice, look, effects, transitions, music and sound. Scorp1 is the editor that runs the work.

```
 website / socials ──► research ──► style skill ──► storyboard + script ──► AUDIO PACK ──► you, in ElevenLabs
                                                                                                    │
 video.mp4 ◄── render ◄── preview ◄── build (HyperFrames) ◄── retime to your audio ◄── audio-in/ ◄──┘
```

## What you get

| Stage | Files |
|---|---|
| Brief (`/scorp1 <link>`) | `business-profile.md`, `storyboard.md`, and `audio-pack/`: a step-by-step ElevenLabs README, one paste-ready file per voice line, the whole read as `transcript.txt`, the script with directions and pronunciations, the sound design cue sheet, and custom sound and music prompts |
| Render (`/scorp1 render`) | `video.mp4` (poster baked in as the thumbnail), `poster.jpg`, `captions.srt`, `share-copy.md` (a caption for each platform), `credits.txt`, and the editable HyperFrames project in `composition/` |

## Styles

| Style | For | Default |
|---|---|---|
| `launch` | Something new: a site, app, shop, branch or menu | 30s landscape |
| `product` | One product or service as the hero | 20s vertical |
| `offer` | A discount, bundle, seasonal deal or deadline | 15s vertical |
| `story` | The people, the origin, the craft | 45s landscape |
| `proof` | Real public reviews and ratings do the selling | 25s vertical |
| `howto` | How to order, book or use it, step by step | 30s vertical |

Leave `--style` out and Scorp1 recommends one from its research.

## Requirements

- **Claude Code** and/or **Codex**
- **Node.js** (for `npx hyperframes`), **Python 3.10+** and **ffmpeg** on your PATH
- **HyperFrames skills** (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`). Install or refresh them with:
  ```bash
  npx hyperframes skills update
  ```
- **A speech model** for word timings (installed once per machine):
  ```bash
  npx hyperframes models install parakeet
  ```
- An **ElevenLabs** account for the voice. Or `--voice voicestudio` to have Scorp1 make the voice itself in [VoiceStudio](#making-the-voice-with-voicestudio) on your PC, `--voice kokoro` for HyperFrames' built-in text-to-speech, or `--voice none` for music only.

## Install (once, works from every folder)

Clone the repo once, anywhere you like, then install it as a user-level plugin in either tool or both:

```bash
git clone https://github.com/NdireS/Video-generator.git
```

**Claude Code**
```bash
claude plugin marketplace add ./Video-generator
```
```bash
claude plugin install scorp1@scorp1 --scope user
```
Claude Code reads the plugin straight from the repo folder, so edits take effect in the next session.

**Codex**
```bash
codex plugin marketplace add ./Video-generator
```
```bash
codex plugin add scorp1@scorp1
```
Codex keeps a copy in `~/.codex/plugins/cache/scorp1/`. After you edit the repo, run `codex plugin add scorp1@scorp1` again (bump `version` in `.codex-plugin/plugin.json` if it doesn't pick the change up).

## How to use it: Claude Code

1. **Open any folder** where you want the videos to live (each business gets `scorp1-output/<business>/…` there), and start Claude Code.
2. **Ask for the advert:**
   ```
   /scorp1 https://stavore.com --style product --format vertical --duration 30
   ```
   Or in plain words: *"Make an advert video for stavore.com"*. Socials work too: add the business's Instagram, TikTok or Facebook links after the website. Scorp1 also searches the web for the business by name. Add any direction after the options ("Sheng is fine", "aim at uni students").
3. **Help it read the socials.** If Instagram, TikTok or Facebook block reading, Scorp1 asks for screenshots of the profile and top posts. Drop them in `research/inbox/` inside the run folder.
4. **Choose or confirm the style** when it recommends one.
5. **Read the brief.** You get the storyboard, the script lines, and `audio-pack/README.md`. Change any line now; it rebuilds the pack.
6. **Make the audio in ElevenLabs** (see below), and save the files into the run's `audio-in/` folder.
7. **Render:**
   ```
   /scorp1 render
   ```
   It finds the run waiting for audio, cleans and times everything to your voice, builds the video, and opens the preview with a draft render.
8. **Approve or ask for changes** ("make the logo bigger", "swap VO03 for this line"). Then it renders the final video, poster, captions and share copy.

Other commands: `/scorp1 status` (where every run stands and what is missing), `/scorp1 styles` (installed styles). Add `--no-stops` to skip the approval stops.

## How to use it: Codex

The same flow; the skill is called with `$` instead of `/`:

1. Open your working folder in Codex.
2. `$scorp1 https://stavore.com --style product`, or just ask "make an advert video for this business: <link>" (Codex picks the skill from its description).
3. Follow the brief, make the audio in ElevenLabs, drop the files in `audio-in/`.
4. `$scorp1 render`.
5. Approve the draft, then get the final.

You can switch tools between the stages: brief in Codex, render in Claude Code, or the other way round. The run folder holds all the state.

## Making the audio in ElevenLabs

Everything you need is in `audio-pack/README.md`, written for that advert. In short:

1. **Voice:** open *Voices > Voice Library* and search the phrase the pack gives (for example "Kenyan female warm narration"). Use the same voice for every line.
2. **Model and settings:** as listed in the pack (model, stability, similarity, style, speed).
3. **Lines:** paste each `lines/VO01.txt`, `VO02.txt`, … and download each as `VO01.mp3`, `VO02.mp3`, … The names just need `VO` and the number in them.
   *Or* paste `transcript.txt` as one take and save it as `voiceover.mp3`. Scorp1 cuts it into lines itself.
4. **Custom sounds** (optional): paste each prompt into *Sound Effects* and save as `SFX01.mp3`, … Skip any and Scorp1 uses its built-in library.
5. **Music** (only if the pack asks): generate in *Music* and save as `music.mp3`.
6. Put everything in the run's `audio-in/` folder and run `/scorp1 render`.

## Making the voice with VoiceStudio

If the VoiceStudio app is installed, Scorp1 can make the voice itself and go straight from the link to the finished video:

```
/scorp1 https://stavore.com --style product --voice voicestudio --no-stops
```

Open VoiceStudio first (it takes a few minutes to start). Scorp1 uses its fast KittenTTS engine, one request per line, about 15-40 seconds each. Add a direction to pick the voice ("male voice", "use my cloned voice"). Leave out `--no-stops` to read and approve the script before the voice is made. In Codex, type `$scorp1` instead of `/scorp1`, and give it network access: Codex blocks the network by default, even `localhost`, so it can't reach VoiceStudio or research the business. Either pick **Full access** in the chat's permissions menu, or allow it for good in `~/.codex/config.toml`:

```toml
[sandbox_workspace_write]
network_access = true
```

Any other voice tool works the same way (a local text-to-speech app, your own recording): save one file per line as `VO01`, `VO02`, … in `audio-in/`.

Silence at the start or end of a file and uneven loudness don't matter: Scorp1 trims and levels every file, transcribes it to check it matches the script, and lines up the picture and sound effects with the exact words.

## Making your own style

A style is just a skill named `scorp1-<name>`:

1. Copy `skills/scorp1/templates/style-template.md` to `~/.claude/skills/scorp1-<name>/SKILL.md` (Claude Code) and/or `~/.agents/skills/scorp1-<name>/SKILL.md` (Codex). A project-only style can go in `./.scorp1/styles/scorp1-<name>/SKILL.md`.
2. Fill in every section: when to pick it, defaults, structure, voice, look, motion and effects, transitions, music, sound effects, captions, CTA, and what to avoid.
3. Use it: `/scorp1 <link> --style <name>`.

Or ask: *"Make a new Scorp1 style called `luxury` for high-end fashion: slow, black and gold, cello music"*, and the agent fills the template in for you.

## The helper script

`skills/scorp1/scripts/scorp1.py` (standard-library Python, plus ffmpeg) does the work that must be exact. The agent runs it; you can too:

| Command | Does |
|---|---|
| `init` | Creates a run folder and its state |
| `latest` / `status` | Finds runs; shows what is waiting and missing |
| `pack` | Builds the ElevenLabs audio pack from `plan.json` |
| `estimate` | Times the plan from word counts before any audio exists |
| `ingest` | Trims, levels (−16 LUFS) and transcribes your files; splits a single take into lines; checks each line against the script |
| `retime` | Times every scene, line, sound effect and the music duck from the real audio; copies the audio into the composition and writes the `<audio>` tags |
| `captions` | Writes `captions.srt` and caption groups: the script's spelling at the heard word times |
| `styles` | Lists installed styles |

Tests for the timing helpers: `python tests/test_scorp1.py`.

## Example

Tested end to end on [stavore.com](https://stavore.com) in October 2026. Scorp1 read the website and searched the web; it found no social accounts, so the advert is built from the site's own screens, logo and colours. The run used the `product` style and six voice lines, and produced a 27-second 1080×1920 video with music, seven sound effects and word-by-word captions.

## Repo layout

```
.claude-plugin/          Claude Code plugin + marketplace manifests, icon
.codex-plugin/           Codex plugin manifest
.agents/plugins/         Codex marketplace manifest
skills/
  scorp1/                the editor: SKILL.md, references/ (one per step), scripts/scorp1.py,
                         templates/ (plan.example.json, style-template.md), assets/ (music, sfx)
  scorp1-launch/         style skills
  scorp1-product/
  scorp1-offer/
  scorp1-story/
  scorp1-proof/
  scorp1-howto/
tests/                   timing helper tests (python tests/test_scorp1.py)
```

## Credits

Music by Sascha Ende (ende.app), CC BY 4.0: credit it in every post that uses it. Sound effects by Kenney and unicae_games, CC0. The cue presets and sound catalogue come from [brag](https://github.com/latent-spaces/brag) (MIT). Details in [CREDITS.md](CREDITS.md).
