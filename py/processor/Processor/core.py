from os import environ
from base64 import decodebytes
from asyncio import sleep, TimeoutError
from aiohttp import ClientSession
from aiohttp.client_exceptions import ServerDisconnectedError, ClientConnectorError
from io import BytesIO

from google.auth.transport import requests
from google.oauth2 import id_token


async def process_task(request, service, endpoint="", origin="default", priority=True, timeout=30, retries=1, maxRetries=5):
	request["origin"] = origin

	url = resolve_endpoint(service, priority)
	if priority:
		headers = {
			"content-type": "application/json",
			"accept": "application/json"
		}
	else:
		authReq = requests.Request()
		token = id_token.fetch_id_token(authReq, url)
		headers = {
			"Authorization": "Bearer " + token,
			"content-type": "application/json",
			"accept": "application/json"
		}

	try:
		async with ClientSession(headers=headers) as session:
			async with session.post(url + service + endpoint, json=request, timeout=30) as response:
				if response.status == 200:
					data = await response.json()
					if service in ["parser"]:
						return data
					elif service in ["chart", "heatmap", "depth"]:
						payload, message = data.get("response"), data.get("message")
						if payload is not None and payload["data"] is not None:
							payload["data"] = BytesIO(decodebytes(payload["data"].encode()))
						return payload, message
					else:
						payload, message = data.get("response"), data.get("message")
						return payload, message
				else:
					print(f"Error: {response.status}")
	except (ServerDisconnectedError, ClientConnectorError, TimeoutError) as e:
		if retries >= maxRetries: raise e
		print(f"Retrying {service}{endpoint} request ({retries}/{maxRetries - 1})")
		await sleep(retries)

	if retries >= maxRetries: raise Exception("exhausted retries")
	else: return await process_task(request, service, endpoint, origin, priority, timeout, retries + 1)

async def process_task_with(session, request, service, endpoint="", origin="default", priority=True, timeout=30, retries=1, maxRetries=5):
	request["origin"] = origin

	try:
		async with session.post(url + service + endpoint, json=request, timeout=30) as response:
			if response.status == 200:
				data = await response.json()
				if service in ["parser"]:
					return data
				elif service in ["chart", "heatmap", "depth"]:
					payload, message = data.get("response"), data.get("message")
					if payload is not None and payload["data"] is not None:
						payload["data"] = BytesIO(decodebytes(payload["data"].encode()))
					return payload, message
				else:
					payload, message = data.get("response"), data.get("message")
					return payload, message
			else:
				print(f"Error: {response.status}")
	except (ServerDisconnectedError, ClientConnectorError, TimeoutError) as e:
		if retries >= maxRetries: raise e
		print(f"Retrying {service}{endpoint} request ({retries}/{maxRetries - 1})")
		await sleep(retries)

	if retries >= maxRetries: raise Exception("exhausted retries")
	else: return await process_task_with(session, request, service, endpoint, origin, priority, timeout, retries + 1)

def resolve_endpoint(service, priority=True):
	match service:
		case "parser":
			return "http://parser:6900/" if environ['PRODUCTION'] else "http://parser:6900/"
		case "candle":
			return "http://candle-server:6900/" if environ['PRODUCTION'] else "http://candle-server:6900/"
		case "chart":
			if priority:
				return "http://image-server:6900/" if environ['PRODUCTION'] else "http://image-server:6900/"
			else:
				return "https://image-server-yzrdox65bq-uc.a.run.app/" if environ['PRODUCTION'] else "http://image-server:6900/"
		case "depth":
			return "http://quote-server:6900/" if environ['PRODUCTION'] else "http://quote-server:6900/"
		case "detail":
			return "http://quote-server:6900/" if environ['PRODUCTION'] else "http://quote-server:6900/"
		case "heatmap":
			if priority:
				return "http://image-server:6900/" if environ['PRODUCTION'] else "http://image-server:6900/"
			else:
				return "https://image-server-yzrdox65bq-uc.a.run.app/" if environ['PRODUCTION'] else "http://image-server:6900/"
		case "quote":
			return "http://quote-server:6900/" if environ['PRODUCTION'] else "http://quote-server:6900/"
		case _:
			return None