# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

import os

from django.core.asgi import get_asgi_application
from django.core.handlers.asgi import ASGIHandler

import cvat.utils.remote_debugger as debug
from cvat.apps.test.websocket import websocket_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cvat.settings.development")

django_application = get_asgi_application()


async def application(scope, receive, send):
    if scope["type"] == "websocket" and scope["path"] == "/ws/class-wise-analytics/":
        return await websocket_application(scope, receive, send)

    return await django_application(scope, receive, send)


if debug.is_debugging_enabled():

    class DebuggerApp(ASGIHandler):
        """
        Support for VS code debugger
        """

        def __init__(self) -> None:
            super().__init__()
            self.__debugger = debug.RemoteDebugger()

        async def handle(self, *args, **kwargs):
            self.__debugger.attach_current_thread()
            return await super().handle(*args, **kwargs)

    django_application = DebuggerApp()
