from flask import request, Flask, jsonify
from flask_basicauth import BasicAuth
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://workmongo:mongo007@cluster0.kjvosuu.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri)

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
basic_auth = BasicAuth(app)

client.admin.command('ping')
print("Pinged your deployment. You successfully connected to MongoDB!")
db = client["students"]
collection = db["std_info"]

@app.route("/")
def Greet():
    return "<p>Welcome to Book Management Systems</p>"

@app.route("/students", methods=["GET"])
@basic_auth.required
def get_all_students():
    data = collection.find()
    return jsonify(list(data))

@app.route("/students/<string:student_id>", methods=["GET"])
@basic_auth.required
def get_student(student_id):
    student = collection.find_one({"_id": student_id})
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404
    
@app.route("/students", methods=["POST"])
@basic_auth.required
def create_student():
    try:
        data = request.get_json()

        student = {
            "_id": str(data.get("_id")),
            "fullname": data.get("fullname"),
            "major": data.get("major"),
            "gpa": float(data.get("gpa"))
        }
        collection.insert_one(student)
        return jsonify({"message": "Student created successfully"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Cannot create new student"}), 500

@app.route("/students/<string:student_id>", methods=["PUT"])
@basic_auth.required
def update_student(student_id):
    print(f"Updating student with ID: {student_id}")

    student = collection.find_one({"_id": student_id})
    if student:
        data = request.get_json()
        collection.update_one({"_id": student_id}, {"$set": data})
        updated_student = collection.find_one({"_id": student_id})
        return jsonify(updated_student)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students/<string:student_id>", methods=["DELETE"])
@basic_auth.required
def student_delete(student_id):
    student = collection.find_one({"_id": student_id})
    if student:
        collection.delete_one({"_id": student_id})
        return jsonify({"message": "Student deleted successfully"}), 200
    else:
        return jsonify({"error": "Student not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
