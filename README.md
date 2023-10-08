# Haward-Health-Blog-Extractor
This is the python code for extracting the security advisories data from Howards Health Blog specifically

Run all code in series wrna code nhi chalinga na data milinga

follow these simple steps:
1. Run article_link_scrapper.py: scrapes all link which we have to scrape remober removing duplicates as real values are around 2900 and the value are repeated
2. Run data_scrapper_from_links.py: this code scrapes the data from the links in .csv file save all articles seperately in designated directory. Make sure you removed dupilactes from the .csv file eairlier. Afterwards you have to compile all the text in one file code given in next file
3. Run compiler.py: this code compiles all .txt file in the directory which we have scraped and you are done with the data you have scrapped the haward blog for health.

   NOw you got the data. MORE CODE FOR SCRAPING MORE HEALTH WEBSITE COMING SOONS
