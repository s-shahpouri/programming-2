import asyncio
import aiohttp
import json


class NetworkClient:
    '''This class provides the methods to fetch data from the server'''

    def __init__(self, base_url):
        self.base_url = base_url

    async def fetch_data(self, endpoint, callback):
        if endpoint.startswith('http'):
            url = endpoint
        else:
            url = self.base_url + '/' + endpoint

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(f"Fetching data from {url}: {response.status}")
                if response.status == 200:
                    data = await response.text()
                    # print only the first 100 characters
                    print(f"Data received: {data[:100]}...")
                    result = json.loads(data)
                    return callback(result)
                else:
                    print(f"Error fetching data from {url}: {response.status} {await response.text()}")
                    return None


def calculate_average_year(data):
    '''Calculates the average temperature for each month in the given data'''
    averages = {}
    for key, value in data.items():
        if key != 'Year':
            averages[key] = sum(value.values()) / len(value)

    return {'Average Temperature': averages}


def calculate_average_month(data):
    '''Calculates the average temperature for each month in the given data'''
    averages = {}
    for key, value in data.items():
        if key != 'Year':
            averages[key] = sum(value.values()) / len(value)

    return {'Average Temperature': averages}


async def main():
    '''This is the main method'''
    client = NetworkClient("http://localhost:8040/data")
    tasks = [
        client.fetch_data("all", calculate_average_year),
        client.fetch_data("1991", calculate_average_month),
        #
        client.fetch_data(
            # see my note at the server-side
            "http://localhost:8040/data/1991-2000", calculate_average_month)
    ]
    # wait for all tasks to complete
    results = await asyncio.gather(*tasks)

    # print the results
    for result in results:
        if result is not None:
            print("Result:", result)
        else:
            print("No result returned for a task")

if __name__ == "__main__":
    asyncio.run(main())
