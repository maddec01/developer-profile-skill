# Linear App Theme

A Linear.app-inspired dark theme for Zed.

The UI palette follows Linear's dark product aesthetic: dark app chrome, slightly lighter editor/content surfaces, subtle dividers, muted gray text, and a restrained purple/indigo accent. Syntax highlighting uses a quiet, theme-native palette with grays for secondary code and muted accent colors for structure:

| Token group | Color |
| --- | --- |
| Variables/text | `#DADCE0` |
| Parameters | `#D2D7DE` |
| Functions/methods/titles | `#FFDF9F` |
| Types/modules/tags | `#9FAEFA` |
| Literals/strings/constants | `#89D196` |
| Keywords/labels/special vars | `#C89BE8` |
| Properties/attributes/links | `#DADCE0` / `#D2D7DE` |
| Operators/brackets | `#AEB4BE` |
| Punctuation/delimiters | `#A0A8B3` / `#8B93A1` |
| Comments | `#7F8793` |

## Install locally

1. Open Zed's Extensions page.
2. Choose `Install Dev Extension`.
3. Select this `linear-zed-theme` directory.
4. Pick `Linear App Dark` from the theme selector.

## Publishing note

Before publishing this as a standalone Zed extension, move this directory into its own repository or update `repository` in `extension.toml` to the final public theme repository URL.
