from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pipeline.shared_content import agents, current_chat, history, status
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


@app.route('/get_current_agent', methods=['POST'])
@cross_origin()
def agent():
    return jsonify({"status": "ok", "agent": status.agent})


@app.route('/get_system_prompt', methods=['POST'])
@cross_origin()
@api_code_validation
def agent_get_system_prompt():
    data = request.get_json()
    agent = data.get('agent', None)
    return jsonify({"status": "ok", "content": agents.get(agent).get_system_prompt()})


@app.route('/set_system_prompt', methods=['POST'])
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


@app.route('/get_agents', methods=['POST'])
@cross_origin()
@api_code_validation
def get_agents():
    return jsonify({"status": "ok", "agents": [agent for agent in agents]})


@app.route('/get_history', methods=['POST'])
@cross_origin()
@api_code_validation
def get_history():
    return jsonify({"status": "ok", "history": history})


@app.route('/get_current_chat', methods=['POST'])
@cross_origin()
@api_code_validation
def get_current_chat():
    return jsonify({"status": "ok", "chat": current_chat})
