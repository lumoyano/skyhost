import subprocess
import os

# Directories for templates and VM disks
TEMPLATE_DIR = "/home/vboxuser/template"
IMAGE_DIR = "/var/lib/libvirt/images"

def create_vm(name: str, template: str, cpu: int, ram: int):
    """
    Creates a VM using a qcow2 backing file and virt-install --import.
    Returns metadata needed by the controller/UI.
    """

    # 1. Resolve template path
    template_path = os.path.join(TEMPLATE_DIR, f"{template}.qcow2")
    if not os.path.exists(template_path):
        return {"error": f"Template not found: {template_path}"}

    # 2. Create VM disk as a qcow2 backing file
    vm_disk = os.path.join(IMAGE_DIR, f"{name}.qcow2")

    try:
        subprocess.run([
            "qemu-img", "create",
            "-f", "qcow2",
            "-b", template_path,
            vm_disk
        ], check=True)
    except subprocess.CalledProcessError:
        return {"error": "Failed to create qcow2 backing file"}

    # 3. Define VM using virt-install --import
    try:
        subprocess.run([
            "virt-install",
            "--name", name,
            "--memory", str(ram),
            "--vcpus", str(cpu),
            "--disk", f"path={vm_disk},format=qcow2",
            "--import",
            "--network", "network=default",
            "--graphics", "vnc,listen=0.0.0.0",
            "--noautoconsole"
        ], check=True)
    except subprocess.CalledProcessError:
        return {"error": "virt-install failed"}

    # 4. Start VM
    try:
        subprocess.run(["virsh", "start", name], check=True)
    except subprocess.CalledProcessError:
        return {"error": "Failed to start VM"}

    # 5. Detect VM IP (placeholder)
    ip = get_vm_ip(name)

    # 6. Detect VNC port (placeholder)
    vnc_port = get_vnc_port(name)

    # 7. Start websockify (placeholder)
    ws_port = start_websockify(vnc_port)

    return {
        "status": "running",
        "vm_name": name,
        "template": template,
        "cpu": cpu,
        "ram": ram,
        "ip": ip,
        "vnc_port": vnc_port,
        "websocket_port": ws_port
    }


def delete_vm(name: str):
    """
    Stops and deletes a VM and its qcow2 disk.
    """

    # Stop VM if running
    subprocess.run(["virsh", "destroy", name], check=False)

    # Remove VM definition
    subprocess.run(["virsh", "undefine", name], check=False)

    # Delete disk
    disk_path = os.path.join(IMAGE_DIR, f"{name}.qcow2")
    if os.path.exists(disk_path):
        os.remove(disk_path)

    # TODO: stop websockify if running

    return {"status": "deleted", "vm_name": name}


def get_vm_count():
    """
    Returns number of VMs defined on this host.
    """
    result = subprocess.run(
        ["virsh", "list", "--all"],
        capture_output=True,
        text=True
    )
    lines = result.stdout.strip().split("\n")
    return max(0, len(lines) - 2)


# -----------------------------
# PLACEHOLDERS TO IMPLEMENT NEXT
# -----------------------------

def get_vm_ip(name: str):
    """
    Placeholder for IP detection using virsh domifaddr.
    """
    return None


def get_vnc_port(name: str):
    """
    Placeholder for detecting VNC port from virsh dumpxml.
    """
    return None


def start_websockify(vnc_port: int):
    """
    Placeholder for launching websockify on a free port.
    """
    return None
