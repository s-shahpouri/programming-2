# A program that downloads the first ten articles that cite a given Pubmed ID in parallel.

# libraries
import ssl
from Bio import Entrez
import multiprocessing as mp
import os
import time
import yaml

# Yup, much better

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config


config = load_config('config.yml')
Entrez.email = config['email']
Entrez.api_key = config['api_key']


# This is required to avoid SSL error
ssl._create_default_https_context = ssl._create_unverified_context


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
            file.write(handle.read().decode('utf-8'))
    except Exception as e:
        print(f"An error occurred with article {article_id}: {e}")


def download_articles(pubmed_id, parallel):
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

        if parallel:
            with mp.Pool(10) as p:  # the Pool size: 10 for 10 parallel processes
                p.map(fetch_article, references[:10])
        else:
            for article_id in references[:10]:
                fetch_article(article_id)

    except Exception as e:
        print(f"An error occurred: {e}")


# id of the article to be processed
pubmed_id = "30049270"


def main():
    start_time = time.time()
    print(f"Processing article {pubmed_id}...")
    method = input("Choose method (1 for parallel, 2 for non-parallel): ")

    if method == "1":
        download_articles(pubmed_id, parallel=True)
    elif method == "2":
        download_articles(pubmed_id, parallel=False)
    else:
        print("Invalid choice. Please choose 1 for parallel or 2 for non-parallel.")
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


if __name__ == "__main__":
    main()

# did you notice any differences in performance?