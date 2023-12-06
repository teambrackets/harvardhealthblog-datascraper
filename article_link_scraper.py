import requests
from bs4 import BeautifulSoup
import csv

# Define the base URL and starting page number
base_url = "https://www.health.harvard.edu/blog"
page_number = 1

# Create a set to store unique links
unique_links = set()

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

            # Extract and check for unique links
            for link in links:
                link_url = link.get("href")
                if link_url and link_url.startswith("https://www.health.harvard.edu/blog"):
                    unique_links.add(link_url)

        # Move to the next page
        page_number += 1
    else:
        print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")

# Create a CSV file to store the unique links
csv_file = open("harvard_health_links.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Link"])

# Write the unique links to the CSV file
for link in unique_links:
    csv_writer.writerow([link])

# Close the CSV file
csv_file.close()

print("Scraping completed, and unique links saved to 'harvard_health_links.csv'.")
