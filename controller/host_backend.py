from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psutil
import httpx

app = FastAPI()

vms = 0

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # lock this down for final development
    allow_methods=["*"],
    allow_headers=["*"],
)

class VMRequest(BaseModel):
    template: str  # will be "alpine" or "lubuntu"


@app.get("/health")
def status():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "vms": vms  # placeholder until virsh is connected
    }


@app.post("/start-vm")
def start_vm(request: VMRequest):
    # spin up the VM
    vms += 1
    return {"vm_name": "vm-abc123"}