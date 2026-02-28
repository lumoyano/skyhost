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
    name: str
    cpu: int = 1
    ram: int = 512
    # "http://192.168.1.10:8001",
    # "http://192.168.1.11:8001",

HOSTS = [
    "http://192.168.56.102:8002",
    "http://192.168.56.103:8003"
]



def get_hosts():
    results = []
    for host in HOSTS:
        try:
            response = httpx.get(f"{host}/health", timeout=5.0)
            results.append({"host": host, "health": response.json()})
        except Exception:
            results.append({"host": host, "health": None})
    return results

def get_best_host():
    hosts = get_hosts()

    reachable = [h for h in hosts if h["health"] is not None] 
    if not reachable: 
        return None
    
    best_host = min(reachable, key=lambda h: h["health"]["cpu"] + h["health"]["ram"])
    # Can add weights in next version: 
    # best_host = min(hosts, key=lambda h: (h["health"]["cpu"] * 0.3) + (h["health"]["ram"] * 0.7))
    return best_host


@app.get("/")
def root():
    return {"message": "SkyHost Controller is running"}

@app.get("/hosts")
def hosts_endpoint():
    return get_hosts()



@app.post("/request-vm")
def request_vm(request: VMRequest):
    print(request.template)  # "alpine" or "lubuntu"
    host = get_best_host()

    if host is None: 
        return {"error": "No hosts available"}

    host_url = host["host"] 
    response = httpx.post( 
        f"{host_url}/start-vm", 
        json={ 
            "template": request.template + "-template", 
            "name": request.name, 
            "cpu": request.cpu, 
            "ram": request.ram } ) 
    
    return { 
        "host": host_url, 
        "vm": response.json() 
    }