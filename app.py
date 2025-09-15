# app.py
from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS
import logging
import os

app = Flask(__name__, static_folder="ui")
CORS(app)
logging.basicConfig(level=logging.INFO)

UI_DIR = os.path.join(os.getcwd(), "ui")
ASSETS_DIR = os.path.join(os.getcwd(), "assets")

@app.route("/")
def index():
    # default landing page
    return send_from_directory(UI_DIR, "login_page.html")

@app.route("/ui/<path:filename>")
def ui_files(filename):
    # serve UI html/css/js from ui/
    if os.path.exists(os.path.join(UI_DIR, filename)):
        return send_from_directory(UI_DIR, filename)
    abort(404)

@app.route("/assets/<path:filename>")
def assets(filename):
    if os.path.exists(os.path.join(ASSETS_DIR, filename)):
        return send_from_directory(ASSETS_DIR, filename)
    abort(404)

@app.route("/api/query", methods=["POST"])
def api_query():
    """
    Example POST payload:
    { "query": "failed logins last 24h", "limit": 100 }
    This stub returns a generated-query string and sample results.
    """
    data = request.get_json(silent=True) or {}
    nl = data.get("query", "") or data.get("nl_query", "")
    logging.info("NL Query received: %s", nl)

    # stub: auto-generated query (replace with real translator later)
    generated_query = f"/* AUTO-GENERATED */ SELECT * FROM logs WHERE message LIKE '%{nl[:60]}%' LIMIT {data.get('limit', 100)}"

    sample_results = [
        {"timestamp": "2025-09-15T05:00:00Z", "src_ip": "10.0.0.2", "user":"alice", "event":"login_failure"},
        {"timestamp": "2025-09-15T05:02:12Z", "src_ip": "10.0.0.3", "user":"bob", "event":"login_success"}
    ]
    return jsonify(status="ok", generated_query=generated_query, results=sample_results)

@app.route("/api/visualize", methods=["POST"])
def api_visualize():
    """
    Expect payload: { "data": [...], "type": "bar" }
    Returns data shaped for plotting by the UI.
    """
    data = request.get_json(silent=True) or {}
    # simple stub aggregation
    sample_chart = {
        "labels": ["login_failure", "login_success"],
        "values": [42, 158],
        "title": "Login results (sample)"
    }
    return jsonify(status="ok", chart=sample_chart)

@app.route("/api/investigate", methods=["POST"])
def api_investigate():
    """
    Expect { "incident_id": "INC-1234" } or { "context": "10.0.0.2 suspicious" }
    Returns recommended investigation steps (stub).
    """
    data = request.get_json(silent=True) or {}
    context = data.get("context") or data.get("incident_id") or "unknown"
    logging.info("Investigate request: %s", context)
    steps = [
        "1) Validate alerts and timestamps",
        "2) Enrich IPs with threat intel",
        "3) Pull related logs (auth, network) for 24h window",
        "4) Contain if confirmed (isolate host)"
    ]
    return jsonify(status="ok", context=context, recommended_steps=steps)

if __name__ == "__main__":
    # debug for development; bind 0.0.0.0 so VM/host can access if needed
    app.run(host="0.0.0.0", port=5000, debug=True)
