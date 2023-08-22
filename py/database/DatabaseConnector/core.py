from time import time
from aiohttp import ClientSession
from traceback import format_exc


class DatabaseConnector(object):
	def __init__(self, mode):
		self.mode = mode

	@staticmethod
	async def process_task(endpoint, request=None, retries=3):
		url = "http://database:6900/"
		async with ClientSession() as session:
			async with session.post(url + endpoint, json=request) as response:
				if response.status == 200:
					return await response.json()
		if retries <= 1: raise Exception("time out")
		else: return await process_task(endpoint, request, retries-1)

	async def check_status(self):
		try: return await DatabaseConnector.process_task(f"{self.mode}/status")
		except: return False

	async def keys(self, default={}):
		try: response = await DatabaseConnector.process_task(f"{self.mode}/keys")
		except: return default

		if response is None:
			return default
		return response

	async def get(self, value, default=None):
		try: response = await DatabaseConnector.process_task(f"{self.mode}/fetch", {"key": value})
		except: return default

		if response is None:
			return default
		return response

	async def match(self, value, default=None):
		if self.mode != "account":
			raise Exception("match is only available for account mode")

		try: response = await DatabaseConnector.process_task(f"{self.mode}/match", {"key": value})
		except: return default

		if response is None:
			return default
		return response