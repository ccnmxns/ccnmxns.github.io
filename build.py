"""Build the site: python3 -m pip install -r requirements.txt && python3 build.py"""
from pathlib import Path
from datetime import date
from html import escape
import re
import shutil
import markdown
ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)
shutil.copytree(ROOT / 'assets', DIST / 'assets', dirs_exist_ok=True)
home = (ROOT / 'templates/home.html').read_text()
style = home.split('<style>')[1].split('</style>')[0]
style += '\n.article{padding-top:45px}.article h1{font-size:clamp(30px,5vw,44px);margin:20px 0}.article h2{font-size:23px;text-transform:none;letter-spacing:-.02em;color:var(--ink);margin:35px 0 15px}.article h3{font-size:19px}.article pre{background:#eceee6;padding:20px;overflow-x:auto;border:1px solid var(--line);border-radius:4px;font-size:13px;line-height:1.65}.article :not(pre)>code{background:#eceee6;padding:2px 5px;overflow-wrap:anywhere}.article img{max-width:100%}.post{display:block;padding:22px 0;border-bottom:1px solid var(--line);text-decoration:none}.post h3{font-size:20px;font-weight:500;line-height:1.4;margin:5px 0 8px}.post:hover h3{text-decoration:underline;text-underline-offset:4px}.post p{color:var(--muted);font-size:15px}.post:last-child{border-bottom:0}'
posts=[]
for source in (ROOT/'content/posts').glob('*.md'):
    text=source.read_text()
    match=re.match(r'^---\n(.*?)\n---\n(.*)$',text,re.S)
    if not match: raise ValueError(f'{source.name}: expected front matter')
    meta=dict(line.split(':',1) for line in match[1].splitlines() if ':' in line)
    meta={k.strip():v.strip() for k,v in meta.items()}
    if meta.get('draft','false').lower()=='true': continue
    for field in ('title','date','summary'):
        if not meta.get(field): raise ValueError(f'{source.name}: missing {field}')
    date.fromisoformat(meta['date'])
    if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',source.stem): raise ValueError('Use lowercase hyphenated filenames')
    meta.update(slug=source.stem,body=markdown.markdown(match[2],extensions=['fenced_code','tables','sane_lists']))
    posts.append(meta)
posts.sort(key=lambda p:(p['date'],p['slug']),reverse=True)
blogdir=DIST/'blog'
if blogdir.exists(): shutil.rmtree(blogdir)
blogdir.mkdir()
def page(title,content,description):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} — Carlos Cañellas</title><meta name="description" content="{escape(description,quote=True)}"><style>{style}</style></head><body><header><a class="wordmark" href="/">/ccnmxns</a><nav aria-label="Main navigation"><a href="/#pometa">Pometa</a><a href="/#about">About</a><a href="/blog/" aria-current="page">Blog</a><a href="/#links">Links</a></nav></header><main id="main">{content}</main><footer><span>© {date.today().year} Carlos Cañellas</span><span>Keep it simple.</span><a href="/#support">Support me on Ko-fi ↗</a></footer></body></html>'
def card(p):
    return f'<a class="post" href="/blog/{p["slug"]}/"><time class="date" datetime="{p["date"]}">{date.fromisoformat(p["date"]).strftime("%d %B %Y")}</time><h3>{escape(p["title"])} ↗</h3><p>{escape(p["summary"])}</p></a>'
for p in posts:
    folder=blogdir/p['slug'];folder.mkdir()
    content=f'<article class="article"><a class="small" href="/blog/">← All posts</a><h1>{escape(p["title"])}</h1><p class="date"><time datetime="{p["date"]}">{date.fromisoformat(p["date"]).strftime("%d %B %Y")}</time> · Carlos Cañellas</p>{p["body"]}</article>'
    (folder/'index.html').write_text(page(p['title'],content,p['summary']))
listing=''.join(card(p) for p in posts) or '<p>No posts yet.</p>'
(blogdir/'index.html').write_text(page('Blog','<div class="article"><p class="label">Notes from the terminal</p><h1>Blog.</h1><p class="intro">Things I learn, build, and figure out along the way.</p>'+listing+'</div>','Notes on Linux, infrastructure, and platform engineering.'))
section='<section id="blog"><h2>03 / Blog</h2>'+''.join(card(p) for p in posts[:3])+'<p class="small" style="margin-top:20px"><a href="/blog/">All posts →</a></p></section>'
(DIST/'index.html').write_text(re.sub(r'<!-- BLOG_START -->.*?<!-- BLOG_END -->',lambda _:section,home,flags=re.S).replace('</style>',style[len(home.split('<style>')[1].split('</style>')[0]):]+'</style>',1))
print(f'Built homepage, blog index, and {len(posts)} post(s).')
