from flask import Flask, request, render_template, redirect, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

users = {
    1: {"id": 1, "username": "alice", "role": "user", "secret": "alice_secret"},
    2: {"id": 2, "username": "bob", "role": "user", "secret": "bob_secret"},
    3: {"id": 3, "username": "admin", "role": "admin", "secret": "admin_secret"},
}

comments = []

if not os.path.exists("uploads"):
    os.mkdir("uploads")

@app.route("/", methods=["GET", "POST"])
def index():
    global comments
    if request.method == "POST":
        comments.append(request.form.get("comment"))
        return redirect("/")
    return render_template("index.html", comments=comments)

@app.route("/profile/<int:user_id>")
def profile(user_id):
    return render_template("profile.html", user=users[user_id])

@app.route("/admin")
def admin():
    if request.args.get("admin") == "true":
        return render_template("admin.html", users=users)
    return "Forbidden"

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return f"Uploaded {file.filename}"

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)

app.run(host="0.0.0.0", port=5000, debug=True)
