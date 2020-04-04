# A simple FIFO wrapper

It implements a blocking reading, and a blocking writing with optional timeout.

It requires a path to a fifo to initilize. The fifo doesn't need to be there, the class will create it when initilized.

Notice that fifos are strictly uni-directional.

## Usage

### Init

```python
from simplefifo.fifomanager import FIFOManager
```

Open for read:

```python
fm = FIFOManager('fifofile1', 'r')
```

Open for write:

```python
fm = FIFOManager('fifofile1', 'w')
```

Notice that this only initilize the instance. It won't open the fifo.

### Read from fifo

Call ```read()``` function. It will be blocked until the writer closes the fifo. 

```python
read_string = fm.read()
```

To listen to the fifo continuously, you can add a while true loop around it:

```python
while True:
	read_string = fm.read()
	do_something(read_string)
```

### Write to fifo

Call ```write()``` function. It will block until it has a reader.

```python
fm.write('some string')
```

You might want to add a timeout.

The function will return after timeout seconds, and it will abort its pending writing.

For example, adding a 5 seconds timeout.

```python
fm.write('some string', 5)
```
