#!/usr/bin/env python

from __future__ import print_function
from lxml import etree
import sys
import libvirt
import argparse

def usage():
    print("description of the parameters will be here")

def optParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('--name',required=True)
    parser.add_argument ('--count',required=True)
    parser.add_argument ('--ram',type=int,required=True)
    parser.add_argument ('--cpu',required=True)
    parser.add_argument ('--img',required=True)
    parser.add_argument ('--dompath',required=True)
 
    return parser

if __name__ == "__main__":

    parser = optParser()
    namespace = parser.parse_args(sys.argv[1:])

#    print (namespace)

    root = etree.Element('domain', type='kvm')

    name = etree.Element('name')
    name.text = namespace.name
    root.append(name)

    memory = etree.Element('memory', unit='KiB')
    memory.text = str(namespace.ram*1024)
    root.append(memory)

    current_memory = etree.Element('currentMemory', unit='KiB')
    current_memory.text = str(namespace.ram*1024)
    root.append(current_memory)

    vcpu = etree.Element('vcpu', placement='static')
    vcpu.text = namespace.cpu
    root.append(vcpu)

    os_def = etree.Element('os')
    os_type = etree.SubElement(os_def, 'type', arch='x86_64', machine='pc-i440fx-xenial')
    os_type.text = 'hvm'
    os_boot = etree.SubElement(os_def, 'boot', dev='hd')
    root.append(os_def)

    features = etree.Element('features')
    acpi = etree.SubElement(features, 'acpi')
    apic = etree.SubElement(features, 'apic')
    pae = etree.SubElement(features, 'pae')
    root.append(features)

    clock= etree.Element('clock', offset='utc')
    root.append(clock)

    on_power = etree.Element('on_power')
    on_power.text = 'destroy'
    root.append(on_power)
    on_reboot= etree.Element('on_reboot')
    on_reboot.text = 'restart'
    root.append(on_reboot)
    on_crash = etree.Element('on_crash')
    on_crash.text = 'restart'
    root.append(on_crash)

    devices = etree.Element('devices')
    emulator = etree.SubElement(devices, 'emulator')
    emulator.text = '/usr/bin/kvm-spice'
    disk_1 = etree.SubElement(devices, 'disk', type='file', device='disk')
    disk_1_driver = etree.SubElement(disk_1, 'driver', name='qemu', type='qcow2')
    disk_1_source = etree.SubElement(disk_1, 'source', file=namespace.img)
    disk_1_target = etree.SubElement(disk_1, 'target', dev='hda', bus='ide')
    serial = etree.SubElement(devices, 'serial', type='pty')
    serial_target=etree.SubElement(serial, 'target', port='0')
    serial.append(serial_target)
    devices.append(serial)
    console = etree.SubElement(devices, 'console', type='pty')
    console_target=etree.SubElement(serial, 'target', port='0')
    console.append(console_target)
    devices.append(console)
    network = etree.SubElement(devices, 'interface', type='network')
    #net_mac = etree.SubElement(network, 'mac', address='52:54:00:28:eb:e8')
    net_source = etree.SubElement(network, 'source', network='default')
    net_model = etree.SubElement(network, 'model', type='rtl8139')
    devices.append(network)
    root.append(devices)

    xmlconfig = etree.tostring(root, pretty_print=True)

    print (xmlconfig)

    conn = libvirt.open('qemu+ssh://libvirt-qemu@172.18.194.229/system')
    if conn == None:
        print('Failed to open connection to qemu:///system', file=sys.stderr)
        exit(1)
    
    dom = conn.createXML(xmlconfig, 0)
    if dom == None:
        print('Failed to create a domain from an XML definition.', file=sys.stderr)
        exit(1)

    try:
        p = conn.lookupByName(namespace.name)
    except libvirt.libvirtError:
        print ("Domain %s not found" % name)
        sys.exit(0)

    ifaces = p.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE, 0)
    if (ifaces == None):
        print ('Failed to get domain interfaces')
        sys.exit(0)

    print("The interface IP addresses:")
    for (name, val) in ifaces.iteritems():
        if val['addrs']:
            for ipaddr in val['addrs']:
                if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                    print(ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV4")
                    ip = ipaddr['addr']
    
    print('Guest '+dom.name()+' has booted', file=sys.stderr)

    conn.close()
    exit(0)

