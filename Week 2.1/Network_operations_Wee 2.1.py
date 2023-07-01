from http.server import SimpleHTTPRequestHandler
import socketserver
import pandas as pd


class DataProvider:
    '''This class reads the data from the csv file
    and provides the data in json format.'''

    def __init__(self, file_path):
        '''Reads the file'''
        self.data = pd.read_csv(file_path)
        print(self.data.columns)

    def get_data(self, Year):
        '''Returns the data in json format for the given Year or range or 'all'''

        if Year == 'all':
            return self.data.to_json()

        elif isinstance(Year, int):
            data_of_year = self.data[self.data['Year'] == Year]

            if not data_of_year.empty:
                return data_of_year.to_json()
            else:
                raise ValueError('No data available for the requested Year.')
        elif isinstance(Year, list) and len(Year) == 2:
            data_range = self.data[(self.data['Year'] >= Year[0]) & (
                self.data['Year'] <= Year[1])]

            if not data_range.empty:
                return data_range.to_json()
            else:
                raise ValueError('No data available for the requested range.')
        else:
            raise ValueError('Invalid input parameter.')


class ServerHandler(SimpleHTTPRequestHandler):
    ''''This class handles the http requests and sends the response'''
    data_provider = DataProvider('dSST.csv')

    def do_GET(self):
        '''Handles the GET request and sends the response'''
        if not self.path.startswith('/data'):
            self.send_error(404, 'Not found')
            return

        # extract Year or range or 'all' from the request path
        Year = self.path[6:]

        try:
            '''Get the data for the given Year or range or 'all' and send the response'''
            if Year == 'all':
                data = self.data_provider.get_data('all')
            elif Year.isdigit():
                data = self.data_provider.get_data(int(Year))
            elif '-' in Year:
                from_Year, to_Year = map(int, Year.split('-'))
                data = self.data_provider.get_data([from_Year, to_Year])
            else:
                self.send_error(
                    400, 'Bad Request: Invalid Year or range format')
                return

            # send the response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(data, 'utf-8'))

        except ValueError as e:
            # send the error response
            self.send_error(400, 'Bad Request: ' + str(e))


PORT = 8080

# Create an object of the above class
http = socketserver.TCPServer(("", PORT), ServerHandler)

# Start the server
print("serving at port", PORT)
http.serve_forever()
