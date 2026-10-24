# PSM I coach

A skill that coaches Professional Scrum Master I preparation from the [2020 Scrum Guide](https://scrumguides.org/scrum-guide.html). It runs in Cursor and in Claude Code from the same files. The Guide is the only source of Scrum rules. Industry habits (story points, the three Daily Scrum questions, Sprint 0, and the like) are labeled as habits, and they are never the correct answer.

Open this repository and ask in chat. You do not need to name the skill. Mention PSM I, the Scrum Guide, a quiz, flip cards, or flash cards and the coach takes that mode. In Claude Code you can also type `/psm-i-coach`.

## Start a session

Paste any example below. If you only say “help me prepare,” the coach gives a 6-question diagnostic, waits for your answers, scores them, and tells you which mode to do next.

A scored session is written to `study/progress.md` the first time you finish one. Later, “review what I missed” starts from that log.

## What you can ask for

| You want | Say this | What you get |
| --- | --- | --- |
| The big picture | `Analyze the Scrum Guide` | Entity catalog, relationship map, must-know exam distinctions, and practices that are not in the Guide. The map is drawn for chat in Cursor, and pasted as the stored diagram in Claude Code |
| A mixed quiz | `Quiz me` | 8 questions: best answer, select-all-that-apply, and true/false. The key stays hidden until you answer |
| A shorter or longer quiz | `Quiz me with 5 questions on Events and Done` | A quiz limited to the size and focus areas you name |
| Relationship memory | `Make flip cards` | Two relationship cards for each focus area. Cursor opens them as a deck. Claude Code shows them one at a time in chat |
| One topic’s relationships | `Flip cards on Events` | Relationship cards for that topic only, shown the same way as a full flip deck |
| Definitions | `Flash cards` | One card per Guide entity: definition, where it sits, and what people confuse it with |
| A few cards in chat | `Flash card me on Sprint Goal, one at a time` | Front first. The back appears after you try. This is also how Claude Code delivers every card deck |
| A workplace situation | `Give me 3 scenarios` | A short situation and four actions. One action fits the Guide |
| Accountability speed round | `Who is accountable? Ten questions` | One-line prompts: ordering, sizing, canceling a Sprint, the Definition of Done, and similar |
| A pair you keep mixing up | `Distinguish Product Goal, Sprint Goal, and Definition of Done` | You fill the comparison, then the coach shows the Guide version |
| “Is this Scrum?” | `Is planning poker required by Scrum?` | Required, allowed but not prescribed, or contradicts the Guide |
| A mock sitting | `Mini-exam, 20 questions, 15 minutes` | Mixed questions. Coaching waits until you submit the set |
| Teach it back | `Teach-back: I will explain the Daily Scrum` | You explain. The coach marks missing relationships and old wording |
| One focus area | `Topic pack: Stakeholders and Customers` | A short catalog slice, 6 flip cards, and 5 questions for that area only. The questions match in both tools. The cards follow the flip-card rule for that tool |
| Every key topic, one at a time | `Revisit the key topics` | Topic 1 of 12 only, read from a stored topic file. Say `next` for the following topic. The walk resumes where you stopped |
| Refresh the stored Guide analysis | `Refresh the knowledge from the Scrum Guide` | Re-reads the Guide and updates the local entity, relationship, and topic files. An ordinary quiz does not do this |
| Continue from misses | `Review what I missed` | Drills the tags you miss most often in `study/progress.md` |

Focus-area names the coach uses: Empiricism, Scrum Values, Scrum Team, Events, Artifacts, Done, Self-Managing Teams, Facilitation, Coaching, Product Value, Product Backlog Management, Stakeholders & Customers.

## What works in both, and what Claude Code does instead

Cursor reads `.cursor/skills/psm-i-coach/`. Claude Code reads `.claude/skills/psm-i-coach`, a symlink to that same folder. Edit the files under `.cursor/skills/`. Both tools then see the change. Start Claude Code in this repository. A claude.ai chat or a Claude cloud session does not load this project folder; those use the skill after it is uploaded to the account.

The prompts above are the same in both tools. These modes return the same kind of reply: quiz, scenario, who is accountable, distinguish, “is this Scrum?”, mini-exam, teach-back, the questions inside a topic pack, the one-topic revisit, review, refresh, and `study/progress.md`. [revisit.html](revisit.html) is a browser page, so it is the same wherever you open it.

Two modes use a different surface:

| You ask for | In Cursor | In Claude Code |
| --- | --- | --- |
| The relationship map (`Analyze the Scrum Guide`) | Sections A–D in chat. The stored diagram is formatted for the conversation. A canvas map is created when you ask to keep one. | The same four sections in chat. The diagram is the Mermaid block stored in `knowledge/relationships.md`, then the edge list. |
| Flip cards, flash cards, and the cards inside a topic pack | A deck beside the chat. Click a card to flip it. The chat message is the topic list and the card count. Ask for a handful in chat when you want one card at a time. | One card at a time in the chat. The front comes first. Reply, and the back follows. There is no side deck to reopen. |

## How a quiz works

1. You get the questions only. Select-all items do not say how many options are correct.
2. Reply with a letter, a set of letters, or True or False for each question, in order. The coach shows that shape with placeholders, and does not fill in a sample that could be the key.
3. The coach scores, explains each miss from the Guide, names the trap, and adds three follow-up questions on the weak areas.
4. Best-answer and true/false are worth 1 point. A select-all item is worth 1 point only when your set matches exactly.

## Examples

**Map the Guide**

```text
Analyze the Scrum Guide. I want the entity catalog, the relationship map, the PSM I traps, and what is not Scrum.
```

**Practice the way the exam asks**

```text
Quiz me with 8 questions. Mix best answer, select all that apply, and true/false. Cover Events, Artifacts, and Done.
```

```text
1<letter>, 2<letters separated by spaces>, 3 True or False, and so on for each question.
```

That line shows the shape of a reply. On a live quiz the coach leaves the placeholders empty, so the example is not an answer key.

**Memorize a relationship, then a definition**

```text
Flip cards on accountabilities: who orders the Product Backlog, who sizes, who selects Sprint items, and who may cancel a Sprint.
```

```text
Flash cards for the three commitments only.
```

In Cursor, flip-card and flash-card decks open beside the chat so you can flip them again later. A small set stays in the conversation, one card at a time. In Claude Code, every card stays in the conversation that way: front, your try, then the back.

**Apply a rule to a situation**

```text
Scenario: during the Sprint the Developers discover the selected items are larger than expected, and the Sprint Goal is still valid. What should they do? Give me four options.
```

**Clean up old terminology**

```text
Teach-back. Self-organizing means the team picks its own tasks, and the Scrum Master is their servant-leader. Correct me against the 2020 Guide.
```

The coach answers in 2020 terms: accountabilities, commitments, self-managing, Developers, and one Scrum Team.

**Check a habit before it becomes a wrong answer**

```text
Classify these: velocity, Definition of Ready, burn-down chart, three Daily Scrum questions, Sprint Review as a release gate.
```

**Revisit every key topic in order**

```text
Revisit the key topics, one at a time.
```

You get topic 1 of 12 (Empiricism): the Guide sense, the entities in that topic, the relationships that decide exam answers, and one trap. Nothing after that topic is taught yet.

```text
next
```

That advances to topic 2. `back` returns to the previous topic. `from the start` resets to Empiricism. `quiz this` asks 3 questions on the current topic and stays there until you say `next`.

The order is Empiricism, Scrum Values, Scrum Team, Events, Artifacts, Done, Self-Managing Teams, Facilitation, Coaching, Product Value, Product Backlog Management, and Stakeholders & Customers. Each topic is already written in `.cursor/skills/psm-i-coach/knowledge/topics/`. A later session that says `revisit the key topics` continues at the next unshown topic. The coach does not re-analyze the Guide for that turn.

The same walk is also in [revisit.html](revisit.html), next to this file. Open it in a browser, read one topic, then use Next. Each topic draws its relationships as a diagram, and the Relationships section opens with a framework map. Underlined words jump to the entity definition.

**Sit a short mock, then continue tomorrow**

```text
Mini-exam. 20 mixed questions. Give me 15 minutes. Do not explain until I submit all answers.
```

```text
Review what I missed, and start with flip cards for my weakest area.
```

## A study loop that fits the skill

1. Analyze the Guide once, and keep the relationship map.
2. Revisit the 12 key topics one at a time, and say `next` when a topic is familiar.
3. Flash cards for entities you cannot define in one sentence.
4. Flip cards for the relationships those entities have.
5. A topic pack for one weak focus area.
6. Scenarios and “who is accountable?” on that same area.
7. A mini-exam when a topic feels familiar.
8. Next session: resume the topic walk, or review the miss log, before starting a new topic.

## What the coach will treat as out of bounds

Scrum rules in a normal session come from the local knowledge files, which were prepared from the November 2020 Scrum Guide. Ask to refresh those files when you want them checked against the current Guide page again. If that refresh cannot fetch the page, the stored files stay as they are.

Exam logistics — number of questions, time limit, pass mark, and whether materials are allowed — are scrum.org assessment rules, not Guide content. Ask for them explicitly if you want the coach to check the current PSM I page.

Complementary practices can be discussed. They are not keyed as “Scrum requires this.”

## Files

| Path | Purpose |
| --- | --- |
| `.claude/skills/psm-i-coach` | Symlink to the folder below, so Claude Code loads the same coach |
| `.cursor/skills/psm-i-coach/SKILL.md` | Coach instructions and mode router. This is the file to edit |
| `.cursor/skills/psm-i-coach/knowledge/index.md` | Which file to open, revisit order, and how to refresh |
| `.cursor/skills/psm-i-coach/knowledge/entities.md` | Canonical definitions. Edit here first |
| `.cursor/skills/psm-i-coach/knowledge/relationships.md` | Canonical edges, each with an id, plus the relationship diagram |
| `.cursor/skills/psm-i-coach/knowledge/topics/` | One serving file per key topic, in walk order |
| `.cursor/skills/psm-i-coach/formats.md` | Question, card, and progress templates |
| `.cursor/skills/psm-i-coach/traps.md` | Exam distinctions and practices that are not Guide rules |
| `revisit.html` | Browser copy of the 12 topics, the entity definitions, and the relationships |
| `study/progress.md` | Created after your first scored session, and updated as the topic walk advances |
