#!/usr/bin/env bash
set -e

echo "[0/8] Switching to a stable Ubuntu mirror (Cloudflare)..."
sudo sed -i 's|http://us.archive.ubuntu.com/ubuntu|http://ubuntu.cloudflare.com/ubuntu|g' /etc/apt/sources.list
sudo sed -i 's|http://archive.ubuntu.com/ubuntu|http://ubuntu.cloudflare.com/ubuntu|g' /etc/apt/sources.list

echo "[1/8] Updating system..."
sudo apt update && sudo apt upgrade -y

echo "[2/8] Installing controller dependencies..."
sudo apt install -y \
  python3 python3-venv python3-pip \
  qemu-utils cloud-image-utils \
  git curl jq

echo "[3/8] Creating SkyHost directory structure..."
mkdir -p ~/skyhost/{controller,templates}
mkdir -p ~/skyhost/templates/{alpine,lubuntu}

echo "[4/8] Creating Python virtual environment..."
cd ~/skyhost/controller
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

echo "[5/8] Installing Python packages..."
pip install --upgrade pip
pip install fastapi uvicorn[standard]

echo "[6/8] Creating FastAPI skeleton..."
if [ ! -f "main.py" ]; then
cat << 'EOF' > main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
EOF
fi

echo "[7/8] Creating run script..."
cat << 'EOF' > run.sh
#!/usr/bin/env bash
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
EOF
chmod +x run.sh

echo "[8/8] Controller setup complete."
echo "Start the API with: cd ~/skyhost/controller && ./run.sh"
