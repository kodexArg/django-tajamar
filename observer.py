import asyncio
import websockets
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

clients = set()
stop_event = asyncio.Event()
timer_task = None

class ChangeHandler(FileSystemEventHandler):
    """Handles filesystem events and notifies connected websocket clients."""

    def __init__(self, loop):
        """Initialize with the event loop."""
        self.loop = loop

    def on_any_event(self, event):
        """Trigger on any filesystem event and restart the notify timer."""
        global timer_task
        if timer_task and not timer_task.done():
            timer_task.cancel()
        timer_task = asyncio.run_coroutine_threadsafe(self.notify_clients(), self.loop)

    async def notify_clients(self):
        """Wait for 2 seconds to allow Django to stabilize and then notify all clients."""
        try:
            await asyncio.sleep(2)
            if clients:
                await asyncio.gather(*(client.send("reload") for client in clients))
        except asyncio.CancelledError:
            pass  # Handle the task being cancelled due to a new event

async def handler(websocket, path):
    """Handle new websocket connections and manage client set."""
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)

def start_observer(loop):
    """Start the filesystem observer to monitor changes."""
    event_handler = ChangeHandler(loop)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

async def stop_on_keypress():
    """Stop the asyncio event loop on pressing the 'C' key."""
    loop = asyncio.get_running_loop()
    
    def wait_for_keypress():
        while True:
            if input().strip().lower() == 'c':
                loop.call_soon_threadsafe(stop_event.set)
                break

    thread = threading.Thread(target=wait_for_keypress, daemon=True)
    thread.start()
    await stop_event.wait()

async def main():
    """Main entry point for the asyncio event loop."""
    loop = asyncio.get_running_loop()
    observer_task = asyncio.to_thread(start_observer, loop)
    server = await websockets.serve(handler, "localhost", 6789)

    await asyncio.gather(observer_task, server.wait_closed(), stop_on_keypress())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
