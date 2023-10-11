from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pipeline.shared_content import status, agents
from app.background_flow import flow
import threading
import os
from dotenv import load_dotenv


load_dotenv()
API_CODE = os.getenv("API_CODE", "")
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

@app.route('/get_system_prompt', methods=['POST', 'GET'])
@cross_origin()
def agent_get_system_prompt():
    data = request.get_json()
    api_code = data.get('api_code', None)
    agent = data.get('agent', None)
    if api_code != API_CODE:
        return jsonify({"status": "failed"})
    
    return jsonify({"status": "ok", "content": agents.get(agent).get_system_prompt()})

@app.route('/set_system_prompt', methods=['POST', 'GET'])
@cross_origin()
def agent_set_system_prompt():
    data = request.get_json()
    api_code = data.get('api_code', None)
    agent = data.get('agent', None)
    content = data.get('content', None)
    if api_code != API_CODE:
        return jsonify({"status": "failed"})
    
    if not content:
        return jsonify({"status": "failed"})
    
    agents.get(agent).set_system_prompt(content)
    return jsonify({"status": "ok"})
