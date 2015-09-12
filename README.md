# deep-compare
The problem deep compare solves is figuring out where two 
potentially deep and complicated Python data structures differ.

This is important for unit tests where you hsve expected data and if the code under test
fails and generates slightly different result, you often want to see where exactly inside
the complex data structure things went south.

The code is in a module called deeper.py

The logic is very simple. Corresponding dictionaries, lists and tuples from both data structures 
are traversed and their items are compared one by one.

deeper will check and report the following for various data types: 

# Sets

* item count is different
* the difference between the sets if any (which item just in set A, which items just in set B)

# Lists / Tuples

* item count is different
* are the lists / tuples equal except for sort order?
* the index i of the first different item and the items themselves from list A and list B

# Dictionaries

* item count is different
* if the keys are different the keys just in A and the keys just in B
* if the keys are the same the key-value pairs that are different between A and B
