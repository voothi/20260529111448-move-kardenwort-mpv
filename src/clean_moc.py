# -*- coding: utf-8 -*-
\"\"\"
ZID: 20260529131050
Author: Antigravity AI Coding Assistant
Description: Loops through all lines in the designated conversation file's MOC section,
             extracts the 14-digit ZID, cleans and normalizes the description into English
             (one phrase, ending with a period, no newlines, no special characters),
             and prepends it immediately after the ZID, keeping the original body text intact.
\"\"\"

import os
import re
import configparser
from pathlib import Path

def load_config():
    \"\"\"Loads the configuration from config.ini\"\"\"
    config = configparser.ConfigParser()
    config_path = Path(__file__).parent.parent / "config.ini"
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file config.ini not found at {config_path}. Please copy config.ini.template to config.ini.")
    config.read(config_path)
    return {
        "conversation_file": Path(config.get("MOC", "conversation_file")),
    }

def clean_description(desc):
    \"\"\"
    Cleans the given description to produce a single English phrase.
    Removes paths, urls, commands, non-ASCII characters (e.g., Cyrillic), 
    and special characters, and appends a single trailing period.
    \"\"\"
    # Remove URLs, slash commands, markdown/wikilinks, and paths
    desc = re.sub(r'https?://\S+', '', desc)
    desc = re.sub(r'/[a-zA-Z0-9_-]+', '', desc)
    desc = re.sub(r'\[.*?\]\(.*?\)', '', desc)
    desc = re.sub(r'\[\[.*?\]\]', '', desc)
    desc = re.sub(r'\[.*?\]', '', desc)
    desc = re.sub(r'[a-zA-Z]:\\\S+', '', desc)
    desc = re.sub(r'\bopsx-[a-z0-9_-]+\b', '', desc, flags=re.I)
    desc = re.sub(r'\bcreate-release-\d+\b', '', desc, flags=re.I)
    desc = re.sub(r'\b\d{14}(?:-[a-z0-9_-]+)?\b', '', desc, flags=re.I)
    desc = re.sub(r'\.?\S*\.(?:md|py|lua|txt|json|png|jpg|mp4)\b', '', desc, flags=re.I)
    
    # Remove Cyrillic characters/words entirely
    desc = re.sub(r'[\u0400-\u04FF]+', '', desc)
    
    # Get the first sentence by splitting on delimiters
    sentences = re.split(r'[.!?\n]', desc)
    first_sentence = ''
    for s in sentences:
        s = s.strip()
        if s:
            first_sentence = s
            break
            
    # Keep only English letters, numbers, and spaces
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', first_sentence)
    cleaned = ' '.join(cleaned.split()).strip()
    cleaned = re.sub(r'^[oxOX]\s+', '', cleaned)
    
    if not cleaned or len(cleaned) < 2:
        return 'Updated reference.'
    
    # Capitalize the first letter and add a period
    cleaned = cleaned[0].upper() + cleaned[1:] + '.'
    return cleaned

def main():
    try:
        cfg = load_config()
    except Exception as e:
        print(f"Configuration Error: {e}")
        return
        
    conversation_file = cfg["conversation_file"]
    if not conversation_file.exists():
        print(f"Target conversation file not found: {conversation_file}")
        return
        
    print(f"Reading and processing conversation file: {conversation_file}")
    with open(conversation_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    moc_started = False
    new_lines = []
    processed_count = 0
    
    for idx, line in enumerate(lines):
        if '## MOC.' in line:
            moc_started = True
            new_lines.append(line)
            continue
        elif moc_started and line.startswith('##'):
            moc_started = False
            new_lines.append(line)
            continue
            
        if moc_started and line.strip():
            parts = line.strip().split()
            # Check if line starts with a 14-digit ZID
            if parts and parts[0].isdigit() and len(parts[0]) == 14:
                zid = parts[0]
                rest = line.strip()[len(zid):].strip()
                cleaned = clean_description(rest)
                new_lines.append(f'{zid} {cleaned} {rest}\n')
                processed_count += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(conversation_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    print(f"Successfully processed {processed_count} ZID lines and updated {conversation_file}!")

if __name__ == '__main__':
    main()
