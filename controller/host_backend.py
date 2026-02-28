from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from manager import create_vm, delete_vm, get_vm_count
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
    template: str # "alpine" or "lubuntu" 
    name: str # VM name 
    cpu: int = 1 
    ram: int = 512


@app.get("/health")
def status():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "vms": get_vm_count()  
    }


@app.post("/start-vm") 
def start_vm(req: VMRequest):
     result = create_vm( 
         name=req.name, 
         template=req.template, 
         cpu=req.cpu, 
         ram=req.ram 
         ) 
     return result 

@app.post("/delete-vm/{name}") 
def delete_vm_endpoint(name: str): 
    return delete_vm(name)