from channel_utils import Channel
from encoder_utils import Encoder
from decoder_utils import Decoder
import numpy as np

L = 10 # Number of previous bits used
N = 23 # Number of output bits per input bit

# filenames
original_file  = '80char.txt'
encoded_file   = 'encoded.txt'
channel_output = 'channel_output.txt'
decoded_file   = 'decoded.txt'

def generate_generator_matrix():
    """
    Creates the generator matrix.
    We make sure that for each generator_polynomial (A line of the generator matrix), the first and the last bits are set to 1
    This is because we at least want b_i and b_{i-L} to be used to use the whole range L. The remaining coefficients are chosen
    at random as no method exists to optimally pick them deterministically.
    """
    generator_matrix = np.random.choice([0, 1], size=(N, L+1))
    generator_matrix[:,0] = 1
    generator_matrix[:,L] = 1
    return generator_matrix

def run_all(generator_matrix):
    channel = Channel(changingIndex=True, verbose=False)
    encoder = Encoder(input_file=original_file,  output_file=encoded_file, generator_matrix=generator_matrix, verbose=False)
    decoder = Decoder(input_file=channel_output, output_file=decoded_file, generator_matrix=generator_matrix, verbose=False)
    encoder.encode()
    channel.sendFileWithOutput(inputFileName=encoded_file, outputFileName=channel_output)
    decoded = decoder.decode()
    return decoded

nb_runs = 20
nb_matrix_trials = 3
with open(original_file, 'rb') as f:
    success_rates = []
    original_bytes = f.read()
    best_matrix = np.array([])
    best_success_rate = 0
    for j in range(nb_matrix_trials):
    	correctly_decoded = 0
    	decoding_errors = 0
    	generator_matrix = generate_generator_matrix()
    	print('Generator matrix :\n', generator_matrix)    
    	for i in range(nb_runs):
	        print(f'Matrix {j+1} - Run {i+1} :')
	        decoded = run_all(generator_matrix)
	        if decoded == original_bytes:
	            print('Successfully decoded')
	            correctly_decoded += 1
	        else:
	            print('Decoding error')
	            decoding_errors += 1
    	success_rate = correctly_decoded/(correctly_decoded + decoding_errors)
    	if success_rate >= best_success_rate:
	        best_success_rate = success_rate
	        best_matrix = generator_matrix
    	success_rates.append(success_rate)
    	print(f'Success rate : {success_rate}')
    	print()
    	print()
    print(f'Success rates : {success_rates}')
    print(f'Best success rate : {best_success_rate} obtained with matrix : \n{best_matrix}')

