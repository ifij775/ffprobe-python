'''
FFUtils
'''

# Calculate bitrate (b/s) from packets
def calc_bitrate_from_packets(packets, duration):
    bytes = sum([packet.size() for packet in packets],0)
    return bytes*8/duration
