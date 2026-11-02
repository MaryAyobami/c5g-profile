"""
This profile sets up 3 nodes to run the Confidential5G experiment.
"""

import geni.portal as portal
import geni.rspec.pg as pg

pc = portal.Context()
request = pc.makeRequestRSpec()


def add_node(name, image, hardware_type):
    node = request.RawPC(name)
    node.disk_image = image
    node.component_manager_id = "urn:publicid:IDN+utah.cloudlab.us+authority+cm"
    if hardware_type:
        node.hardware_type = hardware_type
    return node


def add_lan(name, members):
    lan = request.LAN(name)
    for node, ip in members:
        iface = node.addInterface("if-" + name)
        iface.addAddress(pg.IPv4Address(ip, "255.255.255.0"))
        lan.addInterface(iface)


sgx = add_node("sgx-node", "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU24-64-STD", "d750")
tdx = add_node("tdx-node", "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU24-64-STD", "d760")
ueransim = add_node("ueransim-node", "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD", None)


add_lan("lan-core", [(sgx, "10.10.1.1"), (tdx, "10.10.1.2")])

add_lan("lan-ran", [(ueransim, "10.10.2.1"), (sgx, "10.10.2.2"), (tdx, "10.10.2.3")])

pc.printRequestRSpec(request)
