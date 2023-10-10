from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pipeline.shared_content import status
from app.background_flow import flow
import threading


app = Flask(__name__)
cors = CORS(app)

pipeline = threading.Thread(target=flow.run, args=(""))
pipeline.start()


@app.route('/state', methods=['POST', 'GET'])
@cross_origin()
def state():
    return status.status


@app.route('/agent', methods=['POST', 'GET'])
@cross_origin()
def agent():
    return status.agent
