class PacketBase:
    @staticmethod
    def like(packet_data: dict) -> bool:
        return False

    def __init__(self, packet_data: dict):
        self.packet_data = packet_data
