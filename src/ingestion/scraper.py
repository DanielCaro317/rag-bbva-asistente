import json
import re
import time
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

from src.config import settings

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
SKIP_EXT = (".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",
            ".zip", ".mp4", ".doc", ".docx", ".xls", ".xlsx", ".css", ".js")


def _slug(url):
    path = urlparse(url).path.strip("/") or "index"
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", path).strip("-")
    return (slug[:120] or "index")


def _clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "nav", "footer", "header", "svg", "form"]):
        tag.decompose()
    title = soup.title.get_text(strip=True) if soup.title else ""
    lines = [ln.strip() for ln in soup.get_text(separator="\n").splitlines()]
    text = "\n".join(ln for ln in lines if ln)
    return title, text


class SiteScraper:
    def __init__(self, base_url=None, max_pages=None):
        self.base_url = (base_url or settings.scraper_base_url).rstrip("/") + "/"
        self.domain = urlparse(self.base_url).netloc
        self.max_pages = max_pages or settings.scraper_max_pages
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept-Language": "es-CO,es;q=0.9",
        })
        self.robots = self._load_robots()

    # Leemos robots.txt con la misma sesión para respetar lo que el sitio permite
    def _load_robots(self):
        rp = RobotFileParser()
        try:
            resp = self.session.get(urljoin(self.base_url, "/robots.txt"), timeout=15)
            rp.parse(resp.text.splitlines() if resp.status_code == 200 else [])
        except requests.RequestException:
            rp.parse([])
        return rp

    def _allowed(self, url):
        return self.robots.can_fetch(USER_AGENT, url)

    def _internal_links(self, base, soup):
        for a in soup.find_all("a", href=True):
            href = urljoin(base, a["href"].split("#")[0])
            if (href.startswith("http")
                    and urlparse(href).netloc == self.domain
                    and not href.lower().endswith(SKIP_EXT)):
                yield href

    def run(self):
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        CLEAN_DIR.mkdir(parents=True, exist_ok=True)
        seen, saved = set(), []
        queue = deque([self.base_url])

        while queue and len(saved) < self.max_pages:
            url = queue.popleft()
            if url in seen or not self._allowed(url):
                continue
            seen.add(url)
            try:
                resp = self.session.get(url, timeout=20)
            except requests.RequestException:
                continue
            if resp.status_code != 200 or "text/html" not in resp.headers.get("content-type", ""):
                continue

            slug = _slug(url)
            (RAW_DIR / f"{slug}.html").write_text(resp.text, encoding="utf-8")
            title, text = _clean_html(resp.text)
            (CLEAN_DIR / f"{slug}.md").write_text(f"# {title}\n\n{text}", encoding="utf-8")
            saved.append({"url": url, "slug": slug, "title": title, "chars": len(text)})

            soup = BeautifulSoup(resp.text, "html.parser")
            for link in self._internal_links(url, soup):
                if link not in seen:
                    queue.append(link)
            time.sleep(0.5)  # crawl educado

        (CLEAN_DIR / "manifest.json").write_text(
            json.dumps(saved, ensure_ascii=False, indent=2), encoding="utf-8")
        return saved


def main():
    scraper = SiteScraper()
    saved = scraper.run()
    print(f"Guardadas {len(saved)} paginas desde {scraper.base_url}")


if __name__ == "__main__":
    main()
