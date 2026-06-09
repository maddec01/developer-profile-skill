# Linear App Theme

A Linear.app-inspired dark theme for Zed.

The UI palette follows Linear's dark product aesthetic: near-black surfaces, subtle borders, muted gray text, and the Linear purple/indigo accent. Syntax highlighting uses the public token colors exposed by Linear's Diffs illustration:

| Token | Color |
| --- | --- |
| Text | `#E2E4E7` |
| Comment | `#8B93A1` |
| String | `#FFDF9F` |
| Constant | `#8FA6FF` |
| Variable | `#F7BF8B` |
| Keyword | `#F79CE0` |
| Entity/function | `#83DCDC` |
| Punctuation | `#D2D7DE` |

## Install locally

1. Open Zed's Extensions page.
2. Choose `Install Dev Extension`.
3. Select this `linear-zed-theme` directory.
4. Pick `Linear App Dark` from the theme selector.

## Publishing note

Before publishing this as a standalone Zed extension, move this directory into its own repository or update `repository` in `extension.toml` to the final public theme repository URL.
