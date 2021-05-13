import numpy as np

class Encoder:

    def __init__(self, input_file, output_file, verbose=False):
        self.input_file = input_file
        self.output_file = output_file
        self.verbose = verbose
        
    def file_to_bits(self, filename, little_endian=True):
        bits = []
        with open(filename, 'rb') as f:
            bytes = f.read()
            if self.verbose:
                print(f'Original file : {bytes}\n')
            for b in bytes:
                for i in range(8):
                    bits.append((b >> i) & 1 if little_endian else (b >> (7 - i)) & 1)
            if self.verbose:
                print(f'Bits array : {bits}\n')
            return np.array(bits)
    
    def bits_to_values(self, bits_array):
        # TODO : encode bits into values in [-1, 1]
        print('Warning : bits_to_values not implemented!\n')
        return bits_array
    
    def encode(self):
        bits_array = self.file_to_bits(self.input_file, little_endian=False)
        values_array = self.bits_to_values(bits_array)
        if self.verbose:
            print(f'Encoded values : {values_array}\n')
        np.savetxt(self.output_file, values_array)
    
   
