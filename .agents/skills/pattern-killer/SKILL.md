---
name: pattern-killer
description: Kill AI-isms and robotic writing patterns to produce natural, human-sounding content. Use when (1) User says a draft has "AI smell" or sounds robotic, (2) User asks to humanize, de-AI, or naturalize text, (3) User wants to flag a pattern for the living database, (4) Running the 3-agent humanization workflow, (5) Reviewing any content where authentic voice matters.
---

# Pattern Killer

A living skill that evolves to catch and eliminate AI writing tells. The more you use it, the sharper it gets.

## Core Concepts

**AI-ism**: Any word choice, sentence structure, or phrasing that screams "written by AI." Examples include:
- Overly formal transitions ("Furthermore," "Moreover," "It is important to note")
- Hedging language ("It seems that," "One might argue," "In many cases")
- Robotic lists ("First, second, third, finally")
- Generic intensifiers ("significant," "crucial," "essential" without specifics)
- Passive voice overload
- Perfectly parallel structures that feel too... perfect

**Pattern Database**: Stored in [references/patterns.md](references/patterns.md). Each entry contains:
- The flagged pattern (what to watch for)
- The user's preferred alternative (what to use instead)
- Context notes (when/why it feels wrong)

## Quick Actions

### Flag a New Pattern

When the user spots an AI-ism and tells you their preferred alternative:

1. Read [references/patterns.md](references/patterns.md)
2. Add a new entry:
   ```markdown
   ### [Pattern Name]
   **Flagged**: "[the AI-ism phrase]"
   **Replace with**: "[preferred alternative]"
   **Context**: [when this pattern appears, why it feels robotic]
   **Added**: [date]
   ```
3. Confirm the addition

### Humanize a Draft (Quick Mode)

For fast, single-pass humanization:

1. Read [references/patterns.md](references/patterns.md)
2. Scan the draft for any flagged patterns
3. Rewrite with these rules:
   - Break up overly parallel structures
   - Replace formal transitions with conversational flow
   - Swap passive for active voice where possible
   - Add specific details instead of generic intensifiers
   - Vary sentence length (short punch mixed with longer flow)
   - Remove hedging unless uncertainty is truly the point
4. Return the polished draft

## 3-Agent Humanization Workflow

For high-stakes content where voice authenticity is critical, spawn three parallel agents:

**Agent 1: The Spotter**
```
Read the pattern-killer skill's references/patterns.md

Task: Review this draft and flag every AI tell you find.

For each issue, output:
- Location (sentence or paragraph)
- The flagged pattern
- Why it feels robotic
- Severity (1-5, 5 = immediately obvious AI)

Also flag any NEW patterns not in the database yet.
```

**Agent 2: The Rewriter**
```
Read the pattern-killer skill's references/patterns.md

Task: Rewrite this draft using the flagged issues as your guide.

Principles:
- Write like you're talking to a smart friend
- Kill all formal transitions
- Replace "AI vocabulary" with specific, concrete language
- Vary sentence rhythm (don't let it get too sing-song)
- Use contractions, fragments, conversational rhythm
- When in doubt, read it aloud - if it sounds like a presentation, fix it

Return the full rewritten draft.
```

**Agent 3: The Scorer**
```
Task: Score each sentence in this draft on humanization.

For each sentence, output:
- Sentence (quoted)
- Score: 1-5 (1 = obvious AI, 5 = sounds human)
- Brief note on what helps or hurts the score

Then give an overall draft score and top 3 patterns that still feel AI.
```

### Orchestrate the Workflow

```python
# Pseudocode for coordination
spotter_flags = agent1.run(draft)
rewritten = agent2.run(draft, context=spotter_flags)
scores = agent3.run(rewritten)

final = synthesize(rewritten, scores)
# Present: final draft + any new patterns to add to database
```

## Writing Principles (Reference)

When humanizing, aim for these qualities:

| AI Pattern | Human Alternative |
|------------|-------------------|
| "Furthermore/Moreover/Additionally" | Just skip it, or use "Plus," "And," "What's more" |
| "It is important to note that..." | Just say the thing, or "Here's the thing:" |
| "In conclusion/In summary" | End the thought, or "So:" |
| "significant/crucial/essential" | Say WHY it matters specifically |
| "leverage/utilize" | "use" |
| "delve into/explore" | "look at," "dig into," "figure out" |
| Perfect parallel lists | Break the rhythm, make one item longer |
| "One might argue that..." | Just argue it, or "You could say" |
| "It seems that..." | Remove or commit to the statement |

## Maintenance

- Add new patterns as they're discovered
- Review patterns.md periodically for outdated entries
- The database is a living document - it should grow with every project
