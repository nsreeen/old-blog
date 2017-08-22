title: Regex and finite state machines
date: 2017-08-22 13:30:00
published: true
type: post

<br>
Regular expressions patterns are implemented as finite state machines! I find this pretty cool, and finding this out has helped me to understand both things a bit better. 

<br>
## Why is this cool?
This means that we can:
- find substrings on just one pass through a string, 
- without looking ahead (only knowing about one character at a time),
- while only keeping track of a few extra  variables (or states).

<br>
## What is a finite state machine?
A finite state machine is just a model for understanding something.  It models something that has different states, and that can only be in one of those states at one time. 

<br>
For example, a door can either be locked or not locked:
![An image of two circles: one has 'locked' written inside, and the other has 'unlocked' written inside.  There are two arrows, each pointing from one circle to the other.](/door_states.png)

<br>
We can add the conditions that cause the state to change:
![The same image as above, but with labels added to the arrows: 'turn key right' leads to 'unlocked', and 'turn key left' leads to 'locked'.](/door_states_with_conditions.png)

<br>
A finite state machine is defined by:
- possible states
- conditions that cause transitions between states to occur
- the starting state (if appropriate - the door is always either locked or unlocked, so the diagrams above don't have a separate starting state)

<br>
## A regular expression as a finite state machine
If I wanted to search a string for substrings that:
- start with `a`,
- have one or more `b`'s in the middle,
- and end with `c`,

<br>
I could search for the regex pattern `ab+c` (where `+` means the previous character can occur one or more times).

<br>
So:
- `abc`, `abbbc`, and `abbbbbbbbc` would all match, 
- but `ac` and `acb` wouldn't match.

<br>
We can draw this as a finite state machine:
![Image of a finite state machine with circles representing the states 0, 1, 2, 3, and 'not a match'.  'a' can move us from state 0 to 1, 'b' from state 1 to 2, and 'c' from state 2 to 3.  State 3 is double circled.](/regex_machine.png)

<br>
Notes:
* the double circle shows that state 3 is an end state (ie. if we get to state 3, we have found a match)
* some inputs do not cause a change in state (eg. in state 0, any input that is not `a` causes the state to remain 0)

<br>
## Keeping track of states
If we want to find out if a string (say: `aabc`) contains our pattern, we will iterate through the string and keep track of our possible states. We'll start out with only one possible states: state 0.  At each character in the string, we will update all possible states with the new input, removing states that `do not match`

<br>
We will iterate through each character like this:

 Current possible States | Input character | Update possible states 
  ------------- | -------------   | -------------
  0             | `a`             | 1 
  0, 1          | `a`             | 1 
  0, 1          | `b`             | 0, 2
  0, 2          | `c`             | 0, 3


<br>
State 3 is one of our current states, so we know that the string contains our pattern! 

<br>
If we wanted to find the matching substrings (ie. return the index of each match), we'd have to also keep track of those too. 


<br><br><br>

