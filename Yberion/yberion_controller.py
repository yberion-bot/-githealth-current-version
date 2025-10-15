import logging
import threading
import queue
import time
from yberion_nexus_builder import YberionHost  # import your host

# ---------------- Logging ----------------
logging.basicConfig(
    filename="yberion_controller.log",
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logging.info("Yberion Controller starting...")

# ---------------- Initialize Host ----------------
host = YberionHost()
host.initialize()

# ---------------- Controller Interface ----------------
def send_task(task, priority="normal"):
    """
    Dispatch a task to agents with optional priority handling.
    - priority: normal | critical
    """
    if priority == "critical":
        logging.info(f"CRITICAL TASK issued: {task}")
    else:
        logging.info(f"Task issued: {task}")
    host.dispatch_task(task)

def interactive_console():
    """
    Simple interactive console to send tasks to the Nexus host.
    """
    print("Yberion Controller Interactive Mode")
    print("Type 'exit' to quit.")
    while True:
        task = input("Enter task for Junior: ")
        if task.lower() in ["exit", "quit"]:
            logging.info("Controller exiting...")
            host.running = False
            break

        # Detect critical tasks
        priority = "critical" if "DAN" in task.upper() else "normal"
        send_task(task, priority=priority)
        print(f"Dispatched task: {task} (priority: {priority})")

# ---------------- Run Controller ----------------
if __name__ == "__main__":
    interactive_console()
