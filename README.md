# Move Kardenwort MPV Vault Utility

[![Version](https://img.shields.io/badge/version-v1.2.0-blue)](https://github.com/voothi/20260529111448-move-kardenwort-mpv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A focused, highly efficient utility tool designed to extract and move all files (notes and image/media assets) belonging to a specific subproject from a larger Obsidian vault into a clean, standalone, independent vault directory based on recursive Wikilink traversal.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Kardenwort Ecosystem](#kardenwort-ecosystem)
- [Signature](#signature)
- [License](#license)

---

## Description
When working inside a massive Obsidian vault (such as `U:\voothi.vault\voothi`), subprojects can easily become scattered across various folders. This utility solves this by starting at the root Map of Content (MOC) file of a project (e.g. `20260429111108-kardenwort-mpv.md`), scanning it recursively for all nested `[[Wikilinks]]`, and collecting all related markdown notes and media assets into a flat, highly navigable independent vault.

[Return to Top](#move-kardenwort-mpv-vault-utility)

## Features
- **Recursive Wikilink Graph Traversal**: Automatically finds all direct and indirect document dependencies starting from the root note.
- **Asset Relocation**: Detects linked `.png`, `.jpg`, and other media files in your notes and relocates them into a designated assets subfolder.
- **Journal Filter Safety**: Intentionally skips standard daily notes matching `YYYY-MM-DD` patterns to prevent pulling in the main journal timelines.
- **MOC Cleaner / Formatter**: Loops through MOC listings to generate and prepend clean, alphanumeric English-only descriptions to all ZID lines while preserving original body content.
- **X Prefix and Alias Cleanup**: Scans the relocated vault to recursively rename files, strip `X` patterns from titles/aliases, and automatically update all internal Wikilinks/references.
- **Security Scanner**: Includes an audit tool to automatically scan the newly generated vault for potential passwords, private API keys, or sensitive personal credentials.

[Return to Top](#move-kardenwort-mpv-vault-utility)

## Project Structure
```text
20260529111448-move-kardenwort-mpv/
├── config.ini               # Active settings (vault paths, root file, and outputs)
├── config.ini.template      # Settings template for clean configuration
├── .gitignore               # Excludes python caches and local configs
├── README.md                # Documentation and setup instructions
├── src/                     # Source directory containing utilities
│   ├── trace_links.py       # Dry-run graph scanning and missing link detection
│   ├── move_vault.py        # Relocates notes and assets to the destination vault
│   ├── check_sensitive.py   # Scans relocated vault for potential PII or passwords
│   ├── clean_moc.py         # Standardizes and prepends descriptions to MOC ZID lines
│   └── remove_xs.py         # Renames notes, cleans X prefixes in aliases/headers, and rewrites Wikilinks
```

[Return to Top](#move-kardenwort-mpv-vault-utility)

## Configuration

Configuring the utility is simple via the `config.ini` file located at the root of the project.

### Default `config.ini`
```ini
[Vault]
# Path to the source Obsidian vault
source_vault = U:\voothi.vault\voothi

# Relative path or absolute path to the root note of the subproject MOC
root_file = U:\voothi.vault\voothi\journal\daily\20260429111108-kardenwort-mpv.md

# Path to the target new vault directory
dest_vault = U:\voothi.vault\kardenwort-mpv

# Subfolder inside dest_vault where all media assets/images will be placed
assets_subfolder = assets

[MOC]
# Path to the conversation file to format/clean MOC lines
conversation_file = U:\voothi.vault\kardenwort-mpv\conversations\20260529011639-conversation.md
```

[Return to Top](#move-kardenwort-mpv-vault-utility)

## Usage

### 1. Dry Run / Trace Links
Analyze the project boundaries and check for any unresolved references or missing assets without making any changes to your files:
```powershell
python src/trace_links.py
```

### 2. Execute Vault Extraction
Perform the migration. This will move all identified markdown notes to the root of the destination vault and assets into the assets directory:
```powershell
python src/move_vault.py
```

### 3. Scan Vault for Credentials
Ensure that your new vault does not contain any passwords, private tokens, or personal identifiers before sharing it publicly:
```powershell
python src/check_sensitive.py
```

### 4. Clean and Format MOC
Cleans, standardizes, and prepends short, English-only descriptions to all ZID lines under the MOC section of your conversation file:
```powershell
python src/clean_moc.py
```

### 5. Remove X Prefixes and Clean Headers
Automatically renames all notes containing `x-x-x-`, `x-x-`, or `x-` prefixes in the isolated vault, updates their aliases and H1 headers, and rewrites all internal Wikilinks recursively to point to the clean targets:
```powershell
python src/remove_xs.py
```

[Return to Top](#move-kardenwort-mpv-vault-utility)

## Kardenwort Ecosystem
This utility is part of the **[Kardenwort](https://github.com/kardenwort)** environment, designed to manage sub-components, documentation, and standalone vault assets efficiently.

[Return to Top](#move-kardenwort-mpv-vault-utility)

## Signature
- **Project Anchor ZID**: `20260529150742`
- **Signatory**: Antigravity AI Coding Assistant

[Return to Top](#move-kardenwort-mpv-vault-utility)

## License
MIT License. See LICENSE file for details.
