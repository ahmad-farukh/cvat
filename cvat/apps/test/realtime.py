import json

import redis
from django.conf import settings
from django.db import transaction


CHANNEL = "cvat:analytics:class-wise"


def publish_class_wise_update():
    def publish():
        client = redis.Redis(
            host=settings.REDIS_INMEM_SETTINGS["HOST"],
            port=int(settings.REDIS_INMEM_SETTINGS["PORT"]),
            db=int(settings.REDIS_INMEM_SETTINGS["DB"]),
            password=settings.REDIS_INMEM_SETTINGS.get("PASSWORD") or None,
            socket_timeout=1,
        )

        try:
            client.publish(
                CHANNEL,
                json.dumps({"type": "class-wise-update"}),
            )
        finally:
            client.close()

    transaction.on_commit(publish)
