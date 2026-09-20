---
title: "Why I Started Using AI Seriously In 2026"
date: "January 25, 2026"
pubDate: 2026-01-25
tags: ['ai', 'vibecoding', 'gemini', 'claude']
crosspost: false
type: "Project"
summary: "I used AI for the better part of 2025 because I had to understand it for work. Here is why that changed in 2026 and what I learned about treating prompts as instruction manuals."
reading_time: 12
---

## AI Was Just Something I Did For Work In 2025

I used AI for the better part of 2025 because I had to understand it for work. 

I got Gemini Pro when I bought my phone and spent a few hours here and there messing around with it, but never as something I would turn to first. 

When they announced a new model I'd run my tests:

- **For Writing:** Make a Sonnet about a hot dog in iambic pentameter (Gemini 3 Pro was the first "Good" one)

- **For Images:** Make The Philly Phanatic (Spoiler, still struggles with this one)

But after I ran my tests, or asked it a few questions to see how it responded, I'd go back to normal search, and be on my way. 

I wrote some POVs on AI Mode and AI Overviews, but didn't really see myself turning to them unless I was researching something for work.

> [!NOTE]
> For Those Short On Time
> I know that not everyone has the time to read my ramblings so here's the core argument:
> - A Prompt should be treated as an instruction manual, not a question
> - Vibe Coding is like playing a video game you love on a higher difficulty settings, but with better gear
> - If you're considering models: Gemini has the most generous free/cheap plans, Claude is worth the hype.

## I Got (And Still Get) Annoyed By AI Being Shoved Everywhere

I think one of the reasons it took be a bit to warm up to AI was that I couldn't escape it.

- Open my text app? AI
- Open LinkedIn? AI
- Open Outlook at work? Search still sucks, but now it sucks **WITH AI**

There's some things that AI is great for, but there's a lot where it feels like they just tacked it on to add "value" without thinking how to make it useful. 

Between these "features" and trying to use AI as just a glorified search engine, it's not surprising that I was skeptical of AI for most of last year. 

## Gemini Gems (Agents) Changed My View Of What AI Could Do

So, what changed? Gems

> [!TIP]
> Gemini Gems | TLDR
> Gems are custom prompts that you can save with specific instructions on what the AI should do, what information it needs to consider, and how it should respond.
> 
> Other AI Tools offer something similar, but most refer to them as "Agents." Agents can be more powerful, but the concept is the same

If you want more, you can keep reading. Otherwise skip to "Dipping My Toes In Vibe Coding"

## Prompts Matter | Gems SR:PW

> [!IMPORTANT]
> Treat Prompts As Instruction Manuals, Not Questions

When I first started working with AI, I treated it like a verbose search. I could just stream of thought a question to the model, and it would do the rest. 

I was wrong.

A prompt isn't a question. Sure, It can be. But it's a bit like hopping in your car to go to your neighbors. Using an AI for a simple question is overkill. 

If you're going to ask the AI a question, really ask it a question. Don't just say "pizza near me." 

You can use search for that and get the same (likely still better!) results. So you ask "I want places that offer gluten free pizza near me that are known for being heavy on the cheese application"

You're not just asking a question, you're giving the model more constraints over what you'll accept as an answer.

An agent, or a Gem, is an **Instruction Manual** for the AI. You can get really detailed, telling it not only what to look for, but also how to look and what kind of information you expect in return. 

### How To Build An Effect Agent Or Gem

There's not a perfect way to construct a gem/agent because it can vary based on the agent you're using, how you process information, and what you want it to do. I can just describe what works for me and leave it at that. 

Very broadly, an agent needs a few key items:

* Description/Role

* Steps to complete in task

* Rules to follow

* The output you want

* (optional) Next steps

Depending on your ask, these can be small or massive sections.

#### Description

This is a short summary of why the agent/gem exists. Something like "This tool can write content in my brand's voice and format it in a way that is easy to copy into my CMS" can be enough. 

The goal isn't to give a grand vision, but just a TLDR. The rest of the content gives you what you need.

#### Steps To Complete The Task

This is where you need to specify how the bot responds. 

* What kind of information are you going to give it? A link? Text? Code?

* What should it do with that information? QA/Edit/Research?

More complex asks will require more complex task lists. Think of these like an `order of operations` for the model.

#### The output you Want

Now you tell the agent/gem how you want its answer. 

* Do you want it to be brief or explain it's reasoning?

* If it's making code, do you want it in JS or Python?

* If you're getting text, do you want it as a markdown file?

#### Optional - Make Some Followups

This, to me, is one of the most powerful features of a model. You can define pre-defined follow ups so if you find yourself doing something after you get the output a lot, give it an option. 

In gemini, these look like this: 

```text
## Follow Ups
After providing an answer, give users a couple of recommended next steps they can take
* **/polish** - Create a high level executive summary of the content with the target for a non-technical CMO. Include a 90 day action plan
* **/visualize** - Use Nano Banana Pro To Turn The Core Argument into an image that can be inserted into a slide deck
* **/compare** - Provide another argument and have the agent provide the same logic to the process, identifying strengths and weaknesses and showing who is better on the merits
```

When you get a response, the model will give you these options and you can continue the conversation. 

One cool thing I've noticed is that 

#### A Great Prompt Is Never Final

Making a good agent, especially your FIRST good one, will take time. 

==**A lot of time.** ==

Then you'll use it and LOVE the output, until you start thinking of ways to improve it. 

My most used gems are updated and rewritten frequently. I'll notice them making a mistake over and over, or I'll think of a new way to augment them to make them more powerful. 

Agents actually excel at helping to improve their own code. If you notice a flaw, ask them questions about it, get them to explain their logic and improve it. Then ask how they would rewrite their prompt so the issue isn't made again. 

## Vibe Coding Helped Me Code Outside Of Work Again

I didn't start coding until I started working at my current company. 

That's a lie, I used to program my TI-83+ in High school because I hated remembering the Physics formulas, but outside of that brief experimentation, the most advanced I got with programming was adjusting some HTML on Myspace in college.

When I started at my current job, we had a couple of defunct python tools that no one knew how to fix, so I brute forced them to get them working again. 

And I loved it.

Coding is like building legos, or getting your base in a video game functioning perfectly. 

I had all these aspirations of getting better at coding and building cool stuff outside of work. 

But when I got outside of work, I didn't have the drive to code.

At work, I spent my time understanding the ins and outs of the stuff I needed to do for my job, and so when I clocked out, I wanted to do something totally different but researching new things felt like work. 

Late last year, I started Vibe coding. 

The thrill of getting something functional cannot be overstated, but what I really liked is that after I got something working I could ask **WHY**.  I think I've spent more time adjusting the code and working on features and corrections than I have building new things and I love it. 

Now, coding is almost like a game. 

I don't claim to be an expert. I will *NEVER* claim that something I've vibe coded is "Entirely mine."  I have the ideas, but everything else is collaborative. 

I want to write more about this (and yes, about the ethics of AI more broadly) later, so I'll leave it at this:

Before I started vibe coding I had the DESIRE to code and the desire to write. Now I am doing both. This blog, and all it's rambling, will always be 100% me unless you see a big flashing warning telling you otherwise. 

## This All Sounds Interesting, Jason, How Can I Start?

The easiest way to start is just pick a model and start experimenting with it. There are tools out there that promise to give you access to EVERY model out there, but if you're going to try something, the cheapest way is usually through the platforms provided by the company itself.

### Gemini Offers The Cheapest Way To Try Using Agents

The free Gemini account (anyone with a Gmail can get it) offers access to Gems, so you can start messing around with creating agents. 

They also allow you to use Antigravity and AI Studio, two of their vibe coding tools, on their free plan, though usage is pretty limited.

If you DO go with them, their entry level AI is $20 a month or $200 a year. But it comes with 2TB of plan storage and you can share that AI with others on your plan (though I believe you also share usage)

Talking to Gemini is like talking to Google. Stuff like BOOLEAN scripts and JSON entry can help you give detailed instructions to your model, improving your 

#### How To Access

- Google - Google Search and AI Mode use a modified version of Gemini
- gemini web app (gemini.google.com) - This is where you can get gems
- AI Studio - create simple apps and tools using Gemini
<li>AntiGravity - Download this to build using an agent-first development model 

- As an aside: This also provides (limited) access to Claude models so you can try them here!

</li>
- Gemini CLI - Terminal application for your computer

#### Things To Think About

`Pros:` 

* Generous Free Tier (Can use all tools for free) and some really nice secondary benefits if you subscribe (2TB of storage, sharing plan, etc). 

* Nano Banana Pro (Image generation) is seriously top notch. 

* Email chain summaries genuinely useful

`Cons:`

* When you want to start seriously coding, Gemini can fight you a bit on context. What I mean is that you have to be **Very** specific about what you want Gemini to do because when it decides to do something, it can go off the rails. 

* Specificity Loop: If you're adapting your prompts using a single problem, the prompt can get overly specific and start missing details when you try something new.

### Claude Is An Exponential Improvement, But You Pay For It

I am relatively new to Claude. I had Gemini pro for a year and about 2-3 months of active usage. I have a week of usage under my belt for Claude so take that into consideration. 

But holy crap is it a big difference. 

Claude allows you to chat with it for free, but to do anything serious with it, you'll need to pay. But what do you get for paying?

Gemini feels like you're using old school search. It is VERY powerful, but left to it's own devices (especially 3 pro) it will start pulling in some wild stuff that isn't related to your core project. 

Opus is the most powerful model that Claude offers. Like Gemini, it will do thinking and suggest stuff that you didn't initially ask for, but these things are **much** more likely to be on task. 

#### How To Access

<li>Through the web (Claude.ai) - Free with an account

- Pro users can access Claude Code through their browser, as long as they're interacting with projects on Github

</li>
<li>Claude Code - Must Pay for an account (Accounts are $20,100,200 per month)

- This is a Command Line interface 

</li>
<li>Claude Cowork - Must pay for an account

- This is a more user friendly interact to automate tasks on your desktop

</li>

#### Things to think about

`Pros`

* Extremely effective for coding

* Models seem to understand context more and are less likely to drive (though they still need hand holding)

* If you use the command line tool, I think that Claude is better than Gemini's offering

`Cons`

* You need a paid account to do any of the coding

* You can run out of our usage *really* easily, especially if you use Opus for everything. (you don't need opus for everything)

* Because of how Claude works, it's very easy to get ahead of yourself with a plan. So back up often

### But what about Open AI, Grok, etc?

Grok is owned by a Nazi, OpenAI's cofounder is the biggest contributor to Donald Trump. No AI company is without blame, but there should be some standards.

### Ok but what about open source models?

Open source models are great! I plan on researching them more. But they're not going to be as easy to get started with if you're just exploring AI, so don't start there. If you want a challenge, by all means, but if you want a quicker jumping off point, do Gemini or Claude.
