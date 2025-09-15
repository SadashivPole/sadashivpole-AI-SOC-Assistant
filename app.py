from flask import Flask, render_template

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("login_page.html")

@app.route("/dashboard")
def dashboard():
    return render_template("performance_dashboard.html")

@app.route("/audit")
def audit():
    return render_template("audit_log.html")

@app.route("/investigation")
def investigation():
    return render_template("investigation_console.html")

@app.route("/admin")
def admin():
    return render_template("admin_settings.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
