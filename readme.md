# SkyHost

SkyHost is a lightweight virtual machine orchestration platform designed to turn old or low-spec hardware into a small, unified compute cluster.

It provides:

- A central **Controller API**
- Lightweight **Host Agents**
- A simple **Web UI**
- VM provisioning using KVM + libvirt

SkyHost is built for schools, labs, hackathons, clubs, and small teams that want to repurpose existing hardware without deploying heavy enterprise tooling.

---

## What Problem Does SkyHost Solve?

Many organizations have spare machines that go unused because managing them together is complicated.

SkyHost makes it possible to:

- Connect multiple low-spec machines
- Automatically choose the least-loaded host
- Provision virtual machines through a web interface
- Keep the system simple and understandable

This project is intentionally lightweight and educational. It focuses on clarity and usability over complexity.

---

## How It Works

SkyHost has three core components:

### 1. Controller

- Built with **FastAPI**
- Maintains a registry of host nodes
- Polls each host for CPU, RAM, and VM usage
- Uses a simple least-loaded scheduling strategy
- Exposes a `/request-vm` endpoint
- Returns the VM console link after provisioning

The Controller acts as the brain of the cluster.

---

### 2. Host Agent

- Runs on each host machine
- Built with **FastAPI**
- Exposes:
  - `GET /status` → system metrics and VM count
  - `POST /start-vm` → clone and start a VM
- Uses:
  - `virsh` (libvirt) to manage VMs
  - `psutil` to gather system metrics

Each Host Agent manages virtualization locally while reporting status to the Controller.

---

### 3. Web UI

- Lightweight HTML + JavaScript
- Communicates only with the Controller
- Displays cluster status
- Allows users to request new VMs
- Displays returned VM links

No direct communication occurs between the UI and host machines.

---

## Architecture Overview

```
User → Web UI → Controller → Host Agent → KVM/libvirt → Virtual Machine
```

---

## Repository Structure

```
skyhost/
│
├── controller/      # Central scheduling API
├── agent/           # Host-side VM management service
├── ui/              # Web dashboard
├── bootstrapper/    # Setup helper scripts
├── vm-scripts/      # VM template setup instructions
└── docs/            # Architecture and documentation
```

---

## Technology Stack

**Backend**
- Python 3
- FastAPI
- psutil
- httpx / requests

**Virtualization**
- KVM
- libvirt
- virsh

**Frontend**
- HTML / JavaScript
- Bootstrap (or lightweight React)

**Recommended Host OS**
- Ubuntu Server 22.04

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/skyhost
cd skyhost
```

### 2. Start the Controller

```bash
cd controller
uvicorn app:app --reload --port 9000
```

### 3. Start a Host Agent

On each host machine:

```bash
cd agent
uvicorn agent:app --host 0.0.0.0 --port 8000
```

### 4. Open the Web UI

Open `ui/index.html` in a browser or serve it with a simple static server.

Once running, you can request virtual machines through the web interface.

---

## Future Improvements

- Smarter scheduling strategies
- Authentication and multi-user support
- VM lifecycle management (stop, destroy, snapshot)
- Web-based VM console integration
- Centralized logging

---

## License

MIT License
