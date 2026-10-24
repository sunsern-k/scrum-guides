#!/usr/bin/env python3
"""Build the root revisit.html page from the local knowledge files."""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
KNOWLEDGE = ROOT / ".cursor/skills/psm-i-coach/knowledge"
OUT = ROOT / "revisit.html"

TOPIC_TITLES = {
    "01": "Empiricism",
    "02": "Scrum Values",
    "03": "Scrum Team",
    "04": "Events",
    "05": "Artifacts",
    "06": "Done",
    "07": "Self-Managing Teams",
    "08": "Facilitation",
    "09": "Coaching",
    "10": "Product Value",
    "11": "Product Backlog Management",
    "12": "Stakeholders & Customers",
}


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def parse_entities(text: str) -> list[dict]:
    entities = []
    for part in re.split(r"\n## ", text)[1:]:
        lines = part.splitlines()
        fields: dict[str, str] = {}
        for line in lines[1:]:
            match = re.match(r"- ([^:]+): (.*)", line)
            if match:
                fields[match.group(1)] = match.group(2).strip()
        entities.append({"name": lines[0].strip(), "fields": fields})
    return entities


def parse_topic(text: str) -> dict:
    lines = text.splitlines()
    meta: dict[str, str] = {}
    sections: dict[str, str] = {}
    current = None
    buf: list[str] = []

    def flush() -> None:
        if current:
            sections[current] = "\n".join(buf).strip()

    for line in lines[1:]:
        if line.startswith("## "):
            flush()
            current = line[3:].strip()
            buf = []
        elif current is None and line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            meta[key] = value.strip()
        elif current is not None:
            buf.append(line)
    flush()
    return {"title": lines[0][2:].strip(), "meta": meta, "sections": sections}


def parse_relationships(text: str) -> list[dict]:
    groups: list[dict] = []
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = {"title": line[3:].strip(), "edges": []}
            groups.append(current)
            continue
        if current is None or not line.startswith("- R"):
            continue
        parts = [part.strip() for part in line[2:].split(" | ")]
        if len(parts) < 6:
            continue
        topics = parts[4].removeprefix("topics=")
        current["edges"].append(
            {
                "id": parts[0],
                "from": parts[1],
                "relation": parts[2],
                "to": parts[3],
                "topics": [item.strip() for item in topics.split(",") if item.strip()],
                "basis": parts[5],
            }
        )
    return groups


def make_linkify(names: list[str], skip: set[str] | None = None):
    skip = skip or set()
    ordered = sorted(names, key=len, reverse=True)
    pattern = re.compile(
        r"\b(" + "|".join(re.escape(name) for name in ordered) + r")\b",
        re.IGNORECASE,
    )
    canonical = {name.lower(): name for name in names}

    def linkify(text: str) -> str:
        escaped = html.escape(text)

        def replace(match: re.Match) -> str:
            raw = match.group(1)
            name = canonical[raw.lower()]
            if name in skip:
                return raw
            return f'<a href="#entity-{slug(name)}">{raw}</a>'

        return pattern.sub(replace, escaped)

    return linkify


def render_blocks(text: str, linkify) -> str:
    if not text.strip():
        return ""
    chunks = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if lines and all(line.startswith("- ") for line in lines):
            items = "".join(f"<li>{linkify(line[2:])}</li>" for line in lines)
            chunks.append(f"<ul>{items}</ul>")
        else:
            chunks.append(f"<p>{linkify(' '.join(lines))}</p>")
    return "\n".join(chunks)


def topic_links(numbers: list[str]) -> str:
    links = []
    for number in numbers:
        title = TOPIC_TITLES.get(number, number)
        links.append(f'<a href="#topic-{number}">{html.escape(title)}</a>')
    return ", ".join(links)


CSS = """
:root {
  color-scheme: light;
  --bg: #f3f5f7;
  --paper: #ffffff;
  --ink: #1b2836;
  --muted: #3e4c5a;
  --line: #d5dee6;
  --accent: #0c4f5c;
  --accent-soft: #e5f2f4;
  --header: #12323a;
  --header-ink: #f7fbfb;
  --trap: #f8f4ec;
  --aside: #e7eef1;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
}
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
  font-size: 1.0625rem;
  line-height: 1.65;
}
a { color: var(--accent); }
a:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.skip {
  position: absolute;
  left: 0.75rem;
  top: -3rem;
  background: white;
  padding: 0.4rem 0.7rem;
  z-index: 20;
}
.skip:focus { top: 0.5rem; }
header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: var(--header);
  color: var(--header-ink);
}
.header-inner {
  max-width: 68rem;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.8rem 1.25rem;
}
.brand {
  color: var(--header-ink);
  font-weight: 600;
  text-decoration: none;
  letter-spacing: 0.01em;
}
header nav { display: flex; gap: 1.1rem; }
header nav a {
  color: var(--header-ink);
  text-decoration: none;
  font-size: 0.98rem;
}
header nav a:hover { text-decoration: underline; text-underline-offset: 0.2em; }
.layout {
  max-width: 68rem;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 17.5rem minmax(0, 1fr);
  gap: 2rem;
  padding: 1.5rem 1.25rem 3.5rem;
}
aside {
  position: sticky;
  top: 4.1rem;
  align-self: start;
  max-height: calc(100vh - 5rem);
  overflow: auto;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 0.85rem 0.7rem;
}
.aside-label {
  margin: 0.15rem 0.45rem 0.45rem;
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.toc a {
  display: grid;
  grid-template-columns: 1.6rem 1fr;
  gap: 0.35rem;
  padding: 0.32rem 0.45rem;
  border-radius: 6px;
  color: var(--ink);
  text-decoration: none;
  font-size: 0.95rem;
}
.toc a:hover { background: var(--accent-soft); }
.toc .num { color: var(--muted); font-variant-numeric: tabular-nums; }
main { min-width: 0; overflow-wrap: break-word; }
.panel {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 1.4rem 1.4rem 0.6rem;
  margin-bottom: 1.25rem;
}
h1, h2, h3 { line-height: 1.25; font-weight: 600; }
#topics, #entities, #relationships { scroll-margin-top: 4.75rem; }
h1 { font-size: 1.8rem; margin: 0 0 0.55rem; }
h2 { font-size: 1.45rem; margin: 0 0 0.7rem; scroll-margin-top: 4.6rem; }
h3 { font-size: 1.08rem; margin: 1.15rem 0 0.35rem; scroll-margin-top: 4.6rem; }
.lede { margin: 0 0 1rem; color: var(--muted); }
.prose a { text-decoration-thickness: 1px; text-underline-offset: 0.16em; }
.prose p { margin: 0.65rem 0; }
.prose ul { margin: 0.4rem 0 0.8rem; padding-left: 1.2rem; }
.prose li { margin: 0.38rem 0; }
.topic { padding: 0.3rem 0 1.3rem; border-top: 1px solid var(--line); scroll-margin-top: 4.4rem; }
.kicker {
  margin: 1rem 0 0.25rem;
  color: var(--accent);
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.03em;
}
.callout { margin: 1rem 0; padding: 0.85rem 1rem 0.95rem; border-radius: 8px; }
.trap { background: var(--trap); }
.not-this { background: var(--aside); }
.callout h3 { margin-top: 0; }
.pager {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  margin: 1rem 0 0.4rem;
}
.pager a {
  text-decoration: none;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 0.45rem 0.75rem;
  font-weight: 600;
  background: var(--bg);
}
.pager a:hover { background: var(--accent-soft); }
.entity, .edge { padding: 0.95rem 0 1rem; border-top: 1px solid var(--line); scroll-margin-top: 4.6rem; }
.entity h3, .edge h3 { margin-top: 0; }
.quote {
  margin: 0.75rem 0;
  padding: 0.15rem 0 0.15rem 0.85rem;
  border-left: 3px solid var(--accent);
}
.meta { margin: 0.55rem 0 0; color: var(--muted); font-size: 0.95rem; }
.edge-id {
  margin: 0;
  font-family: ui-monospace, Consolas, monospace;
  font-size: 0.78rem;
  color: var(--muted);
}
.edge-rel { margin: 0.12rem 0; font-weight: 600; }
.group-title { margin-top: 1.6rem; }
.diagram-scroll {
  overflow-x: auto;
  margin: 0.75rem 0 1rem;
  padding: 0.75rem;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: var(--bg);
}
.diagram-scroll svg { display: block; }
.diagram-scroll text {
  font-family: "Segoe UI", system-ui, sans-serif;
  font-size: 15px;
}
.diagram-scroll a { fill: var(--accent); }
footer {
  max-width: 68rem;
  margin: 0 auto;
  padding: 0 1.25rem 2.5rem;
  color: var(--muted);
  font-size: 0.95rem;
}
@media (max-width: 800px) {
  .header-inner {
    flex-direction: column;
    align-items: stretch;
    gap: 0.35rem;
    padding: 0.65rem 0.9rem 0.7rem;
  }
  .brand { white-space: nowrap; }
  header nav { gap: 0.85rem; }
  .layout { grid-template-columns: 1fr; gap: 0.9rem; }
  aside {
    position: sticky;
    top: 5.5rem;
    max-height: none;
    overflow: auto;
  }
  h2, h3, .topic, .entity, .edge, #topics, #entities, #relationships { scroll-margin-top: 14rem; }
  .toc { display: flex; gap: 0.25rem; }
  .toc a { white-space: nowrap; }
  .pager { flex-direction: column; }
}
"""

# Highlight the topic currently in the URL hash.
for number in TOPIC_TITLES:
    CSS += (
        f"body:has(#topic-{number}:target) .toc a[href=\"#topic-{number}\"] "
        "{ background: var(--accent-soft); color: var(--accent); font-weight: 600; }\n"
    )


def wrap_words(text: str, limit: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if len(trial) <= limit:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def svg_box(x: float, y: float, w: float, h: float, lines: list[str], linkify, fill: str = "var(--paper)") -> str:
    texts = []
    for index, line in enumerate(lines):
        texts.append(
            f'<text x="{x + w / 2}" y="{y + 26 + index * 22}" text-anchor="middle" fill="var(--ink)">{linkify(line)}</text>'
        )
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="var(--line)"/>'
        + "".join(texts)
    )


def box_height(line_count: int) -> int:
    return 18 + line_count * 22 + 12


def edge_diagram(edges: list[dict], linkify, label: str) -> str:
    if not edges:
        return ""
    width = 520
    y = 16
    parts: list[str] = []
    for edge in edges:
        from_lines = wrap_words(edge["from"], 42)
        rel_lines = wrap_words(edge["relation"], 36)
        to_lines = wrap_words(edge["to"], 42)
        from_h = box_height(len(from_lines))
        to_h = box_height(len(to_lines))
        rel_h = max(36, 16 + len(rel_lines) * 20)
        parts.append(svg_box(16, y, 488, from_h, from_lines, linkify))
        y += from_h
        arrow_bottom = y + rel_h - 8
        parts.append(
            f'<line x1="48" y1="{y + 2}" x2="48" y2="{arrow_bottom - 6}" stroke="var(--accent)" stroke-width="1.5"/>'
            f'<polygon points="48,{arrow_bottom} 43,{arrow_bottom - 8} 53,{arrow_bottom - 8}" fill="var(--accent)"/>'
        )
        for index, line in enumerate(rel_lines):
            parts.append(
                f'<text x="64" y="{y + 20 + index * 20}" fill="var(--accent)" font-size="13">{html.escape(line)}</text>'
            )
        y += rel_h
        parts.append(svg_box(16, y, 488, to_h, to_lines, linkify, "var(--accent-soft)"))
        y += to_h + 22
    height = y + 4
    body = "".join(parts)
    return (
        f'<figure class="diagram-scroll"><svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(label)}">{body}</svg></figure>'
    )


def sprint_svg(linkify) -> str:
    events = [
        ("Sprint Planning", "Why, What, How", "8 hours"),
        ("Daily Scrum", "Sprint Goal", "15 minutes"),
        ("Sprint Review", "Stakeholders", "4 hours"),
        ("Retrospective", "Done and quality", "3 hours"),
    ]
    parts = [
        '<rect x="8" y="8" width="504" height="300" rx="8" fill="none" stroke="var(--accent)" stroke-width="1.5"/>',
        '<text x="24" y="34" fill="var(--accent)" font-size="16" font-weight="600">Sprint</text>',
        '<text x="84" y="34" fill="var(--muted)" font-size="13">one month or less · contains the other events</text>',
    ]
    for index, (title, note, time) in enumerate(events):
        column = index % 2
        row = index // 2
        parts.append(svg_box(20 + column * 246, 48 + row * 108, 234, 96, [title, note, time], linkify))
    parts.append(
        '<text x="260" y="274" text-anchor="middle" fill="var(--muted)" font-size="13">'
        "Only the Product Owner cancels a Sprint,"
        "</text>"
        '<text x="260" y="294" text-anchor="middle" fill="var(--muted)" font-size="13">'
        "and only if the Sprint Goal is obsolete."
        "</text>"
    )
    body = "".join(parts)
    return (
        '<figure class="diagram-scroll"><svg xmlns="http://www.w3.org/2000/svg" width="520" height="316" '
        'viewBox="0 0 520 316" role="img" aria-label="Sprint containing four events">'
        f"{body}</svg></figure>"
    )


def framework_svg(linkify) -> str:
    parts: list[str] = []
    y = 12

    def add_box(lines: list[str], fill: str = "var(--paper)") -> None:
        nonlocal y
        height = box_height(len(lines))
        parts.append(svg_box(16, y, 488, height, lines, linkify, fill))
        y += height

    def add_arrow(label: str) -> None:
        nonlocal y
        rel_h = 36
        arrow_bottom = y + rel_h - 8
        parts.append(
            f'<line x1="48" y1="{y + 2}" x2="48" y2="{arrow_bottom - 6}" stroke="var(--accent)" stroke-width="1.5"/>'
            f'<polygon points="48,{arrow_bottom} 43,{arrow_bottom - 8} 53,{arrow_bottom - 8}" fill="var(--accent)"/>'
            f'<text x="64" y="{y + 22}" fill="var(--accent)" font-size="13">{html.escape(label)}</text>'
        )
        y += rel_h

    add_box(["Transparency", "Work is visible"])
    add_arrow("enables")
    add_box(["Inspection", "Events set the cadence"], "var(--accent-soft)")
    add_arrow("enables")
    add_box(["Adaptation", "As soon as you learn"])
    y += 16
    parts.append(f'<rect x="16" y="{y}" width="488" height="44" rx="8" fill="var(--accent-soft)" stroke="var(--line)"/>')
    parts.append(
        f'<text x="260" y="{y + 28}" text-anchor="middle" fill="var(--ink)">{linkify("Commitment · Focus · Openness · Respect · Courage")}</text>'
    )
    y += 60
    team_top = y
    parts.append('<text x="32" y="' + str(y + 24) + '" fill="var(--ink)" font-size="15" font-weight="600">Scrum Team</text>')
    parts.append(
        f'<text x="492" y="{y + 24}" text-anchor="end" fill="var(--muted)" font-size="12">Self-managing · 10 or fewer</text>'
    )
    y += 36
    for lines in (
        ["Product Owner", "Maximizes value. Orders the backlog."],
        ["Scrum Master", "Establishes Scrum. Timeboxes events."],
        ["Developers", "Own the Sprint plan. Conform to Done."],
    ):
        add_box(lines, "var(--accent-soft)")
        y += 8
    parts.append(
        f'<rect x="16" y="{team_top}" width="488" height="{y - team_top}" rx="8" fill="none" stroke="var(--line)"/>'
    )
    y += 16
    sprint_top = y
    parts.append(f'<text x="32" y="{y + 24}" fill="var(--accent)" font-size="15" font-weight="600">Sprint</text>')
    parts.append(
        f'<text x="88" y="{y + 24}" fill="var(--muted)" font-size="12">one month or less · contains the other events</text>'
    )
    y += 36
    events = [
        ("Sprint Planning", "Why, What, How", "8 hours"),
        ("Daily Scrum", "15 minutes", "Developers"),
        ("Sprint Review", "Stakeholders", "4 hours"),
        ("Retrospective", "Closes the Sprint", "3 hours"),
    ]
    for index, lines in enumerate(events):
        column = index % 2
        row = index // 2
        parts.append(svg_box(28 + column * 236, y + row * 104, 224, 96, list(lines), linkify))
    y += 208
    parts.append(
        f'<text x="260" y="{y + 8}" text-anchor="middle" fill="var(--muted)" font-size="13">Only the Product Owner cancels a Sprint,</text>'
        f'<text x="260" y="{y + 28}" text-anchor="middle" fill="var(--muted)" font-size="13">and only if the Sprint Goal is obsolete.</text>'
    )
    y += 40
    parts.append(
        f'<rect x="16" y="{sprint_top}" width="488" height="{y - sprint_top}" rx="8" fill="none" stroke="var(--accent)" stroke-width="1.5"/>'
    )
    y += 20
    for artifact, commitment, note in (
        ("Product Backlog", "Product Goal", "One long-term objective"),
        ("Sprint Backlog", "Sprint Goal", "Flexible scope"),
        ("Increment", "Definition of Done", "Must be usable"),
    ):
        add_box([artifact])
        add_arrow("commitment")
        add_box([commitment], "var(--accent-soft)")
        parts.append(f'<text x="260" y="{y + 18}" text-anchor="middle" fill="var(--muted)" font-size="13">{html.escape(note)}</text>')
        y += 36
    body = "".join(parts)
    return (
        f'<figure class="diagram-scroll"><svg xmlns="http://www.w3.org/2000/svg" width="520" height="{y + 8}" '
        f'viewBox="0 0 520 {y + 8}" role="img" aria-label="Scrum framework map of pillars, team, Sprint, and commitments">'
        f"{body}</svg></figure>"
    )


def main() -> None:
    entities = parse_entities((KNOWLEDGE / "entities.md").read_text())
    names = [entity["name"] for entity in entities]
    topics = []
    for path in sorted((KNOWLEDGE / "topics").glob("*.md")):
        number = path.name[:2]
        topic = parse_topic(path.read_text())
        topic["number"] = number
        topic["file"] = path.name
        topics.append(topic)
    groups = parse_relationships((KNOWLEDGE / "relationships.md").read_text())
    linkify = make_linkify(names)

    toc = []
    topic_html = []
    for index, topic in enumerate(topics):
        number = topic["number"]
        label = TOPIC_TITLES[number]
        toc.append(
            f'<a href="#topic-{number}"><span class="num">{number}</span>'
            f"<span>{html.escape(label)}</span></a>"
        )
        parts = [
            f'<article class="topic" id="topic-{number}">',
            f'<p class="kicker">Topic {int(number)} of 12</p>',
            f"<h2>{html.escape(label)}</h2>",
        ]
        topic_edges = [
            edge
            for group in groups
            for edge in group["edges"]
            if number in edge["topics"]
        ]
        for section in ("Guide sense", "Entities", "Relationships"):
            body = topic["sections"].get(section, "")
            parts.append(f"<h3>{html.escape(section)}</h3>")
            if section == "Relationships":
                if number == "04":
                    parts.append(sprint_svg(linkify))
                parts.append(edge_diagram(topic_edges, linkify, f"{label} relationships"))
            parts.append(render_blocks(body, linkify))
        for section, css in (("Exam trap", "trap"), ("Not this", "not-this")):
            body = topic["sections"].get(section, "")
            parts.append(f'<div class="callout {css}"><h3>{html.escape(section)}</h3>')
            parts.append(render_blocks(body, linkify))
            parts.append("</div>")
        pager = ['<nav class="pager" aria-label="Topic order">']
        if index > 0:
            prev = topics[index - 1]
            pager.append(
                f'<a href="#topic-{prev["number"]}">Previous: {html.escape(TOPIC_TITLES[prev["number"]])}</a>'
            )
        else:
            pager.append("<span></span>")
        if index < len(topics) - 1:
            nxt = topics[index + 1]
            pager.append(
                f'<a href="#topic-{nxt["number"]}">Next: {html.escape(TOPIC_TITLES[nxt["number"]])}</a>'
            )
        else:
            pager.append('<a href="#entities">Next: Entity definitions</a>')
        pager.append("</nav></article>")
        parts.extend(pager)
        topic_html.append("\n".join(parts))

    entity_html = []
    for entity in entities:
        own = make_linkify(names, {entity["name"]})
        fields = entity["fields"]
        numbers = [item.strip() for item in fields.get("Topics", "").split(",") if item.strip()]
        entity_html.append(
            f'<article class="entity" id="entity-{slug(entity["name"])}">'
            f"<h3>{html.escape(entity['name'])}</h3>"
            f"<p>{own(fields.get('Sense', ''))}</p>"
        )
        if fields.get("Guide"):
            entity_html.append(f'<p class="quote">{own(fields["Guide"])}</p>')
        if fields.get("Not this"):
            entity_html.append(f'<p><strong>Not this.</strong> {own(fields["Not this"])}</p>')
        entity_html.append(f'<p class="meta">Used in {topic_links(numbers)}</p></article>')

    relation_html = []
    for group in groups:
        relation_html.append(f'<h3 class="group-title">{html.escape(group["title"])}</h3>')
        for edge in group["edges"]:
            relation_html.append(
                f'<article class="edge" id="edge-{edge["id"].lower()}">'
                f'<p class="edge-id">{html.escape(edge["id"])}</p>'
                f'<p class="edge-rel">{linkify(edge["from"])} {linkify(edge["relation"])} '
                f'{linkify(edge["to"])}</p>'
                f'<p>{linkify(edge["basis"])}</p>'
                f'<p class="meta">Topics: {topic_links(edge["topics"])}</p>'
                "</article>"
            )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PSM I revisit — key topics, entities, and relationships</title>
  <style>
{CSS}
  </style>
</head>
<body>
  <a class="skip" href="#topics">Skip to topics</a>
  <header>
    <div class="header-inner">
      <a class="brand" href="#topics">PSM I revisit</a>
      <nav aria-label="Page sections">
        <a href="#topics">Topics</a>
        <a href="#entities">Entities</a>
        <a href="#relationships">Relationships</a>
      </nav>
    </div>
  </header>
  <div class="layout">
    <aside>
      <p class="aside-label">Key topics</p>
      <nav class="toc" aria-label="Topics in order">
        {"".join(toc)}
      </nav>
    </aside>
    <main>
      <section class="panel prose" id="topics">
        <h1>Revisit the key topics</h1>
        <p class="lede">Twelve topics from the November 2020 Scrum Guide, in study order. Read one, then use Next. Relationship diagrams sit above the sentences. Underlined words are entities and open their definitions.</p>
        {"".join(topic_html)}
      </section>
      <section class="panel prose" id="entities">
        <h2>Entities</h2>
        <p class="lede">Definitions used by the topics above. A line marked as a quotation uses the Guide's words.</p>
        {"".join(entity_html)}
      </section>
      <section class="panel prose" id="relationships">
        <h2>Relationships</h2>
        <p class="lede">Who is accountable for what, which event serves which purpose, and which commitment belongs to which artifact.</p>
        {framework_svg(linkify)}
        {"".join(relation_html)}
      </section>
    </main>
  </div>
  <footer>
    <p>Serving copy of the November 2020 Scrum Guide, prepared for PSM I study. Quotations are marked. Everything else is a paraphrase. Source: <a href="https://scrumguides.org/scrum-guide.html">scrumguides.org/scrum-guide.html</a>.</p>
  </footer>
</body>
</html>
"""
    OUT.write_text(page)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
