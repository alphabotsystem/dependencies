from zmq.asyncio import Context
from zmq import PUSH
from orjson import dumps


class IchibotRelay(object):
	def __init__(self):
		context = Context.instance()
		self.socket = context.socket(PUSH)
		self.socket.connect("tcp://ichibot-relay-server:6900")

	async def submit_image(self, messageId, request):
		await self.socket.send_multipart([b"image", str(messageId).encode(), dumps(request), b"", b""])

	async def submit_vote(self, messageId, channelId, authorId, vote):
		await self.socket.send_multipart([b"submit", str(messageId).encode(), str(channelId).encode(), str(authorId).encode(), str(vote).encode()])