import json
import matplotlib.pyplot as plt
from csv_convertor import Reader


class AverageYear:
    def __init__(self, config_path='config.yaml'):
        self.reader = Reader(config_path)
        self.temperatures = []

    def calculate_average(self):
        while True:
            data = self.reader.get_lines()
            if not data:
                break
            for entry in json.loads(data):
                year = int(entry['Year'])
                annual_mean_temp = float(entry['J-D'])
                self.temperatures.append((year, annual_mean_temp))

    def plot_average(self):
        if not self.temperatures:
            return
        years, temps = zip(*self.temperatures)
        plt.plot(years, temps)
        plt.xlabel('Year')
        plt.ylabel('Average Temperature Anomaly')
        plt.title('Average Yearly Temperature Anomaly')
        plt.show()


# Create an instance of AverageYear
average_year = AverageYear('C:\zshahpouri\programming 2\config.yml')

# Calculate the average temperatures
average_year.calculate_average()

# Plot the average yearly temperature anomaly
average_year.plot_average()


class AverageMonth:
    def __init__(self, config_path='config.yaml'):
        self.reader = Reader(config_path)
        self.temperatures = []
        self.month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def calculate_average(self):
        while True:
            data = self.reader.get_lines()
            if not data:
                break
            for entry in json.loads(data):
                year = int(entry['Year'])
                monthly_temps = [float(entry[month])
                                 for month in self.month_names]
                self.temperatures.append((year, monthly_temps))

    def plot_telorance(self):
        if not self.temperatures:
            return
        years, temps = zip(*self.temperatures)
        for i, month in enumerate(self.month_names):
            monthly_avg = [temps[j][i] for j in range(len(temps))]
            plt.plot(years, monthly_avg, label=month)
        plt.xlabel('Year')
        plt.ylabel('Average Temperature Anomaly')
        plt.title('Average Monthly Temperature Anomaly')
        plt.legend()
        plt.show()

    def plot_average_per_month(self):
        if not self.temperatures:
            return
        years, temps = zip(*self.temperatures)
        monthly_avg = [sum(temp) / len(temp) for temp in zip(*temps)]
        plt.plot(self.month_names, monthly_avg, marker='o')
        plt.xlabel('Month')
        plt.ylabel('Average Temperature Anomaly')
        plt.title('Average Temperature Anomaly per Month')
        plt.show()


# Create a single instance of Reader
average_month = AverageMonth('C:\zshahpouri\programming 2\config.yml')


# Average temperatures
average_month.calculate_average()

# Plots
average_month.plot_telorance()
average_month.plot_average_per_month()
