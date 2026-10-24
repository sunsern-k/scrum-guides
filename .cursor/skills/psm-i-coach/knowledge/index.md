# Knowledge index

- Edition: November 2020 Scrum Guide
- Source: https://scrumguides.org/scrum-guide.html
- Updated: 2026-10-24
- Status: serving copy. Read these files on study requests. Do not re-fetch or re-analyze unless a refresh is requested or a file is missing.

## What to open

| Need | Open this file only |
| --- | --- |
| Full entity catalog, one definition, flash cards | `knowledge/entities.md` |
| Full relationship set, graph section (B) | `knowledge/relationships.md` |
| One revisit stop | the matching file under `knowledge/topics/` |
| Exam traps and non-Guide practices | `traps.md` |
| Ordered walk, refresh procedure | this file |

## Revisit order

Do not reorder. One file per turn. Resume from the next number in `study/progress.md`.

| # | Focus area | File |
| --- | --- | --- |
| 1 | Empiricism | `knowledge/topics/01-empiricism.md` |
| 2 | Scrum Values | `knowledge/topics/02-scrum-values.md` |
| 3 | Scrum Team | `knowledge/topics/03-scrum-team.md` |
| 4 | Events | `knowledge/topics/04-events.md` |
| 5 | Artifacts | `knowledge/topics/05-artifacts.md` |
| 6 | Done | `knowledge/topics/06-done.md` |
| 7 | Self-Managing Teams | `knowledge/topics/07-self-managing-teams.md` |
| 8 | Facilitation | `knowledge/topics/08-facilitation.md` |
| 9 | Coaching | `knowledge/topics/09-coaching.md` |
| 10 | Product Value | `knowledge/topics/10-product-value.md` |
| 11 | Product Backlog Management | `knowledge/topics/11-product-backlog-management.md` |
| 12 | Stakeholders & Customers | `knowledge/topics/12-stakeholders-and-customers.md` |

## How the files share facts

- `entities.md` is the canonical definition of each entity. Every entry lists the topic numbers that repeat it.
- `relationships.md` is the canonical edge list. Each edge has an id (`R01`) and the topic numbers that repeat it.
- A topic file is the serving copy for one revisit stop. It restates the entities and edges that stop needs, and cites their ids.
- On a normal request, trust the file the router told you to open. Do not cross-read the Guide, and do not reconcile files in that turn.
- `traps.md` is not a second catalog. It only holds distinctions and practices that are not Guide rules.

## Refresh

Do this only when the user asks to refresh or update the knowledge, or when the file you need is missing.

1. Fetch https://scrumguides.org/scrum-guide.html.
2. Change the affected entries in `entities.md` and `relationships.md`.
3. Search `knowledge/topics/` for those entity names and edge ids, and update those serving copies.
4. Set `Updated` in this file.
5. Rebuild the root page with `python3 .cursor/skills/psm-i-coach/scripts/build_revisit_html.py`.
6. If the fetch fails, leave the local files as they are and say they were not updated. Do not rebuild the page from a failed fetch.

A study question, a quiz, or a disagreement in chat does not by itself start a refresh. If the user disputes one claim, correct that claim from the local file first. Refresh only if they ask for the Guide to be checked.
