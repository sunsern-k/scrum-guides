# Output formats

## (A)–(D) knowledge graph

```markdown
## (A) Entity catalog
Grouped: theory, values, accountabilities, events, artifacts, commitments, related concepts.
For each: name, Guide sense in one or two sentences, paraphrase or a short quote.

## (B) Relationship map
Mermaid diagram with labeled edges, then a bullet list of edges the diagram cannot show cleanly.
Edge verbs: accountable for, serves, commitment of, enables, contains, inspects, adapts, selects, orders, conforms to.

## (C) PSM I must-know contexts
Tricky distinctions and rules that change the keyed answer. Each item: the distinction, the Guide basis, the usual wrong pick.

## (D) Common traps / non-Scrum practices
Two columns in prose: heard in industry → status (not required / allowed but not prescribed / contradicts the Guide).
```

## Question item

Use in `quiz`, `topic`, and `mini-exam`. Mix types. Tag every item.

```markdown
**Q1.** Best answer · Events
Stem. No "all of the above." No hint of how many options are correct.

- A. ...
- B. ...
- C. ...
- D. ...

<!-- key withheld until the user answers
Answer: C
Guide: short clause or paraphrase; say which.
Trap: what A, B, and D confuse.
-->
```

Select-all stem ends with "Select all that apply." True/false is one sentence and the options True and False.

After the user answers, reveal each item as:

```markdown
**Q1.** Correct / Incorrect — your answer: B · key: C
Guide: ...
Trap: ...
```

### Example — best answer

**Q.** Best answer · Events  
During a Sprint, the Developers learn that several selected items are larger than expected. The Sprint Goal is still valid. What is the Guide-faithful next step?

- A. Ask the Scrum Master to drop items so the forecast is met
- B. Lower the Definition of Done for this Sprint
- C. Renegotiate scope with the Product Owner without changing the Sprint Goal
- D. Cancel the Sprint

Key: C. Scope may be clarified and renegotiated with the Product Owner as more is learned. Quality does not decrease. Only the Product Owner may cancel a Sprint, and only if the Sprint Goal becomes obsolete. A swaps accountability onto the Scrum Master. B lowers quality. D cancels a Sprint whose goal is still valid.

### Example — select all

**Q.** Select all · Events  
Which statements match the Scrum Guide? Select all that apply.

- A. The Daily Scrum is 15 minutes
- B. Developers must use the three questions (yesterday, today, impediments)
- C. The Developers choose the structure and techniques
- D. The Product Owner is required to attend every Daily Scrum
- E. A Product Owner actively working Sprint Backlog items participates as a Developer

Key: A, C, E. B and D are habits. The Guide does not prescribe the three questions or require the Product Owner at the Daily Scrum.

### Example — true / false

**Q.** True/False · Artifacts  
The Sprint Review is the only time an Increment may be delivered to stakeholders.

Key: False. An Increment may be delivered before the end of the Sprint. The Sprint Review is not a gate to releasing value.

## Flip card

Relationship or rule, not a bare definition. Include the focus area on the front.

```markdown
Front: Events — Who may cancel a Sprint, and when?
Back: Only the Product Owner, and only if the Sprint Goal becomes obsolete.
Edge: Product Owner —authority to cancel→ Sprint
Exam trap: The Scrum Master does not cancel a Sprint to protect the team.
```

Per-topic deck: filter to one tag. Cross-topic deck: two cards per focus area, ordered Empiricism through Stakeholders & Customers.

## Flash card

One entity. Definition first. Relationship second. Confusion last.

```markdown
Front: Sprint Goal
Back: The single objective for the Sprint. Commitment of the Sprint Backlog. It creates coherence and focus and allows flexibility in the exact work. The Developers commit to it; scope can still be renegotiated with the Product Owner without changing the goal.
Not this: a promise to finish every selected Product Backlog item, or another name for the Product Goal.
```

## Scenario

```markdown
**S1.** Facilitation
Situation in 4–6 lines. No cartoon villain. Ask: what is the best next action, and which accountability does it respect?
Options: 4 actions. Exactly one is required or clearly best under the Guide.
```

Wrong options should still sound helpful (take over ordering, add a new event, assign tasks, skip the Retrospective).

## Accountable

One line, no story.

```markdown
Who is accountable for ordering the Product Backlog?
```

Expected shape of the later key: the accountability, whether they may delegate the work, and who they are not.

## Distinguish

```markdown
Product Goal vs Sprint Goal vs Definition of Done
For each: which artifact, what it commits to, time horizon, who is most involved, what goes wrong if you swap them.
```

Ask the user to fill the row before you show it.

## Not-scrum

```markdown
Practice: Planning poker
Status: Outside the Guide. Allowed only as a technique the team may choose. Not a rule. Not a keyed "Scrum requires…" answer.
```

Status values: `required` · `allowed, not prescribed` · `contradicts the Guide`.

## Teach-back

Ask the user to explain one entity and two relationships, in their own words, without notes if they are willing. Then:

```markdown
Fidelity: high / mixed / off
Kept: ...
Missing relationship: ...
Terminology to swap: self-organizing → self-managing
Next card: ...
```

## Mini-exam

State item count and the user's minute budget before the first question. No coaching between items. At the end: score, percent, misses grouped by focus-area tag, then three follow-ups on the worst tag.

## Revisit stop

One topic only. Read that topic file and fill this shape from it. Do not pull in the next file or re-analyze the Guide.

```markdown
**Topic 4 of 12 — Events**
Guide sense: one short paragraph. Paraphrase unless a clause must be quoted.
Entities: Sprint, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective.
Relationships:
- Sprint contains the other four events.
- Only the Product Owner may cancel a Sprint, and only if the Sprint Goal becomes obsolete.
Trap: the three Daily Scrum questions are not required.
Next: Artifacts. Say "next" to continue, "back" for Scrum Team, or "quiz this" for 3 questions before moving on.
```

After the user answers a "quiz this" set, score it, then repeat the same "Next:" line. Do not start the following topic in that message.

## Progress log

Path: `study/progress.md` at the repo root. Update after a scored session. Also update `## Revisit` whenever a revisit stop is shown, including an unscored one. Do not log other unscored reading.

```markdown
# PSM I progress

## Revisit
- Next: knowledge/topics/05-artifacts.md (5 of 12)
- Last shown: Events

## Weak areas
- Events: 3
- Done: 1

## Sessions
### 2026-10-24 · quiz · 6/8
- Misses: Daily Scrum attendees (Events); lowering quality (Done)
- Next: flip deck on Events, then 3 scenarios
```

Keep a running miss count per tag. Newest session on top.
