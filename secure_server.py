from flask import Flask, request, render_template_string
from cryptography.fernet import Fernet
import json
import os

app = Flask(__name__)

PASSWORD = "1234"   # নিজের password সেট করো
KEY_FILE = "secret.key"
DATA_FILE = "logs_encrypted.bin"

HTML_LOGIN = """
<h2>Secure Login</h2>
<form method="POST">
Password: <input type="password" name="password">
<input type="submit" value="Login">
</form>
"""

HTML_DASHBOARD = """
<h2>📊 Secure Call & SMS Logs</h2>
<h3>📞 Calls</h3>
<pre>{{calls}}</pre>
<h3>📩 SMS</h3>
<pre>{{sms}}</pre>
"""

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    return open(KEY_FILE, "rb").read()

def encrypt_logs():
    data = {
        "calls": [
            ["+8801711111111", "2026-02-18 12:01"],
            ["+8801711111111", "2026-02-18 12:02"],
            ["+8801912345678", "2026-02-18 12:05"]
        ],
        "sms": [
            ["+8801711111111", "2026-02-18 12:03", "Hello"],
            ["+8801812345678", "2026-02-18 12:06", "Test SMS"]
        ]
    }

    fernet = Fernet(load_key())
    encrypted = fernet.encrypt(json.dumps(data).encode())

    with open(DATA_FILE, "wb") as f:
        f.write(encrypted)

def decrypt_logs():
    fernet = Fernet(load_key())
    with open(DATA_FILE, "rb") as f:
        encrypted = f.read()
    decrypted = fernet.decrypt(encrypted)
    return json.loads(decrypted)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == PASSWORD:
            logs = decrypt_logs()
            return render_template_string(
                HTML_DASHBOARD,
                calls="\n".join([str(i) for i in logs["calls"]]),
                sms="\n".join([str(i) for i in logs["sms"]])
            )
        else:
            return "❌ Wrong Password"
    return HTML_LOGIN

if __name__ == "__main__":
    if not os.path.exists(KEY_FILE):
        generate_key()
    encrypt_logs()
    app.run(host="0.0.0.0", port=5000)
