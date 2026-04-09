import subprocess
import time
import os
import sys

def run_monitor():
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'm.py')
    log = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crash_log.txt')
    while True:
        try:
            os.system("pkill -f king")
            with open(log, "a") as f:
                f.write(f"\n--- Restart: {time.ctime()} ---\n")
                subprocess.run([sys.executable, target], stderr=f)
            time.sleep(5)
        except KeyboardInterrupt: break
        except Exception as e:
            with open(log, "a") as f: f.write(f"Error: {str(e)}\n")
            time.sleep(10)

if __name__ == "__main__": run_monitor()
