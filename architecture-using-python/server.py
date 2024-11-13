from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

# In-memory "database"
tasks = [
    {'id': 1, 'title': 'Task 1', 'done': False},
    {'id': 2, 'title': 'Task 2', 'done': True}
]

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        # Get all tasks
        if path == '/tasks' and not query_params:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'tasks': tasks}).encode())

        # Get a specific task
        elif path.startswith('/tasks/') and len(path.split('/')) == 3:
            task_id = int(path.split('/')[2])
            task = next((task for task in tasks if task['id'] == task_id), None)
            if task:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'task': task}).encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Task not found'}).encode())

        # Invalid path
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Invalid path'}).encode())

    def do_POST(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Create a new task
        if path == '/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length).decode())
            new_task = {
                'id': len(tasks) + 1,
                'title': post_data.get('title', ''),
                'done': False
            }
            tasks.append(new_task)
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'task': new_task}).encode())

        # Invalid path
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Invalid path'}).encode())

if __name__ == '__main__':
    PORT = 8000
    server = HTTPServer(('localhost', PORT), RequestHandler)
    print(f'Starting server on http://localhost:{PORT}')
    server.serve_forever()