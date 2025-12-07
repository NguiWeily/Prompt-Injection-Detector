from flask import Flask, request, jsonify
from detector import detect_injection

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Adversarial Prompt Injection Detector running"})

@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json(force=True)
    user_input = data.get("input", "")

    result = detect_injection(user_input)

    return jsonify(result)

@app.route("/proxy", methods=["POST"])
def proxy():
    """
    Example endpoint showing how you might place the detector
    in front of an LLM. It does NOT forward to any paid API.
    """
    data = request.get_json(force=True)
    user_input = data.get("input", "")

    security = detect_injection(user_input)

    if security["verdict"] == "high":
        return jsonify({
            "blocked": True,
            "reason": "Prompt identified as adversarial.",
            "score": security["final_score"]
        })

    return jsonify({
        "blocked": False,
        "response": f"(Simulated model reply) You said: {user_input}"
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
