import json
import yaml
import time


class CsvConverter:
    """This class converts CSV data to JSON."""

    def __init__(self, header):
        self.header = header

    def csv_to_json(self, csv_lines):
        json_data = []
        for line in csv_lines:
            values = line.strip().split(',')
            if len(values) != len(self.header):
                print("Warning: numbers of keys and values don't match in line:", line)
                continue
            data_dict = dict(zip(self.header, values))
            json_data.append(data_dict)
        return json.dumps(json_data, indent=2)


class Reader:
    def __init__(self, config_path='config.yml'):
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)

        self.file_path = config.get('csv_file_path', 'dSST.csv')
        self.stride = config.get('stride', 5)

        self.line_number = 2  # Start from the second line (data rows)
        with open(self.file_path, 'r') as file:
            header = file.readline().strip().split(',')
        self.converter = CsvConverter(header)
        self.observers = set()

    def get_lines(self):
        lines = []
        with open(self.file_path, 'r') as file:
            for _ in range(self.line_number, self.line_number + self.stride):
                line = file.readline()
                if not line:
                    break
                lines.append(line)
        self.line_number += len(lines)
        if lines:
            return self.converter.csv_to_json(lines)
        else:
            return ''

    def add_observer(self, observer):
        self.observers.add(observer)

    def remove_observer(self, observer):
        self.observers.discard(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()

# Observer class


class DataObserver:
    def __init__(self, reader):
        self.reader = reader

    def update(self):
        data = self.reader.get_lines()
        if data:
            print("New data is available:", data)


if __name__ == "__main__":
    # Example usage
    red = Reader('C:\zshahpouri\programming 2\config.yml')
    observer = DataObserver(red)
    red.add_observer(observer)

    while True:
        red.notify_observers()
        time.sleep(5)
