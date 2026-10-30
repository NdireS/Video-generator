# Step 7: Preview, approve, deliver

## Preview

1. `npx hyperframes preview --background` from `composition/`, and check the URL answers. Give the person the link: they can scrub it and edit there.
2. `npx hyperframes render --quality draft --output ../draft.mp4`.
3. Show the draft and ask for approval or changes. Mark the phase `preview`.

Changes to words or voice: update `plan.json`, run `pack` again, regenerate only the changed lines, then `ingest` and `retime`, and re-sync the scenes whose times moved. Changes to picture: edit the scene files and check again.

## Final

1. `npx hyperframes render --quality delivery --output ../video.mp4` from `composition/`.
2. **Poster.** Pick the frame that sells the advert on its own: the hero product or the offer, sharp, with the headline readable and the brand visible. Extract it to `poster.jpg` (`ffmpeg -ss <t> -i video.mp4 -frames:v 1 -q:v 2 poster.jpg`), then bake it as frame 0 so every platform shows it as the thumbnail:
   ```
   ffmpeg -i video.mp4 -i poster.jpg -filter_complex "[0:v][1:v]overlay=enable='eq(n,0)'" -c:a copy -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p video.tmp.mp4
   ```
   then replace `video.mp4` with `video.tmp.mp4`.
3. **Verify** with ffprobe: duration equals `timing.total`, size equals the format, frame count equals `total × fps`, audio present. Check loudness: the voice sits around −16 LUFS, and the peak stays under −1 dB (`ffmpeg -i video.mp4 -af loudnorm=print_format=summary -f null -`).
4. `captions.srt`: already written if captions were on; copy it next to the video.
5. `share-copy.md`: a post caption per platform the profile says they use, in the business's voice, with the CTA and their handle or link:
   - Instagram / Facebook: 1–3 short lines, CTA, 3–6 relevant hashtags, music credit.
   - TikTok: one punchy line, CTA, 3–5 hashtags.
   - WhatsApp Status / broadcast: one line and the link or number, no hashtags.
   - X / LinkedIn when relevant.
6. `credits.txt`: the music credit (bundled tracks: `Music: Sascha Ende, ende.app (CC BY 4.0)`), "Sound effects: Kenney (CC0)" if used, the ElevenLabs voice name if the person wants it, and where each image came from.
7. Mark the phase `delivered`.

## Tell the person

Where the video, poster, captions and share copy are; the length, format and size; what the music credit is and that it must stay in the post; and how to change it (edit in the Studio, or tell Scorp1 what to change).
