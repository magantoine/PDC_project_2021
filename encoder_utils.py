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

    def convolution(self, bits):
        """
        does the convolution of the bits to obtain the output the following fashion:

        b_n => (x_{3n}, x_{3n+1}, x_{3n+2}) = (b_n*b_{n-2}, b_{n-1}*b_{n-2}, b_n*b_{n-1}*b_{n-2})
        """
        xs = np.zeros((2*len(bits),))
        for i in range(len(bits)):
            if(i == 0):
                xs[2*i] = bits[i]
                xs[2*i + 1] = bits[i]
                #xs[2*i + 2] = bits[i]
            if(i == 1):
                xs[2*i] = bits[i]
                xs[2*i + 1] = bits[i - 1] * bits[i]
                #xs[2*i + 2] = bits[i - 1] * bits[i]
            else :
                xs[2*i] = bits[i] * bits[i - 2]
                xs[2*i + 1] = bits[i - 1] * bits[i - 2] * bits[i]
                #xs[3*i + 2] = bits[i] * bits[i - 1] * bits[i - 2]

        return xs
    
    def encode(self):
        bits_array = self.file_to_bits(self.input_file, little_endian=False)
        with open(self.input_file) as f:
            print(f.read())
        values_array = self.bits_to_values(bits_array)
        conv = self.convolution(values_array)
        print(visualize_convolution(values_array, conv))
        for bit in conv:
            print(bit)
        np.savetxt(self.output_file, values_array)
        print(f'Total number of bits used : {len(values_array)}')
    
   
def visualize_convolution(bit_vector, conv):
    print("length comparaison : ")
    print("conv = ", len(conv))
    print("init = ", len(bit_vector))
    print("ratio : ", len(conv) / len(bit_vector))
    for i in range(len(bit_vector)):
        if(i == 0):
            print(f"b_0 = {bit_vector[i]}")
        elif(i == 1):
            print(f"b_0, b_1 = {(bit_vector[i - 1], bit_vector[i])}")
        else :
            print(f"bn-2, bn-1, bn = {(bit_vector[i - 2], bit_vector[i - 1], bit_vector[i])}")
        print(f"(x2n, x2n+1) = {(conv[2*i], conv[2*i + 1])}")