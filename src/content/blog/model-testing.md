---
title: "I Benchmarked Anthropic's Advisor Strategy on Task Decomposition. The Expensive Model Was the Worst."
date: "April 09, 2026"
pubDate: 2026-04-09
tags: ['coding/ai', 'benchmarking']
crosspost: true
type: "Research"
summary: "Anthropic's Advisor Strategy promises near-Opus intelligence at near-Sonnet cost. A server-side tool that pairs a cheap executor model with an expensive advisor. I benchmarked it in task decomposition."
reading_time: 14
---

## The Claim vs. The Data

Anthropic's [Advisor Strategy](https://claude.com/blog/the-advisor-strategy) promises near-Opus intelligence at near-Sonnet cost. A server-side tool that pairs a cheap executor model with an expensive advisor. 

One API call, no extra round-trips, the executor decides when to consult.

The published benchmarks are compelling: +2.7 percentage points on SWE-bench Multilingual, 11.9% cost reduction per agentic task, and Haiku with an Opus advisor more than doubling its BrowseComp score.

I wanted to know: **does this hold up on task decomposition?** Breaking complex product requirements into executable task graphs is the foundation of my autonomous agent system. 

It's architecturally demanding, structurally unforgiving, and something that Anthropic's published evaluations don't cover.

So I built a benchmark and ran it.

---

## The Benchmark

### What I Measured

My benchmark evaluates how well a model decomposes, or breaks down, a Product Requirements Document (PRD) into an executable task graph.

This is the kind of work that drives a lot of how I use the tool. I measured two things:

**Decomposition** — turning a PRD into a structured task graph with epics (sprints), dependencies, file assignments, and parallel execution paths.

This helps agents reliably complete tasks without running out of context or potentially overwriting the same file multiple times.

**Enrichment** — adding execution metadata to each task: acceptance criteria (`done_when`), complexity estimates, and implementation context. These help agents know when a task is done, how long it should take, and what files it touches.

### Test Fixtures

I used two PRDs of deliberately different complexity:

<table>
<thead>
<tr>
<th>PRD</th>
<th>Domain</th>
<th>Word Count</th>
<th>Expected Tasks</th>
<th>Complexity</th>
</tr>
</thead>
<tbody>
<tr>
<td>**LinkCrate**</td>
<td>CLI bookmark manager</td>
<td>535 words</td>
<td>10-16</td>
<td>Simple — single-epic, clear boundaries</td>
</tr>
<tr>
<td>**Weaver**</td>
<td>Autonomous agent executor</td>
<td>3,057 words</td>
<td>25-55</td>
<td>Complex — multi-epic, Docker, async, cross-cutting concerns</td>
</tr>
</tbody>
</table>

LinkCrate is a PRD I use as a benchmark to ensure my workflow doesn't have regressions (which is when a previous part of the workflow starts to fail after adding new complexity).

Weaver is the PRD I used to create the workflow the benchmark is run in. It's a complex, multi-epic project that requires careful planning and coordination to complete successfully.

### Scoring Methodology

Each decomposition is scored across six weighted dimensions:

<table>
<thead>
<tr>
<th>Dimension</th>
<th>Weight</th>
<th>What It Measures</th>
</tr>
</thead>
<tbody>
<tr>
<td>**Parallelism**</td>
<td>25%</td>
<td>Critical path ratio and parallel width. Shorter critical path = more tasks can run concurrently.</td>
</tr>
<tr>
<td>**Granularity**</td>
<td>20%</td>
<td>Task count within the target sweet spot. Too few = under-specified. Too many = over-fragmented.</td>
</tr>
<tr>
<td>**Dependency Coherence**</td>
<td>20%</td>
<td>File conflict rate — how many dependency edges the validator had to add because the model missed them. Fewer corrections = better planning.</td>
</tr>
<tr>
<td>**Specificity**</td>
<td>15%</td>
<td>Task title word count and file reference rate. Vague tasks ("set up backend") score low. Specific tasks ("implement Redis session store in src/auth/session.py") score high.</td>
</tr>
<tr>
<td>**Epic Balance**</td>
<td>10%</td>
<td>Even distribution of tasks across epics. Lopsided graphs indicate structural misunderstanding.</td>
</tr>
<tr>
<td>**TDD Structure**</td>
<td>10%</td>
<td>Test task matching — does each implementation task have a corresponding test task?</td>
</tr>
</tbody>
</table>

**Composite overall score** weights quality (55%), cost efficiency (25%), and speed (20%):

```text
overall = quality × 0.55 + cost_factor × 0.25 + speed_factor × 0.20
```

Cost and speed factors are normalized against per-PRD baselines ($0.50/120s for simple, $2.00/180s for complex). 

This means that a model that produces excellent quality at unreasonable costs have a penalty but models that can create good quality at reasonable costs are rewarded.

Enrichment scoring uses a parallel rubric: 

<table>
<thead>
<tr>
<th>Dimension</th>
<th>Weight</th>
<th>What It Measures</th>
</tr>
</thead>
<tbody>
<tr>
<td>**Completeness**</td>
<td>25%</td>
<td>Fraction of tasks that received all three enrichment fields (done_when, complexity, context). A task missing any one field counts as incomplete.</td>
</tr>
<tr>
<td>**Context Depth**</td>
<td>20%</td>
<td>Average number of context keys per task, normalized against 8 keys as the ceiling. More context keys = richer implementation guidance. Caps at 1.0.</td>
</tr>
<tr>
<td>**Specificity**</td>
<td>20%</td>
<td>Average character length of done_when acceptance criteria, normalized against 200 chars. Longer = more specific pass/fail criteria. Caps at 1.0.</td>
</tr>
<tr>
<td>**JSON Validity**</td>
<td>20%</td>
<td>Percentage of enrichment responses that were valid, parseable JSON. Measures structural reliability of the model's output format.</td>
</tr>
<tr>
<td>**Per-Skill Reliability**</td>
<td>15%</td>
<td>The worst success rate across all enrichment skills. Uses min, not average. One flaky skill drags the whole score. Measures consistency across different enrichment types.</td>
</tr>
</tbody>
</table>

### The Test Matrix

I tested 8 model configurations across both PRDs:

**Baselines (3):**

- Haiku 4.5 solo

- Sonnet 4.6 solo

- Opus 4.6 solo

**Advisor variants (5):**

- Sonnet executor + Opus advisor (max_uses: 3 and 5)

- Haiku executor + Opus advisor (max_uses: 3 and 5)

- Haiku executor + Sonnet advisor (max_uses: 3)

The advisor tool (`advisor_20260301`) is configured as a server-side tool in the Messages API. max_uses is how many times that agent can call the advisor model per run. This was done to help control costs, as the advisor model is significantly more expensive than the executor model and the executor decides when it makes the call, there is no way to configure that logic. 

---

## The Results

### Simple Decomposition (LinkCrate, 535 words)

<table>
<thead>
<tr>
<th>Variant</th>
<th>Quality</th>
<th>Cost</th>
<th>Time</th>
<th>Crit Path</th>
<th>Width</th>
<th>Conflicts</th>
<th>Overall</th>
</tr>
</thead>
<tbody>
<tr>
<td>**Haiku+Opus adv(5)**</td>
<td>83.2</td>
<td>$0.259</td>
<td>82.9s</td>
<td>7/10</td>
<td>3</td>
<td>0</td>
<td>**84.1**</td>
</tr>
<tr>
<td>**Haiku solo**</td>
<td>81.1</td>
<td>$0.020</td>
<td>38.7s</td>
<td>7/11</td>
<td>3</td>
<td>1</td>
<td>**87.7 ★**</td>
</tr>
<tr>
<td>Opus solo</td>
<td>74.8</td>
<td>$0.459</td>
<td>111.3s</td>
<td>8/11</td>
<td>2</td>
<td>3</td>
<td>75.8</td>
</tr>
<tr>
<td>Sonnet+Opus adv(3)</td>
<td>72.3</td>
<td>$0.350</td>
<td>135.4s</td>
<td>9/10</td>
<td>2</td>
<td>2</td>
<td>74.8</td>
</tr>
<tr>
<td>Sonnet solo</td>
<td>70.1</td>
<td>$0.097</td>
<td>101.6s</td>
<td>9/10</td>
<td>2</td>
<td>3</td>
<td>78.1</td>
</tr>
<tr>
<td>Haiku+Opus adv(3)</td>
<td>68.3</td>
<td>$0.269</td>
<td>79.8s</td>
<td>7/7</td>
<td>1</td>
<td>0</td>
<td>75.9</td>
</tr>
<tr>
<td>Sonnet+Opus adv(5)</td>
<td>62.3</td>
<td>$0.362</td>
<td>135.6s</td>
<td>9/9</td>
<td>1</td>
<td>2</td>
<td>69.1</td>
</tr>
<tr>
<td>Haiku+Sonnet adv(3)</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>FAILED (timeout)</td>
</tr>
</tbody>
</table>

**The winner: Haiku solo.** 87.7 overall. $0.02. 39 seconds. The cheapest model in the matrix produced the best value on simple decomposition, and it wasn't close. 

This was honestly surprising, since it is not what I expected and prior to this point I thought I needed Sonnet for these tasks.

Haiku+Opus advisor(5) achieved the highest raw quality (83.2), but at 13x the cost and 2x the time. This lowered the overall score, since the small increase in quality is not worth that cost differential since any errors in decomposition are addressed during the enrichment phase.

Opus solo, the most expensive option at $0.459, scored 75.8 overall with 3 file conflicts and only 2-wide parallelism. It over-structured a simple problem.

Pricier isn't always better! 

But, this was a relatively simple PRD, something you could comfortably complete in a Claude session or two. The real test is complex decomposition.

### Complex Decomposition (Weaver, 3,057 words)

Weaver is a system that you can call from the command line and give it a PRD. 

The tool then has to spin up a docker container, clone a development environement into that repo, decompose the PRD into tasks, and then autonomously build that PRD into functional cobe by calling agents to tackle each task.

This is a real tool that I've built and use everyday for my workflow, and the complexity makes it an excellent benchmark.

<table>
<thead>
<tr>
<th>Variant</th>
<th>Quality</th>
<th>Cost</th>
<th>Time</th>
<th>Crit Path</th>
<th>Width</th>
<th>Conflicts</th>
<th>Overall</th>
</tr>
</thead>
<tbody>
<tr>
<td>**Sonnet solo**</td>
<td>83.2</td>
<td>$0.199</td>
<td>238.3s</td>
<td>12/26</td>
<td>4</td>
<td>0</td>
<td>**83.5 ★**</td>
</tr>
<tr>
<td>Sonnet+Opus adv(5)</td>
<td>82.9</td>
<td>$0.609</td>
<td>297.2s</td>
<td>11/24</td>
<td>4</td>
<td>0</td>
<td>80.4</td>
</tr>
<tr>
<td>Haiku+Opus adv(5)</td>
<td>71.3</td>
<td>$0.474</td>
<td>167.1s</td>
<td>13/27</td>
<td>5</td>
<td>15</td>
<td>78.1</td>
</tr>
<tr>
<td>Opus solo</td>
<td>69.3</td>
<td>$0.993</td>
<td>284.7s</td>
<td>17/27</td>
<td>3</td>
<td>16</td>
<td>72.1</td>
</tr>
<tr>
<td>Haiku+Sonnet adv(3)</td>
<td>60.9</td>
<td>$0.170</td>
<td>173.3s</td>
<td>12/21</td>
<td>3</td>
<td>12</td>
<td>73.2</td>
</tr>
<tr>
<td>Sonnet+Opus adv(3)</td>
<td>74.0</td>
<td>$0.636</td>
<td>906.6s</td>
<td>13/21</td>
<td>4</td>
<td>0</td>
<td>63.7</td>
</tr>
<tr>
<td>Haiku solo</td>
<td>9.0</td>
<td>$0.039</td>
<td>80.9s</td>
<td>—/0</td>
<td>0</td>
<td>0</td>
<td>47.6</td>
</tr>
<tr>
<td>Haiku+Opus adv(3)</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>FAILED (FK constraint)</td>
</tr>
</tbody>
</table>

**The winner: Sonnet solo.** 83.5 overall. $0.20. Zero file conflicts. 4-wide parallelism. Clean, well-structured task graphs at reasonable cost.

This also surprised me because I previous used Opus for this level, assuming that I needed the reasoning abilities to handle the complexity of the PRD. It turns out that Sonnet is more than capable, at least at this level. 

**Haiku solo produced zero tasks.** It couldn't handle multi-epic decomposition at all. Quality score: 9.0. While Haiku easily handled simple PRDs, it completely failed at complex decomposition.

**The rescue: Haiku+Opus advisor(5) recovered to 71.3 quality** with 27 tasks and 5-wide parallelism. The advisor genuinely saved an otherwise dead run. But at $0.474, you're paying more than double what Sonnet costs and the outcome still couldn't match Sonnet. 

For decomposition tasks, this was the only scenario where the advisor provided noticable value. 

I plan on investigating why, but it was a surprising outcome and counter to what I expected going into this benchmark. 

**The surprise: Opus solo was the worst value.** $0.993 for 69.3 quality, 16 file conflicts, and the longest critical path in the matrix (17/27). The most expensive model produced task graphs that were harder to execute in parallel.

### Enrichment (LinkCrate, 15 tasks)

After a task is decomposed, the next step is to enrich it. This will give useful context to that task to help the model get the task done right the first time. This process also can catch issues with the decomposition, such as missing context or tasks that are too complex. 

<table>
<thead>
<tr>
<th>Variant</th>
<th>Quality</th>
<th>Cost</th>
<th>Time</th>
<th>Done%</th>
<th>Cplx%</th>
<th>JSON%</th>
<th>Advisor Calls</th>
<th>Overall</th>
</tr>
</thead>
<tbody>
<tr>
<td>**Haiku solo**</td>
<td>93.0</td>
<td>$0.138</td>
<td>48.8s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>—</td>
<td>**94.0 ★**</td>
</tr>
<tr>
<td>Sonnet solo</td>
<td>93.0</td>
<td>$0.658</td>
<td>130.4s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>—</td>
<td>88.0</td>
</tr>
<tr>
<td>Haiku+Sonnet adv(3)</td>
<td>79.0</td>
<td>$0.123</td>
<td>126.4s</td>
<td>100%</td>
<td>87%</td>
<td>87%</td>
<td>1/20</td>
<td>84.8</td>
</tr>
<tr>
<td>Haiku+Opus adv(3)</td>
<td>93.0</td>
<td>$1.289</td>
<td>93.0s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>9/30</td>
<td>83.5</td>
</tr>
<tr>
<td>Haiku+Opus adv(5)</td>
<td>92.8</td>
<td>$1.811</td>
<td>109.3s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>13/30</td>
<td>78.7</td>
</tr>
<tr>
<td>Opus solo</td>
<td>93.0</td>
<td>$3.378</td>
<td>141.0s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>—</td>
<td>68.2</td>
</tr>
<tr>
<td>Sonnet+Opus adv(3)</td>
<td>93.0</td>
<td>$3.423</td>
<td>210.8s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>18/30</td>
<td>66.8</td>
</tr>
<tr>
<td>Sonnet+Opus adv(5)</td>
<td>93.0</td>
<td>$3.617</td>
<td>207.8s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>20/30</td>
<td>66.8</td>
</tr>
</tbody>
</table>

**Enrichment is something all models handle well.** Every model except one hit 93.0 quality with 100% completion across all metrics. The difference is entirely cost:

- Haiku: $0.14 for 93.0 quality
- Opus: $3.38 for 93.0 quality
- Sonnet+Opus adv(5): $3.62 for 93.0 quality

That's a **24x cost difference for identical output.**

The one exception: **Haiku+Sonnet advisor(3) dropped to 79.0 quality** with 87% completion rates. 

In this case, Sonnet acted like a middle manager who came and started making changes to a project that was already being handled perfectly by Haiku. It introduced errors and inefficiencies that Haiku would have never made on its own.

### Complex Enrichment (Weaver, 34 tasks)

This is the test that completes the story. Simple enrichment was easy for all of the agents. Does that hold when you're enriching 34 tasks from a complex, multi-epic PRD with cross-cutting concerns?

<table>
<thead>
<tr>
<th>Variant</th>
<th>Quality</th>
<th>Cost</th>
<th>Time</th>
<th>Done%</th>
<th>Cplx%</th>
<th>JSON%</th>
<th>Advisor Calls</th>
<th>Overall</th>
</tr>
</thead>
<tbody>
<tr>
<td>**Haiku solo**</td>
<td>95.3</td>
<td>$0.780</td>
<td>170.8s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>—</td>
<td>**93.4 ★**</td>
</tr>
<tr>
<td>Sonnet solo</td>
<td>95.3</td>
<td>$3.438</td>
<td>495.2s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>—</td>
<td>83.4</td>
</tr>
<tr>
<td>Haiku+Sonnet adv(3)</td>
<td>81.6</td>
<td>$1.105</td>
<td>523.2s</td>
<td>100%</td>
<td>94%</td>
<td>94%</td>
<td>26/41</td>
<td>80.3</td>
</tr>
<tr>
<td>Haiku+Opus adv(3)</td>
<td>95.3</td>
<td>$11.203</td>
<td>483.3s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>51/68</td>
<td>67.3</td>
</tr>
<tr>
<td>Haiku+Opus adv(5)</td>
<td>95.3</td>
<td>$11.307</td>
<td>480.0s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>52/68</td>
<td>67.2</td>
</tr>
<tr>
<td>Opus solo</td>
<td>95.3</td>
<td>$16.331</td>
<td>467.1s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>—</td>
<td>65.9</td>
</tr>
<tr>
<td>Sonnet+Opus adv(5)</td>
<td>95.3</td>
<td>$17.228</td>
<td>714.0s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>55/68</td>
<td>62.5</td>
</tr>
<tr>
<td>Sonnet+Opus adv(3)</td>
<td>95.3</td>
<td>$17.865</td>
<td>740.5s</td>
<td>100%</td>
<td>100%</td>
<td>100%</td>
<td>57/68</td>
<td>62.1</td>
</tr>
</tbody>
</table>

Surprisingly, the pattern **holds** at scale. 

- Haiku: **$0.78** for 95.3 quality
- Sonnet: $3.44 for 95.3 quality
- Opus: $16.33 for 95.3 quality
- Sonnet+Opus adv(3): $17.87 for 95.3 quality

That's a **23x cost difference** between the cheapest and most expensive configurations for identical quality output.

The advisor variants present their own story. This time, the executor agent asked for help most of the time, resulting in higher costs for no noticable benefit. 

Another interesting finding was that the haiku+sonnet pairing was the only advisor to **degrade** quality overall. It seems something about that pairing just doesn't work well within this framework. 

---

## Five Things I Learned

### 1. Model selection should be complexity-routed, not uniform.

Models handle tasks differently depending on the complexity of the task, and so the model you select should change with that complexity. These are the rules I implemented in my workflow. 

<table>
<thead>
<tr>
<th>PRD Complexity</th>
<th>Decompose Model</th>
<th>Enrich Model</th>
<th>Cost</th>
<th>Why</th>
</tr>
</thead>
<tbody>
<tr>
<td>**Simple** (<2K words)</td>
<td>Haiku</td>
<td>Haiku</td>
<td>$0.16</td>
<td>Haiku dominates on quality AND cost</td>
</tr>
<tr>
<td>**Complex** (>2K words)</td>
<td>Sonnet</td>
<td>Haiku</td>
<td>$0.34</td>
<td>Sonnet for structure, Haiku for metadata</td>
</tr>
</tbody>
</table>

When creating a system designed to scale, this complexity routing isn't optional. Not only did Haiku save money, but 

### 2. Complex models can make the job harder

This was the most counterintuitive finding. Opus, which is Anthropic's most complex public model, consistently underperformed Sonnet and even lost to Haiku for simpler tasks on **accuracy** not just cost. 

- **Simple PRDs:** 3 file conflicts, narrow parallelism (width 2), $0.459
- **Complex PRDs:** 16 file conflicts, longest critical path (17/27), width 3, $0.993

Opus generates sophisticated-looking task graphs that are structurally harder to execute. More dependencies, more conflicts, less parallelism. It sees connections that simpler models miss, which could have value in specific cases. But it makes the plans harder for models to execute. 

**More capable does not mean more effective.** The model that understands the most can cause more problems. 

### 3. The advisor pattern's sweet spot is narrower than the marketing suggests.

Anthropic's published benchmarks show broad improvements on coding (SWE-bench) and browsing (BrowseComp). On task decomposition, the picture is different:

- **Simple PRDs:** No benefit. Haiku solo already wins. Adding an advisor increases cost 13x for marginal quality improvement.
- **Complex PRDs:** Advisor rescues Haiku from total failure (0 → 71.3 quality), but Sonnet solo still beats it at less than half the cost.
- **Enrichment:** Pure waste. The advisor adds cost without improving the 95.3 quality ceiling — or actively degrades performance. On complex enrichment, the advisor was consulted on 84% of calls and produced zero measurable improvement at $17.87.

The advisor pattern works when an executor encounters problems **it can't recognize on its own**. On well-structured tasks with clear success criteria, the executor doesn't need help — and the advisor's presence introduces noise.

### 4. Enrichment is a commodity — stop overspending on it.

This held across both simple and complex tasks. On simple enrichment (15 tasks), seven of eight models hit 93.0 quality. On complex enrichment (34 tasks from a multi-epic PRD), seven of eight hit 95.3.

The cost spread on complex enrichment: $0.78 (Haiku) to $17.87 (Sonnet+Opus advisor). That's a **23x cost difference for identical output** on the same 34 tasks.

Task enrichment is structured, fill-in-the-blank work. It does not require architectural reasoning. It does not benefit from deep analysis. It certainly does not benefit from a $25/MTok advisor model that gets consulted on 84% of calls and adds nothing.

**Haiku is the only defensible choice for enrichment.** Everything else is paying more for the same output.

### 5. The most valuable finding is what NOT to buy.

The conventional wisdom: more capable model = better output. Pay more, get more.

The data says otherwise. On decomposition, Opus ($0.99) produces worse task graphs than Sonnet ($0.20). On enrichment, Opus ($3.38) produces identical output to Haiku ($0.14). The advisor pattern ($0.47-$3.62) doesn't improve on Sonnet or Haiku solo for any task type we tested.

The right question isn't "which model is most capable?" It's **"which model produces the best executable output for this specific task?"** Those are different questions with different answers.

---

## My Recommended Routing

Based on 40 benchmark runs across 8 model configurations and 4 test matrices:

```text
TASK DECOMPOSITION
──────────────────────────────────────────
PRD < 2,000 words  →  Haiku 4.5    $0.02/run   39s
PRD > 2,000 words  →  Sonnet 4.6   $0.20/run  238s
Never              →  Opus 4.6     (over-structures)
Never              →  Advisor      (cost without benefit)

TASK ENRICHMENT
──────────────────────────────────────────
All complexity     →  Haiku 4.5    $0.14/run   49s
Never              →  Advisor      (interferes or wastes)
Never              →  Opus/Sonnet  (24x cost, identical output)
```

**Projected savings vs. uniform Sonnet:** 62% on simple PRDs, 30% on enrichment.

**Projected savings vs. uniform Opus:** 96% on simple PRDs, 96% on enrichment.

---

## What This Means For You

If you're running Opus everywhere because "it's the best," you're likely paying 5-24x more than necessary on the majority of your pipeline. 

The data shows that, at least for task decomposition and enrichment, there's a quality ceiling that cheaper models already hit.

I plan on testing building next, but this was a fascinating result.

**The expensive model isn't always the best model. Sometimes it's the worst.**

---

*This study was conducted using my's proprietary benchmarking infrastructure, built on Loom, which is a tool that helps me manage complex projects across sessions and track ideas for future improvements.*

<blockquote>

## Methodology Notes

**Benchmark infrastructure:** Custom Python framework using async orchestration, Pydantic data models, and Testcontainers for isolated Postgres + Redis per run. Snapshots freeze decomposition output for independent enrichment benchmarking.

**Advisor integration:** Anthropic's `advisor_20260301` server-side tool, configured with `anthropic-beta: advisor-tool-2026-03-01` header. Advisor token usage tracked separately via `skill_runs` table metadata extraction.

**Scoring normalization:** Quality, cost, and speed are independently scored and composited (55/25/20 weighting). Cost and speed baselines are per-PRD to account for inherent complexity differences.

**Limitations:**

- Two PRD fixtures (simple and complex). Results may vary on different domains or intermediate complexity.

- Single run per variant. Statistical significance requires multiple runs per configuration.

- Advisor performance on agentic coding tasks (SWE-bench-like work) was not tested and may differ significantly.

</blockquote>
