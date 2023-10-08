import requests
from bs4 import BeautifulSoup
import csv
import os

# Define the base URL and starting page number
base_url = "https://www.health.harvard.edu/blog"
page_number = 1

# Create a CSV file to store the links
csv_file = open("harvard_health_links.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Page Number", "Link"])

while page_number <= 122:
    # Construct the URL for the current page
    url = f"{base_url}?page={page_number}"
    
    # Send an HTTP GET request
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the <div> element with class "mt-16"
        div_element = soup.find("div", class_="mt-16")
        
        # Find all links within the <div> element
        if div_element:
            links = div_element.find_all("a")
            
            # Extract and save the links to the CSV file
            for link in links:
                link_url = link.get("href")
                if link_url and link_url.startswith("https://www.health.harvard.edu/blog"):
                    csv_writer.writerow([page_number, link_url])
        
        # Move to the next page
        page_number += 1
    else:
        print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")

# Close the CSV file
csv_file.close()

print("Scraping completed and links saved to 'harvard_health_links.csv'.")

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

# Directory where the .txt files are located
directory = "harvard_health_articles"

# List all .txt files in the directory
txt_files = [file for file in os.listdir(directory) if file.endswith(".txt")]

# Sort the files based on their page number (assuming the filenames are in the format "article_{page_number}.txt")
txt_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

# Output file to store the compiled content
output_file = "compiled_articles.txt"

# Function to compile the content of all .txt files
def compile_txt_files(txt_files, output_file):
    with open(output_file, "w", encoding="utf-8") as output:
        for txt_file in txt_files:
            file_path = os.path.join(directory, txt_file)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                output.write(content)
                output.write("\n\n")

# Compile the .txt files into a single file
compile_txt_files(txt_files, output_file)

print(f"Compilation completed. Compiled articles saved in '{output_file}'.")
