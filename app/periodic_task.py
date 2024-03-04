import asyncio
from contextlib import suppress

class Periodic: #https://stackoverflow.com/questions/37512182/how-can-i-periodically-execute-a-function-with-asyncio
    def __init__(self, func, time):
        self.func = func
        self.time = time
        self.is_started = False
        self._task = None
        self._stop_event = asyncio.Event()

    async def start(self):
        if not self.is_started:
            if self._stop_event.is_set():
                self._stop_event.clear()
            self.is_started = True
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            self._stop_event.set()
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while not self._stop_event.is_set():
            await asyncio.sleep(self.time)
            await self.func()

class PeriodicCheckBool: #https://stackoverflow.com/questions/37512182/how-can-i-periodically-execute-a-function-with-asyncio
    def __init__(self, func, time):
        self.func = func
        self.time = time
        self.is_started = False
        self._task = None
        self._stop_event = asyncio.Event()


    async def start(self):
        if not self.is_started:
            if self._stop_event.is_set():
                self._stop_event.clear()
            self.is_started = True
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while not self._stop_event.is_set():
            await asyncio.sleep(self.time)
            result = await self.func()