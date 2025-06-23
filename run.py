from app import app
from dotenv import load_dotenv
import os
import threading
import webbrowser
import time

load_dotenv()

def open_browser():
    time.sleep(1)  # Espera a que el servidor esté listo
    url = f"http://{os.getenv('FLASK_RUN_HOST', '127.0.0.1')}:{os.getenv('FLASK_RUN_PORT', 5000)}/home"
    webbrowser.open(url)

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=open_browser).start()
    app.run(
        host=os.getenv("FLASK_RUN_HOST", "0.0.0.0"), 
        port=int(os.getenv("FLASK_RUN_PORT", 5000)), 
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )
