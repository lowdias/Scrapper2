"""
Author: Ilias Kamal
Email: ilias.kamal@example.com
Date: March 24, 2023

Description: Scrapes news articles from a website using BeautifulSoup and stores them in a SQLite database
"""

import requests
from bs4 import BeautifulSoup
import sqlite3

# Define the URL of the news website to scrape
url = "https://www.bbc.com/news"

# Make a request to the website
response = requests.get(url)

# Parse the HTML content of the website using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the articles on the website
articles = soup.find_all("article")

# Connect to the SQLite database and create a table to store the articles
conn = sqlite3.connect("news_articles.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS articles (title TEXT, summary TEXT, url TEXT)")

# Loop through the articles and extract the title, summary, and URL
for article in articles:
    title = article.find("h3").text.strip()
    summary = article.find("p").text.strip()
    url = article.find("a")["href"]

    # Insert the data into the SQLite database
    c.execute("INSERT INTO articles (title, summary, url) VALUES (?, ?, ?)", (title, summary, url))

# Commit the changes to the database and close the connection
conn.commit()
conn.close()
