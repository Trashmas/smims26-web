import time, redis

_key_state_text = "state_text_value"
_key_last_change = "state_text_last_change"

class Bridge:
	def __init__(self, default_text):
		self.rd = redis.from_url(environ["KV_URL"])
		if rd.get(_key_state_text) is None:
			rd.set(_key_state_text, default_text)
		if rd.get(_key_last_change) is None:
			rd.set(_key_last_change, "0.0")
	
	def get_text(self):
		return rd.get(_key_state_text).decode()
	
	def get_last_change(self):
		return float(rd.get(_key_last_change).decode())
	
	def set_text_and_update_time(self, text):
		rd.set(_key_state_text, text)
		rd.set(_key_last_change, str(time.time()))
