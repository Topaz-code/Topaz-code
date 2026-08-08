#!/usr/bin/env python3
"""
Build the terminal-style profile UI and inject it into README.md
between the <!-- START_TERMINAL --> / <!-- END_TERMINAL --> markers.

It also fetches a fresh random fun fact each time it runs.

    python3 update_readme.py

To use your own photo instead of the placeholder avatar:
    python3 assets/ascii.py path/to/your-photo.jpg --invert --out assets/portrait.txt
    python3 update_readme.py
"""
import json
import re
import textwrap
import urllib.request

WIDTH = 72  # content width (matches the ASCII portrait width)

# --------------------------------------------------------------------------
# 1. Random fun fact of the day (kept from the original script)
# --------------------------------------------------------------------------
URL = "https://uselessfacts.jsph.pl/api/v2/facts/random"
try:
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as response:
        fun_fact = json.loads(response.read().decode()).get("text", "")
    if not fun_fact:
        raise ValueError("empty fact")
except Exception:
    fun_fact = "My script couldn't reach the API, but I am still awesome."


# --------------------------------------------------------------------------
# 2. Small helpers for building perfectly-aligned terminal lines
# --------------------------------------------------------------------------
def bar(filled, total=20, char="█"):
    """Return e.g. [██████████████████░░] for filled=18, total=20."""
    empty = total - filled
    return "[" + char * filled + "░" * empty + "]"


def skill(label, filled, total, pct):
    return f"  {label:<12}{bar(filled, total)} {pct}"


def line(content=""):
    """Wrap a content line with the window borders and pad to exact width."""
    return "│ " + content.ljust(WIDTH) + " │"


def divider(top=True):
    return ("┌" if top else "├") + "─" * (WIDTH + 2) + ("┐" if top else "┤")


# --------------------------------------------------------------------------
# 3. Assemble the terminal session
# --------------------------------------------------------------------------
portrait = open("assets/portrait.txt", encoding="utf-8").read().splitlines()

session = [
    "$ ./emmy --init",
    "Initializing profile for magaji-emmanuel...",
    bar(20) + " 100% modules loaded",
    "",
    *portrait,
    "",
    "$ whoami",
    "  Magaji Emmanuel — developer, dreamer, professional doer-of-nothing",
    "",
    "$ cat ~/favorites.txt",
    "  01. favorite activity : nothing",
    "  02. favorite song     : The Queen and the Poet",
    "",
    "$ ls ~/skills",
    "  VS Code · Antigravity · Arena · Python · HTML/CSS · TypeScript · Laziness",
    "",
    "$ ./skill-meter.sh",
    skill("Python", 18, 20, "90%"),
    skill("TypeScript", 18, 20, "90%"),
    skill("HTML/CSS", 17, 20, "85%"),
    skill("VS Code", 20, 20, "100%"),
    skill("Antigravity", 16, 20, "80%"),
    skill("Arena", 20, 20, "100%"),
    skill("Laziness", 24, 24, "∞"),
    "",
    "$ cat ~/hobbies.txt",
    "  gaming · music · trying new things · LLMs · learning · sleeping",
    "",
    "$ git shortlog -sne",
    "     1  Arena.ai Agent <arena-ai>",
    "",
    "$ curl -s https://emmyrabs.vercel.app",
    "  [200 OK] -> my little corner of the internet",
    "",
    "$ cat ~/fact_of_the_day.txt",
    *[f"  {f}" for f in textwrap.wrap(fun_fact, WIDTH - 4)],
    "",
    "$ ./today.sh",
    "  [x] wake up",
    "  [x] think about coding",
    "  [ ] actually code",
    "  [ ] do nothing (expert level)",
    "",
    "$ █",
]

window = [
    divider(),
    line("● ● ●   magaji@topaz-code: ~ (zsh)"),
    divider(top=False),
    *[line(s) for s in session],
    "└" + "─" * (WIDTH + 2) + "┘",
]

terminal_ui = "```\n" + "\n".join(window) + "\n```"

# --------------------------------------------------------------------------
# 4. Inject into README.md between the hidden markers
# --------------------------------------------------------------------------
with open("README.md", "r", encoding="utf-8") as file:
    readme_content = file.read()

pattern = r"(?<=<!-- START_TERMINAL -->\n)[\s\S]*(?=\n<!-- END_TERMINAL -->)"
if re.search(pattern, readme_content):
    readme_content = re.sub(pattern, terminal_ui, readme_content)
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)
    print("README.md successfully updated!")
else:
    print("Could not find the START_TERMINAL/END_TERMINAL markers in README.md")
