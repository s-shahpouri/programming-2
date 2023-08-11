import http.server
import socketserver
import json
from data_provider import DataProvider

# Step 1: Create a custom RequestHandler


class CustomRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/data"):

            try:
                # Extract the endpoint from the URL path
                endpoint = self.path.split("/")[2:]
                # Create an instance of the DataProvider class
                dp = DataProvider()

                if endpoint[0] == "all":
                    # Retrieve all data from the DataProvider
                    data = dp.get_data()

                elif endpoint[0].isdigit():
                    if len(endpoint) == 1:
                        # Retrieve data for a specific year
                        data = dp.get_data(int(endpoint[0]))

                    else:
                        raise ValueError("Invalid endpoint")
                elif endpoint[0].isdigit() and endpoint[1].isdigit():
                    # Retrieve data for a range of years

                    data = dp.get_data([int(endpoint[0]), int(endpoint[1])])
                else:
                    raise ValueError("Invalid endpoint")

                # Send a successful response with JSON data
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())

            except ValueError as e:
                # Send a Bad Request response if an error occurs
                self.send_error(400, str(e))

        else:
            # Send a Not Found response for other endpoints
            self.send_error(404)


# Step 3: Create and run the server
PORT = 8040
Handler = CustomRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
if __name__ == "__main__":

    print("serving at port", PORT)

    d = DataProvider()
    # Test case 1: Get all data
    print(d.get_data())

    # Test case 2: Get data for a specific year (e.g., 1991)
    print(d.get_data(1991))

    # Test case 3: Get data for a range of years (e.g., from 1991 to 2000)
    print(d.get_data([1991, 2000]))
    httpd.serve_forever()
