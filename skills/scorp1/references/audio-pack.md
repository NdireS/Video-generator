# Step 4: The audio pack

`python <skill-dir>/scripts/scorp1.py pack <run>` builds `audio-pack/` from `plan.json`. Run it again whenever the plan changes; it rewrites everything there.

## What to check before handing it over

- Open `audio-pack/README.md` and read it as the person will. Every line has its file name, the voice search makes sense for the business, and the settings come from the style.
- `lines/VOnn.txt` contains only what is spoken (plus audio tags for Eleven v3). Nothing in brackets for other models, since they would read it out.
- Prices, phone numbers, web addresses and local names are written as they should be said, with `pronounce` entries for anything else.

## What to tell the person

Keep it short:

```
Your audio pack is ready: <run>/audio-pack/README.md

1. In ElevenLabs, pick a voice: <voice brief> (search "<search>").
2. Model <model>, stability <s>, similarity <x>, style <y>, speed <z>.
3. Generate each line in audio-pack/lines/ and save it as VO01.mp3, VO02.mp3, ...
   (or paste transcript.txt as one take and save voiceover.mp3).
4. <custom sounds / music, if any>
5. Put the files in <run>/audio-in/ and run /scorp1 render.
```

Then list the lines themselves so they can check the script before spending credits:

```
VO01 (hook)   "Juja, your favourite cake plug just went online."
VO02 (cakes)  "Birthdays, weddings, little bento cakes. Every one baked to order."
```

Ask whether to change anything in the script now. If they edit lines, update `plan.json` and run `pack` again.

## ElevenLabs notes

- **Models.** Multilingual v2 is the steadiest for adverts and keeps a voice consistent across separate generations. Eleven v3 is the most expressive and reads audio tags (`[excited]`, `[whispers]`), but varies more between takes, so generate two or three and keep the best. Flash v2.5 is quick and fine for drafts.
- **Settings.** Lower stability gives a livelier read with more variation; higher is calmer and more consistent. Similarity keeps it close to the chosen voice. Style exaggerates the voice's character, so keep it at 0.4 or below for clean adverts. Speed is from 0.7 to 1.2.
- **Consistency.** Same voice, model and settings for every line. If one line comes out different in tone, regenerate that line only.
- **Pauses.** Line breaks between files are free, since Scorp1 places the lines. Inside a line use punctuation: a comma for a short breath, a full stop for a beat, an ellipsis for a longer pause.
- **Sound Effects.** Describe the sound, its material and space, and how it ends ("single soft oven timer ding in a small kitchen, short tail"). Set the duration in the generator.
- **Music.** Instrumental, a genre, tempo and mood, and "no vocals"; a little longer than the advert. A custom track replaces the bundled bed and gets its own credit.
- **Licensing.** Commercial use of ElevenLabs output depends on the person's plan. Mention it once if the advert is for a paying client.
