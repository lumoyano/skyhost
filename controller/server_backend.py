from fastapi import FastAPI
from pydantic import BaseModel
import psutil
import httpx

# py -m pip install fastapi uvicorn[standard] httpx psutil
# py -m uvicorn controller.server_backend:app --host 127.0.0.1 --port 8000

app = FastAPI()

HOSTS = [
    "http://192.168.1.10:8001",
    "http://192.168.1.11:8001",
]

@app.get("/hosts")
def get_hosts():
    results = []
    for host in HOSTS:
        try:
            response = httpx.get(f"{host}/health", timeout=5.0)
            results.append({"host": host, "health": response.json()})
        except Exception:
            results.append({"host": host, "health": "unreachable"})
    return results


@app.get("/status")
def status():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "vms": 0  # placeholder until virsh is connected
    }


class VMRequest(BaseModel):
    template: str  # will be "alpine" or "lubuntu"

@app.post("/request-vm")
def request_vm(request: VMRequest):
    print(request.template)  # "alpine" or "lubuntu"
    return {"received": request.template}