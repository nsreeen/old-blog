title: python internals - what does infinity look like in memory?
date: 2017-05-23 12:00:00
published: false
type: notes


id -> hex -> address (in cpython the id is the memory address, not nec so for other implementations)
how do I look that address up in memory from within python???

inspect? -> seems to be good for examining more complicated things like classes and functions 
https://docs.python.org/3.5/library/inspect.html

is infinity an object that is pointed too (like with integers up to ~?256?) -> compare ids -> no it isn't

# interesting modules:

* tracemalloc: to trace memory allocation by python

* cinspect: like inspect but for parts of python written in c

* ctypes: provides c compatible datatypes, can wrap c libraries in pure python


```
import ctypes

x = float('infinity')

var = ctypes.POINTER(ctypes.c_long)
value = ctypes.c_double(x)

addr = ctypes.addressof(value)

new_var = ctypes.cast(addr, var)

print(new_var)
print(new_var.contents)
```

--->>> <__main__.LP_c_long object at 0x7f78880a8488>
--->>> c_long(9218868437227405312)



>>> search in cpython -> reference to something about c infinity
https://www.gnu.org/software/libc/manual/html_node/Infinity-and-NaN.html

