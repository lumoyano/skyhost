import libvirt
import subprocess
import os
import socket
import uuid
import xml.etree.ElementTree as ET

TEMPLATE_DIR = "/home/vboxuser/template"
IMAGE_DIR = "/var/lib/libvirt/images"


def get_conn():
    conn = libvirt.open("qemu:///system")
    if conn is None:
        raise RuntimeError("Failed to open libvirt connection")
    return conn


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def create_backing_disk(name, template):
    template_path = os.path.join(TEMPLATE_DIR, f"{template}.qcow2")
    vm_disk = os.path.join(IMAGE_DIR, f"{name}.qcow2")

    if not os.path.exists(template_path):
        raise FileNotFoundError("Template not found")

    subprocess.run([
        "qemu-img", "create",
        "-f", "qcow2",
        "-F", "qcow2",
        "-b", template_path,
        vm_disk
    ], check=True)

    return vm_disk


def build_domain_xml(name, cpu, ram, disk_path):
    vm_uuid = str(uuid.uuid4())

    xml = f"""
    <domain type='kvm'>
      <name>{name}</name>
      <uuid>{vm_uuid}</uuid>
      <memory unit='MiB'>{ram}</memory>
      <vcpu>{cpu}</vcpu>

      <os>
        <type arch='x86_64'>hvm</type>
      </os>

      <features>
        <acpi/>
        <apic/>
      </features>

      <cpu mode='host-model'/>

      <devices>
        <disk type='file' device='disk'>
          <driver name='qemu' type='qcow2'/>
          <source file='{disk_path}'/>
          <target dev='vda' bus='virtio'/>
        </disk>

        <interface type='network'>
          <source network='default'/>
          <model type='virtio'/>
        </interface>

        <graphics type='vnc' port='-1' listen='0.0.0.0'/>
        <console type='pty'/>
      </devices>
    </domain>
    """
    return xml


def create_vm(name, template, cpu, ram):
    conn = get_conn()

    try:
        disk_path = create_backing_disk(name, template)

        xml = build_domain_xml(name, cpu, ram, disk_path)

        domain = conn.defineXML(xml)
        if domain is None:
            return {"error": "Failed to define domain"}

        domain.create()  # start VM

        vnc_port = get_vnc_port(domain)
        ws_port = start_websockify(vnc_port) if vnc_port else None

        return {
            "status": "running",
            "vm_name": name,
            "vnc_port": vnc_port,
            "websocket_port": ws_port,
            "websocket_url": f"ws://{get_host_ip()}:{ws_port}" if ws_port else None
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()


def delete_vm(name):
    conn = get_conn()

    try:
        domain = conn.lookupByName(name)

        if domain.isActive():
            domain.destroy()

        domain.undefine()

        disk_path = os.path.join(IMAGE_DIR, f"{name}.qcow2")
        if os.path.exists(disk_path):
            os.remove(disk_path)

        return {"status": "deleted", "vm_name": name}

    except libvirt.libvirtError:
        return {"error": "VM not found"}

    finally:
        conn.close()


def get_vnc_port(domain):
    xml = domain.XMLDesc()
    tree = ET.fromstring(xml)

    graphics = tree.find("./devices/graphics")
    if graphics is not None:
        port = graphics.get("port")
        if port and port != "-1":
            return int(port)

    return None


def start_websockify(vnc_port):
    ws_port = find_free_port(6080, 7000)
    if not ws_port:
        return None

    cmd = f"websockify {ws_port} localhost:{vnc_port} --daemon"
    os.system(cmd)
    return ws_port


def find_free_port(start, end):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return None