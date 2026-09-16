import time

class Bridge:
	def __init__(self, default_text):
		self.current_text = default_text
		self.last_changed = 0.0

	def get_text(self):
		return self.current_text
	
	def get_last_change(self):
		return self.last_changed
	
	def set_text_and_update_time(self, text):
		self.current_text = text
		self.last_changed = time.time()