from flask import render_template, request, jsonify
from app.biased_ai import create_biased_agent
from app.ai_judge import evaluate_response
from app.topic_manager import get_topics_list, load_topic_content
import os

def init_routes(app):
    @app.route('/')
    def home():
        topics = get_topics_list()
        return render_template('index.html', topics=topics)

    @app.route('/chat', methods=['GET', 'POST'])
    def chat():
        topic = request.form.get('topic', 'pluto') if request.method == 'POST' else 'pluto'
        return render_template('chat.html', topic=topic)

    @app.route('/api/chat', methods=['POST'])
    def api_chat():
        data = request.json
        question = data['question']
        topic = data.get('topic', 'pluto')
        
        biased_ai = create_biased_agent(topic)
        if not biased_ai:
            return jsonify({"error": "Topic not found"}), 404
        
        response = biased_ai.invoke(question)["output"]
        evaluation = evaluate_response(question, response, topic)
        
        return jsonify({
            "response": response,
            "evaluation": evaluation
        })

    @app.route('/api/topics', methods=['GET'])
    def api_topics():
        topics = get_topics_list()
        return jsonify({"topics": topics})