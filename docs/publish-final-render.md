# Publish the original selected final PowerPortals render

The project owner confirms that the final rendered video, including the soundtrack they produced, may be publicly displayed. **Do not upload the WAV, MP3, or any standalone audio source file.** Only the completed MP4 with embedded music belongs in the public showcase.

## Exact file

- Private source repository: `RawPowered/powerportals-ai-design-process`
- Source branch: `codex/design-process`
- Original path: `media/versions/31.mp4`
- Intended public path: `media/versions/31.mp4`
- Original published metadata from the private process archive: 114 seconds, 1920 × 1080, 60 fps; approximately 15.4 MB.
- This is the selected final cut (stage 31), not the existing 28-second stage-04 introduction.

## Transfer the exact MP4 using GitHub's web interface

The connected GitHub read interface returned empty binary content for the larger MP4, so **the final file has not been copied by the assistant**. Avoid creating an empty placeholder file or pretending the upload succeeded.

1. Open the [private source video](https://github.com/RawPowered/powerportals-ai-design-process/blob/codex/design-process/media/versions/31.mp4) while signed into GitHub and download its original bytes.
2. Open [the public media/versions folder](https://github.com/RawPowered/power-portals-ai-video-presentation-showcase/tree/main/media/versions).
3. Use **Add file → Upload files**, choose the downloaded `31.mp4` and commit the upload to `main`.
4. Open the public MP4 after upload and check playback, audio, and that no private customer contact data is exposed.
5. After the public media file is verified, update the public site's home page to feature it as the primary video, with stage 04 retained as an early comparison.

**Optional, recommended:** Record the SHA-256 hash of the source video before upload and compare it with the downloaded published copy. Do not confuse a local SHA-256 checksum with Git's blob SHA-1.

## Why separate audio is excluded

The owner owns the music, but authorizes it here only as part of the synchronized audiovisual presentation. An embedded audio stream in a finished MP4 is allowed; separately downloadable WAV/MP3 masters are not. The public repository includes a GitHub Actions check to reject accidentally committed standalone audio files.

## Status

**Awaiting actual source-binary transfer:** No final-cut MP4 has been added as part of these instructions. The public repository currently contains the original 28-second stage-04 MP4 plus authentic video-derived GIFs and critique frames.

[Showcase](../index.html) · [Rights policy](../RIGHTS.md)
