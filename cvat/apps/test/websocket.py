import asyncio

import redis.asyncio as redis

from cvat.apps.test.realtime import CHANNEL


async def websocket_application(scope, receive, send):
    if scope["type"] != "websocket":
        return

    await send({"type": "websocket.accept"})

    client = redis.Redis(
        host="cvat_redis_inmem",
        port=6379,
        db=0,
    )
    pubsub = client.pubsub()

    try:
        await pubsub.subscribe(CHANNEL)

        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True,
                timeout=1.0,
            )

            if message and message["type"] == "message":
                await send({
                    "type": "websocket.send",
                    "text": message["data"].decode("utf-8"),
                })

            try:
                incoming = await asyncio.wait_for(receive(), timeout=0.01)
                if incoming["type"] == "websocket.disconnect":
                    break
            except asyncio.TimeoutError:
                pass
    finally:
        await pubsub.unsubscribe(CHANNEL)
        await pubsub.close()
        await client.close()
