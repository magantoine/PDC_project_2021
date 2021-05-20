import numpy as np
from collections import deque

class Encoder:

    def __init__(self, input_file, output_file, generator_matrix, verbose=False):
        self.input_file = input_file
        self.output_file = output_file
        self.verbose = verbose
        # The generator matrix holds the generator polynomials used to select which of the b_i participate in the product
        self.generator_matrix = generator_matrix
        self.N = generator_matrix.shape[0] # N is the number of output bits per input bit
        self.L = generator_matrix.shape[1] # L is the number of previous bits used when encoding (b_{i-L} ... b_{i-1})
    
    def repetition_encoding(self, array, nb_repetitions=3):
        """
        Apply a repetition code to the input array
        """
        repeated_array = []
        for val in array:
            repeated_array.extend(np.full(shape=nb_repetitions, fill_value=val, dtype=np.int))
        if self.verbose:
            print(f'Repeated values : {repeated_array}\n')
        return repeated_array
    
    def convolutional_encoding(self, array):
        """
        Apply convolutional coding on the input array, using the encoder's generator matrix
        """
        encoded_vals = []
        padded_array = [1] * (self.L - 1) + array # pre-pad the array with (L-1) ones (b_{i-L}...b_{i-1} are initialized to 1)
        for vals in window(padded_array, size=self.L):
            for generator_poly in self.generator_matrix: # For each generator polynomial we output one bit
                elems = generator_poly * list(vals) # Select the values that will participate in the product
                encoded_val = np.prod(elems[elems != 0]) # Discard the 0 values and perform the product
                encoded_vals.append(encoded_val)
        if self.verbose:
            print(f'Convolved values : {encoded_vals}\n')
        return encoded_vals
    
    def encode(self):
        """
        Encode the input sequence for sending to the noisy channel
        """
        bits_array = file_to_bits(self.input_file, little_endian=False) # Read file and get a bit array
        with open(self.input_file) as f:
            print(f.read())
        plus_minus_array = bits_to_plus_minus_one(bits_array) # maps the bits {1 -> +1, 0 -> -1}
        convolved = self.convolutional_encoding(plus_minus_array) # Compute the convolutional code
        repeated = self.repetition_encoding(convolved, nb_repetitions=3) # Apply the repetition code to mitigate the erased index
        np.savetxt(self.output_file, repeated)
        print(f'Total number of bits used : {len(repeated)}')

        
def file_to_bits(filename, little_endian=True, verbose=True):
    """
    Convert input file to bit array
    """
    bits = []
    with open(filename, 'rb') as f:
        bytes = f.read()
        if verbose:
            print(f'Original file : {bytes}\n')
        for b in bytes:
            for i in range(8):
                bits.append((b >> i) & 1 if little_endian else (b >> (7 - i)) & 1)
        if verbose:
            print(f'Bits array : {bits}\n')
        return np.array(bits)
            
def bits_to_plus_minus_one(bits_array):
    """
    Convert bits to +1, -+1 representation
    0 -> -1
    1 -> +1
    """
    return list(map(lambda bit: (-1 if bit == 0 else 1), bits_array))

def window(seq, size):
    """
    Creates a sliding window of size 'size' over the sequence 'seq'
    """
    it = iter(seq)
    win = deque((next(it, None) for _ in range(size)), maxlen=size)
    yield win
    append = win.append
    for e in it:
        append(e)
        yield win

