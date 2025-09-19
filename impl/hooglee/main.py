
import http.server
import socketserver
import os
import json
import urllib.parse
import uuid
import time
import threading
from collections import defaultdict

def solution():
    print("Hello world")

# TODO - replace with LinkedHashMap to ensure order of messages and fast mutations
chat_history = defaultdict(list)
chat_history_lock = threading.Lock()

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_POST(self):
        if self.path == '/new_message':
            self.handle_new_message()
        else:
            super().do_POST()
    
    def do_DELETE(self):
        if self.path == '/delete_message':
            self.handle_delete_message()
        else:
            self.send_error(404, "Not Found")

    def create_chat_history_id(self, source_user_id, destination_user_id):
        # Sort the user IDs to ensure consistent order
        sorted_ids = sorted([source_user_id, destination_user_id])
        return f"{sorted_ids[0]}_{sorted_ids[1]}"
    
    def handle_new_message(self):
        # Handle POST request
        if self.command == 'POST':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Try to parse JSON data
                data = json.loads(post_data.decode('utf-8'))

                source_user_id = data.get('source_user_id')
                destination_user_id = data.get('destination_user_id')
                message = data.get('message')

                print(f"New message received from {source_user_id} to {destination_user_id}: {message}")
            except json.JSONDecodeError:
                # If not JSON, treat as form data
                data = urllib.parse.parse_qs(post_data.decode('utf-8'))
                source_user_id = data.get('source_user_id', [''])[0]
                destination_user_id = data.get('destination_user_id', [''])[0]
                message = data.get('message', [''])[0]

            message_id = str(uuid.uuid4())
            timestamp = int(time.time() * 1000)

            chat_history_id = self.create_chat_history_id(source_user_id, destination_user_id)

            # Thread-safe access to chat_history
            with chat_history_lock:
                chat_history[chat_history_id].append({
                    "source_user_id": source_user_id,
                    "id": message_id,
                    "timestamp": timestamp,
                    "message": message
                })
                # Get a copy of the current chat history for response
                current_chat_history = chat_history[chat_history_id].copy()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "chat_history": current_chat_history,
            }
            self.wfile.write(json.dumps(response).encode())
    
    def handle_delete_message(self):
        # Handle DELETE request
        if self.command == 'DELETE':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                
                try:
                    # Try to parse JSON data
                    data = json.loads(post_data.decode('utf-8'))
                    source_user_id = data.get('source_user_id')
                    destination_user_id = data.get('destination_user_id')
                    message_id = data.get('message_id')
                except json.JSONDecodeError:
                    # If not JSON, treat as form data
                    data = urllib.parse.parse_qs(post_data.decode('utf-8'))
                    source_user_id = data.get('source_user_id', [''])[0]
                    destination_user_id = data.get('destination_user_id', [''])[0]
                    message_id = data.get('message_id', [''])[0]
            else:
                # Handle query parameters for DELETE request
                parsed_url = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                source_user_id = query_params.get('source_user_id', [''])[0]
                destination_user_id = query_params.get('destination_user_id', [''])[0]
                message_id = query_params.get('message_id', [''])[0]
            
            if not all([source_user_id, destination_user_id, message_id]):
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "status": "error",
                    "message": "Missing required parameters: source_user_id, destination_user_id, message_id"
                }
                self.wfile.write(json.dumps(response).encode())
                return
            
            chat_history_id = self.create_chat_history_id(source_user_id, destination_user_id)
            
            # Thread-safe access to chat_history
            with chat_history_lock:
                # Find and remove the message with the specified message_id
                original_length = len(chat_history[chat_history_id])
                chat_history[chat_history_id] = [
                    msg for msg in chat_history[chat_history_id] 
                    if msg.get('id') != message_id
                ]
                
                message_deleted = len(chat_history[chat_history_id]) < original_length
                # Get a copy of the current chat history for response
                current_chat_history = chat_history[chat_history_id].copy()
            
            if message_deleted:
                print(f"Message {message_id} deleted from chat between {source_user_id} and {destination_user_id}")
                status = "success"
                message = "Message deleted successfully"
            else:
                print(f"Message {message_id} not found in chat between {source_user_id} and {destination_user_id}")
                status = "not_found"
                message = "Message not found"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": status,
                "message": message,
                "message_id": message_id,
                "chat_history": current_chat_history
            }
            self.wfile.write(json.dumps(response).encode())

def start_server():
    PORT = 8080
    
    # Change to the directory containing the script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Use ThreadingTCPServer for concurrent request handling
    with socketserver.ThreadingTCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print("Available endpoints:")
        print(f"  POST http://localhost:{PORT}/new_message")
        print(f"  DELETE http://localhost:{PORT}/delete_message")
        print("Server supports concurrent requests using threading")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    start_server()