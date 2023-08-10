import json
import linecache
import yaml


class CsvConverter:
    """This class converts CSV data to JSON."""

    def __init__(self, header):
        # Here we're setting the keys of our CSV data by splitting
        # the first line of the CSV on commas.
        self.header = header

    def csv_to_json(self, csv_lines):
        # This method takes a list of CSV lines (strings)
        # and converts them to JSON.
        json_data = []
        for line in csv_lines:  # Looping over the CSV lines
            values = line.strip().split(',')  # Spliting each line into values

            # Checking if the number of keys matches the number of values
            # If not, we print a warning and skip this line
            if len(values) != len(self.header):
                print("Warning: numbers of keys and values don't match in line:", line)
                continue

            # Creating dictionary from keys and values using the zip function
            data_dict = dict(zip(self.header, values))

            # Converting dictionary to a JSON string and add it to our list
            json_data.append(data_dict)
        return json.dumps(json_data, indent=2)


class Reader:
    ''' This class and previous class reads a CSV file and returns a JSON string.'''

    def __init__(self, config_path='config.yml'):
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)

        self.file_path = config.get('csv_file_path', 'dSST.csv')
        self.stride = config.get('stride', 5)

        self.line_number = 2  # Start from the second line (data rows)
        with open(self.file_path, 'r') as file:
            header = file.readline().strip().split(',')
        self.converter = CsvConverter(header)

    def get_lines(self):
        lines = []
        for _ in range(self.stride):
            line = linecache.getline(self.file_path, self.line_number)
            if not line:
                break  # No more lines to read
            lines.append(line)
            self.line_number += 1
        if lines:
            return self.converter.csv_to_json(lines)
        else:
            return ''


# Example usage
red = Reader('C:\zshahpouri\programming 2\config.yml')
print(red.get_lines())  # Returns lines 2-6 as JSON
print(red.get_lines())  # Returns lines 7-11 as JSON
print(red.get_lines())  # Returns lines 12-16 as JSON
