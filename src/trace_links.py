# -*- coding: utf-8 -*-
"""
ZID: 20260529150341
Author: Antigravity AI Coding Assistant
Description: Recursively traces Wikilinks from the specified root file in the vault
             to identify all connected files and detect any missing or unresolved links.
"""

import os
import re
import configparser
from pathlib import Path

def load_config():
    """Loads the configuration from config.ini"""
    config = configparser.ConfigParser()
    config_path = Path(__file__).parent.parent / "config.ini"
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file config.ini not found at {config_path}. Please copy config.ini.template to config.ini.")
    config.read(config_path)
    return {
        "source_vault": Path(config.get("Vault", "source_vault")),
        "root_file": Path(config.get("Vault", "root_file")),
    }

# Regular expression pattern to extract Obsidian Wikilinks
WIKILINK_RE = re.compile(r'\[\[([^\]|#\n]+)(?:#[^\]|\n]*)?(?:\|[^\]\n]*)?\]\]')

def load_vault(vault_dir):
    """Scans the vault directory and indexes files recursively"""
    print("Scanning vault...")
    all_files = {}
    for root, dirs, files in os.walk(vault_dir):
        for f in files:
            full_path = Path(root) / f
            name_lower = f.lower()
            all_files.setdefault(name_lower, []).append(full_path)
            ext = full_path.suffix
            if ext:
                name_no_ext = f[:-len(ext)].lower()
                all_files.setdefault(name_no_ext, []).append(full_path)
    print(f"Scanned {sum(len(v) for v in all_files.values())} files.")
    return all_files

def extract_links(file_path):
    """Extracts all targets from Wikilinks within a given markdown file"""
    links = []
    if not os.path.exists(file_path):
        return links
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return links
    
    for match in WIKILINK_RE.finditer(content):
        link_target = match.group(1).strip()
        link_target = link_target.strip('"\'')
        if link_target:
            links.append(link_target)
    return links

def resolve_link(link_name, all_files, vault_dir):
    """Resolves a Wikilink to one or more physical file paths in the vault"""
    link_lower = link_name.lower()
    if link_lower in all_files:
        return all_files[link_lower]
    
    parts = link_lower.replace('\\', '/').split('/')
    last_part = parts[-1]
    if last_part in all_files:
        matches = []
        for path in all_files[last_part]:
            path_parts = path.relative_to(vault_dir).as_posix().lower().split('/')
            if all(p in path_parts for p in parts):
                matches.append(path)
        if matches:
            return matches
    return []

def main():
    try:
        cfg = load_config()
    except Exception as e:
        print(f"Configuration Error: {e}")
        return
        
    vault_dir = cfg["source_vault"]
    root_file = cfg["root_file"]
    
    if not root_file.exists():
        print(f"Root file not found: {root_file}")
        return
        
    all_files = load_vault(vault_dir)
    
    to_visit = [root_file]
    visited = set([root_file.resolve()])
    missing_links = set()
    
    # Trace the link network
    idx = 0
    while idx < len(to_visit):
        curr_file = to_visit[idx]
        idx += 1
        
        if curr_file.suffix.lower() == '.md':
            links = extract_links(curr_file)
            for link in links:
                # Skip dates
                if re.match(r'^\d{4}-\d{2}-\d{2}$', link):
                    continue
                    
                resolved_paths = resolve_link(link, all_files, vault_dir)
                if not resolved_paths:
                    missing_links.add((curr_file.name, link))
                    continue
                    
                for path in resolved_paths:
                    resolved_abs = path.resolve()
                    if resolved_abs not in visited:
                        visited.add(resolved_abs)
                        to_visit.append(path)
                        
    print("\n--- Trace Results ---")
    print(f"Total files found in the project tree: {len(visited)}")
    for p in sorted(visited):
        rel = p.relative_to(vault_dir)
        print(f"  {rel}")
        
    if missing_links:
        print("\n--- Missing / Unresolved Links ---")
        for source, link in sorted(missing_links):
            print(f"  In '{source}': [[{link}]]")

if __name__ == '__main__':
    main()
