from flask import Flask, request, jsonify
from detector import detect
import os

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect_route():
    data = request.get_json(force=True)
    prompt = data.get('input') or data.get('prompt') or ''
    system = data.get('system') or ''
    result = detect(prompt, system)
    return jsonify(result)

@app.route('/proxy', methods=['POST'])
def proxy_route():
    """Example middleware endpoint that runs detection before forwarding to an LLM.
    This demo DOES NOT call external APIs. Replace the mocked section with calls to your LLM provider.
    Expected JSON: { 'input': '<user input>', 'system': '<system prompt optional>' }
    """            data = request.get_json(force=True)
    prompt = data.get('input') or data.get('prompt') or ''
    system = data.get('system') or ''
    res = detect(prompt, system)
    # If high risk, block
    if res['final_score'] >= 0.75:
        return jsonify({ 'ok': False, 'reason': 'blocked_by_detector', 'detail': res }), 403
    # For medium risk, we attach a warning and proceed (in real use: human review or modify prompt)
    if res['final_score'] >= 0.35:
        # In production you'd sanitize or ask for confirmation. Here we mock LLM response.
        mock_response = {
            'id': 'mock-1',
            'object': 'text_completion',
            'choices': [{'text': '<<SANITIZED RESPONSE: potential injection detected>>'}]
        }
        return jsonify({ 'ok': True, 'warning': 'medium_risk', 'detector': res, 'llm_response': mock_response })
    # Low risk: mock forwarding to LLM provider (PLACEHOLDER)
    mock_response = {
        'id': 'mock-2',
        'object': 'text_completion',
        'choices': [{'text': '<<MOCK LLM RESPONSE: normal processing>>'}]
    }
    return jsonify({ 'ok': True, 'detector': res, 'llm_response': mock_response })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
