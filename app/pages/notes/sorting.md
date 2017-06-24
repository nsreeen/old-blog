title: built in python list sorting
date: 2017-05-24 12:00:00
published: false
type: notes

Two ways:

# list.sort()
* modifies the list in place, returns None
* possibly more efficient that sorted()
* only works on lists

# sorted(list) 
* returns new sorted list
* works on any iterable

# ascending vs descending
by default both sort to ascending order
pass ```reverse=True``` parameter to the function for descending order
