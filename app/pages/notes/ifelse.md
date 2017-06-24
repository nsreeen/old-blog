title: if else in forth
date: 2017-05-31 12:00:00
published: false
type: notes

a  b
93 97
b  a  c  b
97 93 101 97
IF 5 ELSE 1 THEN

IF -> writes function pointer to Qbranch, leaves a cell blank (index a), pushes the indes to stack
action fills however many cells
ELSE -> writes function pointer to branch, leaves a cell blank (index b), pushes index to stack
action fills however many cells
THEN -> (index c)

THEN:
stack: a b
DUP
a b b
1 -
a b b-1
ROT
b b-1 a
ROT
b-1 a b
push current
b a b c
SWAP
b a c b
                        val  addr  val addr
                        97    94    101   98
stack should look like: b-1    a     c    b
STORE -> put c in b    (b is val, c is addr)
STORE -> put b-1 in a    ( is val, c is addr)

cell1: if func -> if not 0 (true) skip one cell, else jumps to address in next cell
cell2: action
cell3: else func: if 0 (false) skips one cell, else jumps Y cells
cell4: action


"""
