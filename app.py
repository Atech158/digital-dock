from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # ✅ allow Netlify → Render requests

# ---------------- CONFIG ----------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Change these
USERNAME = "admin"
PASSWORD = "1234"
TOKEN = "my_secure_token_987"

latest_file = ""

# ---------------- ROOT ----------------
@app.route("/")
def home():
    return "Server running ✅"

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data:
        return jsonify({"error": "No data"}), 400

    if data.get("username") == USERNAME and data.get("password") == PASSWORD:
        return jsonify({"token": TOKEN})

    return jsonify({"error": "Invalid credentials"}), 401


# ---------------- TOKEN CHECK ----------------
def check_token():
    token = request.args.get("token")
    if token != TOKEN:
        abort(403)


# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    check_token()
    global latest_file

    if request.method == "POST":
        if "file" not in request.files:
            return "No file", 400

        file = request.files["file"]
        if file.filename == "":
            return "Empty filename", 400

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        latest_file = file.filename
        return "Uploaded successfully ✅"

    return '''
    <h2>Upload File</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Upload</button>
    </form>
    '''


# ---------------- GET LATEST FILE NAME ----------------
@app.route("/latest")
def latest():
    check_token()
    return latest_file if latest_file else ""


# ---------------- SERVE FILE ----------------
@app.route("/file/<name>")
def file(name):
    check_token()
    return send_from_directory(UPLOAD_FOLDER, name)


# ---------------- START SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
