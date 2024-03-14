import sys
import socket
import requests
import netifaces as ni

from pyflow import Workflow

def get_interface_ips(interface):
    # This function will attempt to fetch both IPv4 and IPv6 addresses for a specified network interface.
    ip_info = {'ipv4': 'Not available', 'ipv6': 'Not available'}
    addrs = ni.ifaddresses(interface)
    # Get IPv4
    if ni.AF_INET in addrs:
        ip_info['ipv4'] = addrs[ni.AF_INET][0]['addr']
    # Get IPv6
    if ni.AF_INET6 in addrs:
        ip_info['ipv6'] = addrs[ni.AF_INET6][0]['addr']
    return ip_info

def get_public_ip():
    # Fetching public IPv4 and IPv6
    try:
        public_ip_v4 = requests.get('https://api.ipify.org').text
    except Exception as e:
        public_ip_v4 = "Not available"
    try:
        public_ip_v6 = requests.get('https://api64.ipify.org').text
    except Exception as e:
        public_ip_v6 = "Not available"
    return public_ip_v4, public_ip_v6

def main(workflow):
    
    output = []
    public_ipv4, public_ipv6 = get_public_ip()
    output.append({"name":"public","ip":public_ipv4})


    for interface in ni.interfaces():
        try:
            ip_info = get_interface_ips(interface)

            if not ip_info['ipv4'] == "Not available":
                #print(f"{interface} {ip_info['ipv4']}")
                output.append({"name":interface,"ip":ip_info['ipv4']})

            if not ip_info['ipv6'] == "Not available":
                #print(f"{interface} {ip_info['ipv6']}")
                output.append({"name":interface,"ip":ip_info['ipv6']})

        except ValueError:
            # This can happen if a network interface is not up or does not have an IP assigned.
            pass


    for item in output:
        workflow.new_item(
            title=" {}".format(item["ip"]),
            subtitle= item["name"],
            arg=item["ip"],
            copytext=item["ip"],
            valid=True,
        )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
