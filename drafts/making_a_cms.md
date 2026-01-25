---
title: Making a CMS
date: 2026-01-25
tags: #cms #python #webdev
meta: Education and Promotion in a single package
published: True
---

# Making a CMS

I was recently watching a video about vibecoding where they said that you really needed to use a model for a year before you got to the point where you could trust it. 

Of course, I haven't been vibecoding for a year, but I want to get better at it. 

Also, like basically everyone else in my field, I had the idea of making a personal website where I could put information about my work, my work history, and then have a blog that wasn't owned by the corporate overlords. 

So I decided to make a CMS for my blog. 

## Defining Insanity

But WHY you might ask? Wordpress is right there!

Sure, it is, but Wordpress has a lot of drama I don't want to deal with. I also want something that is lightweight and simple. 

In fact, if I could create something that uses Markdown for writing, that would be perfect. 

Yes, I am aware of Hugo. 

The problem with Hugo is that it has a lot of templates to configure and I quickly got lost in trying to pick the perfect theme but none of them felt right. So if I can't find the perfect theme, why not try and create something from my own?

## Defying Gravity
This blog is the output of one snowy afternoon, Google's Antigravity platform, and a lot of coffee. 

Antigravity is an IDE that lets you interact with agents (Mostly Gemini 3) and built whatever you prompt. 

The tool is actually pretty cool, but every time I've used it in the past I ended up creating proof of concept web apps that I run locally so I wanted to see if I could build something. 

## The Process

I started with the homepage. I wanted something that would be simple, but still show that at my core, I really am embracing the developer mindset.

I also knew that I wanted to use (mostly) HTML and CSS for the front end and then Python for the back end because It was what I was most familiar with. 

Once I had something that I liked for the homepage, I moved onto the other main pages. My About page is just a resume (I will be adjusting this later) while my "Work" is still a work in progress because I am not sure how I want to show off stuff there yet. 

## Making the Blog

The blog was the hardest part of this project, but the most fun. I wanted to create a system that would allow me to write in markdown (like now) but then convert everything to a static HTML page AND have a blogroll that users could scroll through that looked like fancy cards. 

This is where the python came in. How it works right now is like this:

* I write in markdown in a specific drafts folder. this folder is part of the .gitignore locally so that it won't get shared before I am ready.
* When I am ready to publish, I tag the frontmatter with `published: True` and then run the publish.py script.
* The publish script will then convert the markdown to HTML and then move it to the blog folder.
* Then, I have another script that will update the blog_posts.js file with the new post. This is how the Blogroll is populated.
* Finally, the last script will publish the changes to GitHub which should push my content to Cloudflare where you can see it. This is the last stage I have to verify wish me luck. 

>But Isn't this just reinventing the wheel?

Yes, yes it is. 

If I just wanted a website, I could use a CMS like Wordpress or even a static site generator like Hugo. 

But I want to learn. I need to be more comfortable with how Agents work so that I know how to instruct them in the future. This isn't Yegge's Gastown, but I am pretty Damn proud of it.