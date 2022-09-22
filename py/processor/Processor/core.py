from os import environ
from base64 import decodebytes
from aiohttp import ClientSession
from io import BytesIO

from google.auth.transport import requests
from google.oauth2 import id_token


endpoints = {
	"parser": "http://parser:6900/" if environ['PRODUCTION'] else "http://parser:6900/",
	"candle": "http://candle-server:6900/" if environ['PRODUCTION'] else "http://candle-server:6900/",
	"chart": "https://image-server-yzrdox65bq-uc.a.run.app/" if environ['PRODUCTION'] else "http://image-server:6900/",
	"depth": "http://quote-server:6900/" if environ['PRODUCTION'] else "http://quote-server:6900/",
	"detail": "http://quote-server:6900/" if environ['PRODUCTION'] else "http://quote-server:6900/",
	"heatmap": "https://image-server-yzrdox65bq-uc.a.run.app/" if environ['PRODUCTION'] else "http://image-server:6900/",
	"quote": "http://quote-server:6900/" if environ['PRODUCTION'] else "http://quote-server:6900/",
}


async def process_task(request, service, endpoint="", retries=3):
	url = endpoints[service]
	authReq = requests.Request()
	token = id_token.fetch_id_token(authReq, url)
	headers = {
		"Authorization": "Bearer " + token,
		"content-type": "application/json",
		"accept": "application/json"
	}

	async with ClientSession(headers=headers) as session:
		async with session.post(url + service + endpoint, json=request) as response:
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

	if retries == 1: raise Exception("time out")
	else: return await process_task(request, service, endpoint, retries-1)