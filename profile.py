"""
This profile sets up 3 nodes to run the Confidential5G experiment.
"""

import geni.portal as portal
import geni.rspec.pg as pg

IMAGE = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU24-64-STD"
NETMASK = "255.255.255.0"

pc = portal.Context()
request = pc.makeRequestRSpec()


def add_node(name, hardware_type):
    node = request.RawPC(name)
    node.disk_image = IMAGE
    if hardware_type:
        node.hardware_type = hardware_type
    return node


def add_link(name, node_a, ip_a, node_b, ip_b):
    link = request.Link(name)
    for node, ip in ((node_a, ip_a), (node_b, ip_b)):
        iface = node.addInterface("if-" + name)
        iface.addAddress(pg.IPv4Address(ip, NETMASK))
        link.addInterface(iface)


sgx = add_node("sgx-node", "d750")
tdx = add_node("tdx-node", "d760")
ueransim = add_node("ueransim-node", None)

add_link("link-sgx-tdx", sgx, "10.10.1.1", tdx, "10.10.1.2")
add_link("link-ueransim-sgx", ueransim, "10.10.2.1", sgx, "10.10.2.2")
add_link("link-ueransim-tdx", ueransim, "10.10.3.1", tdx, "10.10.3.2")

pc.printRequestRSpec(request)
