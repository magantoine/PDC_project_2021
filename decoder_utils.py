import numpy as np

class Decoder:

    def __init__(self, input_file, output_file, n, verbose=False):
        self.input_file = input_file
        self.output_file = output_file
        self.verbose = verbose
        self.n = n
    
    def euclidean_distance(self, x, y):
        x = np.array(x)
        y = np.array(y)
        p = np.sum((x - y)**2)
        return np.sqrt(p)
    
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
        decoded_values = []
        # Guess the erased index
        J = np.argmin(np.array([np.sum(values[::3]**2), np.sum(values[1::3]**2), np.sum(values[2::3]**2)]))
        
        values = np.delete(values, np.arange(J, values.size, 3))
        
        for x in zip(*[iter(values)]*self.n):
            d1 = self.euclidean_distance(list(x), np.full(shape=self.n, fill_value=1, dtype=np.int))
            d2 = self.euclidean_distance(list(x), np.full(shape=self.n, fill_value=-1, dtype=np.int))
            decoded_values.append(1 if d1 <= d2 else 0)
        if self.verbose:
            print(f'Decoded values : {decoded_values}\n')
        return decoded_values
    
    def decode(self):
        # Read raw values from file
        values_array = np.loadtxt(self.input_file)
        # Decode the values
        decoded_values = self.decode_values(values_array)
        # Transform the bit array to bytes
        byte_array = bytearray(self.bits_to_bytes(decoded_values))
        
        # if self.verbose:
        print(byte_array)
        f = open(self.output_file, 'w+b')
        f.write(byte_array)
        f.close()
    
   
