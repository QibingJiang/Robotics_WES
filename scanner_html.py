from flask import Flask, request, render_template_string
import socket
import json
import time

app = Flask(__name__)

# Define a simple HTML template with a form and JavaScript for maintaining focus
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Form Submission</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }
        img {
            width: 600px; /* Adjust the size as needed */
            height: auto; /* Maintain aspect ratio */
            margin-bottom: 20px; /* Space between image and form */
        }
        form {
            width: 400px; /* Set the width of the form */
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px; /* Optional: Add padding inside the form */
            border: 1px solid #ddd; /* Optional: Add border to the form */
            border-radius: 8px; /* Optional: Add rounded corners */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional: Add shadow */
        }
        input, button {
            width: 100%; /* Make input and button take full width of the form */
            height: 40px; /* Set the height of input and button */
            margin: 10px 0; /* Margin on top and bottom for spacing */
            padding: 10px; /* Padding inside input and button */
            font-size: 16px; /* Font size for text inside input and button */
        }
        button {
            background-color: #007bff; /* Button background color */
            color: white; /* Button text color */
            border: none; /* Remove border for button */
            cursor: pointer; /* Change cursor on hover */
        }
        button:hover {
            background-color: #0056b3; /* Button hover color */
        }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const inputField = document.getElementById('userInput');

            function setFocus() {
                inputField.focus();
            }

            // Set focus when the page is loaded
            setFocus();

            // Set focus after form submission
            document.querySelector('form').addEventListener('submit', function() {
                // Simulate form submission
                setTimeout(setFocus, 100); // Delay to ensure focus is set after form is processed
            });
        });
    </script>
</head>
<body>
    <img src="{{ url_for('static', filename='trlogo2021transparent.webp') }}" alt="Placeholder Image">
    <form method="post" action="/">
        <input type="text" id="userInput" name="userInput" required>
        <button type="submit">Send</button>
    </form>
    {% if user_input %}
        <p>Received: {{ user_input }}</p>
    {% endif %}
    {% if error_message %}
        <p style="color: red;">{{ error_message }}</p>
    {% endif %}
</body>
</html>
'''

client_socket = None
server_config = None


@app.route('/', methods=['GET', 'POST'])
def index():
    user_input = None
    error_message = None
    global client_socket

    if request.method == 'POST':
        user_input = request.form.get('userInput', '')
        user_input = user_input.strip()  # Basic sanitization

        if not user_input:
            error_message = "No data received."
            print("no input now.")
        else:
            while True:
                try:
                    if client_socket is None:
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket.connect((server_config['ip'], server_config['tcp_port']))

                    client_socket.sendall(user_input.encode())
                    break

                except Exception as e:
                    print(f"Failed to send message: {e}. TCP re-connect")
                    client_socket.close()
                    time.sleep(1)
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((server_config['ip'], server_config['tcp_port']))

    return render_template_string(HTML_TEMPLATE, user_input=user_input, error_message=error_message)


if __name__ == '__main__':
    with open('local_server.txt', 'r') as file_3:
        server_config = json.loads(file_3.read())

    app.run(server_config['ip'], server_config['hand_scanner_port'], debug=True)
