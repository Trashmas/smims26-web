from flask import Flask, render_template, request, redirect
import time
from math import floor

app = Flask(__name__)

state_text = "Griechischer Wein ist so wie das Blut der Erde"
last_change = 0

cooldown_minutes = 5

def minutes_since_last_change():
	now = time.time()
	return floor((now - last_change) / 60)

@app.route("/")
def index():
	minutes_elapsed = minutes_since_last_change()

	return render_template(
		"index.html",
		state_text = state_text,
		minutes_next_change = cooldown_minutes - minutes_elapsed,
		can_change = minutes_elapsed >= cooldown_minutes
	)

@app.route("/changetext", methods = ["POST"])
def change_text():
	global state_text, last_change

	if minutes_since_last_change() >= cooldown_minutes:
		state_text = request.form["text"]
		last_change = time.time()
	
	return redirect("/")

if __name__ == "__main__":
	app.run(port = 1234, debug = True)