import ssl
from Bio import Entrez
import time


# This is required to avoid SSL error
ssl._create_default_https_context = ssl._create_unverified_context

# My mail address and NCBI API Key
Entrez.email = 'z.shahpouri@st.hanze.nl'
Entrez.api_key = 'ecb9c4efe9d8dd7d8612093defaac6eca209'


def fetch_article(article_id):
    ''' Fetches an article from PMC and saves it into a file'''
    try:
        time.sleep(1)  # Ensure NCBI's rate limit is respected
        handle = Entrez.efetch(db="pmc",
                               id=article_id,
                               rettype="full",  # Changed to "full" from "xml" for full articles
                               retmode="text",  # Changed to "text" from "xml" for full articles
                               api_key=Entrez.api_key)
        # save the article into a file
        with open(f"{article_id}.txt", 'w') as file:
            file.write(handle.read())
    except Exception as e:
        print(f"An error occurred with article {article_id}: {e}")


def download_articles(pubmed_id):
    ''' Downloads the first ten articles that cite the given pubmed id'''
    try:
        file = Entrez.elink(dbfrom="pubmed",
                            db="pmc",
                            LinkName="pubmed_pmc_refs",
                            id=pubmed_id,
                            api_key=Entrez.api_key)
        results = Entrez.read(file)
        references = [str(link["Id"]) for link in results[0]
                      ["LinkSetDb"][0]["Link"]]  # Convert to strings

        # download the first ten articles sequentially
        start_time = time.time()
        for article_id in references[:10]:
            fetch_article(article_id)
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

    except Exception as e:
        print(f"An error occurred: {e}")


pubmed_id = "30049270"


def main():
    print(f"Processing article {pubmed_id}...")
    download_articles(pubmed_id)


if __name__ == "__main__":
    main()
