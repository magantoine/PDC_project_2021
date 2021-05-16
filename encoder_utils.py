import numpy as np

class Encoder:

    def __init__(self, input_file, output_file, n, verbose=False):
        self.input_file = input_file
        self.output_file = output_file
        self.verbose = verbose
        self.n = n // 2 * 3 # Account for the erased bit
        
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
    
    # Encode bits into values in [-1, 1]
    def bits_to_values(self, bits_array):
        values = []
        for bit in bits_array:
            values.extend(np.full(shape=self.n, fill_value=(-1 if bit == 0 else 1), dtype=np.int))
        if self.verbose:
            print(f'Encoded values : {values}\n')
        return values
    
    def encode(self):
        bits_array = self.file_to_bits(self.input_file, little_endian=False)
        values_array = self.bits_to_values(bits_array)
        np.savetxt(self.output_file, values_array)
        print(f'Total number of bits used : {len(values_array)}')
    
   
