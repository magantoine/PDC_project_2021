# PDC_project_2021

channel_utils contains class Channel made to send a message via the channel of the exercise (only for test part, later use, the client given on moodle).
## Utils function :

- ```saveFile``` : takes ```fileName``` (name of the file to save) and ```array``` (the array to write)
## Channel doc :

### parameters:

- ```hardH``` : enforced value for H (default : None, means the value is selected randomly)
- ```changingIndex``` : boolean that states if the erasing index H sould change each time a message is sent (default : False)
- ```verbose``` : Tells if the channel should be verbose or not (default : False)


### functions :

- ```send``` : takes ```chanInput``` (a sequence of float as input) and outputs the result produced by the channel
- ```sendFile``` : takes ```fileName``` (the path to the file) and outputs the result produced by the channel
- ```serialize``` : takes ```channel_input``` (the string to input to the channel) and output a version of the string that go through the channel
- ```deserialize``` : takes ```channel_output``` (takes a list of item $\in \{-1, 1\}$) and outputs the strings to which it corresponds

## Example :

#### (De)serialization :

```python
import channel_utils as cu

ser = cu.serialize("Hello World !")
print(f"Serialized version : {ser}")

des = cu.deserialize(ser)
print(f"Deserialized version : {des}")
```

should print :

```
Serialized version : [-1  1 -1 -1  1 -1 -1 -1 -1  1  1 -1 -1  1 -1  1 -1  1  1 -1  1  1 -1 -1
 -1  1  1 -1  1  1 -1 -1 -1  1  1 -1  1  1  1  1 -1 -1  1 -1 -1 -1 -1 -1
 -1  1 -1  1 -1  1  1  1 -1  1  1 -1  1  1  1  1 -1  1  1  1 -1 -1  1 -1
 -1  1  1 -1  1  1 -1 -1 -1  1  1 -1 -1  1 -1 -1 -1 -1  1 -1 -1 -1 -1 -1
 -1 -1  1 -1 -1 -1 -1  1]
Deserialized version : Hello World !

```



#### Channel usuage :
```python
from channel_utils import Channel
channel = Channel(changingIndex=True, verbose=True)
chanInput = np.random.uniform(-2, 2, 10)
print(f"received : {channel.send(chanInput)}")
```

Should print : 

```
Channel sending with H value 2 :
[-0.39333661  1.          0.         -0.85792374 -1.          0.
  0.54399218 -0.59318073  0.          0.94560034]
received : [ -3.38828823   5.17509715  -0.25823762   1.43121618  -2.09890863
   0.15153544   0.90111504  -2.01639729  -4.00289955 -10.80346648]
```   





