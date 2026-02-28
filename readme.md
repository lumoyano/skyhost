# SkyHost

SkyHost is a lightweight VM-orchestration platform designed to turn old or low-spec hardware into a unified compute cluster. It provides a central controller, host agents, a simple web UI, and a bootstrapper that helps users set up either a Host Node or the Controller.

SkyHost is built for environments like schools, clubs, and small teams where hardware is inconsistent and ease of setup is critical.

---

## Repository Structure

```
skyhost/
│
├── controller/          # holds the FastAPI backend, scheduling logic, and host registry. This is the “brain” of SkyHost.
├── agent/               # contains the Host Agent FastAPI service, virsh integration, and system metrics. This is what runs on every host machine.
├── ui/                  # is the user-facing dashboard. It only talks to the controller, never directly to hosts.
├── bootstrapper/        # is your future installer/ISO downloader. For now, it’s a simple script with a menu.
├── vm-scripts/          # stores setup instructions, not images. qcow2 files stay local.
└── docs/                # Team onboarding, architecture, demo plan
```

Each folder is isolated so teammates can work independently with minimal merge conflicts.

---

## High-Level Architecture

SkyHost consists of four major components:

### Controller

- FastAPI backend  
- Polls all hosts for CPU/RAM/VM count  
- Runs a simple scheduler (least-loaded host)  
- Exposes `/request-vm` for the UI  
- Returns VM console URLs  

### Host Agent

- Runs on each Host Node  
- FastAPI service exposing:
  - `GET /status` → CPU, RAM, VM count  
  - `POST /start-vm` → clone + start VM  
- Uses `virsh` to manage VMs  
- Uses `psutil` for metrics  

### Web UI

- HTML/JS + Bootstrap (or lightweight React)  
- Displays host load  
- Provides a “Request VM” button  
- Shows the VM link returned by the controller  

### VM Templates

- Alpine Linux (lightweight)  
- Lubuntu or Debian LXDE (GUI)  
- Stored locally, not committed to Git  
- Cloned by the Host Agent when provisioning VMs  

### Bootstrapper (Final App)

- Simple script or CLI tool  
- Lets user choose:
  - “Set up Host Node”
  - “Set up Controller”
- Downloads correct ISO or setup script  
- Future: autoinstall, USB creation, EXE bundling  

---

## Tech Stack

### Languages

- Python 3  
- Bash (optional)  
- HTML/JS (or React)  

### Frameworks

- FastAPI (controller + agent)  
- Bootstrap or React (UI)  

### Tools

- KVM + libvirt  
- `virsh` CLI  
- `psutil`  
- `httpx` / `requests`  

### Operating Systems

- Ubuntu Server 22.04 (hosts + controller)  
- Alpine Linux (lightweight guest)  
- Lubuntu or Debian LXDE (GUI guest)  

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/skyhost
cd skyhost
```

### 2. Review the docs

Inside `docs/` you’ll find:

- `TEAM_PROMPT.md` — onboarding prompt for teammates to paste into their LLM  
- `architecture.md` — system overview  
- `demo_plan.md` — how to present SkyHost  
- `setup_instructions.md` — how to prepare hosts and templates  

### 3. Choose your component

Each teammate works inside one folder:

- `controller/` → Controller Developer  
- `agent/` → Host Agent Developer  
- `ui/` → Web UI Developer  
- `bootstrapper/` → Final App Developer  
- `vm-templates/` → VM Template Creator  

---

## Development Overview

### Controller

Run locally:

```bash
cd controller
uvicorn app:app --reload --port 9000
```

### Host Agent

Run on each host:

```bash
cd agent
uvicorn agent:app --host 0.0.0.0 --port 8000
```

### Web UI

Open `ui/index.html` in a browser  
or serve with any static file server.

### Bootstrapper

Run:

```bash
cd bootstrapper
python3 skyhost_setup.py
```

---

## VM Templates

VM templates are **not stored in Git**. Instead, `vm-templates/README.md` explains how to create:

- Alpine template (128–256 MB RAM)  
- GUI template (Lubuntu or Debian LXDE)  

These templates are cloned by the Host Agent when provisioning VMs.

---

## Hackathon Deliverables

- Working controller with scheduling logic  
- Host agent responding to `/status` and `/start-vm`  
- Two VM hosts + one weak machine  
- Web UI that can request VMs  
- Demo showing mixed workloads and scheduling decisions  
- Bootstrapper that lets users choose Host vs Controller setup  

---

## Team Onboarding

Before starting work, each teammate should paste the contents of:

```
docs/TEAM_PROMPT.md
```

into their LLM. This ensures consistent guidance, tech stack usage, and scope control.

---

## License

MIT (or choose your preferred license)