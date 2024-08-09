import asyncio
import websockets
import threading
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

clients = set()
stop_event = asyncio.Event()

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('daphne.sock.lock'):
            asyncio.run(self.notify_clients())

    async def notify_clients(self):
        if clients:
            await asyncio.wait([asyncio.create_task(client.send("reload")) for client in clients])

async def handler(websocket, path):
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)

def start_observer(loop):
    asyncio.set_event_loop(loop)
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./nginx/daphne/daphne.sock', recursive=False)
    observer.start()
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def wait_for_keypress():
    input("Press C to stop\n")
    asyncio.run_coroutine_threadsafe(stop_event.set(), asyncio.get_event_loop())

async def main():
    lockfile_path = './nginx/daphne/daphne.sock'
    if not os.path.exists(lockfile_path):
        print(f"File {lockfile_path} not found. Exiting.")
        return

    loop = asyncio.get_running_loop()
    observer_thread = threading.Thread(target=start_observer, args=(loop,))
    observer_thread.start()

    keypress_thread = threading.Thread(target=wait_for_keypress)
    keypress_thread.start()

    async with websockets.serve(handler, "localhost", 6789):
        await stop_event.wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
