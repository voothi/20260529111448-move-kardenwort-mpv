import os
import re
import configparser
from pathlib import Path

def load_config():
    config = configparser.ConfigParser()
    config_path = Path(__file__).parent.parent / "config.ini"
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file config.ini not found at {config_path}. Please copy config.ini.template to config.ini.")
    config.read(config_path)
    return {
        "dest_vault": Path(config.get("Vault", "dest_vault")),
    }

HIGH_RISK_PATTERNS = [
    re.compile(r'\b(pass(word)?|secret|token|api[_-]?key|private[_-]?key|cred(entials)?)\s*[:=]\s*["\'\w\-]{8,}', re.IGNORECASE),
    re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
    re.compile(r'\b(sk|AIza|ghp)_[a-zA-Z0-9]{15,}\b'),
]

def main():
    try:
        cfg = load_config()
    except Exception as e:
        print(f"Configuration Error: {e}")
        return
        
    project_dir = cfg["dest_vault"]
    
    if not project_dir.exists():
        print(f"Directory not found: {project_dir}")
        return
        
    print(f"Scanning vault: {project_dir}")
    findings = []
    
    for root, dirs, files in os.walk(project_dir):
        for f in files:
            if f.endswith('.md'):
                p = Path(root) / f
                try:
                    content = p.read_text(encoding='utf-8')
                    lines = content.splitlines()
                    for idx, line in enumerate(lines, 1):
                        for r in HIGH_RISK_PATTERNS:
                            matches = r.findall(line)
                            if matches:
                                findings.append((p.name, idx, line.strip()))
                except Exception as e:
                    print(f"Error reading {p}: {e}")
                    
    if findings:
        print(f"\n⚠️ High-risk details found ({len(findings)}):")
        for file, line_no, text in findings[:50]:
            print(f"  [{file}:{line_no}] -> {text}")
        if len(findings) > 50:
            print(f"  ... and {len(findings) - 50} more findings.")
    else:
        print("\n✅ Clean! No high-risk credentials, passwords, or personal details found.")

if __name__ == '__main__':
    main()
