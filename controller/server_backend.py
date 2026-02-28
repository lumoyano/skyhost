from fastapi import FastAPI
from pydantic import BaseModel
import httpx

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


class VMRequest(BaseModel):
    template: str  # will be "alpine" or "lubuntu"

@app.post("/request-vm")
def request_vm(request: VMRequest):
    print(request.template)  # "alpine" or "lubuntu"
    return {"received": request.template}