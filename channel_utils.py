import numpy as np

class Channel:

    def __init__(self, hardH = None, changingIndex=False, verbose=False):
        if(hardH == None) :
            self.H = np.random.randint(3)  ## creation of a channel with a given H
        else :
            self.H = hardH

        self.changingIndex = changingIndex
        self.verbose = verbose

    def send(self, chanInput):
        erasedIndex = 0
        if(self.changingIndex) :
            erasedIndex = np.random.randint(3)
        else :
            erasedIndex = self.H
        chanInput = np.clip(chanInput, -1, 1)
        chanInput[erasedIndex:len(chanInput):3] = 0 ## erased 1 bit out of 4

        print(f"Channel sending with H value {erasedIndex} :\n{chanInput}")
        return chanInput + np.sqrt(10) * np.random.randn(len(chanInput))

    def sendFile(self, fileName):
        chanInput = np.loadtxt(fileName)
        return self.send(chanInput)

    
def save_file(fileName, array):
    np.savetxt(fileName, array)

def serialize(channel_input):
    byte_array = list(map(lambda b : bin(b), bytearray(channel_input, encoding="utf-8")))
    res = np.array([])
    for byte in byte_array:
        if(len(byte[2:]) < 8):
            byte = "0b" + "0" * (8 - len(byte[2:])) + byte[2:]

        for bit in byte[2:]:
            res = np.append(res, bit)
    return np.array(list(map(lambda b : -1 if b == '0' else 1, res)))


def deserialize(channel_output):    
    bit_list = list(map(lambda x : '1' if x == 1 else '0', channel_output))
    res = ""
    bit_sequence = ""
    cnt = 0
    for bit in bit_list:
        cnt += 1
        bit_sequence += bit
        if(cnt % 8 == 0):
            res += chr(int(bit_sequence, 2))
            bit_sequence = ""

    return res  




