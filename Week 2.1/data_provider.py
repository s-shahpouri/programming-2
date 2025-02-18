import pandas as pd
import yaml

# Load configuration from config.yml
with open(r'C:\zshahpouri\programming 2\config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Step 2: Create the DataProvider class


class DataProvider:
    def __init__(self):

        # Retrieve and load CSV file path from the configuration
        csv_file_path = config.get('csv_file_path')
        self.data = pd.read_csv(csv_file_path, index_col="Year")

    def get_data(self, years=None):
        if years is None:

            # Return all data as a dictionary
            return self.data.to_dict()
        elif isinstance(years, int):
            if years not in self.data.index:
                raise ValueError("Year not found")

            # Return data for a specific year as a dictionary
            return self.data.loc[years].to_dict()
        elif isinstance(years, list) and len(years) == 2:
            from_year, to_year = years
            if from_year not in self.data.index or to_year not in self.data.index:
                raise ValueError("Year range not found")

            # Return data for a range of years as a dictionary
            return self.data.loc[from_year:to_year].to_dict()
        else:
            raise ValueError("Invalid parameter")


# The configuration file (config.yml) should contain:
# csv_file_path: "C:\\zshahpouri\\programming 2\\Data\\dSST.csv"

# Note: Make sure to install the 'pyyaml' package using 'pip install pyyaml'
