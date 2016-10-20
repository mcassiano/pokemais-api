# We need to import the jsonify object, it will let us
# output json, and it will take care of the right string
# data conversion, the headers for the response, etc
from flask import Flask, Response, request
from otm import parseRequestBody
import json

# Initialize the Flask application
app = Flask(__name__)


# This route will return a list in JSON format
@app.route('/xp', methods=['POST'])
def index():
    content = request.get_json(silent=True)    
    data = json.dumps(parseRequestBody(content))
    resp = Response(response=data,
                    status=200,
                    mimetype="application/json")

    return resp

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("4567")
    )
