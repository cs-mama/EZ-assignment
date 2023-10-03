from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data for user roles (in-memory database)
users = [
    {"username": "opsuser", "password": "opsuserpassword", "role": "ops"},
    {"username": "clientuser", "password": "clientuserpassword", "role": "client"},
]

# Sample data for uploaded files (in-memory database)
uploaded_files = []

# Authentication middleware
def authenticate(username, password):
    user = next((user for user in users if user["username"] == username), None)
    if user and user["password"] == password:
        return user["role"]
    return None

# Route for user login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = authenticate(username, password)
    if role:
        return jsonify({"message": f"Logged in as {role} user"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Route for uploading files (only accessible by ops users)
@app.route("/upload", methods=["POST"])
def upload_file():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = authenticate(username, password)
    if role != "ops":
        return jsonify({"message": "Permission denied"}), 403

    file_type = data.get("file_type")
    if file_type not in ["pptx", "docx", "xlsx"]:
        return jsonify({"message": "Invalid file type"}), 400

    uploaded_files.append({"file_type": file_type})
    return jsonify({"message": "File uploaded successfully"}), 201

# Route for listing uploaded files (accessible to both ops and client users)
@app.route("/list_files", methods=["GET"])
def list_files():
    return jsonify({"files": [file["file_type"] for file in uploaded_files]}), 200

if __name__ == "__main__":
    app.run(debug=True)
