import protocol_types as p_types
import json
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
        self.frame_header, self.frame_tail = raw_data[:14], raw_data[-4:]
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

        self.parse()

    @staticmethod
    def parse_ip(ip_raw):
        return ".".join([str(i) for i in ip_raw])

    # return frame header information
    def _frame_header(self):
        frame = {
            "source_mac": self.smac,
            "destination_src": self.dmac,
            "frame_type": self.frame_type,
            "frame_check_sequence": bin(int.from_bytes(self.frame_tail, "big")),
        }
        return json.dumps(frame)

    @staticmethod
    def _to_int_str(b):
        return int.from_bytes(b)

    @staticmethod
    def _to_hex_str(b):
        return " ".join([hex(i)[2:].zfill(2) for i in b])

    @staticmethod
    def get_protocol(protocol):
        return (
            p_types.unassigned
            if not p_types.protocols.get(protocol)
            else p_types.protocols.get(protocol)
        )
    # return ip header information
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
            "source_address": self.parse_ip(self.saddr),
            "destination_address": self.parse_ip(self.daddr),
            "option": self._to_hex_str(self.option_padding),
            "data": self._to_hex_str(self.ip_data),
        }
        return json.dumps(ip)

    @staticmethod
    def parse_mac(raw):
        if len(raw) != 6:
            return ""
        return ":".join([hex(i)[2:].zfill(2) for i in raw])

    def parse(self):
        # frame head parsing
        self.dmac, self.smac = self.parse_mac(self.frame_header[:6]), self.parse_mac(
            self.frame_header[6:12]
        )

        # ip package head parsing
        self.ip_version, self.ihl = self.ip_package[0] >> 4, self.ip_package[0] & 15
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
