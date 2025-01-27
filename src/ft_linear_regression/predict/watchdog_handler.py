import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from ..utils.data_utils import JSON_PATH
import matplotlib.pyplot as plt
from queue import Queue, Empty
from ..utils.data_utils import load_parameters_from_json, load_normalized_data
from .plot import linear_regression, theorical_linear_regression, update_plot

def setup_watchdog_handler(data, theorical_regression, parameters, ax1, ax2):
    event_queue = Queue()

    event_handler = JsonFileHandler(event_queue)
    observer = Observer()
    observer.schedule(event_handler, path=Path(JSON_PATH).parent, recursive=False)
    observer.start()
    print(f"Watchdog started. Monitoring {JSON_PATH} for changes...")

    def event_loop():
        try:
            while True:
                try:
                    event = event_queue.get_nowait()
                    if event == "update_plot":
                        update_plot(data, theorical_regression, parameters, ax1, ax2)
                except Empty:
                    pass  # No events in the queue

                plt.pause(0.1)
                time.sleep(0.1)  
        except KeyboardInterrupt:
            print("Stopping the program...")
        finally:
            observer.stop()
            observer.join()

    return observer, event_loop

class JsonFileHandler(FileSystemEventHandler):

    def __init__(self, queue):
        self.queue = queue
        self.file_path = JSON_PATH

    def on_modified(self, event):
        if event.src_path.endswith(str(self.file_path)):
            print(f"{self.file_path} modified. Triggering callback...")
            self.queue.put("update_plot") 
