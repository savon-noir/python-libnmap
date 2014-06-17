#!/usr/bin/env python
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException


# start a new nmap scan on localhost with some specific options
def do_scan(targets, options, fqp=None):
    parsed = None
    nm = NmapProcess(targets, options, fqp=fqp)
    rc = nm.run()
    if rc != 0:
        print("nmap scan failed: {0}".format(nm.stderr))

    try:
        parsed = NmapParser.parse(nm.stdout)
    except NmapParserException as e:
        print("Exception raised while parsing scan: {0}".format(e.msg))

    return parsed


# print scan results from a nmap report
def print_scan(nmap_report):
    print("Starting Nmap {0} ( http://nmap.org ) at {1}".format(
        nmap_report.version,
        nmap_report.started))

    for host in nmap_report.hosts:
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
        else:
            tmp_host = host.address

        print("Nmap scan report for {0} ({1})".format(
              tmp_host,
              host.address))
        print("Host is {0}.".format(host.status))
        print("  PORT     STATE         SERVICE")

        for serv in host.services:
            pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format(
                    str(serv.port),
                    serv.protocol,
                    serv.state,
                    serv.service)
            if len(serv.banner):
                pserv += " ({0})".format(serv.banner)
            print(pserv)
    print(nmap_report.summary)


if __name__ == "__main__":
    report = do_scan("127.0.0.1", "-sT")
    print_scan(report)
    # test with full path to bin
    # /usr/bin/nmap
    report = do_scan("127.0.0.1", "-sT", fqp="/usr/bin/nmap")
    print_scan(report)
    # /usr/bin/lol --> will throw exception
    try:
        report = do_scan("127.0.0.1", "-sV", fqp="/usr/bin/lol")
        print("lolbin")
        print_scan(report)
    except Exception as exc:
        print(exc)
