# TC² Projects: VS Code + GitHub Pages (no backend)

## Files
- index.html + home.css + home.js: public showcase
- projects.html + files.js: Files page (pictures, videos, documents)
- data.js: ALL your content (projects, skills, file lists). Edit this to update the site.
- images/ videos/ docs/: put your files here. background.png, favicon.svg, CNAME: leave as is.

## Add a project or file
1. Copy the file into images/, videos/ or docs/.
2. In data.js add it to the project's files:[ ... ] list (examples at the top of data.js).
3. Test locally (VS Code > Extensions > "Live Server" > right-click index.html > Open with Live Server).
4. Commit and push (below).

## Publish with GitHub Pages
1. Install Git, then in VS Code open this folder > Source Control > Initialize Repository > Commit.
2. Create an empty public repo on github.com (e.g. tcsquared-projects). In VS Code terminal:
   git remote add origin https://github.com/YOURUSERNAME/tcsquared-projects.git
   git branch -M main
   git push -u origin main
3. GitHub repo > Settings > Pages > Source: Deploy from a branch > main / (root) > Save.
4. Pages > Custom domain: tcsquared.co.zw > Save, then tick Enforce HTTPS when available.
5. Later updates: Commit, then Sync/Push in VS Code. The site updates in about a minute.

## DNS for tcsquared.co.zw (at your registrar)
- A records for @ : 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
- CNAME for www : YOURUSERNAME.github.io
Can take minutes to 48 hours. Check GitHub's custom-domain docs if the IPs change.

## Limits
- Everything in the repo is public. Don't upload anything private.
- GitHub blocks files over 100 MB and web uploads over 25 MB. Keep repo under about 1 GB.
- For long videos, upload to YouTube (unlisted) or Google Drive and use kind:"link" in data.js.
