# app.py
import os, json
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

def log(level, msg, **extra):
    payload = {
        "time": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "msg": msg,
        "path": request.path if request else None,
        "method": request.method if request else None
    }
    payload.update(extra)
    print(json.dumps(payload), flush=True)

@app.route("/", methods=["GET"])
def root():
    message = os.getenv("MESSAGE", "Hello")
    release = os.getenv("RELEASE", "dev")
    log("INFO", "served_root", message=message, release=release)
    return jsonify({"message": message, "release": release})

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    log("INFO", "app_start", port=port)
    app.run(host="127.0.0.1", port=port)
