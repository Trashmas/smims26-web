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
	result = rd.get("state_text_last_change")
	if result is None:
		rd.set("state_text_last_change", "0.0")
		last_change = 0.0
	else:
		last_change = float(result.decode())
	return floor((now - last_change) / 60)

@app.route("/")
def index():
	minutes_elapsed = minutes_since_last_change()
	result = rd.get("state_text_value")
	if result is None:
		state_text = "Griechischer Wein ist so wie das Blut der Erde"
		rd.set("state_text_value", state_text)
	else:
		state_text = result.decode()

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