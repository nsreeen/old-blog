title: Calculator Interpreter
date: 2017-07-09 14:00:00
published: true
type: post


I made a toy calculator language, interpreted it in Python, and made a REPL to interact with it.

So far, the language I made can:

- evaluate expressions (with add, subtract, and multiply operators)
- assign variables
- access previously assigned variables and use them in expressions

Making this was a lot of fun.  Before I started, it seemed like too intimidating a project.  I am really glad I went for it anyway, and appreciate the encouragement I got from other people to start it. (a special thanks to Elias!)

I feel it helped me to understand how programming languages work a little better, and made me even more intrigued to learn more.  Working on this also demystified what interpreters and compilers are; including on an intuitive level: there is no black box inside the computer that turns the code I write into meaning; there are just lots of layers of code that do different parts of the task.

I decided to do a write up of this project in a way that would have helped me if I'd found it when I started this project.


<br />
##What does the language look like?
When I made up the language, I tried to make it interesting - I thought that would be more fun.  Since then I have spent sometime debugging only to realize the script was working - I'd made a mistake with my own interesting syntax (I've also learnt to appreciate error messages more, after spending time with my own badly written ones). 

I found out that it's important to have a written grammar for the language.  This helps when you are trying to remember interesting syntax rules, and also maps the way you parse the language later.  It should include [terminal symbols, non terminal symbols](https://en.wikipedia.org/wiki/Terminal_and_nonterminal_symbols), and rules. 

There is only one rule in my language: all statements must be wrapped in `|` and `>`, which are equivalent to "(" and ")".

Terminal symbols are units that cannot really be broken down further. They are:


    !ADD	 :      + operator
    !SUB         :      - operator
    !MUL         :      x operator
    ->		 :      assignment symbol
    integers 0-9 
    names ?[^ ]+ :      variable names must start with `?`, for example `?x`
    |	         :      open bracket
    >	         :      close bracket 


There are four non terminal units in the language.  Non terminals are made of terminal symbols.  They are:

    PROGRAM := STATEMENT +

    STATEMENT := EXPRESSION
                 ASSIGNMENT

    EXPRESSION := | EXPRESSION operator EXPRESSION >
         	  | INTEGER >
                  | NAME >

    ASSIGNMENT := | NAME <- EXPRESSION >


This means that there are four structures of meaning in the language.  Each full piece of code is a program.  Each program is made of one or more statements.  A statement can be an expression or an assignment. 

An expression can be either:

- two expressions separated by an operator (for example `| 2 !ADD 3 >` or `| 4 !ADD ?y >`)
- a number (for example `| 5 >`)
- a name or variable (for example `| ?x >`)

An assignment has the name on the left, an arrow (`<-`) to show assignment, followed by an expression (for example `| ?x <- | 4 > >` )


The following statements are grammatically correct:

- `| 5 !MUL 7 >`
- `| | 2 !ADD | 3 !ADD 1 > > !SUB | 5 !ADD 7 > >`
- `| ?x <- | 1 > >`
- `| ?x <- | 5 !ADD 7 > > | 20 !ADD 10 >`


<br />
##What is an interpreter?
An interpreter takes a program and input and executes it: 

    P + x ---> P(x)

[For more about the difference between interpreters and compilers read this link](http://cs.lmu.edu/~ray/notes/introcompilers/)

An interpreter has these stages: 

1) lexer (split the input into tokens)
2) parser (parse the tokens to get an abstract representation of the program)
3) semantic analysis (add meaning to the representation)
4) evaluation

My interpreter does step three and four in one step. 



<br />
##Part 1: get the tokens (lexer)
Programs or scripts are just text.  The text can be broken up into 'tokens' which have meaning, like words in natural languages.  This involves separating the tokens, and figuring out what kind of token each is.  This step is called lexical analysis.

To check what kind of token each is, regular expressions are used to look for patterns.  In my language this is quite straight forward.  For example, all variable names start with `?` so I can find out if something is a variable by checking if it matches this regular expression: `r'\?.+?'`, and then assign the correct token type tag. 

At the end of this stage there is a series of tokens, stored as named tuples that have both the value and the type. 


<br />
##What is a recursive descent parser?
My interpreter uses the recursive descent parser model.  This kind of parser parses input according to the grammar of the language: it has a set of procedures (ie. functions), and each function deals with a separate non terminal unit of the grammar.  These procedures call each other recursively.  So for my language the non terminal units are: program, statement, expression, assignment;  `parse_program` calls `parse_statement`, which calls `parse_assignment` or `parse_expression`.  You can have an expression inside an expression inside an expression, so `parse_expression` might have to call itself several times. 

The type of recursive descent parser I wrote, called predictive, only looks at most a few tokens ahead at a time.  So it looks ahead only enough to determine whether to send the input on to another function (and determine which function to send it to), or to return it.


<br />
##Part 2: parse the tokens and make a representation of the code (parser)
This step takes a list of tokens, and according to their types it creates an abstract representation of the program. 

The grammar of the language is used to organize the abstract representation of the program's meaning.  My language's grammar has four non terminal parts:

- program
- statement
- expression
- assignment

Each of these four has a function to parse it; **program**, **expression**, and **assignment** are represented by instances of class objects.  **Statements** are an attribute of the program:

```
class Program():
    def __init__(self):
        self.statements = []

class Expression():
    def __init__(self, left=None, right=None, operator=None, value=None):
        self.left = left
        self.right = right
        self.operator = operator
        self.value = value
        self.expression = True


class Assignment():
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value
        self.expression = False
```

The following script:
`| ?x <- | 5 !ADD | ?y !ADD 10 > > >`

Could be represented by:
<img class="col-sm-12" src="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIKICJodHRwOi8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiPgo8IS0tIEdlbmVyYXRlZCBieSBncmFwaHZpeiB2ZXJzaW9uIDIuMzguMCAoMjAxNDA0MTMuMjA0MSkKIC0tPgo8IS0tIFRpdGxlOiAlMyBQYWdlczogMSAtLT4KPHN2ZyB3aWR0aD0iMTE2M3B0IiBoZWlnaHQ9IjM5MnB0Igogdmlld0JveD0iMC4wMCAwLjAwIDExNjMuMjMgMzkyLjAwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIj4KPGcgaWQ9ImdyYXBoMCIgY2xhc3M9ImdyYXBoIiB0cmFuc2Zvcm09InNjYWxlKDEgMSkgcm90YXRlKDApIHRyYW5zbGF0ZSg0IDM4OCkiPgo8dGl0bGU+JTM8L3RpdGxlPgo8cG9seWdvbiBmaWxsPSJ3aGl0ZSIgc3Ryb2tlPSJub25lIiBwb2ludHM9Ii00LDQgLTQsLTM4OCAxMTU5LjIzLC0zODggMTE1OS4yMyw0IC00LDQiLz4KPCEtLSAwIC0tPgo8ZyBpZD0ibm9kZTEiIGNsYXNzPSJub2RlIj48dGl0bGU+MDwvdGl0bGU+CjxlbGxpcHNlIGZpbGw9Im5vbmUiIHN0cm9rZT0iYmxhY2siIGN4PSI2OTguMjM1IiBjeT0iLTM2NiIgcng9IjE3Ny4zNjkiIHJ5PSIxOCIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ic3RhcnQiIHg9IjU2OS43MzUiIHk9Ii0zNjIuMyIgZm9udC1mYW1pbHk9IlRpbWVzLHNlcmlmIiBmb250LXNpemU9IjE0LjAwIj5wYXJzZXIuQXNzaWdubWVudCBpbnN0YW5jZSBhdCAweDdlZmYyODQ1NWQ4ODwvdGV4dD4KPC9nPgo8IS0tIDEgLS0+CjxnIGlkPSJub2RlMiIgY2xhc3M9Im5vZGUiPjx0aXRsZT4xPC90aXRsZT4KPGVsbGlwc2UgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgY3g9IjUzNC4yMzUiIGN5PSItMjc5IiByeD0iMTc0LjM2OSIgcnk9IjE4Ii8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJzdGFydCIgeD0iNDA4LjIzNSIgeT0iLTI3NS4zIiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPnBhcnNlci5FeHByZXNzaW9uIGluc3RhbmNlIGF0IDB4N2VmZjI4NDU1ZGQwPC90ZXh0Pgo8L2c+CjwhLS0gMSYjNDU7JiM0NTswIC0tPgo8ZyBpZD0iZWRnZTEiIGNsYXNzPSJlZGdlIj48dGl0bGU+MSYjNDU7JiM0NTswPC90aXRsZT4KPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgZD0iTTU2Ni42MzYsLTI5Ni43OTNDNTk1LjM4NywtMzExLjY5NSA2MzcuMTcsLTMzMy4zNTEgNjY1LjkwMSwtMzQ4LjI0MiIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSI2NDEuMjM1IiB5PSItMzE4LjgiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+dmFsdWU8L3RleHQ+CjwvZz4KPCEtLSAyIC0tPgo8ZyBpZD0ibm9kZTMiIGNsYXNzPSJub2RlIj48dGl0bGU+MjwvdGl0bGU+CjxlbGxpcHNlIGZpbGw9Im5vbmUiIHN0cm9rZT0iYmxhY2siIGN4PSIxNzIuMjM1IiBjeT0iLTE5MiIgcng9IjE3Mi40NyIgcnk9IjE4Ii8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJzdGFydCIgeD0iNDcuNzM0NyIgeT0iLTE4OC4zIiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPnBhcnNlci5FeHByZXNzaW9uIGluc3RhbmNlIGF0IDB4N2VmZjI4NDU1Y2Y4PC90ZXh0Pgo8L2c+CjwhLS0gMiYjNDU7JiM0NTsxIC0tPgo8ZyBpZD0iZWRnZTIiIGNsYXNzPSJlZGdlIj48dGl0bGU+MiYjNDU7JiM0NTsxPC90aXRsZT4KPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgZD0iTTIzOS4wNTMsLTIwOC42ODlDMzA0LjEyLC0yMjMuOTY4IDQwMi40NjIsLTI0Ny4wNTkgNDY3LjUsLTI2Mi4zMyIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSIzODQuNzM1IiB5PSItMjMxLjgiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+bGVmdDwvdGV4dD4KPC9nPgo8IS0tIDMgLS0+CjxnIGlkPSJub2RlNCIgY2xhc3M9Im5vZGUiPjx0aXRsZT4zPC90aXRsZT4KPGVsbGlwc2UgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgY3g9IjI4LjIzNDciIGN5PSItMTA1IiByeD0iMjciIHJ5PSIxOCIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSIyOC4yMzQ3IiB5PSItMTAxLjMiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+NTwvdGV4dD4KPC9nPgo8IS0tIDMmIzQ1OyYjNDU7MiAtLT4KPGcgaWQ9ImVkZ2UzIiBjbGFzcz0iZWRnZSI+PHRpdGxlPjMmIzQ1OyYjNDU7MjwvdGl0bGU+CjxwYXRoIGZpbGw9Im5vbmUiIHN0cm9rZT0iYmxhY2siIGQ9Ik00My40NDQ5LC0xMTkuOTYyQzU1LjcxMDksLTEzMC43MzkgNzMuNzQyMSwtMTQ1LjUzIDkxLjIzNDcsLTE1NiAxMDIuODAyLC0xNjIuOTI0IDExNS45ODgsLTE2OS4yMjMgMTI4LjMxMywtMTc0LjUwOSIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSIxMDAuNzM1IiB5PSItMTQ0LjgiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+bGVmdDwvdGV4dD4KPC9nPgo8IS0tIDQgLS0+CjxnIGlkPSJub2RlNSIgY2xhc3M9Im5vZGUiPjx0aXRsZT40PC90aXRsZT4KPGVsbGlwc2UgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgY3g9IjEwMC4yMzUiIGN5PSItMTA1IiByeD0iMjciIHJ5PSIxOCIvPgo8L2c+CjwhLS0gNCYjNDU7JiM0NTsyIC0tPgo8ZyBpZD0iZWRnZTQiIGNsYXNzPSJlZGdlIj48dGl0bGU+NCYjNDU7JiM0NTsyPC90aXRsZT4KPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgZD0iTTEwNS4xMjksLTEyMy4wMThDMTA4LjY5MiwtMTMzLjMzMyAxMTQuMjkyLC0xNDYuMzI0IDEyMi4yMzUsLTE1NiAxMjcuODgyLC0xNjIuODggMTM1LjIwNiwtMTY5LjAxMyAxNDIuNDk5LC0xNzQuMTQ5Ii8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJtaWRkbGUiIHg9IjE0NS4yMzUiIHk9Ii0xNDQuOCIgZm9udC1mYW1pbHk9IlRpbWVzLHNlcmlmIiBmb250LXNpemU9IjE0LjAwIj5vcGVyYXRvcjwvdGV4dD4KPC9nPgo8IS0tIDUgLS0+CjxnIGlkPSJub2RlNiIgY2xhc3M9Im5vZGUiPjx0aXRsZT41PC90aXRsZT4KPGVsbGlwc2UgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgY3g9IjE3Mi4yMzUiIGN5PSItMTA1IiByeD0iMjciIHJ5PSIxOCIvPgo8L2c+CjwhLS0gNSYjNDU7JiM0NTsyIC0tPgo8ZyBpZD0iZWRnZTUiIGNsYXNzPSJlZGdlIj48dGl0bGU+NSYjNDU7JiM0NTsyPC90aXRsZT4KPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgZD0iTTE3Mi4yMzUsLTEyMy4yMDFDMTcyLjIzNSwtMTM3Ljk0OCAxNzIuMjM1LC0xNTkuMDg1IDE3Mi4yMzUsLTE3My44MjUiLz4KPHRleHQgdGV4dC1hbmNob3I9Im1pZGRsZSIgeD0iMTg1LjIzNSIgeT0iLTE0NC44IiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPnJpZ2h0PC90ZXh0Pgo8L2c+CjwhLS0gNiAtLT4KPGcgaWQ9Im5vZGU3IiBjbGFzcz0ibm9kZSI+PHRpdGxlPjY8L3RpdGxlPgo8ZWxsaXBzZSBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBjeD0iMjQ0LjIzNSIgY3k9Ii0xMDUiIHJ4PSIyNyIgcnk9IjE4Ii8+CjwvZz4KPCEtLSA2JiM0NTsmIzQ1OzIgLS0+CjxnIGlkPSJlZGdlNiIgY2xhc3M9ImVkZ2UiPjx0aXRsZT42JiM0NTsmIzQ1OzI8L3RpdGxlPgo8cGF0aCBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBkPSJNMjMxLjQwNywtMTIxLjM1MUMyMjMuMTEsLTEzMS4yNjEgMjEyLjA2MywtMTQ0LjQxNyAyMDIuMjM1LC0xNTYgMTk3LjI2NCwtMTYxLjg1OCAxOTEuODAyLC0xNjguMjQ1IDE4Ni45MTcsLTE3My45MzkiLz4KPHRleHQgdGV4dC1hbmNob3I9Im1pZGRsZSIgeD0iMjI5LjIzNSIgeT0iLTE0NC44IiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPnZhbHVlPC90ZXh0Pgo8L2c+CjwhLS0gNyAtLT4KPGcgaWQ9Im5vZGU4IiBjbGFzcz0ibm9kZSI+PHRpdGxlPjc8L3RpdGxlPgo8ZWxsaXBzZSBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBjeD0iNDYxLjIzNSIgY3k9Ii0xOTIiIHJ4PSIzMi40OTQyIiByeT0iMTgiLz4KPHRleHQgdGV4dC1hbmNob3I9Im1pZGRsZSIgeD0iNDYxLjIzNSIgeT0iLTE4OC4zIiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPiFBREQ8L3RleHQ+CjwvZz4KPCEtLSA3JiM0NTsmIzQ1OzEgLS0+CjxnIGlkPSJlZGdlNyIgY2xhc3M9ImVkZ2UiPjx0aXRsZT43JiM0NTsmIzQ1OzE8L3RpdGxlPgo8cGF0aCBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBkPSJNNDc0LjYyNCwtMjA4LjU5QzQ4Ny4zODQsLTIyMy40NDggNTA2LjU0NSwtMjQ1Ljc1OSA1MTkuNjc5LC0yNjEuMDUxIi8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJtaWRkbGUiIHg9IjUyNS4yMzUiIHk9Ii0yMzEuOCIgZm9udC1mYW1pbHk9IlRpbWVzLHNlcmlmIiBmb250LXNpemU9IjE0LjAwIj5vcGVyYXRvcjwvdGV4dD4KPC9nPgo8IS0tIDggLS0+CjxnIGlkPSJub2RlOSIgY2xhc3M9Im5vZGUiPjx0aXRsZT44PC90aXRsZT4KPGVsbGlwc2UgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgY3g9IjY4NS4yMzUiIGN5PSItMTkyIiByeD0iMTczLjU2OSIgcnk9IjE4Ii8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJzdGFydCIgeD0iNTU5LjczNSIgeT0iLTE4OC4zIiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPnBhcnNlci5FeHByZXNzaW9uIGluc3RhbmNlIGF0IDB4N2VmZjI4NDU1ZTE4PC90ZXh0Pgo8L2c+CjwhLS0gOCYjNDU7JiM0NTsxIC0tPgo8ZyBpZD0iZWRnZTgiIGNsYXNzPSJlZGdlIj48dGl0bGU+OCYjNDU7JiM0NTsxPC90aXRsZT4KPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgZD0iTTY1NS40MDIsLTIwOS43OTNDNjI4LjkzLC0yMjQuNjk1IDU5MC40NTksLTI0Ni4zNTEgNTY0LjAwNSwtMjYxLjI0MiIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSI2MzIuMjM1IiB5PSItMjMxLjgiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+cmlnaHQ8L3RleHQ+CjwvZz4KPCEtLSA5IC0tPgo8ZyBpZD0ibm9kZTEwIiBjbGFzcz0ibm9kZSI+PHRpdGxlPjk8L3RpdGxlPgo8ZWxsaXBzZSBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBjeD0iNDYyLjIzNSIgY3k9Ii0xMDUiIHJ4PSIxNzIuNzY5IiByeT0iMTgiLz4KPHRleHQgdGV4dC1hbmNob3I9InN0YXJ0IiB4PSIzMzcuMjM1IiB5PSItMTAxLjMiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+cGFyc2VyLkV4cHJlc3Npb24gaW5zdGFuY2UgYXQgMHg3ZWZmMjg0NTVlYTg8L3RleHQ+CjwvZz4KPCEtLSA5JiM0NTsmIzQ1OzggLS0+CjxnIGlkPSJlZGdlOSIgY2xhc3M9ImVkZ2UiPjx0aXRsZT45JiM0NTsmIzQ1Ozg8L3RpdGxlPgo8cGF0aCBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBkPSJNNTA1LjQ5NiwtMTIyLjQ5QzU0NC44ODcsLTEzNy41MDQgNjAyLjc0MSwtMTU5LjU1NiA2NDIuMDk0LC0xNzQuNTU2Ii8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJtaWRkbGUiIHg9IjU5Ni43MzUiIHk9Ii0xNDQuOCIgZm9udC1mYW1pbHk9IlRpbWVzLHNlcmlmIiBmb250LXNpemU9IjE0LjAwIj5sZWZ0PC90ZXh0Pgo8L2c+CjwhLS0gMTAgLS0+CjxnIGlkPSJub2RlMTEiIGNsYXNzPSJub2RlIj48dGl0bGU+MTA8L3RpdGxlPgo8ZWxsaXBzZSBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBjeD0iMzU0LjIzNSIgY3k9Ii0xOCIgcng9IjI3IiByeT0iMTgiLz4KPHRleHQgdGV4dC1hbmNob3I9Im1pZGRsZSIgeD0iMzU0LjIzNSIgeT0iLTE0LjMiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+P3k8L3RleHQ+CjwvZz4KPCEtLSAxMCYjNDU7JiM0NTs5IC0tPgo8ZyBpZD0iZWRnZTEwIiBjbGFzcz0iZWRnZSI+PHRpdGxlPjEwJiM0NTsmIzQ1Ozk8L3RpdGxlPgo8cGF0aCBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBkPSJNMzY3LjA1NSwtMzQuMDIzNUMzNzYuNDUsLTQ0LjUyNTUgMzg5Ljg1LC01OC40OTQyIDQwMy4yMzUsLTY5IDQxMS42NjYsLTc1LjYxOCA0MjEuNDYyLC04MS45MDg2IDQzMC42MiwtODcuMjg0Ii8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJtaWRkbGUiIHg9IjQxMi43MzUiIHk9Ii01Ny44IiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPmxlZnQ8L3RleHQ+CjwvZz4KPCEtLSAxMSAtLT4KPGcgaWQ9Im5vZGUxMiIgY2xhc3M9Im5vZGUiPjx0aXRsZT4xMTwvdGl0bGU+CjxlbGxpcHNlIGZpbGw9Im5vbmUiIHN0cm9rZT0iYmxhY2siIGN4PSI0MjYuMjM1IiBjeT0iLTE4IiByeD0iMjciIHJ5PSIxOCIvPgo8L2c+CjwhLS0gMTEmIzQ1OyYjNDU7OSAtLT4KPGcgaWQ9ImVkZ2UxMSIgY2xhc3M9ImVkZ2UiPjx0aXRsZT4xMSYjNDU7JiM0NTs5PC90aXRsZT4KPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgZD0iTTQyNC45MDEsLTM2LjMzMzdDNDI0Ljc4OSwtNDYuMjc4MyA0MjUuNzg5LC01OC43NzgzIDQzMC4yMzUsLTY5IDQzMy4wNTksLTc1LjQ5MzEgNDM3LjU5NywtODEuNTczNSA0NDIuMzc4LC04Ni43ODU4Ii8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJtaWRkbGUiIHg9IjQ1My4yMzUiIHk9Ii01Ny44IiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPm9wZXJhdG9yPC90ZXh0Pgo8L2c+CjwhLS0gMTIgLS0+CjxnIGlkPSJub2RlMTMiIGNsYXNzPSJub2RlIj48dGl0bGU+MTI8L3RpdGxlPgo8ZWxsaXBzZSBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBjeD0iNDk4LjIzNSIgY3k9Ii0xOCIgcng9IjI3IiByeT0iMTgiLz4KPC9nPgo8IS0tIDEyJiM0NTsmIzQ1OzkgLS0+CjxnIGlkPSJlZGdlMTIiIGNsYXNzPSJlZGdlIj48dGl0bGU+MTImIzQ1OyYjNDU7OTwvdGl0bGU+CjxwYXRoIGZpbGw9Im5vbmUiIHN0cm9rZT0iYmxhY2siIGQ9Ik00OTEuMTIyLC0zNS43OTMzQzQ4NC44NTIsLTUwLjU5ODIgNDc1Ljc1OCwtNzIuMDY5NiA0NjkuNDU2LC04Ni45NTA3Ii8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJtaWRkbGUiIHg9IjQ5Ni4yMzUiIHk9Ii01Ny44IiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPnJpZ2h0PC90ZXh0Pgo8L2c+CjwhLS0gMTMgLS0+CjxnIGlkPSJub2RlMTQiIGNsYXNzPSJub2RlIj48dGl0bGU+MTM8L3RpdGxlPgo8ZWxsaXBzZSBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBjeD0iNTcwLjIzNSIgY3k9Ii0xOCIgcng9IjI3IiByeT0iMTgiLz4KPC9nPgo8IS0tIDEzJiM0NTsmIzQ1OzkgLS0+CjxnIGlkPSJlZGdlMTMiIGNsYXNzPSJlZGdlIj48dGl0bGU+MTMmIzQ1OyYjNDU7OTwvdGl0bGU+CjxwYXRoIGZpbGw9Im5vbmUiIHN0cm9rZT0iYmxhY2siIGQ9Ik01NTUuMTcyLC0zMy4wOTAxQzU0My45MTYsLTQzLjM5OSA1MjcuOTkzLC01Ny41MjgyIDUxMy4yMzUsLTY5IDUwNS4yNjUsLTc1LjE5NTEgNDk2LjI3MiwtODEuNTU5NiA0ODguMDgxLC04Ny4xMzM4Ii8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJtaWRkbGUiIHg9IjU0Ni4yMzUiIHk9Ii01Ny44IiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPnZhbHVlPC90ZXh0Pgo8L2c+CjwhLS0gMTQgLS0+CjxnIGlkPSJub2RlMTUiIGNsYXNzPSJub2RlIj48dGl0bGU+MTQ8L3RpdGxlPgo8ZWxsaXBzZSBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBjeD0iNjg1LjIzNSIgY3k9Ii0xMDUiIHJ4PSIzMi40OTQyIiByeT0iMTgiLz4KPHRleHQgdGV4dC1hbmNob3I9Im1pZGRsZSIgeD0iNjg1LjIzNSIgeT0iLTEwMS4zIiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPiFBREQ8L3RleHQ+CjwvZz4KPCEtLSAxNCYjNDU7JiM0NTs4IC0tPgo8ZyBpZD0iZWRnZTE0IiBjbGFzcz0iZWRnZSI+PHRpdGxlPjE0JiM0NTsmIzQ1Ozg8L3RpdGxlPgo8cGF0aCBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBkPSJNNjg1LjIzNSwtMTIzLjIwMUM2ODUuMjM1LC0xMzcuOTQ4IDY4NS4yMzUsLTE1OS4wODUgNjg1LjIzNSwtMTczLjgyNSIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSI3MDguMjM1IiB5PSItMTQ0LjgiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+b3BlcmF0b3I8L3RleHQ+CjwvZz4KPCEtLSAxNSAtLT4KPGcgaWQ9Im5vZGUxNiIgY2xhc3M9Im5vZGUiPjx0aXRsZT4xNTwvdGl0bGU+CjxlbGxpcHNlIGZpbGw9Im5vbmUiIHN0cm9rZT0iYmxhY2siIGN4PSI5MDkuMjM1IiBjeT0iLTEwNSIgcng9IjE3My41NjkiIHJ5PSIxOCIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ic3RhcnQiIHg9Ijc4My43MzUiIHk9Ii0xMDEuMyIgZm9udC1mYW1pbHk9IlRpbWVzLHNlcmlmIiBmb250LXNpemU9IjE0LjAwIj5wYXJzZXIuRXhwcmVzc2lvbiBpbnN0YW5jZSBhdCAweDdlZmYyODQ1NWU2MDwvdGV4dD4KPC9nPgo8IS0tIDE1JiM0NTsmIzQ1OzggLS0+CjxnIGlkPSJlZGdlMTUiIGNsYXNzPSJlZGdlIj48dGl0bGU+MTUmIzQ1OyYjNDU7ODwvdGl0bGU+CjxwYXRoIGZpbGw9Im5vbmUiIHN0cm9rZT0iYmxhY2siIGQ9Ik04NjUuNzgsLTEyMi40OUM4MjYuMjEyLC0xMzcuNTA0IDc2OC4wOTksLTE1OS41NTYgNzI4LjU2OSwtMTc0LjU1NiIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSI4MjQuMjM1IiB5PSItMTQ0LjgiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+cmlnaHQ8L3RleHQ+CjwvZz4KPCEtLSAxNiAtLT4KPGcgaWQ9Im5vZGUxNyIgY2xhc3M9Im5vZGUiPjx0aXRsZT4xNjwvdGl0bGU+CjxlbGxpcHNlIGZpbGw9Im5vbmUiIHN0cm9rZT0iYmxhY2siIGN4PSI4MDEuMjM1IiBjeT0iLTE4IiByeD0iMjciIHJ5PSIxOCIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSI4MDEuMjM1IiB5PSItMTQuMyIgZm9udC1mYW1pbHk9IlRpbWVzLHNlcmlmIiBmb250LXNpemU9IjE0LjAwIj4xMDwvdGV4dD4KPC9nPgo8IS0tIDE2JiM0NTsmIzQ1OzE1IC0tPgo8ZyBpZD0iZWRnZTE2IiBjbGFzcz0iZWRnZSI+PHRpdGxlPjE2JiM0NTsmIzQ1OzE1PC90aXRsZT4KPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgZD0iTTgxNC4wNTUsLTM0LjAyMzVDODIzLjQ1LC00NC41MjU1IDgzNi44NSwtNTguNDk0MiA4NTAuMjM1LC02OSA4NTguNjY2LC03NS42MTggODY4LjQ2MiwtODEuOTA4NiA4NzcuNjIsLTg3LjI4NCIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSI4NTkuNzM1IiB5PSItNTcuOCIgZm9udC1mYW1pbHk9IlRpbWVzLHNlcmlmIiBmb250LXNpemU9IjE0LjAwIj5sZWZ0PC90ZXh0Pgo8L2c+CjwhLS0gMTcgLS0+CjxnIGlkPSJub2RlMTgiIGNsYXNzPSJub2RlIj48dGl0bGU+MTc8L3RpdGxlPgo8ZWxsaXBzZSBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBjeD0iODczLjIzNSIgY3k9Ii0xOCIgcng9IjI3IiByeT0iMTgiLz4KPC9nPgo8IS0tIDE3JiM0NTsmIzQ1OzE1IC0tPgo8ZyBpZD0iZWRnZTE3IiBjbGFzcz0iZWRnZSI+PHRpdGxlPjE3JiM0NTsmIzQ1OzE1PC90aXRsZT4KPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgZD0iTTg3MS45MDEsLTM2LjMzMzdDODcxLjc4OSwtNDYuMjc4MyA4NzIuNzg5LC01OC43NzgzIDg3Ny4yMzUsLTY5IDg4MC4wNTksLTc1LjQ5MzEgODg0LjU5NywtODEuNTczNSA4ODkuMzc4LC04Ni43ODU4Ii8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJtaWRkbGUiIHg9IjkwMC4yMzUiIHk9Ii01Ny44IiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPm9wZXJhdG9yPC90ZXh0Pgo8L2c+CjwhLS0gMTggLS0+CjxnIGlkPSJub2RlMTkiIGNsYXNzPSJub2RlIj48dGl0bGU+MTg8L3RpdGxlPgo8ZWxsaXBzZSBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBjeD0iOTQ1LjIzNSIgY3k9Ii0xOCIgcng9IjI3IiByeT0iMTgiLz4KPC9nPgo8IS0tIDE4JiM0NTsmIzQ1OzE1IC0tPgo8ZyBpZD0iZWRnZTE4IiBjbGFzcz0iZWRnZSI+PHRpdGxlPjE4JiM0NTsmIzQ1OzE1PC90aXRsZT4KPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgZD0iTTkzOC4xMjIsLTM1Ljc5MzNDOTMxLjg1MiwtNTAuNTk4MiA5MjIuNzU4LC03Mi4wNjk2IDkxNi40NTYsLTg2Ljk1MDciLz4KPHRleHQgdGV4dC1hbmNob3I9Im1pZGRsZSIgeD0iOTQzLjIzNSIgeT0iLTU3LjgiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+cmlnaHQ8L3RleHQ+CjwvZz4KPCEtLSAxOSAtLT4KPGcgaWQ9Im5vZGUyMCIgY2xhc3M9Im5vZGUiPjx0aXRsZT4xOTwvdGl0bGU+CjxlbGxpcHNlIGZpbGw9Im5vbmUiIHN0cm9rZT0iYmxhY2siIGN4PSIxMDE3LjIzIiBjeT0iLTE4IiByeD0iMjciIHJ5PSIxOCIvPgo8L2c+CjwhLS0gMTkmIzQ1OyYjNDU7MTUgLS0+CjxnIGlkPSJlZGdlMTkiIGNsYXNzPSJlZGdlIj48dGl0bGU+MTkmIzQ1OyYjNDU7MTU8L3RpdGxlPgo8cGF0aCBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBkPSJNMTAwMi4xNywtMzMuMDkwMUM5OTAuOTE2LC00My4zOTkgOTc0Ljk5MywtNTcuNTI4MiA5NjAuMjM1LC02OSA5NTIuMjY1LC03NS4xOTUxIDk0My4yNzIsLTgxLjU1OTYgOTM1LjA4MSwtODcuMTMzOCIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSI5OTMuMjM1IiB5PSItNTcuOCIgZm9udC1mYW1pbHk9IlRpbWVzLHNlcmlmIiBmb250LXNpemU9IjE0LjAwIj52YWx1ZTwvdGV4dD4KPC9nPgo8IS0tIDIwIC0tPgo8ZyBpZD0ibm9kZTIxIiBjbGFzcz0ibm9kZSI+PHRpdGxlPjIwPC90aXRsZT4KPGVsbGlwc2UgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgY3g9IjExMjguMjMiIGN5PSItMTA1IiByeD0iMjciIHJ5PSIxOCIvPgo8L2c+CjwhLS0gMjAmIzQ1OyYjNDU7OCAtLT4KPGcgaWQ9ImVkZ2UyMCIgY2xhc3M9ImVkZ2UiPjx0aXRsZT4yMCYjNDU7JiM0NTs4PC90aXRsZT4KPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgZD0iTTExMDcuNjksLTExNi44OTFDMTEwMi43MywtMTE5LjE4MiAxMDk3LjM4LC0xMjEuMzg5IDEwOTIuMjMsLTEyMyA5OTkuNDI1LC0xNTIuMDUyIDg5MC42LC0xNjkuNDE0IDgwOC44NDIsLTE3OS4zMTQiLz4KPHRleHQgdGV4dC1hbmNob3I9Im1pZGRsZSIgeD0iMTAzMS4yMyIgeT0iLTE0NC44IiBmb250LWZhbWlseT0iVGltZXMsc2VyaWYiIGZvbnQtc2l6ZT0iMTQuMDAiPnZhbHVlPC90ZXh0Pgo8L2c+CjwhLS0gMjEgLS0+CjxnIGlkPSJub2RlMjIiIGNsYXNzPSJub2RlIj48dGl0bGU+MjE8L3RpdGxlPgo8ZWxsaXBzZSBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBjeD0iOTA0LjIzNSIgY3k9Ii0xOTIiIHJ4PSIyNyIgcnk9IjE4Ii8+CjwvZz4KPCEtLSAyMSYjNDU7JiM0NTsxIC0tPgo8ZyBpZD0iZWRnZTIxIiBjbGFzcz0iZWRnZSI+PHRpdGxlPjIxJiM0NTsmIzQ1OzE8L3RpdGxlPgo8cGF0aCBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBkPSJNODgzLjY0NCwtMjAzLjc2Qzg3OC42OTEsLTIwNi4wNTYgODczLjM1MSwtMjA4LjI5OSA4NjguMjM1LC0yMTAgNzkxLjMwNSwtMjM1LjU4IDcwMS4wNiwtMjUzLjI1NiA2MzMuNzgyLC0yNjQuMTYyIi8+Cjx0ZXh0IHRleHQtYW5jaG9yPSJtaWRkbGUiIHg9IjgyMS4yMzUiIHk9Ii0yMzEuOCIgZm9udC1mYW1pbHk9IlRpbWVzLHNlcmlmIiBmb250LXNpemU9IjE0LjAwIj52YWx1ZTwvdGV4dD4KPC9nPgo8IS0tIDIyIC0tPgo8ZyBpZD0ibm9kZTIzIiBjbGFzcz0ibm9kZSI+PHRpdGxlPjIyPC90aXRsZT4KPGVsbGlwc2UgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgY3g9Ijc1My4yMzUiIGN5PSItMjc5IiByeD0iMjciIHJ5PSIxOCIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSI3NTMuMjM1IiB5PSItMjc1LjMiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+P3g8L3RleHQ+CjwvZz4KPCEtLSAyMiYjNDU7JiM0NTswIC0tPgo8ZyBpZD0iZWRnZTIyIiBjbGFzcz0iZWRnZSI+PHRpdGxlPjIyJiM0NTsmIzQ1OzA8L3RpdGxlPgo8cGF0aCBmaWxsPSJub25lIiBzdHJva2U9ImJsYWNrIiBkPSJNNzQyLjg5LC0yOTUuOTg4QzczMy4zMDUsLTMxMC44IDcxOS4wOTMsLTMzMi43NjUgNzA5LjI4OCwtMzQ3LjkxNyIvPgo8dGV4dCB0ZXh0LWFuY2hvcj0ibWlkZGxlIiB4PSI3NDQuNzM1IiB5PSItMzE4LjgiIGZvbnQtZmFtaWx5PSJUaW1lcyxzZXJpZiIgZm9udC1zaXplPSIxNC4wMCI+bmFtZTwvdGV4dD4KPC9nPgo8L2c+Cjwvc3ZnPgo="
alt="Visualization of AST"/>

How is this model created?  The parser has a set of functions to parse the four different units of the grammar.  The functions call each other recursively and consume the tokens. 

For example, when `parse_program` is called it checks there are tokens, and then calls `parse_statement` in a while loop until there are no more tokens. `parse_statement` looks at the next few tokens to determine whether the statement is an expression or assignment.  If there is a variable name (starting with `?`) and an assignment symbol (`<-`) it calls `parse_assignment`, otherwise it calls `parse_expression`. 

At the end of this stage there is an instance of the Program class, which has a list of statements as an attribute.  Each statement can be an instance of either the Expression class or the Assignment class, and can contain another instance of the expression class as an attribute. The expression instances do not yet have value attributes, these will be added in the evaluation stage.  We can call this an [abstract syntax tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree).



<br />
##Part 3: semantic analysis and evaluation 
This step iterates through the statements in the program, and determines their values.  It is similar to step two, in that each non terminal part of the language grammar has an evaluate function, and the functions are called recursively to return the values of all levels of nested expressions. 

At this point variables are also added to the dictionary; if a statement is an assignment instance, its name and value is added to the dictionary.



<br />
##How does the REPL work?
REPL stands for read evaluate print loop.  I made a REPL by writing a script that accepts input, evaluates it (interprets it according to the steps above), and prints the output, in a loop.

When you run the REPL script, it creates a dictionary and then enters a loop.  Each cycle through the loop waits for input.  If the input is 'q' the function returns and the program ends, if it's 'h' help is printed to the terminal. 

Otherwise the interpret function is called on the input (the interpret function calls the lexer, parser, and evaluator), which returns the output.  This part is inside of a try statement, so that if the input cannot be interpreted the REPL does not exit.  The dictionary is also passed and returned, so that variables can be added to the dictionary.



<br />
##The code
[If you want to have a look at my code it is here](https://github.com/Nasreen123/Interpreter) :) 




