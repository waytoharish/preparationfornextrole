# 1. from given string give me a string of unique characters.
```python
val =  "8777A7645B5566C3455"

curr_dict = {}
for i in val:
    if i not in curr_dict:
        curr_dict[i] = 1
        # print(i)
    else:
        curr_dict[i] += 1
        # print(i)
print(curr_dict)

final_lst = tuple(key for key, value in curr_dict.items() if value == 1)
print(final_lst)

```
# 2. Generate the numbers between 0 to 100 divisible by 11 

```python
val = tuple(range(1,100,11))

print(val)
```
