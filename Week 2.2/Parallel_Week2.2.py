# A program that downloads the first ten articles that cite a given Pubmed ID in parallel.

# libraries
import ssl
from Bio import Entrez
import multiprocessing as mp
import os
import time


# This is required to avoid SSL error
ssl._create_default_https_context = ssl._create_unverified_context

# My mail address and NCBI API Key
# You should not have your email and api key in your repo;
# it should be in a config file.

Entrez.email = 'z.shahpouri@st.hanze.nl'
Entrez.api_key = 'ecb9c4efe9d8dd7d8612093defaac6eca209'


def fetch_article(article_id):
    ''' Fetches an article from PMC and saves it into a file'''
    try:

        # Avoid sending too many requests to NCBI
        time.sleep(1)  # Ensure NCBI's rate limit is respected

        # Fetch the article
        handle = Entrez.efetch(db="pmc",
                               id=article_id,
                               rettype="full",  # Changed to "full" from "xml" for full articles
                               retmode="xml",  # Changed to "text" from "xml" for full articles
                               api_key=Entrez.api_key)

        # save the article into a file
        with open(f"{article_id}.txt", 'w') as file:
            file.write(handle.read())
    except Exception as e:
        print(f"An error occurred with article {article_id}: {e}")


def download_articles(pubmed_id):
    ''' Downloads the first ten articles that cite the given pubmed id'''
    try:
        # Get the articles that cite the given pubmed id
        file = Entrez.elink(dbfrom="pubmed",
                            db="pmc",
                            LinkName="pubmed_pmc_refs",
                            id=pubmed_id,
                            api_key=Entrez.api_key)

        # Convert the results to a list of strings
        results = Entrez.read(file)
        references = [str(link["Id"]) for link in results[0]
                      ["LinkSetDb"][0]["Link"]]  # Convert to strings

        # download the first ten articles in parallel
        start_time = time.time()
        with mp.Pool(10) as p:  # the Pool size: 10 for 10 parallel processes

            # Download the first ten articles
            p.map(fetch_article, references[:10])
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

    except Exception as e:
        print(f"An error occurred: {e}")


# id of the article to be processed
pubmed_id = "30049270"


def main():
    print(f"Processing article {pubmed_id}...")
    download_articles(pubmed_id)


if __name__ == "__main__":
    main()
