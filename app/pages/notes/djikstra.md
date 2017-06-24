title: djikstra
date: 2017-05-23 12:00:00
published: false
type: notes

Used to find the shortest path from nodes A to B in a graph that is:
- a DAG (directed acyclic graph)
- weighted 

to implement, need to keep track of:
- the graph and the weights of edges (hashtables within a hashtable)
- the cheapest cost of getting to each node (a hashtable with the nodes as keys and the cost as val)
- the parent of each node (according the to cheapest path found so far - also can be a hashtable)

steps:
1) find cheapest node
2) check if there is a cheaper path to the neighbors of the current node, if so update path/parent and cost of the neighbor
3) repeat until every node in the graph has been processed
4) calculate the end (or look up the end node)
