from Bio import Entrez

# the next two lines are needed to create an environment in which the
# ssl doesn't complain about non-existing public keys...
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# Step 1: provide the api key to the Entrez.email variable
Entrez.email = 'z.shahpouri@st.hanze.nl'

# Step 2: provide the search term and the database to search in
file = Entrez.elink(dbfrom="pubmed",
                    db="pmc",
                    LinkName="pubmed_pmc_refs",
                    id="30049270",
                    api_key='ecb9c4efe9d8dd7d8612093defaac6eca209')

# Step 3: read the results
results = Entrez.read(file)
print(results)
