from time import time
import requests


class DatabaseConnector(object):
	def __init__(self, mode):
		self.mode = mode

	@staticmethod
	def process_task(endpoint, request=None, retries=1):
		url = "http://database:6900/"
		response = requests.post(url + endpoint, json=request)
		if response.status_code == 200:
			return response.json().get("response")
		if retries >= 3: raise Exception("time out")
		else: return DatabaseConnector.process_task(endpoint, request, retries + 1)

	def check_status(self):
		try: return DatabaseConnector.process_task(f"{self.mode}/status")
		except: return False

	def keys(self, default={}):
		try: response = DatabaseConnector.process_task(f"{self.mode}/keys")
		except: return default

		if response is None:
			return default
		return response

	def get(self, value, default=None):
		try: response = DatabaseConnector.process_task(f"{self.mode}/fetch", {"key": str(value)})
		except: return default

		if response is None:
			return default
		return response

	def match(self, value, default=None):
		if self.mode != "account":
			raise Exception("match is only available for account mode")

		try: response = DatabaseConnector.process_task(f"{self.mode}/match", {"key": str(value)})
		except: return default

		if response is None:
			return default
		return response