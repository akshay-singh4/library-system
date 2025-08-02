import os
from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

items = mongo.db.books

@app.route("/")
def index():
    books = []
    for doc in items.find():
        books.append({
            "id": str(doc["_id"]),
            "title": doc.get("title", ""),
            "author": doc.get("author", ""),
            "year": doc.get("year", ""),
            "isbn": doc.get("ISBN", "")
        })
    return render_template("index.html", books=books)


@app.route("/books", methods=["POST"])
def create():
    try:
        data = request.get_json()
        result = items.insert_one(data)
        return jsonify({"_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/books", methods=["GET"])
def get_book():
    docs = []
    for doc in items.find():
        doc["_id"] = str(doc["_id"])
        docs.append(doc)
    return jsonify(docs), 201

@app.route("/books/<id>", methods=["GET"])
def getspecific(id):
    try:
        doc = items.find_one({"_id": ObjectId(id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            return jsonify(doc), 201
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/books/<id>", methods=["PUT"])
def updateBook(id):
    try:
        data = request.get_json()
        result = items.update_one({"_id": ObjectId(id)}, {"$set": data})
        return jsonify({"updated": result.modified_count}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/books/<id>", methods=["DELETE"])
def deleteBook(id):
    try:
        result = items.delete_one({"_id": ObjectId(id)})
        return jsonify({"deleted": True if result.deleted_count > 0 else False})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)