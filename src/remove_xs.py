# -*- coding: utf-8 -*-
"""
ZID: 20260529150742
Author: Antigravity AI Coding Assistant
Description: Recursively scans the target vault for files with 'x-x-x', 'x-x', 'x', or 'z-x' prefixes,
             renames them to remove the prefix from their filenames, cleans internal aliases and H1 headers,
             and updates all Wikilinks/references inside all markdown files in the vault.
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
        "dest_vault": Path(config.get("Vault", "dest_vault")),
    }

def main():
    try:
        cfg = load_config()
    except Exception as e:
        print(f"Configuration Error: {e}")
        return
        
    vault_dir = cfg["dest_vault"]
    if not vault_dir.exists():
        print(f"Target destination vault not found: {vault_dir}")
        return
        
    print(f"Scanning vault for X prefix files: {vault_dir}")
    rename_map = {}
    
    # 1. Discover all files to rename
    for root, dirs, files in os.walk(vault_dir):
        for f in files:
            if f.endswith('.md'):
                m = re.match(r'^(\d{14})-(x-x-x|x-x|x|z-x)-(.*)$', f, re.I)
                if m:
                    zid, prefix, rest = m.groups()
                    new_name = f'{zid}-{rest}'
                    old_path = os.path.join(root, f)
                    new_path = os.path.join(root, new_name)
                    rename_map[old_path] = (new_path, f[:-3], new_name[:-3])
                    
    if not rename_map:
        print("No files with X prefix pattern found.")
        return
        
    print(f"Found {len(rename_map)} files to rename.")
    
    # 2. Update content inside the files before/during renaming
    for old_path, (new_path, old_base, new_base) in rename_map.items():
        with open(old_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove prefixes from aliases and headers in YAML/Markdown H1
        content = re.sub(r'aliases:\s*\n\s*-\s*(?:X\s+x\s+x|X\s+x|x\s+x\s+x|x\s+x|x|X|z-x)\s+(.*)', r'aliases: \n  - \1', content, flags=re.I)
        content = re.sub(r'aliases:\s*\[\s*(?:X\s+x\s+x|X\s+x|x\s+x\s+x|x\s+x|x|X|z-x)\s+([^\]]+)\]', r'aliases: [\1]', content, flags=re.I)
        content = re.sub(r'^#\s+(?:X\s+x\s+x|X\s+x|x\s+x\s+x|x\s+x|x|X|z-x)\s+(.*)', r'# \1', content, flags=re.M | re.I)
        
        with open(new_path, 'w', encoding='utf-8') as file:
            file.write(content)
            
        os.remove(old_path)
        
    print("Renamed all files and updated their internal headers successfully!")
    
    # 3. Update all Wikilinks in all markdown files in the vault recursively
    base_map = {old_base: new_base for _, (_, old_base, new_base) in rename_map.items()}
    updated_files_count = 0
    links_updated_count = 0
    
    for root, dirs, files in os.walk(vault_dir):
        for f in files:
            if f.endswith('.md'):
                file_path = os.path.join(root, f)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                original_content = content
                
                def replace_link(match):
                    global links_updated_count
                    link_target = match.group(1).strip()
                    alias = match.group(2) if len(match.groups()) > 1 else None
                    
                    link_target_clean = link_target.split('#')[0]
                    section = link_target[len(link_target_clean):]
                    
                    if link_target_clean in base_map:
                        new_target = base_map[link_target_clean] + section
                        links_updated_count += 1
                        if alias:
                            new_alias = re.sub(r'^(?:X\s+x\s+x|X\s+x|x\s+x\s+x|x\s+x|x|X|z-x)\s+', '', alias.strip(), flags=re.I)
                            return f'[[{new_target}|{new_alias}]]'
                        else:
                            return f'[[{new_target}]]'
                    return match.group(0)
                
                content = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', replace_link, content)
                content = re.sub(r'\[\[([^\]|]+)\]\]', replace_link, content)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    updated_files_count += 1
                    
    print(f"Successfully updated {links_updated_count} links across {updated_files_count} markdown files!")

if __name__ == '__main__':
    main()
