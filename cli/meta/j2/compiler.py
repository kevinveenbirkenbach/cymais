#!/usr/bin/env python3
import argparse
import os
import re
import sys

# Projekt-Root: vier Ebenen über diesem File
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

INCLUDE_RE = re.compile(r"^(\s*)\{%\s*include\s*['\"]([^'\"]+)['\"]\s*%\}")

def expand_includes(rel_path, seen=None):
    """
    Liest die Datei rel_path (relative zum PROJECT_ROOT),
    ersetzt rekursiv alle "{% include 'path' %}"-Zeilen durch den
    Inhalt der jeweiligen Datei (mit gleicher Einrückung).
    """
    if seen is None:
        seen = set()
    rp = rel_path.replace("\\", "/")
    if rp in seen:
        raise RuntimeError(f"Circular include detected: {rp}")
    seen.add(rp)

    abs_path = os.path.join(PROJECT_ROOT, rp)
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"Template not found: {rp}")

    output_lines = []
    for line in open(abs_path, encoding="utf-8"):
        m = INCLUDE_RE.match(line)
        if not m:
            output_lines.append(line.rstrip("\n"))
        else:
            indent, inc_rel = m.group(1), m.group(2)
            # rekursiver Aufruf
            for inc_line in expand_includes(inc_rel, seen):
                output_lines.append(indent + inc_line)
    seen.remove(rp)
    return output_lines

def parse_args():
    p = argparse.ArgumentParser(
        description="Expand all {% include '...' %} directives in a Jinja2 template (no variable rendering)."
    )
    p.add_argument("template", help="Template path relative to project root")
    p.add_argument(
        "--out",
        help="If given, write output to this file instead of stdout",
        default=None
    )
    return p.parse_args()

def main():
    args = parse_args()

    try:
        lines = expand_includes(args.template)
        text = "\n".join(lines)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(text + "\n")
        else:
            print(text)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
