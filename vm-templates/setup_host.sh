#!/usr/bin/env bash
set -e

echo "[0/8] Switching to a stable Ubuntu mirror (Cloudflare)..."
sudo sed -i 's|http://us.archive.ubuntu.com/ubuntu|http://ubuntu.cloudflare.com/ubuntu|g' /etc/apt/sources.list
sudo sed -i 's|http://archive.ubuntu.com/ubuntu|http://ubuntu.cloudflare.com/ubuntu|g' /etc/apt/sources.list

echo "[1/8] Updating system..."
sudo apt update
sudo apt upgrade -y

echo "[2/8] Installing KVM and libvirt..."
sudo apt install -y \
  qemu-kvm libvirt-daemon-system libvirt-clients \
  virtinst bridge-utils

echo "[3/8] Enabling libvirt..."
sudo systemctl enable --now libvirtd

echo "[4/8] Installing Python and dependencies..."
sudo apt install -y python3 python3-venv python3-pip

echo "[5/8] Creating host-agent environment..."
mkdir -p ~/skyhost-host/agent
cd ~/skyhost-host/agent
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install psutil httpx

echo "[6/8] Creating host-agent skeleton..."
if [ ! -f "agent.py" ]; then
cat << 'EOF' > agent.py
import time, psutil, httpx, socket

CONTROLLER_URL = "http://<controller-ip>:8000"

def get_load():
    return {
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
    }

def register():
    data = get_load()
    try:
        r = httpx.post(f"{CONTROLLER_URL}/register-host", json=data, timeout=5)
        print("Register response:", r.status_code, r.text)
    except Exception as e:
        print("Register failed:", e)

def main():
    register()
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
EOF
fi

echo "[7/8] Creating template directories..."
mkdir -p ~/skyhost-host/templates/{alpine,lubuntu}

echo "[8/8] Host setup complete."
echo "Next steps:"
echo "  1. Manually place your custom qcow2 templates into:"
echo "       ~/skyhost-host/templates/alpine/"
echo "       ~/skyhost-host/templates/lubuntu/"
echo "  2. Update CONTROLLER_URL in agent.py"
echo "  3. Start the agent with:"
echo "       cd ~/skyhost-host/agent && source .venv/bin/activate && python3 agent.py"
