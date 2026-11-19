#!/usr/bin/env python3
"""Report broken external (http/https) links in Markdown and HTML. Standard library only.

Relative links are already checked by validate_gazette.py on every push.
Run manually: python3 scripts/check_external_links.py [--timeout 10]
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
URL_RE = re.compile(r"https?://[^\s)\"'<>\]`]+")
SKIP = ("github.com/Parris-Tech-Services/RepublicOfParristan/pull/new",)

def collect():
    found = {}
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or path.suffix not in (".md", ".html"):
            continue
        for url in URL_RE.findall(path.read_text(encoding="utf-8", errors="replace")):
            url = url.rstrip(".,;:")
            if not url.startswith(SKIP):
                found.setdefault(url, set()).add(str(path.relative_to(ROOT)))
    return found

def check(url, timeout):
    headers = {"User-Agent": "parristan-link-check/1.0"}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if method == "GET" or e.code not in (403, 405, 501):
                return e.code
        except Exception as e:
            if method == "GET":
                return type(e).__name__
    return "unknown"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=float, default=10)
    args = ap.parse_args()
    links = collect()
    with ThreadPoolExecutor(8) as pool:
        results = dict(zip(links, pool.map(lambda u: check(u, args.timeout), links)))
    bad = {u: s for u, s in results.items() if not (isinstance(s, int) and s < 400)}
    for url, status in sorted(bad.items()):
        print(f"{status}\t{url}\t({', '.join(sorted(links[url]))})")
    print(f"Checked {len(links)} external links; {len(bad)} problems.")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
