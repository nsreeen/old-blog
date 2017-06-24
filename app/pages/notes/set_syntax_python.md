title: set syntax in python
date: 2017-05-23 12:00:00
published: false
type: notes

# 1) Remember
```
>>> a = {'a'}
>>> type(a)
<class 'set'>
>>> a
{'a'}

>>> b = {}
>>> type(b)
<class 'dict'>

>>> c = set()
>>> type(c)
<class 'set'>
>>> c
set()
>>> c.add('v')
>>> c
{'v'}
```

# 2) Interesting syntax - set comparison operators

UNION - sum of two sets
union = a | b

INTERSECTION - the items in both sets
intersection = a & b

DIFFERENCE - things in a, that are not in b
difference = a - b



# 3) Comparison methods for set and frozen set classes

len(s)

* Return True or False

x in s
x not in s

s.isdisjoint(s2)  (no elements in common)
s.issubset(s2)  (every element on s is found in s2 ... s <= s2)
s.issuperset(s2) (every element of s2 is in s ... s >= s2))



* Return a set

-- The syntax below may be clearer than the equivalent shown in 1
-- Also, unlike in 1, the argument passed doesn't have to be a set(can be any iterable object)

s.union(s2(, s3, ..))
s.intersection(s2)
s.difference(s2)
s.symmetric difference(s2) 


# 4) Set class methods (not available for frozenset)

* updates the set (in place)

s.update(s2, s3) (adds all elements from s2 and s3 to s)
s.intersection_update(s2, s3)  (removes elements from s that are not found in all other sets)
s.symmetric_difference(s2)
s.add(el)
s.remove(el)  (raises error if el not present)
s.discard(el) (removes set if present, if not present no error raised)
s.pop()  (returns a random el, error is set empty)
s.clear()  (removes all els)



