from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pipeline.shared_content import status, agents
from app.background_flow import flow
import threading
from app.functions import api_code_validation
from pipeline.shared_content import logger


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
@api_code_validation
def agent_get_system_prompt():
    data = request.get_json()
    agent = data.get('agent', None)
    return jsonify({"status": "ok", "content": agents.get(agent).get_system_prompt()})

@app.route('/set_system_prompt', methods=['POST', 'GET'])
@cross_origin()
@api_code_validation
def agent_set_system_prompt():
    data = request.get_json()
    agent = data.get('agent', None)
    content = data.get('content', None)
    
    if not content:
        return jsonify({"status": "failed"})
    
    logger.info(f"agent {agent} system prompt change to:\n{content}")
    agents.get(agent).set_system_prompt(content)
    return jsonify({"status": "ok"})
