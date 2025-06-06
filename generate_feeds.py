import frontmatter
from feedgen.feed import FeedGenerator
from pathlib import Path
import markdown
import json
import datetime
from dateutil.parser import parse as parse_date
from dateutil.tz import UTC
from collections import defaultdict

SITE_URL = "https://cooldocs.dev/blog"
AUTHOR = "pfd"
POSTS_DIR = Path("docs/posts")
OUTPUT_DIR = Path("docs/_generated_feeds")
CATEGORY_PAGE_DIR = Path("docs")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

fg_rss = FeedGenerator()
fg_atom = FeedGenerator()
for fg in (fg_rss, fg_atom):
    fg.id(SITE_URL)
    fg.title("Cool Docs Blog")
    fg.link(href=SITE_URL, rel='alternate')
    fg.description("Updates from pfd's doc lab")
    fg.language("en")

posts = []
for path in POSTS_DIR.glob("*.md"):
    print(f"Processing: {path}")
    post = frontmatter.load(path)
    html = markdown.markdown(post.content)

    raw_date = post.get("date", datetime.datetime.now().isoformat())
    parsed_date = parse_date(str(raw_date))
    if parsed_date.tzinfo is None:
        parsed_date = parsed_date.replace(tzinfo=UTC)

    categories = post.get("categories", [])
    if isinstance(categories, str):
        categories = [categories]

    data = {
        "title": post.get("title", path.stem),
        "author": post.get("author", AUTHOR),
        "date": parsed_date,
        "tags": post.get("tags", []),
        "categories": categories,
        "url": f"{SITE_URL}/{path.stem}/",
        "content_html": html,
        "source": str(path)
    }
    posts.append(data)

posts.sort(key=lambda p: p["date"], reverse=True)

# === Main RSS and Atom feeds ===
for post in posts:
    for fg in (fg_rss, fg_atom):
        fe = fg.add_entry()
        fe.id(post["url"])
        fe.title(post["title"])
        fe.link(href=post["url"])
        fe.author(name=post["author"])
        fe.pubDate(post["date"])
        fe.description(post["content_html"])
        for tag in post["tags"] + post["categories"]:
            fe.category(term=tag)

fg_rss.rss_file(OUTPUT_DIR / "rss.xml")
fg_atom.atom_file(OUTPUT_DIR / "atom.xml")

# === JSON + HTML feeds ===
with open(OUTPUT_DIR / "feed.json", "w") as f:
    json.dump(posts, f, indent=2, default=str)

with open(OUTPUT_DIR / "feed.html", "w") as f:
    f.write("<html><head><title>Cool Docs Blog</title></head><body><h1>Cool Docs Blog</h1><ul>")
    for post in posts:
        f.write(f"<li><a href='{post['url']}'>{post['title']}</a> – {post['date'].isoformat()}</li>")
    f.write("</ul></body></html>")

print("✅ Global feeds written to:", OUTPUT_DIR)

# === Generate category listings and feeds ===
cat_map = defaultdict(list)
for post in posts:
    for cat in post["categories"]:
        cat_map[cat.lower()].append(post)

category_rst_paths = []

for cat, cat_posts in cat_map.items():
    cat_slug = cat.lower().replace(" ", "-")
    cat_feed_file = OUTPUT_DIR / f"{cat_slug}.xml"
    cat_rst_file = CATEGORY_PAGE_DIR / f"{cat_slug}.rst"
    category_rst_paths.append(cat_rst_file)

    # Generate category RSS feed
    fg = FeedGenerator()
    fg.id(f"{SITE_URL}/categories/{cat_slug}")
    fg.title(f"{cat.title()} Posts – Cool Docs Blog")
    fg.link(href=f"{SITE_URL}/categories/{cat_slug}", rel='alternate')
    fg.description(f"Posts filed under '{cat}'")
    fg.language("en")

    for post in sorted(cat_posts, key=lambda p: p["date"], reverse=True):
        fe = fg.add_entry()
        fe.id(post["url"])
        fe.title(post["title"])
        fe.link(href=post["url"])
        fe.author(name=post["author"])
        fe.pubDate(post["date"])
        fe.description(post["content_html"])
        for tag in post["tags"] + post["categories"]:
            fe.category(term=tag)

    fg.rss_file(cat_feed_file)
    print(f"🗂️  Wrote category feed: {cat_feed_file}")

    # Write category listing page
    with cat_rst_file.open("w") as f:
        f.write(f"{cat.title()} Posts\n")
        f.write(f"{'=' * (len(cat) + 6)}\n\n")
        f.write(f"RSS feed: :download:`{cat_slug}.xml <_generated_feeds/{cat_slug}.xml>`\n\n")
        for post in sorted(cat_posts, key=lambda p: p["date"], reverse=True):
            f.write(f"- `{post['title']} <{post['url']}>`__\n")

# === Generate categories.rst with toctree ===
with open(CATEGORY_PAGE_DIR / "categories.rst", "w") as f:
    f.write("Categories\n==========\n\n")
    f.write(".. toctree::\n   :maxdepth: 1\n\n")
    for path in category_rst_paths:
        f.write(f"   {path.stem}\n")

print("📁 Category pages + feeds generated.")