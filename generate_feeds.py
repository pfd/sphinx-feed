import frontmatter
from feedgen.feed import FeedGenerator
from pathlib import Path
import markdown
import json
import datetime
from dateutil.parser import parse as parse_date
from dateutil.tz import UTC

SITE_URL = "https://cooldocs.dev/blog"
AUTHOR = "pfd"
POSTS_DIR = Path("docs/posts")
OUTPUT_DIR = Path("docs/_generated_feeds")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

fg_rss = FeedGenerator()
fg_atom = FeedGenerator()
for fg in (fg_rss, fg_atom):
    fg.id(SITE_URL)  # Atom requires an ID
    fg.title("Cool Docs Blog")
    fg.link(href=SITE_URL, rel='alternate')
    fg.description("Updates from pfd's doc lab")
    fg.language("en")

posts = []
for path in POSTS_DIR.glob("*.md"):
    print(f"Processing: {path}")
    post = frontmatter.load(path)
    html = markdown.markdown(post.content)

    # Parse and normalize date
    raw_date = post.get("date", datetime.datetime.now().isoformat())
    parsed_date = parse_date(str(raw_date))
    if parsed_date.tzinfo is None:
        parsed_date = parsed_date.replace(tzinfo=UTC)

    data = {
        "title": post.get("title", path.stem),
        "author": post.get("author", AUTHOR),
        "date": parsed_date,
        "tags": post.get("tags", []),
        "categories": post.get("categories", []),
        "url": f"{SITE_URL}/{path.stem}/",
        "content_html": html,
        "source": str(path)
    }
    posts.append(data)

posts.sort(key=lambda p: p["date"], reverse=True)

for post in posts:
    for fg in (fg_rss, fg_atom):
        fe = fg.add_entry()
        fe.id(post["url"])  # Use the post URL as a globally unique ID
        fe.title(post["title"])
        fe.link(href=post["url"])
        fe.author(name=post["author"])
        fe.pubDate(post["date"])
        fe.description(post["content_html"])
        for tag in post["tags"] + post["categories"]:
            fe.category(term=tag)

fg_rss.rss_file(OUTPUT_DIR / "rss.xml")
fg_atom.atom_file(OUTPUT_DIR / "atom.xml")

with open(OUTPUT_DIR / "feed.json", "w") as f:
    json.dump(posts, f, indent=2, default=str)

with open(OUTPUT_DIR / "feed.html", "w") as f:
    f.write("<html><head><title>Cool Docs Blog</title></head><body><h1>Cool Docs Blog</h1><ul>")
    for post in posts:
        f.write(f"<li><a href='{post['url']}'>{post['title']}</a> – {post['date'].isoformat()}</li>")
    f.write("</ul></body></html>")

print("✅ Feeds written to:", OUTPUT_DIR)