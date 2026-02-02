import os
import sqlite3
from flask import Flask, request, redirect

app = Flask(__name__)

DB_PATH = "/tmp/notes.db"   # always writable in container


# =========================
# DB init
# =========================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY, text TEXT)"
    )
    conn.commit()
    conn.close()


init_db()


# =========================
# Home Page (HTML inline)
# =========================
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        note = request.form["note"]

        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO notes(text) VALUES(?)", (note,))
        conn.commit()
        conn.close()

        return redirect("/")

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM notes").fetchall()
    conn.close()

    html = """
    <h2>Simple Notes App</h2>

    <form method="post">
        <input name="note" placeholder="Write note">
        <button>Add</button>
    </form>

    <ul>
    """

    for r in rows:
        html += f"<li>{r[1]} <a href='/delete/{r[0]}'>❌</a></li>"

    html += "</ul>"

    return html


# =========================
# Delete
# =========================
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


# =========================
# Run
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
