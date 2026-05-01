from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Lưu tạm trong RAM
# Lưu ý: trên Vercel serverless, dữ liệu có thể bị reset khi function restart
clicks = []


def get_client_ip():
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()

    return request.remote_addr


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/track")
def track_ip():
    client_info = {
        "ip": get_client_ip(),
        "user_agent": request.headers.get("User-Agent", ""),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    clicks.append(client_info)

    return render_template("index.html", tracked=True)


@app.route("/manage")
def manage():
    return render_template("manage.html", clicks=clicks)


@app.route("/api/clicks")
def get_clicks():
    return jsonify(clicks)


# Vercel cần biến app này
if __name__ == "__main__":
    app.run(debug=True, port=5000)