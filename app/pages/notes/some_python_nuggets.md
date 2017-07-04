title: some python nuggets
date: 2017-07-03 12:00:00
published: false
type: notes


## Error raising

- `KeyboardInterrupt` is a use generated interuption

- If an exception occurs during execution of the try clause, the rest of the try clause is skipped.  The except clause is only executed if an exception happens during try AND the type of exception matches the type names after the except keyword.

- A try clause can have more than one except clause, and an except clause may have multiple exceptions as a parenthesized tuple

- `raise <exception-type>()` -> raise an exception, `raise` alone reraises 

- if there is an `else` clause after `try` and `except`, the `else` block will only be executed if `try` succeeds (avoid throwing an error eg when you close the file, after you have already opened and read it successfully)

`finally` clause after `try` is always executed, regardless of whether there were errors


## args* vs args**

two ** -> kwargs**
so args* vs kwargs** (but it's the number of * that is important)


* args* 
- get all excess positional args
- when not sure how many arguments - an arbitrary number can be passed like this



* kwargs 
- get all the excess keyword args
- allow you to handle named arguments that you have not defined in advance


## iadd? in place?

https://docs.python.org/3/library/operator.html


## Avoid errors
str[:-1] -> all but last, if str is empty it will return an empty string (not return an error)

get to access dictionary key - if not found doesnt throw error
dict.get(key, <value to return if not found - default is None>)
you can set it t return anything if the key is not found


## slicing, shallow/deep, what and where is copy


