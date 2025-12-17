import flask # type: ignore
import sqlite3
from flask_limiter import Limiter # type: ignore
from flask_limiter.util import get_remote_address # type: ignore

app = flask.Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day"],
    storage_uri="memory://",
)
conn = sqlite3.connect('anons.db') 
cursor = conn.cursor()  
cursor.execute('''
    CREATE TABLE IF NOT EXISTS anons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slackuser TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')
conn.commit()  
conn.close()

@app.get("/")
@limiter.limit("1 per second")
def index():
    return flask.send_from_directory("static", "index.html")

@app.post("/anons")
def create_anon():
    data = flask.request.get_json()
    slackuser = data.get('slackuser')
    message = data.get('message')
    
    conn = sqlite3.connect('anons.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO anons (slackuser, message) VALUES (?, ?)', (slackuser, message))
    conn.commit()
    conn.close()

    return '', 201
    
@app.get("/anons")
def get_anons():
    conn = sqlite3.connect('anons.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, slackuser, message FROM anons')
    rows = cursor.fetchall()
    conn.close()
    
    anons = [{'id': row[0], 'slackuser': row[1], 'message': row[2]} for row in rows]
    return flask.jsonify(anons)
if __name__ == "__main__":
    app.run()