import numpy as np

class Decoder:

    def __init__(self, input_file, output_file, generator_matrix, verbose=False):
        self.input_file = input_file
        self.output_file = output_file
        self.verbose = verbose
        # The generator matrix holds the generator polynomials used to select which of the b_i participate in the product
        self.generator_matrix = generator_matrix
        self.N = generator_matrix.shape[0] # N is the number of output bits per input bit
        self.L = generator_matrix.shape[1] # L is the number of previous bits used when encoding (b_{i-L} ... b_{i-1})
    
    def guess_J(self, values):
        """
        Guess the J index by taking the sum of squares of all indices = 0, 1, 2 mod 3 respectively and setting J = argmin
        Probability of error is proportional to the total number bits and thus extremely low
        """
        # Guess the erased index
        J = np.argmin(np.array([np.sum(values[::3]**2), np.sum(values[1::3]**2), np.sum(values[2::3]**2)]))
        if self.verbose:
            print(f'Erased index is J = {J}')
        return J
    
    def compactify_values_3_repet(self, values, J):
        """
        Removes the values at index J and output the mean of the remaining 2 values
        Note that instead of throwing one of the bits away, taking the mean makes sure that the output value has only
        half the original noise variance!
        """
        compact_values = []
        values = np.delete(values, np.arange(J, values.size, 3)) # Delete 1 value out of 3 at multiples of the J index
        for x,y in zip(*[iter(values)]*2):
            compact_values.append((x+y)/2.) # Take the mean of the remaining 2 values (this reduces variance)
        return compact_values
    
    def compactify_values_2_repet(self, values, J):
        """
        Removes the values at index J and compactify the remaining values
        Some bits are single and others are duplicated (1/3 of the bits is duplicated).
        If a bit a duplicted we take the mean of the two copies as this reduces the noise variance for this bit.
        """
        compact_values = []
        i = 0
        for x,y in zip(*[iter(values)]*2):
            if i % 3 == J:
                compact_values.append(y) # x has been deleted so we output y
            elif (i+1) % 3 == J:
                compact_values.append(x) # y has been deleted so we output x
            else:
                compact_values.append((x+y)/2.) # Take the mean of the 2 values if none of them has been deleted
            i += 2
        print(f'Compact_values_length : {len(compact_values)}')
        return compact_values
    
    def generate_dico(self, n):
        """
        Generates the dictionary that represents the state diagram
        Given a key K = {bit_sequence} = {b_{i-L} ... {b_i}} it returns the output X of the encoding
        These values or computed only once for efficiency
        """
        dico = {}

        def compute_output(vals):
            encoded_vals = []
            for generator_poly in self.generator_matrix: # We output 1 bit per generator polynomial
                elems = generator_poly * list(vals) # Select only part of the bits
                encoded_val = np.prod(elems[elems != 0]) # Remove the non-selected bits and take the product
                                                         # Corresponds to b_{i-L}b_{i-3}b_i for example
                encoded_vals.append(encoded_val)
            return encoded_vals

        def generateAllBinaryStrings(n, arr, i): 
            if i == n:
                string = list_to_string(arr)
                dico[string] = compute_output(arr)
                return
            arr[i] = -1
            generateAllBinaryStrings(n, arr, i + 1) 
            arr[i] = 1
            generateAllBinaryStrings(n, arr, i + 1)

        arr = [None] * n
        generateAllBinaryStrings(n, arr, 0)
        return dico
    
    def viterbi_decoding(self, values):
        """
        Classical Viterbi decoding algorithm
        A key difference is that we don't pad with a final ending sequence of 1's when we finish, 
        we simply look for the state with the highest metric on the last depth when we finish processing all Y's.
        """
        dico = self.generate_dico(self.L) # Compute the output values of the state diagram
        if len(values) % self.N != 0:
            print(f'Corrupted values of length {len(values)}. Should be a multiple of {self.N}')
        nb_trellis_sections = int(len(values)/self.N)
        
        # Viterbi trellis dimensions :
        height = 2**(self.L-1)
        width = nb_trellis_sections + 1 # + 1 to account for the very first state
        print(f'Trellis height : {height}')
        print(f'Trellis width  : {width}')
        
        #Create the trellis with different arrays that stores various informations
        trellis_metrics = np.full((height, width), fill_value=float('-inf'), dtype=float) # Stores the metrics
        trellis_backpointers = np.full((height, width), fill_value="", dtype=object) # Stores the backpointers (used for backtracking)
        trellis_reaching_bits = np.ndarray((height, width), dtype=int) # Stores the bit used to reach this state

        idx = 1
        first_entry = '1' * (self.L - 1) # We start at state '11...1'
        first_entry_int = plus_minus_string_to_int(first_entry)
        trellis_metrics[first_entry_int, 0] = 0 # Initialize the trellis metric to 0
        active_entries = [first_entry] # Stores the states that have been reached in the previous iteration
        
        print('Decoding ...')
        
        for Y in zip(*[iter(values)]*self.N): # decompose into chunks of self.N lengths to process each trellis section independently
            new_active_entries = [] # We will set the states we reach as active so that they can be used for the next iteration
            for current_state in active_entries:
                for i in [1, -1]: # Handle both arrows (+1 and -1)
                    key = current_state + str(i) # represents {b_{i-L} ... b_i}
                    X = dico[key] # returns a list of self.N ints (the X-vector in the Viterbi algorithm)
                    metric = np.sum(np.array(list(Y)) * X) # Compute the metric
                    next_state = list_to_string(string_to_list(key)[1:]) # We get the next state by forgetting b_{i-L}

                    # Simply transforms the states to ints so that they can be used as indexes in the numpy arrays
                    current_state_int = plus_minus_string_to_int(current_state) 
                    next_state_int = plus_minus_string_to_int(next_state)

                    curr_best_metric = trellis_metrics[next_state_int, idx] # Current metric of the next state
                    potential_metric = metric + trellis_metrics[current_state_int, idx-1] # Metric if we reach it from current state
                    if potential_metric > curr_best_metric: #If higher metric, we update the metric, back_pointers etc...
                        trellis_metrics[next_state_int, idx] = potential_metric
                        trellis_backpointers[next_state_int, idx] = current_state
                        trellis_reaching_bits[next_state_int, idx] = i
                        new_active_entries.append(next_state)
            active_entries = new_active_entries
            idx += 1
            print("Progress: " + "{:.2f}".format(100*idx/nb_trellis_sections)+ "%", end='\r')
        
        idx -= 1
        # Find endpoint
        # We look for the state with highest metric on the final depth
        # Note that we don't need to add dummy bits to get to the state '11...1', it is enough to find the state with highest metric
        final_entry = ""
        best_metric = float('-inf')
        for active_entry in active_entries:
            active_entry_int = plus_minus_string_to_int(active_entry) # Transform state to int to be used as index
            metric = trellis_metrics[active_entry_int, idx]
            if metric > best_metric:
                best_metric = metric
                final_entry = active_entry
                            
        # Backtrack
        # Once we have the final state, we follow teh backpointers until the orignal state at depth 0
        decoded_values = []
        while idx > 0:
            final_entry_int = plus_minus_string_to_int(final_entry) # Transform state to int to be used as index
            decoded_val = trellis_reaching_bits[final_entry_int, idx] # The decoded value is the bit we used to reach this state
            decoded_values.append((0 if decoded_val == -1 else 1))
            final_entry = trellis_backpointers[final_entry_int, idx] # We go to the state on previous depth
            idx -= 1
        
        # Need to reverse since we traversed the trellis backwards
        # We discard the last byte since we send one extra byte when transmitting
        return list(reversed(decoded_values))[:-8]
    
    # Reads array of floats and decodes them into bits
    def decode_values(self, values):
        decoded_values = []
        J = self.guess_J(values)
        values = self.compactify_values_2_repet(values, J) # get rid of the deleted bits and merge the 2 remaining ones
        
        #At this stage we got rid of the repetition code
        # We now need to decode using Viterbi
        decoded_values = self.viterbi_decoding(values)

        if self.verbose:
            print(f'Decoded values : {decoded_values}\n')
        return decoded_values
    
    def decode(self):
        # Read raw values from file
        values_array = np.loadtxt(self.input_file)
        if self.verbose:
            print(f'Nb values to decode : {len(values_array)}')
        # Decode the values
        decoded_values = self.decode_values(values_array)
        # Transform the bit array to bytes
        byte_array = bits_to_bytes(decoded_values)
        
        print(byte_array)
        f = open(self.output_file, 'w+b')
        f.write(byte_array)
        f.close()
        return byte_array

def bits_to_bytes(bits_array):
    """
    Group 8-bits into bytes and return the corresponding byte array
    """
    done = False
    if len(bits_array) % 8 != 0:
        print(f'Corrupted bits array. Length should be multiple of 8, but was {len(bits_array)}')
    bytes_array = []
    it = 0
    for i in range(len(bits_array)//8):
        byte = 0
        for _ in range(8):
            bit = bits_array[it]
            byte = (byte << 1) | bit
            it += 1
        bytes_array.append(byte)
    return bytearray(bytes_array)   


def string_to_list(string):
    """
    Transform a string of {+1, -1} into a list of {+1, -1}
    Example : '1-1-11' is transformed into [1, -1, -1, 1]
    """
    list = []
    i = 0
    while i < len(string):
        if string[i] == '1':
            list.append(1)
            i += 1
        else:
            list.append(-1)
            i += 2
    return np.array(list)

def list_to_string(list):
    """
    Transform a list of {+1, -1} into a string of {+1, -1}
    Example : [1, -1, -1, 1] is transformed into '1-1-11'
    """
    s = ""
    for i in list:
        s += str(i)
    return s

def plus_minus_string_to_int(string):
    """
    Transform a string of {+1, -1} into an integer, where -1 is interpreted as 0 and 1 is interpreted as 1
    Example : '1-1-11' is equivalent to '1001' and is transformed to 1 + 2 * 0 + 4 * 0 + 8 * 1 = 9
    """
    li = list(string_to_list(string))
    li = list(map(lambda e: (0 if e == -1 else 1), li))
    power = 1
    number = 0
    for i in li:
        number += i * power
        power *= 2
    return number