from flask import Flask, request, jsonify
from pymongo import MongoClient
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MONGODB_URI = "mongodb+srv://josephsamuelm2021:Samenoch%4074@cluster0.itztqvl.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)
db = client["mptc"]
collection = db["poster"]



@app.route('/', methods=['POST'])
def upload_data():
    if request.method == 'POST':
        # Retrieve image and text from the request (you'll handle this part later)
        image = request.files['file']
        text = request.form['text']

        # Convert the image to bytes (base64 encoding)
        image_bytes = base64.b64encode(image.read()).decode('utf-8')

        # Insert the image and text into the MongoDB collection
        data = {"image": image_bytes, "text": text}
        collection.insert_one(data)

        return jsonify({"message": "Data updated and saved to MongoDB Atlas"})

@app.route('/get_latest_data', methods=['GET'])
def get_latest_data():
    # Find the most recent document in the collection (assuming you have a timestamp field)
    latest_data = collection.find_one(sort=[('_id', -1)])

    if latest_data:
        # Extract the image and text from the retrieved document
        image_bytes = latest_data["image"]
        text = latest_data["text"]

        # Return the image as a base64-encoded string and text in the JSON response
        response_data = {
            "image": image_bytes,
            "text": text
        }

        return jsonify(response_data)
    else:
        return jsonify({"message": "No data found"})


    

if __name__ == '__main__':
    app.run(port=5000)
