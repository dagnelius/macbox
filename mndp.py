import struct
import socket


class MNDP:

    @staticmethod
    def packet_to_dict(packet) -> dict[str, str]:
        data = {}
        index = 0

        while index < len(packet):
            tlv_type, tlv_length = struct.unpack('!HH', packet[index:index + 4])
            index += 4
            tlv_value = packet[index:index + tlv_length]
            index += tlv_length

            if tlv_type == 1:
                data['mac_address'] = ':'.join(f'{b:02x}' for b in tlv_value)
            elif tlv_type == 5:
                data['vendor_name'] = tlv_value.decode()
            elif tlv_type == 7:
                data['software_version'] = tlv_value.decode()
            elif tlv_type == 8:
                data['platform_name'] = tlv_value.decode()
            elif tlv_type == 10:
                data['uptime'] = struct.unpack('!I', tlv_value)[0]
            elif tlv_type == 11:
                data['device_identity'] = tlv_value.decode()
            elif tlv_type == 12:
                data['platform_architecture'] = tlv_value.decode()
            elif tlv_type == 14:
                data['interface_count'] = tlv_value[0]
            elif tlv_type == 15:
                data['ipv6_address'] = ':'.join(f'{tlv_value[i:i + 2].hex()}' for i in range(0, len(tlv_value), 2))
            elif tlv_type == 16:
                data['interface_name'] = tlv_value.decode()
            elif tlv_type == 17:
                data['ipv4_address'] = '.'.join(str(b) for b in tlv_value)
        return data

    @staticmethod
    def trigger_discovery():

        mndp_query = b'\x00\x0e\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        mndp_port = 5678

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Send the MNDP query packet to the broadcast address '224.0.0.56'
        sock.sendto(mndp_query, ('255.255.255.255', mndp_port))

    @staticmethod
    def listen_for_packets():
        ip = "0.0.0.0"
        port = 5678

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, port))
        print(f"Listening for UDP packets on {ip}:{port}")

        while True:
            data, addr = sock.recvfrom(1024)
            data = MNDP.packet_to_dict(data)
            print(data)
