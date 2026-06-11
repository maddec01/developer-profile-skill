# Linear App Theme

A Linear.app-inspired dark theme for Zed.

The UI palette follows Linear's dark product aesthetic: dark app chrome, slightly lighter editor/content surfaces, subtle dividers, muted gray text, and a restrained purple/indigo accent. Syntax highlighting uses a quiet, theme-native palette with grays for secondary code and muted accent colors for structure:

| Token | Color |
| --- | --- |
| Text/variable | `#DADCE0` |
| Secondary syntax | `#AEB4BE` |
| Comment | `#7F8793` |
| Literal/string | `#89D196` |
| Function/method | `#FFDF9F` |
| Type/module/tag | `#9FAEFA` |
| Keyword/label/special | `#C89BE8` |
| Punctuation | `#A0A8B3` |

## Install locally

1. Open Zed's Extensions page.
2. Choose `Install Dev Extension`.
3. Select this `linear-zed-theme` directory.
4. Pick `Linear App Dark` from the theme selector.

## Publishing note

Before publishing this as a standalone Zed extension, move this directory into its own repository or update `repository` in `extension.toml` to the final public theme repository URL.
