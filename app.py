from flask import Flask, request, jsonify, send_from_directory, abort
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# LOGIN CREDENTIALS (change these)
USERNAME = "admin"
PASSWORD = "1234"

# GENERATED TOKEN (simple)
TOKEN = "my_secure_token_987"

latest_file = ""

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data["username"] == USERNAME and data["password"] == PASSWORD:
        return jsonify({"token": TOKEN})
    return jsonify({"error": "Invalid credentials"}), 401


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
        file = request.files["file"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        latest_file = file.filename
        return "Uploaded"

    return '''
    <h2>Upload File</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Upload</button>
    </form>
    '''

# ---------------- FETCH ----------------
@app.route("/latest")
def latest():
    check_token()
    return latest_file

@app.route("/file/<name>")
def file(name):
    check_token()
    return send_from_directory(UPLOAD_FOLDER, name)


app.run(host="0.0.0.0", port=10000)
