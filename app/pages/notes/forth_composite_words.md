title: Implementing forth composite word
date: 2017-05-26 12:00:00
published: false
type: notes


** The words needed for the implementation are currently being written in the language being used for the interpreter/ compiler (ie C, python).  Some of them can be written in forth, eventually (once we can compile words).  The code for them is in forth as it's more succinct and elegant (and is the goal eventually)


# Dictionary entry:
* name
* immediate flag
* link (backwards, to previous link, so there is a linked list within the dictionary)
* code pointer (the code that will be executed when the word is called.  For composite words this is the ENTER word)
* data field (For variables or constants this is a number.  For composite words this is a word list, with exit added to the end.  For native words, this is NEXT)


# Quit is the outermost loop:
: QUIT
   RP0 RP!  // clears return stack
   BEGIN
      STATE @ 
         IF
            COMPILE-WORD
         ELSE
            INTERPRET-WORD
         THEN
   AGAIN ;

A simplified version, without compiling, is just:

: QUIT
   RP0 RP!   // clears return stack
   BEGIN
      INTERPRET
   AGAIN ; 


# Interpreting:

:INTERPRET
   BL WORD   // consumes input stream til a space, pushes word to stack
   FIND      // consumes word from stack, looks for it in the dictionary
             // if found pushes: address 1
             // else pushes: word 0
   IF
      EXECUTE  // executes address on stack!!!
   ELSE
      >NUMBER
   THEN ;


# Composite words

For composite words, the code pointer in their dictionary entry will point to ENTER, the cells directly after the code pointer will have the word list for that word (ie. the words between : and ; when the word is defined), and will end with EXIT. 

When executing composite words, the interpreter has to keep track of where to return to.  ENTER and EXIT start and end this process of keeping track.  **or is it always happening? does the PC do anything before ENTER?

The program counter (PC) is used to keep track.  The PC stores the address of the cell directly after the one being executed (find?).  ENTER pushes the contents of the PC to the return stack (if the PC is not storing anything, this is also fine - the return stack will be emptied? or should we check before we push to the RS? prob should check)

Every native word should finish with NEXT.  NEXT loads the value of PC onto the stack, increments the PC by 1, and calls execute

EXIT takes the top value from the return stack and stores it in the PC


.S
None
<function print_stack at 0x7fc8aaee7730>
DUP
1     4
<function dup at 0x7fc8aaee7ae8>
*
4     7
<function mul at 0x7fc8aaee7b70>
SQUARED
7     10
<function enter at 0x7fc8aaee7c80>
5     12
8     13
<function exit at 0x7fc8aaee7bf8>





we only need to put pc on rs if we are already nested!!!

so enter -> start using pc to track where we are
before changing it, we check if it already holds something
(of if something on the RT? how do we reset it???)
if it does we push that to the rs before changing the pc
else we just change it

** how to keep pc one ahead?




: NEXT
   IF PC NOT NONE ( because it will run at the end of every native word)
   PC++
   PUSHPS(PC) ;

: ENTER
   PUSHS(PC)
   PC = INDEX
   NEXT

: EXIT 
   PC = popRS
   NEXT
