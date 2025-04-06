from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.securedb
collection = db.messages

@app.route("/")
def index():
    messages = collection.find()
    return render_template("index.html", messages=messages)

@app.route("/add", methods=["GET", "POST"])
def add_message():
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            collection.insert_one({"text": message})
        return redirect(url_for("index"))
    return render_template("add.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
