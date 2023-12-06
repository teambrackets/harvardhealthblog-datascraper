import csv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Create a directory to store the text files
if not os.path.exists("harvard_health_articles"):
    os.makedirs("harvard_health_articles")

# Create a set to store unique links
unique_links = set()

# Function to scrape and save an article
def scrape_and_save_article(link, filename):
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the <div> with class "max-w-md-lg mx-auto"
        article_div = soup.find("div", class_="max-w-md-lg mx-auto")

        # Ignore the <div> with class "inline-ad not-prose"
        if article_div:
            for div in article_div.find_all("div", class_="inline-ad not-prose"):
                div.decompose()

            # Extract text from the article and save it to a .txt file
            with open(filename, "w", encoding="utf-8") as file:
                file.write(article_div.get_text())
        else:
            print(f"No article content found for {link}")
    else:
        print(f"Failed to retrieve {link}. Status code: {response.status_code}")

# Read the links from the CSV file and scrape each article
with open("harvard_health_links.csv", "r", newline="", encoding="utf-8") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        link = row[0]  # Get the link from the single column

        # Check if the link has a valid scheme (http:// or https://)
        parsed_url = urlparse(link)
        if parsed_url.scheme and parsed_url.netloc:
            # Check if the link is not in the set of unique links
            if link not in unique_links:
                filename = f"harvard_health_articles/article_{len(unique_links) + 1}.txt"
                scrape_and_save_article(link, filename)
                unique_links.add(link)
        else:
            print(f"Invalid link: {link}")

# Write unique links to a new CSV file
with open("unique_harvard_health_links.csv", "w", newline="", encoding="utf-8") as unique_csvfile:
    csv_writer = csv.writer(unique_csvfile)
    for link in unique_links:
        csv_writer.writerow([link])

print("Scraping completed, and unique articles saved in 'harvard_health_articles' directory.")
print("Unique links saved in 'unique_harvard_health_links.csv'.")
