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
