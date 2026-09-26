#!/usr/bin/env python3
"""
Generates the static ja/en pages from template.html + i18n/*.json.
Usage: python3 build.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PLACEHOLDER_RE = re.compile(r"\{\{\s*([\w.]+)\s*\}\}")

AUTO_GENERATED_NOTICE = (
    "<!-- This file is auto-generated from template.html + i18n/*.json.\n"
    "     Edit those source files and run `python3 build.py` to regenerate. -->\n"
)

LOCALES = [
    {"code": "ja", "file": "i18n/ja.json", "out_file": "index.html", "asset_prefix": ""},
    {"code": "en", "file": "i18n/en.json", "out_file": "en/index.html", "asset_prefix": "../"},
]


def read_json(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def get(context, dotted_path):
    value = context
    for key in dotted_path.split("."):
        if not isinstance(value, dict) or key not in value:
            raise KeyError(f'Missing template value for "{dotted_path}"')
        value = value[key]
    return value


def render(template, context):
    def replace(match):
        return str(get(context, match.group(1)))

    return PLACEHOLDER_RE.sub(replace, template)


def main():
    common = read_json("i18n/common.json")
    template = (ROOT / "template.html").read_text(encoding="utf-8")

    for locale in LOCALES:
        t = read_json(locale["file"])
        is_ja = locale["code"] == "ja"

        context = {
            "t": t,
            "common": common,
            "asset": {
                "css": f"{locale['asset_prefix']}css/style.css",
                "js": f"{locale['asset_prefix']}js/script.js",
            },
            "navLang": {
                "enCurrentClass": "" if is_ja else " is-current",
                "enCurrentAttr": "" if is_ja else ' aria-current="page"',
                "jaCurrentClass": " is-current" if is_ja else "",
                "jaCurrentAttr": ' aria-current="page"' if is_ja else "",
            },
        }

        html = AUTO_GENERATED_NOTICE + render(template, context)
        out_path = ROOT / locale["out_file"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"built {locale['out_file']}")


if __name__ == "__main__":
    main()
