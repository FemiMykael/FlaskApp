from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.securedb
collection = db.messages

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        message = request.form.get("text")
        if message:
            # Save new task with "completed" as False by default
            collection.insert_one({"text": message, "completed": False})
        return redirect(url_for("admin"))
    
    messages = list(collection.find())
    return render_template("admin.html", messages=messages)

@app.route("/delete/<id>", methods=["POST"])
def delete_message(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("admin"))

@app.route("/complete/<id>", methods=["POST"])
def mark_complete(id):
    # "on" is sent if checkbox is checked
    completed = request.form.get("completed") == "on"
    collection.update_one({"_id": ObjectId(id)}, {"$set": {"completed": completed}})
    return redirect(url_for("admin"))

@app.route("/edit/<id>", methods=["POST"])
def edit_task(id):
    new_text = request.form.get("edit_text")
    if new_text:
        collection.update_one({"_id": ObjectId(id)}, {"$set": {"text": new_text}})
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
