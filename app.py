# app.py
import os
import logging
from pathlib import Path
from functools import wraps
from flask import Flask, request, jsonify, send_file, abort
from flask_cors import CORS

# ---------- Config ----------
BASE = Path.cwd()
UI_DIR = BASE / "ui"
ASSETS_DIR = BASE / "assets"
API_KEY = os.environ.get("AI_SOC_API_KEY")   # optional: set in environment for simple auth
MAX_BODY = 2 * 1024 * 1024  # 2 MB max body

# ---------- Flask setup ----------
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
app.config["MAX_CONTENT_LENGTH"] = MAX_BODY

# ---------- Helpers ----------
def safe_resolve(base_dir: Path, filename: str):
    """Resolve a filename under base_dir and prevent path traversal."""
    try:
        base = base_dir.resolve()
        target = (base / filename).resolve()
    except Exception:
        return None
    # ensure target is inside base
    if str(target).startswith(str(base) + os.sep) or target == base:
        return target
    return None

def require_api_key(f):
    """Optional decorator if API_KEY env var is set."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if API_KEY:
            key = request.headers.get("X-API-KEY") or request.args.get("api_key")
            if not key or key != API_KEY:
                return jsonify(status="error", message="Unauthorized"), 401
        return f(*args, **kwargs)
    return wrapped

# ---------- Health ----------
@app.route("/health")
def health():
    return jsonify(status="ok", ui_dir=str(UI_DIR.exists()), assets_dir=str(ASSETS_DIR.exists()))

# ---------- Static UI/Assets serving ----------
@app.route("/")
def index():
    p = safe_resolve(UI_DIR, "login_page.html")
    if p and p.exists():
        return send_file(p)
    abort(404)

@app.route("/ui/<path:filename>")
def ui_files(filename):
    p = safe_resolve(UI_DIR, filename)
    if p and p.exists():
        return send_file(p)
    abort(404)

@app.route("/assets/<path:filename>")
def assets(filename):
    p = safe_resolve(ASSETS_DIR, filename)
    if p and p.exists():
        return send_file(p)
    abort(404)

# ---------- API stubs ----------
@app.route("/api/query", methods=["POST"])
@require_api_key
def api_query():
    if not request.is_json:
        return jsonify(status="error", message="Invalid JSON"), 400
    data = request.get_json()
    nl = data.get("query") or data.get("nl_query") or ""
    logging.info("NL Query received: %s", nl[:200])

    # NOTE: THIS IS A STUB. Never build real SQL by concatenating untrusted text in production.
    safe_snippet = nl.replace("'", "''")[:200]
    limit = int(data.get("limit", 100))
    generated_query = f"/* AUTO-GENERATED */ SELECT * FROM logs WHERE message LIKE '%{safe_snippet}%' LIMIT {limit}"

    sample_results = [
        {"timestamp": "2025-09-15T05:00:00Z", "src_ip": "10.0.0.2", "user": "alice", "event": "login_failure"},
        {"timestamp": "2025-09-15T05:02:12Z", "src_ip": "10.0.0.3", "user": "bob", "event": "login_success"},
    ]
    return jsonify(status="ok", generated_query=generated_query, results=sample_results)

@app.route("/api/visualize", methods=["POST"])
@require_api_key
def api_visualize():
    if not request.is_json:
        return jsonify(status="error", message="Invalid JSON"), 400
    data = request.get_json()
    # stub aggregation logic
    sample_chart = {
        "labels": ["login_failure", "login_success"],
        "values": [42, 158],
        "title": "Login results (sample)"
    }
    return jsonify(status="ok", chart=sample_chart)

@app.route("/api/investigate", methods=["POST"])
@require_api_key
def api_investigate():
    if not request.is_json:
        return jsonify(status="error", message="Invalid JSON"), 400
    data = request.get_json()
    context = data.get("context") or data.get("incident_id") or "unknown"
    logging.info("Investigate request: %s", context)
    steps = [
        "1) Validate alerts and timestamps",
        "2) Enrich IPs with threat intel",
        "3) Pull related logs (auth, network) for 24h window",
        "4) Contain if confirmed (isolate host)"
    ]
    return jsonify(status="ok", context=context, recommended_steps=steps)

# ---------- Error handlers ----------
@app.errorhandler(404)
def not_found(e):
    return jsonify(status="error", message="Not found"), 404

@app.errorhandler(413)
def too_large(e):
    return jsonify(status="error", message="Payload too large"), 413

@app.errorhandler(500)
def server_error(e):
    logging.exception("Server error")
    return jsonify(status="error", message="Internal server error"), 500

# ---------- Run ----------
if __name__ == "__main__":
    debug_mode = os.environ.get("DEBUG", "1") == "1"
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
