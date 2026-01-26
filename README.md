# _mediumroast CMS

This  is an attempt at getting better at vibe coding. 

I wanted to set up my own CMS for my site because I wanted something simple, but the theme confusion with HUGO was frustrating me and I didn't need anything more than a basic (ish) site.

## Capabilities
* The Generic pages (index, about,work, contact) are all static HTML pages
* The blog page updates to show a list of blog posts in order by publish date (newest first)
* The actual blog is fun. It will take markdown files in a .gitignore draft folder and IF the frontmater is marked "publish" will convert it to HTML
    * This should also include images, but that is a work in progress
 
## How Updating Works
There are python scripts. If you select "Deploy.py" the script will look in your drafts folder, convert any of the blogs there to HTML it needs to. 

Then it will update the menifest (the blogroll) as well as the XML sitemap with the new content

Finally it will stage and commit the changes to Github, which then gets published to my website. 

This is an entirely vibe coded project. I do not intend this CMS to be used for anything but this site. But if you wanna do something with it, have fun. 
