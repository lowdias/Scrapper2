"""
Author: Ilias Kamal
Email: ilias.kamal@gmail.com
Date: March 24, 2023

Description: Scrapes news articles from a website using Scrapy and stores them in a SQLite database, run "scrapy runspider scrappy_2.py" in a terminal to begin the crawl
"""

import scrapy
import sqlite3


class BBCSpider(scrapy.Spider):
    name = "bbc"
    start_urls = [
        "https://www.bbc.com/news",
    ]

    def __init__(self):
        self.connection = sqlite3.connect("articles.db")
        print(sqlite3.version)
        self.cursor = self.connection.cursor()

        # Create a table to store the articles
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            date TEXT,
            content TEXT,
            url TEXT
        )""")

    def parse(self, response):
        # Extract article links from the homepage
        for article_link in response.css("a.gs-c-promo-heading.gs-o-faux-block-link__overlay-link::attr(href)"):
            yield response.follow(article_link, self.parse_article)

        # Follow links to additional pages of articles
        for next_page in response.css("a.gs-c-pagination-button.gs-c-pagination-button--next.gs-o-button::attr(href)"):
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        # Extract the article title, author, date, and content
        title = response.css("h1.story-body__h1::text").get()
        author = response.css("div.byline__name::text").get()
        date = response.css("div.date::text").get()
        content = "\n".join(response.css("div.story-body__inner p::text").getall())

        # Store the extracted data in the database
        sql = "INSERT INTO articles (title, author, date, content, url) VALUES (?, ?, ?, ?, ?)"
        values = (title, author, date, content, response.url)
        self.cursor.execute(sql, values)
        self.connection.commit()

        # Return the extracted data as a dictionary (optional)
        yield {
            "title": title,
            "author": author,
            "date": date,
            "content": content,
            "url": response.url,
        }

    def closed(self, reason):
        self.connection.close()
