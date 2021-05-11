# PDC_project_2021

channel_utils contains class Channel made to send a message via the channel of the exercise (only for test part, later use, the client given on moodle).

## Channel doc :

### parameters:

- ```hardH``` : enforced value for H (default : None, means the value is selected randomly)
- ```changingIndex``` : boolean that states if the erasing index H sould change each time a message is sent (default : False)
- ```verbose``` : Tells if the channel should be verbose or not (default : False)


### functions :

- ```send``` : takes ```chanInput``` (a sequence of float as input) and outputs the result produced by the channel

### Example :

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





