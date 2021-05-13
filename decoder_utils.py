import numpy as np

class Decoder:

    def __init__(self, input_file, output_file, verbose=False):
        self.input_file = input_file
        self.output_file = output_file
        self.verbose = verbose
    
    def bits_to_bytes(self, bits_array):
        done = False
        if len(bits_array) % 8 != 0:
            print('Corrupted bits array. Length should be multiple of 8')
        bytes_array = []
        it = 0
        for i in range(len(bits_array)//8):
            byte = 0
            for _ in range(8):
                bit = bits_array[it]
                byte = (byte << 1) | bit
                it += 1
            bytes_array.append(byte)
        return bytes_array
    
    # Reads array of floats and decodes them into integers (from the Alphabet)
    def decode_values(self, values):
        return list(map(lambda val : int(val), values))
    
    # Reads array of integers (from the Alphabet) and transforms them to bits
    def values_to_bits(self, values, block_size=1):
        return values
    
    def decode(self):
        # Read raw values from file
        values_array = np.loadtxt(self.input_file)
        # Decode the values
        decoded_values = self.decode_values(values_array)
        # Transform the decoded values to a bit array
        bits_array = self.values_to_bits(decoded_values)
        # Transform the bit array to bytes
        byte_array = bytearray(self.bits_to_bytes(bits_array))
        
        if self.verbose:
            print(byte_array)
        f = open(self.output_file, 'w+b')
        f.write(byte_array)
        f.close()
    
   
