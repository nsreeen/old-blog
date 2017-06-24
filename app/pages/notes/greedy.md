title: what are greedy algorithms?
date: 2017-05-18 12:00:00
published: false
type: notes

algorithms that try to find the optimal global solution by finding the optimal local solution

-> keep picking the best option at each stage

examples:

scheduling multiple events in a room ->>> gives best solution

knapsack problem ->>> gives a decent solution (not optimal)

set covering problem (radio stations cover dfferent states, how many stations do you need to cover all the states?



APPROXIMATION ALGORITHMS
when calculating the exact answer takes too long
judged by:
how close to the optimal they are
how long they take
steps:
- find the answer for this step that is best (fulfills most of the criteria we still need, or adds most value, etc)
- repeat until full or have everything we need




NP-COMPLETE
to choose the best solution, you have to calculate every possible solution and then choose the best
it cannot be broken down (ie divide and conquer or dynamic style)
the time it takes to do this grows quickly compared to the input size
it will take too long, so you can calculate an approximate solution

how to tell the problem is np-complete?
- quick to slow fast with addition of more items
- 'all combinations of x'
- set or sequence based, and hard to solve 
- 'every possible version'
