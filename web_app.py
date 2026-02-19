from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect("hacker_calllog.db")
    c = conn.cursor()
    c.execute("SELECT * FROM logs")
    rows = c.fetchall()
    conn.close()

    html = """
    <h1>📞 Call Logs</h1>
    <table border=1>
    <tr><th>ID</th><th>Name</th><th>Phone</th><th>Type</th><th>Duration</th><th>DateTime</th></tr>
    {% for row in rows %}
    <tr>
    {% for col in row %}
    <td>{{col}}</td>
    {% endfor %}
    </tr>
    {% endfor %}
    </table>
    """
    return render_template_string(html, rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
