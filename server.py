from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import csv

class PollHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/poll.html' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('c:/6_July/poll.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        if self.path == '/submit_poll':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)
            
            # Process the form data
            self.handle_poll(data)
            
            # Respond to the client
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Poll submitted successfully!')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

    def handle_poll(self, data):
        try:
            # Extract userID from form data
            userID = data.get('userID', [''])[0]
            
            # Open CSV file in append mode
            with open('poll_results.csv', 'a', newline='') as csvfile:
                fieldnames = ['userID', 'question1', 'question2']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write header if file is empty
                if csvfile.tell() == 0:
                    writer.writeheader()

                # Write data to CSV
                writer.writerow({
                    'userID': userID,
                    'question1': data.get('option1', [''])[0],
                    'question2': data.get('option2', [''])[0]
                })

            print(f'Data saved successfully for userID {userID}')

        except Exception as e:
            print('Error saving data:', e)

def run(server_class=HTTPServer, handler_class=PollHandler, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
