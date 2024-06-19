import httpx
import asyncio
import time
import feedparser
from bs4 import BeautifulSoup
from config import site_list
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from datetime import datetime, timezone
import logging
import html

logging.disable(logging.INFO)


class Article:
    def __init__(self, title, link, source, logo, publication_date, tags=None, preview_image="", article_content=""):
        if tags is None:
            tags = set()
        self.title: str = html.unescape(title)
        self.sourceName: str = source
        self.sourceLogo: str = logo
        self.article_link: str = link
        self.preview_image: str = preview_image
        self.publicationDate: datetime = datetime.strptime(publication_date, '%a, %d %b %Y %H:%M:%S %z').astimezone(
            timezone.utc)
        self.article_content: str = article_content
        self.tagList: list = tags


async def get_article(site, entry, client):
    article = Article(entry['title'], entry['link'], site['name'], site['logo'], entry['published'])
    page = await client.get(article.article_link)
    soup = BeautifulSoup(page.content, 'lxml')

    for link in entry['links']:
        if 'image' in link['type']:
            article.preview_image = link['href']


    if 'delete_tags' in site:
        for tag in site['delete_tags']:
            for k in soup.findAll(tag.split("_")[0], class_=tag.split("_")[1]):
                k.decompose()
    try:
        article.article_content = soup.select(site['content_selector'])[0]
    except Exception as e:
        print(e)
        pass

    if 'additional_tags' in site:
        article.tagList = site['additional_tags']

    if 'tags_selector' in site:
        tags_list = [x.text.strip() for x in (soup.select(site['tags_selector'])[0]).findChildren()]
        article.tagList = article.tagList+tags_list

    return article


async def get_articles(site, client):
    site_articles = []
    tasks = []
    site_start_time = time.time()
    print("parsing started:", site['name'])

    try:
        resource = await client.get(site['link'])
    except:
        print("parsing error:", site['name'],", time:", time.time() - site_start_time)
        return []

    if resource.status_code == 200:
        feed = feedparser.parse(resource.text)
        for entry in feed.entries:
            tasks.append(asyncio.ensure_future(get_article(site, entry, client)))

        responses = await asyncio.gather(*tasks)
        for response in responses:
            site_articles.append(response)
    print("parsing ended:", site['name'],", time:", time.time() - site_start_time)

    return site_articles


Articles = []


async def main():
    start_time = time.time()

    async with httpx.AsyncClient() as client:
        tasks = []
        for site in site_list:
            tasks.append(asyncio.ensure_future(get_articles(site, client)))

        responses = await asyncio.gather(*tasks)
        for response in responses:
            Articles.extend(response)

    end_time = time.time()
    print("Time overall", end_time - start_time)


asyncio.run(main())

engine = create_engine("sqlite+pysqlite:///instance/news_aggregator.db", echo=True)


print('Committing to database')
start_time = time.time()
with engine.connect() as conn:
    for article in Articles:
        try:
            conn.execute(
                text(
                    f"""
                    INSERT INTO articles (title, article_link, source_logo, source_name, preview_image, publication_date, article_content, tag_list)
                    VALUES (:x1, :x2, :x3, :x4, :x5, :x6, :x7, :x8)
                    """),
                [{"x1": article.title, "x2": article.article_link, "x3": article.sourceLogo, "x4": article.sourceName,
                  "x5": article.preview_image, "x6": article.publicationDate, "x7": str(article.article_content),
                  "x8": str(article.tagList)}],
            )
            conn.commit()
        except sqlalchemy.exc.IntegrityError:
            pass
end_time = time.time()

print("Committing complete, time:", end_time - start_time)
