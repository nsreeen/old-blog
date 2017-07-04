title: cryptopals 1 base64
date: 2017-07-03 12:00:00
published: false
type: notes

I just did the first cryptopals challenge with Nandaja.  This is what I learnt.


# How to encode from hex to base64


For the cryptopals challenge, we started with a hex string. These are the stages:

1) going from a hex string to binary numbers

2) shifting the pattern of bits making up the binary numbers

3) going from binary numbers to hex numbers

4) going from hex numbers to a base64 encoded string


* Part 1

To convert from hexadecimal to binary, take each digit of the hex string and convert it to a 4 bit binary number.  A 4 bit binary number is a binary number that has four digits (representing 8 4 2 1), for example `0010` is a 4 bit binary number representing the decimal number `2`. 

Then concatenate all the 4 bit binary numbers we have into a long bit pattern.


* Part 2

We shift the pattern of bits, and add some zeros to pad it out, so that for every 3 digits we start with, we end up with 4 digits later on.

Take 6 digits at a time from the pattern of bits.  Each one becomes an 8 bit binary number by adding two zeros to the left side.  For example, if our bit pattern is `0100100100100111...` we would take `010010` and add two zeros to get `00010010`.


* Part 3

We convert each 8 bit binary number to a hexadecimal number.  So the example from earlier (`00010010`) would be `18` as a hexadecimal number.


* Part 4

We use the base65 encoding table to convert each two digit hexadecimal number to a letter.


# What is base64 encoding used for?

Storing and transmitting binary data in ASCII.  Base64 takes 6 bits and converts each one to an ASCII character.  There are less that 100 ASCII characters, so 6 are the maximum number of bits we can store as one ASCII character.





