with open("data.txt", "r") as f:
    data = f.readlines()

hex = data[0].strip()
bin_num = ""
for h in hex:
    bin_curr = bin(int(h, 16))[2:]
    padding = 4 - len(bin_curr)
    bin_curr = "".join(["0" for i in range(padding)]) + bin_curr
    bin_num += bin_curr

version_sum = 0
# depth-first search
# each member of packet stack is a list of length 6:
# 0: start ind of packet, 1: current position of parser,
# 2: length of this packet (header + subpackets), 3: length of this packet parsed,
# 4: number of subpackets in packet, 5: number of subpackets parsed,
packet_stack = [[0, 0, -1, -1, -1, -1]]
while len(packet_stack) > 0:
    curr_packet = packet_stack[-1]
    start_ind, curr_pos, len_subpacket_string, len_subpacket_string_parsed, num_subpackets_total, num_subpackets_parsed = curr_packet
    version = int(bin_num[curr_pos:curr_pos + 3], 2)
    curr_pos += 3
    version_sum += version
    type_id = int(bin_num[curr_pos: curr_pos + 3], 2)
    curr_pos += 3
    if type_id == 4:
        # literal value
        bit_arr = ""
        keep_reading = True
        while keep_reading:
            keep_reading = bin_num[curr_pos] == "1"
            curr_pos += 1
            bit_arr += bin_num[curr_pos: curr_pos + 4]
            curr_pos += 4
        value = int(bit_arr, 2)
        popped = True
        while (len(packet_stack) > 0) and popped:
            # update parent node and pop it off the stack if parsing is complete
            node = packet_stack[-1]
            node[1] = curr_pos
            popped = False
            if (node[2] == -1) and (node[4] == -1):
                # literal
                packet_stack.pop()
                popped = True
            elif node[2] != -1:
                node[3] = curr_pos - node[0]
                if node[2] == node[3]:
                    packet_stack.pop()
                    popped = True
                else:
                    packet_stack.append([curr_pos, curr_pos, -1, -1, -1, -1])
            elif node[4] != -1:
                node[5] += 1
                if node[4] == node[5]:
                    packet_stack.pop()
                    popped = True
                else:
                    packet_stack.append([curr_pos, curr_pos, -1, -1, -1, -1])
    else:
        # there are subpackets
        length_type_id = int(bin_num[curr_pos])
        curr_pos += 1
        if length_type_id == 0:
            length_of_subpackets = int(bin_num[curr_pos:curr_pos + 15], 2)
            curr_pos += 15
            curr_packet[1] = curr_pos
            curr_packet[2] = length_of_subpackets + curr_pos - start_ind
            curr_packet[3] = curr_pos - start_ind
            packet_stack.append([curr_pos, curr_pos, -1, -1, -1, -1])
        else:
            number_of_subpackets = int(bin_num[curr_pos:curr_pos + 11], 2)
            curr_pos += 11
            curr_packet[1] = curr_pos
            curr_packet[4] = number_of_subpackets
            curr_packet[5] = 0
            packet_stack.append([curr_pos, curr_pos, -1, -1, -1, -1])

print(version_sum)
