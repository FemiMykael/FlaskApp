from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.securedb
collection = db.messages

@app.route("/")
def index():
    messages = collection.find()
    return render_template("index.html", messages=messages)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        message = request.form.get("text")
        if message:
            collection.insert_one({"text": message})
        return redirect(url_for("admin"))
    
    messages = collection.find()
    return render_template("admin.html", messages=messages)

@app.route("/delete/<id>", methods=["POST"])
def delete_message(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
