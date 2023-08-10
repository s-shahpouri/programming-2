import json
import linecache
import matplotlib.pyplot as plt
import pandas as pd
import yaml
from csv_convertor_extended import Reader
from csv_convertor_extended import DataObserver
import time


class AverageYear:
    def __init__(self, reader):
        self.reader = reader
        self.temperatures = []

    def update(self):
        data = self.reader.get_lines()
        if data:
            for entry in json.loads(data):
                year = int(entry['Year'])
                annual_mean_temp = float(entry['J-D'])
                self.temperatures.append((year, annual_mean_temp))
            self.plot_average()

    def plot_average(self):
        if not self.temperatures:
            return
        years, temps = zip(*self.temperatures)
        plt.plot(years, temps)
        plt.xlabel('Year')
        plt.ylabel('Average Temperature Anomaly')
        plt.title('Average Yearly Temperature Anomaly')
        plt.show()


class AverageMonth:
    def __init__(self, reader):
        self.reader = reader
        self.temperatures = []
        self.month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def update(self):
        data = self.reader.get_lines()
        if data:
            for entry in json.loads(data):
                year = int(entry['Year'])
                monthly_temps = [float(entry[month])
                                 for month in self.month_names]
                self.temperatures.append((year, monthly_temps))
            self.plot_telorance()
            self.plot_average_per_month()


# Create a single instance of Reader
reader = Reader('C:\zshahpouri\programming 2\config.yml')

# Create instances of consumers
observer = DataObserver(reader)
average_year = AverageYear(reader)
average_month = AverageMonth(reader)

# Add the observer to the reader
reader.add_observer(observer)

# Start the loop to read and process data
while True:
    reader.notify_observers()
    time.sleep(5)
