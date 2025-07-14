```python

def myfun(*args, **kwargs):
	print(args)
	print(kwargs)

myfun("hello", "2", "two", 1,"2",3, id="iota", name="karvin")

*args --> collects the input arguments as a list
*kwargs --> colects the input arguments as dictionary 
