#!/usr/bin/env python

from __future__ import print_function
from lxml import etree
import sys, getopt
import libvirt

def usage():
    print("description of the parameters will be here")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "count=","name=","ram=","disksize=","cpunum=","osimg=","storepath="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
        output = None
        verbose = False
        for opt, arg in opts:
            if opt == "-v":
                verbose = True
            elif opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt == "--name":
                print (arg)
            elif opt == "--count":
                count_nodes = arg
                print (count_nodes)
            else:
                assert False, "Please use -h"
                usage()

# create XML 
root = etree.Element('domain', type='kvm')

name = etree.Element('name')
name.text = 'VM_NAME'
root.append(name)

memory = etree.Element('memory', unit='KiB')
memory.text = '262144'
root.append(memory)

current_memory = etree.Element('currentMemory', unit='KiB')
current_memory.text = '262144'
root.append(current_memory)

vcpu = etree.Element('vcpu', placement='static')
vcpu.text = '1'
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
disk_1_source = etree.SubElement(disk_1, 'source', file='/vm/iso/xenial-server-cloudimg-amd64-disk1.img')
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


# pretty string
xmlconfig = etree.tostring(root, pretty_print=True)

print (xmlconfig)

#conn = libvirt.open('qemu:///system')
#if conn == None:
#    print('Failed to open connection to qemu:///system', file=sys.stderr)
#    exit(1)
#
#dom = conn.createXML(xmlconfig, 0)
#if dom == None:
#    print('Failed to create a domain from an XML definition.', file=sys.stderr)
#    exit(1)
#
#print('Guest '+dom.name()+' has booted', file=sys.stderr)
#
#conn.close()
#exit(0)

if __name__ == "__main__":
    main()
