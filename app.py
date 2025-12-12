from flask import Flask, jsonify
from pymongo import MongoClient

# Baga Flask!
app = Flask(__name__)

# Ne conectam la MongoDB!
client = MongoClient("mongodb://localhost:27017/")
db = client["proiect_crypto"]
collection = db["istoric_preturi"]

# Definim ruta API! (executam functia cand cineva intra)
@app.route('/api/preturi', methods=['GET'])
def get_preturi():
    # Extragem toate documentele din baza de date
    date_db = list(collection.find({}, {'_id': 0}))
    
    # Le trimitem inapoi ca JSON!
    return jsonify(date_db)

# Pornim serverul!
if __name__ == '__main__':
    app.run(debug=True)

# http://127.0.0.1:5000/api/preturi-->Link pentru Postman!
