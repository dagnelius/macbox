import socket
from mndp import MNDP


if __name__ == "__main__":
    MNDP.listen_for_packets()
    MNDP.trigger_discovery()
