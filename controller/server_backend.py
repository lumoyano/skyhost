from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

# py -m pip install fastapi uvicorn[standard] httpx psutil
# py -m uvicorn controller.server_backend:app --host 127.0.0.1 --port 8000 --reload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # lock this down for final development
    allow_methods=["*"],
    allow_headers=["*"],
)

class VMRequest(BaseModel):
    template: str  # will be "alpine" or "lubuntu"

    # "http://192.168.1.10:8001",
    # "http://192.168.1.11:8001",

HOSTS = [
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002"
]



def get_hosts():
    results = []
    for host in HOSTS:
        try:
            response = httpx.get(f"{host}/health", timeout=5.0)
            results.append({"host": host, "health": response.json()})
        except Exception:
            results.append({"host": host, "health": "unreachable"})
    return results

def get_best_host():
    hosts = get_hosts()
    best_host = min(hosts, key=lambda h: h["health"]["cpu"] + h["health"]["ram"])


@app.get("/")
def root():
    return {"message": "SkyHost Controller is running"}

@app.get("/hosts")
def hosts_endpoint():
    return get_hosts()



@app.post("/request-vm")
def request_vm(request: VMRequest):
    print(request.template)  # "alpine" or "lubuntu"

    httpx.post(f"{"host"}/start-vm", json={"template": request.template})
    return {"received": request.template}