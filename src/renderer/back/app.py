'''
Date: 2020-10-28 08:18:18
LastEditors: Please set LastEditors
LastEditTime: 2020-12-11 01:31:21
'''
from flask import Flask, request
import json
from scapy.all import *
from package import Package as PKG
import websocket as ws
from back1 import Sniffer 

def get_ifaces():
    dt = list(ifaces.data.items())
    dt = [i[1].data for i in dt]
    return dt


package_queue = []
# mp = MyPcap("Intel(R) Ethernet Connection (2) I219-V")
con = None
t1 = None
mp = None
sniffer = None
app = Flask(__name__)
SUCCESS = {"status": 0}
FAILED = {"status": -1}
@app.route("/api/getInterface")
def getInterface():
    return json.dumps(get_ifaces())

@app.route("/api/start")
def start():
    global sniffer
    no = request.args.get("no")
    try:
        sniffer.start_sniffer(6)
    except Exception as e:
        print(e)
        return json.dumps(FAILED)
    return json.dumps(SUCCESS)
    
@app.route("/api/pause")
def pause():
    global sniffer
    try:
        sniffer.pause_sniffer()
    except:
        return json.dumps(FAILED)
    return json.dumps(SUCCESS)

@app.route("/api/close")
def close():
    global sniffer

    sniffer.close_sniffer()
    return json.dumps(SUCCESS)
    


def mainprocess():
    global package_queue, mp, con, t1,sniffer
    con = ws.create_connection("ws://127.0.0.1:8083/")
    sniffer = Sniffer()
    @sniffer.handler
    def mhandler(x):
        global con
        time.sleep(2)
        p = PKG(raw(x))
        print("===Ether===")
        print(p.ethernet_header)
        t = {"detail": [{"name":"ethernet", "child": [{"name":i[0], "value": i[1]} for i in list(p.ethernet_header.items())]}]}
        if p.ip_version:
            print("===IP===")
            print(p.ipv4 if p.ip_version == 4 else p.ipv6)
            t["ip"] = p.ipv4 if p.ip_version == 4 else p.ipv6
            t["detail"].append({"name":"ip", "child": [{"name":i[0], "value": i[1]} for i in list(t["ip"].items()) if i[0] not in ["TCP", "UDP"]]})
            temp = t["ip"].get("TCP") or t["ip"].get("UDP")
            if temp:
                t["detail"].append({"name":t["ip"].get("protocol")["keyword"], "child": [{"name":i[0], "value": i[1]} for i in list(temp.items())]})   
            # con.send(json.dumps(p.ipv4 if p.ip_version == 4 else p.ipv6))
        elif p.frame_type == "arp":
            print("===ARP===")
            print(p.arp)
            t["arp"] = p.arp
            t["detail"].append({"name":"arp", "child": [{"name":i[0], "value": i[1]} for i in list(t["arp"].items())]})
            # con.send(json.dumps(p.arp))
        t["ethernet"] = p.ethernet_header
        t["ethernet"]["len"] = len(raw(x))
        try:
            con.send(json.dumps(t))
        except:
            time.sleep(5)
            if (con != None):
                con.close()
            con = ws.create_connection("ws://127.0.0.1:8083/")

    # sniffer.start_sniffer(22)
    app.run(debug=True)
    con.close()
    # @mp.listener
    # def pkg_callback(win_pcap, param, header, pkt_data):
    #     global package_queue,con
    #     time.sleep(5)
    #     p = Package(pkt_data)
    #     con.send(p._ip_header())
    #     print(p._ip_header())
    #     print(pkt_data)
    #     print("-------------------")
    # mp.run()
    # con.close()
        # mp.run()

# sniffer.start_sniffer(3)
# sniff(prn=handler, count=5)
mainprocess()