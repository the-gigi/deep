# Deep

![deep image](http://i.imgur.com/tEZ0FD1.png)

The **deep** repository exposes two functions for performing operations on 
deeply nested Python objects:

* deep_compare()
* deep_getsizeof()

The code is in a module called [deeper.py](https://github.com/the-gigi/deep/blob/master/deeper.py)

The tests are in [deeper_test.py](https://github.com/the-gigi/deep/blob/master/deeper_test.py)

Note: it is not a Python package. Just a couple of functions.

## deep_compare()

The problem deep_compare() solves is figuring out where two 
potentially deep and complicated Python data structures differ.

This is important for unit tests where you hsve expected data and if the code under test
fails and generates slightly different result, you often want to see where exactly inside
the complex data structure things went south.

The logic is very simple. Corresponding dictionaries, lists and tuples from both data structures 
are traversed and their items are compared one by one.

deep_compare() will check and report the following for various data types: 

### Sets

* item count is different
* the difference between the sets if any (which item just in set A, which items just in set B)

### Lists / Tuples

* item count is different
* are the lists / tuples equal except for sort order?
* the index i of the first different item and the items themselves from list A and list B

### Dictionaries

* item count is different
* if the keys are different the keys just in A and the keys just in B
* if the keys are the same the key-value pairs that are different between A and B

## deep_getsizeof()

The problem deep_getsizeof() solves is how to calculate the memory foot print
of a potentially deeply nested Python object. Think a dictionary that contains
other dictionaries that contain lists of sets of tuples of primitive object.

The Python standard library has in the sys module a function called 
[getsizeof()](https://docs.python.org/dev/library/sys.html#sys.getsizeof). 
This function returns only the memory of the object itself and not the 
memory of object it refers to or contains. After writing my deep_getsizeof()
I discovered this [recursive sizeof recipe](http://code.activestate.com/recipes/577504).
But, I like my version better and also it gave me the opportunity to add 
another function to the **deep** repo.   
