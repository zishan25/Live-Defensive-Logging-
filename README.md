# Live-Defensive-Logging-
pkg update && pkg upgrade -y
pkg install python git clang make libffi-dev openssl-dev -y
pip install --upgrade pip setuptools wheel
pip install flask
pip install cryptography --no-build-isolation
python -c "import flask, cryptography; print('✅ Installed!')"
pkg update -y && pkg upgrade -y && pkg install python git clang make libffi-dev openssl-dev -y && pip install --upgrade pip setuptools wheel && pip install flask cryptography
