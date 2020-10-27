# from typing import Protocol
import protocol_types as p_types
import json
# class EtherPackage()
class Package:
    def __init__(self, raw_data):
        # data link layer
        self.frame_type_dict = {
            2048: "ipv4",
            2054: "arp",
            34916: "PPPoE",
            33024: "802.1Q",
            34525: "ipv6",
        }
        self.frame_header, self.frame_tail, self.frame_head_length = raw_data[:14], raw_data[-4:], int.from_bytes(raw_data[12:14], "big")
        self.frame_type = self.frame_type_dict.get(
            int.from_bytes(self.frame_header[12:14], "big")
        )
        self.frame_type = "Unknown" if not self.frame_type else self.frame_type
        self.ip_package = raw_data[14:-4] if raw_data != None else None
        # ip header
        self.ip_version = None
        self.ihl = None
        # self.ver_ihl = None # ip version and ip package head length
        self.tos = None  # type of service
        self.tlen = None  # total length
        self.identification = None  # 标识(Identification)
        self.flags = None
        self.offset = None
        self.flags_fo = None  # 标志位(Flags) (3 bits) + 段偏移量(Fragment offset) (13 bits)
        self.ttl = None  # 存活时间(Time to live)
        self.proto = None  # 协议(Protocol)
        self.crc = None  # 首部校验和(Header checksum)
        self.saddr = None  # 源地址(Source address) with 4 byte
        self.daddr = None  # 目的地址(Destination address)
        self.op_pad = None  # 选项与填充(Option + Padding)
        # udp header
        self.src_port = None  # 源端口(Source port)
        self.dist_port = None  # 目的端口(Destination port)
        self.len = None  # UDP数据包长度(Datagram length)
        self.crc = None  # 校验和(Checksum)

        
        self.ethernet_header = None
        self.ipv4 = None
        self.ipv6 = None
        self.arp = None
        self.parse()
    
    def parse(self):
        self.parse_ethernet()
        if self.frame_type in ["ipv4", "ipv6"]:
            self.parse_ip()
        elif self.frame_type == "arp":
            self.parse_arp()


    @staticmethod
    def parse_ipv4_addr(ip_raw):
        return ".".join([str(i) for i in ip_raw])

    def _frame_header(self):
        self.ethernet_header = {
            "source_mac": self.smac,
            "destination_src": self.dmac,
            "frame_type": self.frame_type,
            "frame_head_length": self.frame_head_length,
            "frame_check_sequence": bin(int.from_bytes(self.frame_tail, "big")),

        }
        # return json.dumps(frame)

    @staticmethod
    def _to_int_str(b):
        return int.from_bytes(b)

    @staticmethod
    def _to_hex_str(b):
        return " ".join([hex(i)[2:].zfill(2) for i in b])
    @staticmethod
    def _to_hex(b):
        return [hex(i)[2:].zfill(2) for i in b]
    @staticmethod
    def get_protocol(protocol):
        return (
            p_types.unassigned
            if not p_types.protocols.get(protocol)
            else p_types.protocols.get(protocol)
        )

    def _ip_header(self):
        ip = {
            "ip_version": self.ip_version,
            "ip_head_length": self.ihl,
            "type_of_service": self.tos,
            "tlen": self.tlen,
            "identification": self._to_hex_str(self.identification),
            "flags": self.flags,
            "fragment_offset": self.offset,
            "time_to_live": self.ttl,
            "protocol": self.get_protocol(self.proto),
            "header_checksum": str(bin(self.crc)),
            "source_address": self.parse_ipv4_addr(self.saddr),
            "destination_address": self.parse_ipv4_addr(self.daddr),
            "option": self._to_hex_str(self.option_padding),
            "data": self._to_hex_str(self.ip_data),
        }
        return json.dumps(ip)

    @staticmethod
    def parse_mac(raw):
        if len(raw) != 6:
            return ""
        return ":".join([hex(i)[2:].zfill(2) for i in raw])
    @staticmethod
    def parse_ipv6_addr(addr):
        return ":".join([self._to_hex(addr[i:i+4]) for i in range(0, len(addr), 4)])
    def parse_ethernet(self):
        # frame head parsing
        self.dmac, self.smac = self.parse_mac(self.frame_header[:6]), self.parse_mac(self.frame_header[6:12])
        self._frame_header()
    def parse_ip(self):
        # ip package head parsing
        self.ip_version = self.ip_package[0] >> 4
        if self.ip_version == 4:
            self.parse_ipv4(self.ip_package)
        elif self.ip_version == 6:
            self.parse_ipv6(self.ip_package)
        else:
            pass


    def parse_ipv4(self, pkg):
        self.ipv4 = {"ip_version": 4}
        self.ihl = self.ip_package[0] & 15
        self.tos = self.ip_package[1]
        self.tlen_raw = self.ip_package[2:4]
        self.tlen = int.from_bytes(self.tlen_raw, "big")
        self.identification = self.ip_package[4:6]
        self.flags_fo = int.from_bytes(self.ip_package[6:8], "big")
        self.flags, self.offset = self.flags_fo >> 13, self.flags_fo & ((1 << 14) - 1)
        self.ttl, self.proto = self.ip_package[8], self.ip_package[9]
        self.crc = int.from_bytes(self.ip_package[10:12], "big")
        self.saddr = self.ip_package[12:16]
        # self.saddr = int.from_bytes(self.ip_package[12:16], 'big')
        self.daddr = self.ip_package[16:20]
        # self.daddr = int.from_bytes(self.ip_package[16:20], 'big')
        self.option_padding = self.ip_package[20 : self.ihl << 2]
        self.ip_data = self.ip_package[(self.ihl << 2) :]
        # parse data
        self.ipv4 = {
            "ip_version": 4,
            "ip_head_length": self.ihl,
            "type_of_service": self.tos,
            "tlen": self.tlen,
            "identification": self._to_hex_str(self.identification),
            "flags": self.flags,
            "fragment_offset": self.offset,
            "time_to_live": self.ttl,
            "protocol": self.get_protocol(self.proto),
            "header_checksum": str(bin(self.crc)),
            "source_address": self.parse_ipv4_addr(self.saddr),
            "destination_address": self.parse_ipv4_addr(self.daddr),
            "option": self._to_hex_str(self.option_padding),
            "data": self._to_hex_str(self.ip_data),
        }
        if self.proto == 6:
            self.parse_tcp(self.ip_data)
        elif self.proto == 17:
            self.parse_udp(self.ip_data)
        return self.ipv4

    def parse_ipv6(self, pkg):
        # traffic class
        tc = ((pkg[0] & 0b1111) << 4) | (pkg[1] >> 4)
        # flow label
        fl = (pkg[1] & 0b1111).to_bytes(1, 'big') + pkg[2:4]
        # payload length
        plen = int.from_bytes(pkg[4:6])
        # next header
        nh = pkg[6]
        # hop limit
        hlim = pkg[7]
        # source 
        src = pkg[8:24]
        # destination
        dst = pkg[24:40]
        # data
        data = pkg[40:]
        self.ipv6 = {
            "tc": tc,
            "fl": fl,
            "plen": plen,
            "nh": nh,
            "hlim": hlim,
            "src": self.parse_ipv6_addr(src),
            "dst":self.parse_ipv4_addr(dst),
            "data": self._to_hex_str(data)
        }
        return self.ipv6
    
    def parse_arp(self, pkg):
        hwtype = int.from_bytes(pkg[0:2]) # hardware type
        ptype = int.from_bytes(pkg[2:4]) # protocol type
        hwlen = pkg[4] # hardware address length
        plen = pkg[5] # protocol address length
        op = int.from_bytes(pkg[6:8])
        hwsrc = self.parse_ipv6_addr(pkg[8:14]) # hw src
        psrc = self.parse_ipv4_addr(pkg[14:18]) # ip src
        hwdst = self.parse_ipv6_addr(pkg[18:24]) # hw dst
        pdst = self.parse_ipv4_addr(pkg[24:28]) # ip dst
        self.arp = {
            "hwtype": hwtype,
            "ptype": ptype,
            "hwlen": hwlen,
            "plen": plen,
            "op": op,
            "hwsrc": hwsrc,
            "psrc": psrc,
            "hwdst": hwdst,
            "pdst": pdst
        }
        return self.arp

    def parse_udp(self, pkg):
        sport = pkg[0:2]
        dport = pkg[2:4]
        ulen = pkg[4:6]
        chksum = pkg[6:8]
        data = pkg[8:]
        self.ipv4["UDP"] = {
            "sport": int.from_bytes(sport, "big"),
            "dport": int.from_bytes(dport, "big"),
            "len": int.from_bytes(ulen, "big"),
            "chksum": str(bin(int.from_bytes(chksum, "big"))),
            "data": self._to_hex_str(data)
        }
    def get_tcp_flag(self, flag):
        t = ['FIN', 'SYN', 'RST', 'PSH', 'ACK', 'URG', 'ERR']
        cnt = 0
        while (not (flag & 1)) and cnt < 6:
            flag >>= 1
            cnt += 1
        return t[cnt]


    def parse_tcp(self, pkg):
        sport = pkg[0:2]
        dport = pkg[2:4]
        seq = pkg[4:8]
        ack = pkg[8:12]
        dataofs = pkg[12] >> 4
        reserved = (pkg[13] & 15) << 2 | (pkg[14] >> 6)
        flags = self.get_tcp_flag(pkg[14] & ((1 << 7) - 1))
        window = pkg[14: 16]
        chksum = pkg[16: 18]
        urgptr = pkg[18: 20]
        options = pkg[20: dataofs << 4]
        data = pkg[dataofs << 4:]
        self.ipv4["tcp"] = {
            "sport": sport,
            "dport": dport,
            "seq": seq,
            "ack": ack,
            "dataofs": dataofs,
            "reserved": reserved,
            "flags": flags,
            "chksum": chksum,
            "urgptr": urgptr,
            "options": options,
            "data": data
        }