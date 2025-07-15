```python

def myfun(*args, **kwargs):
	print(args)
	print(kwargs)

myfun("hello", "2", "two", 1,"2",3, id="iota", name="karvin")

*args --> collects the input arguments as a list
*kwargs --> colects the input arguments as dictionary

```

## Collections

1. List -> Mutable and ordered collection

2. Tuple -> Immutable and ordereed collection

3. Set -> Mutable collection that stores only non repeatable element

4. Dictionary


### Dictionary 

```pgsql

# Initialize dictionary with default values
d = {}  # empty dictionary
d = dict()  # empty dictionary
d = {}.fromkeys(['a', 'b', 'c'], 0)  # initialize with default values
d = defaultdict(int)  # from collections, auto-initializes with 0 for integers
d = defaultdict(list)  # auto-initializes with empty list

# Adding/Updating
d[key] = value  # basic assignment
d.update({key: value})  # update/add single or multiple key-value pairs
d.setdefault(key, default_value)  # set key with default if doesn't exist
d[key] = d.get(key, 0) + 1  # increment counter pattern
d[key] = d.setdefault(key, 0) + 1  # another counter pattern

# Getting Values
value = d.get(key, default)  # get with default if key doesn't exist
value = d[key]  # direct access (raises KeyError if not found)

# Removing
d.pop(key, default)  # remove and return value (with optional default)
del d[key]  # remove key (raises KeyError if not found)
d.clear()  # remove all items

# Checking
key in d  # check if key exists
any(value == x for x in d.values())  # check if value exists
all(value > x for x in d.values())  # check condition for all values

# Iterating
[*d.keys()]  # keys as list
[*d.values()]  # values as list
[*d.items()]  # key-value pairs as list
sorted(d.items(), key=lambda x: x[1])  # sort by values
sorted(d.items(), key=lambda x: (-x[1], x[0]))  # sort by values desc, keys asc

# Dictionary Comprehension
{k: v for k, v in zip(keys, values)}  # create from two lists
{x: x**2 for x in range(5)}  # create with computed values
{k: v for k, v in d.items() if v > 0}  # filter dictionary

# Counter operations (from collections import Counter)
Counter(list_or_string)  # count occurrences
Counter(text).most_common(n)  # n most common elements
Counter(a) & Counter(b)  # intersection of counters
Counter(a) | Counter(b)  # union of counters

# Advanced Operations
{**d1, **d2}  # merge dictionaries (Python 3.5+)
dict(sorted(d.items()))  # sort by keys
max(d.items(), key=lambda x: x[1])  # get key with max value
min(d, key=d.get)  # get key with min value

```


