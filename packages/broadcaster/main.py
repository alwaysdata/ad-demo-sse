import os
import random

import zmq
from flask import Flask, render_template

ZMQ_PORT = os.environ.get("ZMQ_PORT", 5556)
ZMQ_HOST = os.environ.get("ZMQ_HOST", "0.0.0.0")

app = Flask(__name__)
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.setsockopt(zmq.IPV6, 1)
socket.connect(f"tcp://{ZMQ_HOST}:{ZMQ_PORT}")


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/event/<type>")
def event(type):
    if type == "log:open":
        data = {"event": "login", "message": "someone logged in", "urgent": False, "level": "debug"}
    elif type == "pill:blue":
        data = {"event": "user:btn", "message": "someone picked a blue pill", "urgent": False, "level": "info"}
    elif type == "pill:red":
        data = {"event": "user:btn", "message": "someone picked a red pill", "urgent": True, "level": "info"}

    socket.send_json(data)
    return "", 201
