# Adversarial Prompt Injection Detector (Hackathon MVP)

Minimal, hackathon-ready detector + proxy to reduce prompt-injection attacks against LLM integrations.

**What it includes**
- `app.py` - Flask app exposing:
  - `POST /detect` — score a prompt for injection attempts.
  - `POST /proxy` — example middleware that would validate and forward prompts to an LLM (mocked).
- `detector.py` - core heuristics & rules engine with explainable scoring.
- `requirements.txt` - Python dependencies.
- `tests/test_detector.py` - simple unit tests.
- `examples/` - example prompts and curl commands.

**Quick start (local)**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```
Then POST JSON `{"input": "<user input>", "system": "<system prompt optional>"}` to `http://localhost:5000/detect`.

**How it works (MVP)**
- Rule-based detectors (regex, keywords, hidden characters).
- Heuristic scoring that produces a numeric score and an explanation of which rules fired.
- Middleware demonstrates how to use the detector before calling an LLM API.

**Notes**
- This is a demo/hackathon MVP — for production you should:
  - Add robust unit tests and CI.
  - Integrate ML embeddings / similarity checks for stealthy injections.
  - Rate-limit and monitor logs; protect the middleware itself.
  - Use secure key management for LLM API keys.
