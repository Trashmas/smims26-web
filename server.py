from flask import Flask, render_template, request, redirect
import time
from math import floor
from os import environ
import kv_redis
import kv_dummy
import redis

app = Flask(__name__)

default_text = "Griechischer Wein ist so wie das Blut der Erde"

if "KV_URL" in environ:
	kv_bridge = kv_redis.Bridge(default_text)
else:
	print("Using dummy KV")
	kv_bridge = kv_dummy.Bridge(default_text)

cooldown_minutes = 5

def minutes_since_last_change():
	now = time.time()
	last_change = kv_bridge.get_last_change()
	return floor((now - last_change) / 60)

@app.route("/")
def fuck():
	return "Diese Webseite wurde vorübergehend von Vater Staat lahmgelegt. Bitte habt Geduld Genossen."

@app.route("/ljkadsjflkadsjfklasdjfklasdjf")
def index():
	minutes_elapsed = minutes_since_last_change()
	state_text = kv_bridge.get_text()

	return render_template(
		"index.html",
		state_text = state_text,
		minutes_next_change = cooldown_minutes - minutes_elapsed,
		can_change = minutes_elapsed >= cooldown_minutes
	)

@app.route("/changetext", methods = ["POST"])
def change_text():
	words = request.form["text"].lower().split(" ")
	if "fdp" in words:
		return "Die FDP ist hier verboten! Wir haben Mitarbeiter zu deinem Haus geschickt die dich beseitigen werden"
	elif "afd" in words:
		return "Das hier ist Münster!!! So eine blaue Scheiße wollen wir hier nicht"

	if minutes_since_last_change() >= cooldown_minutes and len(request.form["text"]) > 1:
		kv_bridge.set_text_and_update_time(request.form["text"])
	
	return redirect("/")

if __name__ == "__main__":
	app.run(port = 1234, debug = True)