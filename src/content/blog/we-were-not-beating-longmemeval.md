---
title: "My Memory System Cheated To Beat LongMemEval Until I Fixed It"
date: "May 03, 2026"
pubDate: 2026-05-03
tags: ['coding/ai', 'memory']
crosspost: true
type: "Development"
summary: "Last week I ran Weft, my homegrown memory layer, through LongMemEval and it scored 69.0% overall, 72.1% task-averaged. I was pleased. I shouldn't have been. The number was a lie, and the system that produced it was destroying the test data and calling it a win."
reading_time: 9
---

Last week I ran Weft, my homegrown memory layer, through LongMemEval and it scored 69.0% overall, 72.1% task-averaged. I was pleased. I shouldn't have been. The number was a lie, and the system that produced it was destroying the test data and calling it a win.

Here's how I found out.

I didn't design Weft for LongMemEval, or even for chat-shaped agents. I built it to remember behaviors and patterns across my coding sessions — preferences, anti-patterns, decisions — extracted and stored semantically so the agent can recall them later without knowing exactly when or how they were saved.

In the past few weeks I've started extending the platform because I'm building a chat-shaped agent and I want it to have persistent memory. I wanted to see how the existing belief-tier extraction held up against a standard benchmark. LongMemEval-Oracle was the first test: each question only sees its gold sessions, no distractors — easy mode.

69.0% overall. Better than I expected for something I built without really knowing what an agent memory layer should contain.

## The Honest Number

Shortly after this benchmark, I noticed a bug in the classifier and shipped a one-line fix. After the fix, the same harness on the same dataset scored 43.6%.

The 69% had been a lie. The classifier had been silently failing on every long input — Claude was wrapping its JSON intent classification in markdown code fences, my parser was throwing on the fenced text, and the pipeline was falling back to writing the entire 12k-character session blob into a single belief-tier memory with confidence 0. 

Once the classifier started actually working, the system finally told me what belief-tier extraction does to chat-shaped input.

It eats it. 

Weft wasn't beating LongMemEval; it was destroying the test data and calling it a win.

## What the honest number looked like

```text
before fix    after fix    Δ 
overall                   0.690         0.436        -0.254
task-averaged             0.721         0.420        -0.301

single-session-assistant  0.875         0.161        -0.714
single-session-preference 0.667         0.267        -0.400
single-session-user       0.857         0.671        -0.186
multi-session             0.602         0.459        -0.143
knowledge-update          0.731         0.641        -0.090
temporal-reasoning        0.594         0.323        -0.271
```

Turns out cheating was easy. 

Once the math was honest, what should be the easiest question — "what did the assistant say about X" — dropped from 87.5% to 16.1%. The most direct thing a memory system can be asked, and mine failed more than four times out of five.

Why?

My system took a statement and atomized it into a belief. Something basic like "user prefers Sony cameras" might be true, but without the rest of the conversation around it you don't know how true it is, or who said it, or when.

When asked to recall what the user actually said, the system couldn't find it — atomization had buried the literal phrasing under its abstractions. Great for behavioral coding, where preferences and patterns are exactly what should be extracted; terrible for dialogue retrieval, where the trace itself is the answer. Wrong shape for the question.

## The architectural reframe

Many memory layers assume the right thing to store is *what the user means*. You take the dialogue, run an LLM over it, extract atomized facts, and store those. The dialogue itself is a shipping container; once the cargo is unloaded, you discard it.

LongMemEval's six question types disagree.

- "What's my preference for X" — semantic, fits atomized facts.
- "What did you tell me about X" — needs the assistant turn intact.
- "How many X have I mentioned" — needs enumeration across the dialogue trace.
- "How long between X and Y" — needs date-anchored ordering.
- "Has my X changed" — needs version history across sessions.
- "What did I tell you about X" — needs the user turn intact.

Only "what is my preference" fits cleanly into the belief-tier shape. The other five want the dialogue trace itself: the actual turns, with their roles attached, in chronological order, with their dates intact.

Ironically, Weft already had a turn tier. I'd built it into the agent runtime to log dialogue traces as they happened — a logging path in my head, not a recall path — and when I wired up the benchmark adapter, the turn tier never came up. Recall was exactly what the benchmark was asking for, and I'd had the right tool the whole time.

## What the turn-tier system does

The turn-tier ingest creates one episode per haystack question and writes each conversational turn as one row in `episode_turns`, with `occurred_at` set from the session date. Each turn carries its own embedding. Recall does hybrid retrieval (vector + BM25, RRF fusion) over the turn rows directly. 

Multi-anchor temporal questions like "how many days between the launch and the demo" get a per-anchor split.

I run a separate recall for "the launch" and "the demo," union the results, and let the Reader do the arithmetic on two grounded sets instead of one conflated pile.

The idea is that now the entire conversation is available in semantic search, not just the atomized facts I extract from it.

## The honest number, redone

```text
honest belief    turn tier      Δ
overall                   0.436            0.892          +0.456
task-averaged             0.420            0.889          +0.469

single-session-assistant  0.161            0.982          +0.821
single-session-user       0.671            0.971          +0.300
single-session-preference 0.267            0.767          +0.500
multi-session             0.459            0.872          +0.414
temporal-reasoning        0.323            0.872          +0.549
knowledge-update          0.641            0.872          +0.231
```

Single-session-assistant: 16.1% to 98.2%. Fifty-five out of fifty-six questions correct.

The system is now genuinely better. Even compared to the "cheater" run, the 89% beats 69% and it didn't depend on the parser breaking to help get better numbers. 

I can run the system tomorrow and get the same answer, and that answer is good.

## Surviving distractors

Oracle is the easy test — each question references one to five sessions, each session has its "gold" evidence embedded somewhere inside, and the system only has to find the right turn in a small pile. But Oracle isn't the only test LongMemEval offers.

LongMemEval-S takes the same 500 questions and pads each reference window (the "haystack") out with 43 distractor sessions, for 48 total. More sessions, longer sessions. Instead of searching ~600 candidate turns, the system now has roughly 12k to search through.

I ran a 50% stratified sample (n=251), preserving question-type proportions. Same harness. Same prompts. Same model. Same code.

```text
Oracle (n=500)   S (n=251 stratified)   Δ
overall                       0.892            0.837                   -0.055
task-averaged                 0.889            0.857                   -0.033
single-session-assistant      0.982            1.000                   +0.018
single-session-user           0.971            0.943                   -0.029
single-session-preference     0.767            0.800                   +0.033
knowledge-update              0.872            0.846                   -0.026
temporal-reasoning            0.872            0.791                   -0.081
multi-session                 0.872            0.761                   -0.111
```

A 5.5-point overall drop across 25× more haystack content. Synthesis categories take a real hit — multi-session loses 11 points, temporal loses 8 — but even at S they're still beating the honest belief baseline on the easier Oracle test by roughly 30 points. The system isn't perfect, but it's a heck of a lot better.

Single-session-assistant scored 28 out of 28 on the stratified S sample. That category does not care about distractor pressure; the dialogue trace preserves what atomization was destroying, and adding distractors does not hide it.

Anyone can win on Oracle. Surviving distractors is harder and it is what makes a memory system trustworthy.

## What I now believe about chat memory

Belief-tier extraction is not the right default storage shape for conversational input. 

Belief works for declarative facts the user states and you want to remember as facts ("I'm allergic to peanuts," "I prefer Sony cameras"). It does not work for the rest of what shows up in chat. Anything that needs the user's exact phrasing, the assistant's exact phrasing, the role attribution, the temporal ordering, the conversational continuity, or the ability to figure out time or frequency needs the exact dialogue trace. 

The belief tier should be a synthesis layer over the turns — conversations appended at write time, then read back later by a separate agent that synthesizes the durable facts (preferences, habits, declarative claims) into the belief tier. The system keeps the details of a conversation for when they matter and the distilled facts for when they don't.

In practice, this means memories for chat-shaped agents go into `weft_turn_append` first. When a question comes in, the system tries the turn tier; if that fails, it falls back to the belief tier. The turn tier handles "what did we talk about" — recent, specific, role-attributed. The belief tier handles "what is true about this person" — durable, distilled, accumulated.

I went into this testing thinking beliefs would be the primary storage shape for my agents. I had it backwards. The turns layer matters first; beliefs only come into play when the question isn't about conversation specifics. That's why belief-tier extraction works well for the behavioral coding context Weft was originally built for — coding sessions ask "what does this user prefer," not "what did the assistant say in turn 4" — and why it fell apart the moment I pointed it at chat.

## What I haven't measured yet

LongMemEval-M has ~500 sessions per question — ten times S. I have not run it. I do not know what the turn tier does at that scale, and the architectural claim has a known asymptote: as the candidate pool grows, hybrid recall over a flat embedding space gets harder, and at some haystack size the candidate top-K stops containing the gold turn. Where exactly that wall sits is an open question for a follow-up.

I also didn't test what happens when a conversation grows past S-sized haystacks into something larger. Aging may degrade retrieval, and my system's built-in pruning and consolidation will probably need tuning before it holds up at that scale.

I have that on my roadmap, but I felt these findings were important enough to write about now.

This post is not "I solved memory." This post is "I audited my own benchmark, found the abstraction was wrong, swapped the storage shape, and the honest number doubled."

## How to reproduce

Note: the repo is currently private and will go public in the not-too-distant future, once I've finished a cleanup pass. Once it's available, code lives in `benchmarks/longmemeval/` in [github.com/MennoAf/weft-memory](https://github.com/MennoAf/weft-memory).

Two commands:

```text
# honest belief baseline (what the system did before turn tier)
uv run python -m benchmarks.longmemeval.adapter \
  --dataset path/to/longmemeval_oracle.json \
  --mode extracted

# turn tier
uv run python -m benchmarks.longmemeval.adapter \
  --dataset path/to/longmemeval_oracle.json \
  --mode turns --tier turns
```

Score with:

```text
uv run python -m benchmarks.longmemeval.judge --hyp <output.jsonl>
```

Total reproduction cost: roughly $15 across both runs and the gpt-4o judge. Anyone can re-run, get the same numbers, and decide whether they believe me.

If the lift evaporates on your reproduction, I want to know. The architectural claim is that storage shape matters more than retrieval cleverness for chat-shaped input. The largest piece of evidence I have for it is the 46-point spread between honest belief and turn tier; the next-largest is the 30-point spread that survives distractors on S.

If you have a memory system that is hitting an analogous ceiling, the question to ask is what shape your dialogue is in once it's stored — atoms or trace. If it's atoms, you might be measuring something other than what you think you are.
