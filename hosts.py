from terminaltables import AsciiTable
import argparse
import os


def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def update_hosts(hosts):
    hostsstring = ""

    for d, i in hosts.items():
        if validate_ip(i):
            hostsstring = hostsstring + i + "\t\t\t" + d + "\n"

    f = open(os.environ['WINDIR'] + '\\System32\\drivers\\etc\\hosts','w')
    f.seek(0)
    f.truncate()
    f.write(hostsstring)

    f.close()


def read_hosts():
    hosts = {}
    for line in open(os.environ['WINDIR'] + '\\System32\\drivers\\etc\\hosts'):
        if not line.startswith('#'):
            host = line.split()
            if len(host):
                hosts[host[1]] = host[0]

    return hosts


def add_host(domain, ip, hosts):
    if not validate_ip(ip):
        print("Invalid Ip!")
    else:
        hosts[domain] = ip

        print("Hosts updated!")

    return hosts


def remove_host(domain, hosts):
    del hosts[domain]
    return hosts


def display_table(hosts):
    table_data = [
        ["Hostname", "Ip"]
    ]

    for d, i in hosts.items():
        table_data.append([d, i])

    table = AsciiTable(table_data)
    print(table.table)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add')
    parser.add_argument('-ip', '--ip')
    parser.add_argument('-rm', '--remove')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.3')
    args = parser.parse_args()

    hosts = read_hosts()

    if args.add is not None and args.ip is not None:
        hosts = add_host(args.add, args.ip, hosts)
        update_hosts(hosts)

    if args.remove is not None:
        hosts = remove_host(args.remove, hosts)
        update_hosts(hosts)

    display_table(hosts)


if __name__ == "__main__":
    main()
