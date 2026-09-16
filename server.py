from flask import Flask, render_template, request, redirect
import time
from math import floor
from os import environ
import redis

app = Flask(__name__)

rd = redis.from_url(environ["KV_URL"])
cooldown_minutes = 5

def minutes_since_last_change():
	now = time.time()
	last_change = float(rd.get("state_text_last_change").decode())
	return floor((now - last_change) / 60)

@app.route("/")
def index():
	minutes_elapsed = minutes_since_last_change()
	state_text = rd.get("state_text_value").decode()

	return render_template(
		"index.html",
		state_text = state_text,
		minutes_next_change = cooldown_minutes - minutes_elapsed,
		can_change = minutes_elapsed >= cooldown_minutes
	)

@app.route("/changetext", methods = ["POST"])
def change_text():
	if minutes_since_last_change() >= cooldown_minutes:
		rd.set("state_text_value", request.form["text"])
		rd.set("state_text_last_change", str(time.time()))
	
	return redirect("/")

if __name__ == "__main__":
	app.run(port = 1234, debug = True)