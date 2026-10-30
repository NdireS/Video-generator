# Step 6: Build the edit

The composition lives in `<run>/composition/`. Build it with HyperFrames, following its contract. Scorp1 adds the rules below.

## Set up

1. Read `timing.json`: `width`, `height`, `fps`, `total`, `scenes[]`, `vo[]` (with absolute `words[]`), `sfx[]`, `music`.
2. Copy the media you will show from `research/media/` into `composition/assets/` (images in `assets/img/`, logo in `assets/brand/`). Audio is already in `assets/audio/`.
3. `index.html` is the root: `data-width`, `data-height` and `data-duration` = `timing.total`. It holds one host per scene and the audio tags, and ends with the root's own (empty) timeline, or `check` fails with `missing_timeline_registry`:

```html
<script>
  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = gsap.timeline({ paused: true });
</script>
```

## Scene hosts

One sub-composition per scene in `compositions/<scene-id>.html`, hosted with the times from `timing.json`:

```html
<div id="cakes" data-composition-id="cakes" data-composition-src="compositions/cakes.html"
     data-start="3.733" data-duration="6.167" data-track-index="2" data-track-kind="graphics"
     data-width="1080" data-height="1920" style="z-index: 2"></div>
```

Later scenes sit above earlier ones (`z-index`), so an `overlap` is where the transition happens: the incoming scene's first `overlap` seconds are its transition in.

## Audio

Paste `plan/audio-clips.html` into `index.html` as it is. The times, levels, duck and file paths come from `retime`. To change any of them, change `plan.json` and run `retime` again; never edit them by hand. If `retime` reported music shorter than the video, loop it with a second clip on another track with a crossfade, or pick a longer track.

## Land the picture on the words

Inside a scene, local time = absolute time − the scene's `data-start`. For every on-screen moment the storyboard ties to the voice, find the word in `timing.json` (`vo[].words[]`) and start the tween about 0.1s before the word's `start`:

```js
// VO02 says "weddings" at 4.993 (absolute); scene starts at 3.733 → local 1.26
tl.fromTo("#circle-weddings", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }, 1.16);
```

Write a comment with the word and absolute time next to each such tween, so a retime can be followed by a quick re-sync. Sound effects that belong to a visual action are already at the word's time; animate the action to match the sound's `start` in `timing.json`.

Music beats: the cue preset (`plan.json` → `music.cues`) lists beats and strong cues. Cuts and big reveals that aren't tied to a word should land on a strong cue.

## Captions on screen

When captions are on, read the HyperFrames `references/captions.md` and build one captions host covering the whole video from `plan/caption-groups.json`, styled by the style skill. Keep captions inside the title-safe area and clear of the platform UI (bottom 20% and right edge on TikTok and Reels).

## Look and motion

The style skill sets the type, colour, layout, effects, transitions and pacing. The brand's own colours and fonts from the research come first; the style shapes how they are used. Before hand-building a named effect (a glitch, film grain, a light leak, kinetic type, a chart), search the registry (`/hyperframes-registry`).

## Check

```
npx hyperframes lint
npx hyperframes check --json
npx hyperframes snapshot --at <mid-point of every scene>
```

Fix every error. Look at every snapshot: real media shows, text is readable and inside the safe area, nothing is cut off, and the brand looks like the brand. Then mark the phase `composing` and continue to delivery.
