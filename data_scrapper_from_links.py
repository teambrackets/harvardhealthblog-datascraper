import csv
import os
import requests
from bs4 import BeautifulSoup

# Create a directory to store the text files
if not os.path.exists("harvard_health_articles"):
    os.makedirs("harvard_health_articles")

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
    next(csvreader)  # Skip the header row
    for row in csvreader:
        page_number, link = row
        filename = f"harvard_health_articles/article_{page_number}.txt"
        scrape_and_save_article(link, filename)

print("Scraping completed and articles saved in 'harvard_health_articles' directory.")
