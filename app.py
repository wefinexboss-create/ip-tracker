from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage (sẽ reset khi restart)
clicks = []

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track')
def track_ip():
    client_info = {
        'ip': get_client_ip(),
        'user_agent': request.headers.get('User-Agent', ''),
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    clicks.append(client_info)
    return render_template('index.html', tracked=True)

@app.route('/manage')
def manage():
    return render_template('manage.html', clicks=clicks)

@app.route('/api/clicks')
def get_clicks():
    return jsonify(clicks)

# Vercel handler
def handler(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track')
def track_ip():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    client_info = {
        'ip': get_client_ip(),
        'user_agent': request.headers.get('User-Agent', ''),
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    c.execute('INSERT INTO clicks (ip, user_agent, time) VALUES (?, ?, ?)',
              (client_info['ip'], client_info['user_agent'], client_info['time']))
    conn.commit()
    conn.close()
    
    return render_template('index.html', tracked=True)

@app.route('/manage')
def manage():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM clicks ORDER BY id DESC')
    clicks = c.fetchall()
    conn.close()
    
    return render_template('manage.html', clicks=clicks)

@app.route('/api/clicks')
def get_clicks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM clicks ORDER BY id DESC')
    clicks = c.fetchall()
    conn.close()
    return jsonify(clicks)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)