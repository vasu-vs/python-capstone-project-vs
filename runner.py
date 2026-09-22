import threading
import time
import uvicorn
import client

server = threading.Thread(
    target=uvicorn.run,
    args=("main:app",),
    kwargs={"host": "127.0.0.1", "port": 8000},
    daemon=True
)

server.start()
time.sleep(2)
client.main()