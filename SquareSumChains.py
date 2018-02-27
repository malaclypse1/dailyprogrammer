#!/usr/bin/env python
# python 3.60
# /r/dailyprogrammer challenge for 1/26/18
# Description
#
# For this challenge your task is, given a number N, rearrange the numbers 1 to N so that all adjacent pairs of numbers
# sum up to square numbers.
#
# There might not actually be a solution. There also might be multiple solution. You are only required to find one, if
# possible.
#
# For example, the smallest number for which this is possbile is 15:
#
# 8 1 15 10 6 3 13 12 4 5 11 14 2 7 9
#
#  8 +  1 =  9 = 3^2
#  1 + 15 = 16 = 4^2
# 15 + 10 = 25 = 5^2
# 10 +  6 = 16 = 4^2
# ...
#
# Example Input
#
# 15
# 8
#
# Example Output
#
# 8 1 15 10 6 3 13 12 4 5 11 14 2 7 9
# Not possible
#
# Challenge Input
#
# 23
# 24
# 25
# 256
#
# Credit
#
# This challenge was suggested by user /u/KeinBaum, many thanks. If you have an idea for a challenge, please share it
# in /r/dailyprogrammer_ideas and there's a good chance we'll use it.

# premise: build a graph with nodes 1 through n, connect nodes with nodes that form a square sum (so for n = 15,
# 1 connects to 3 (sum 4), 8 (sum 9) and 15 (sum 16). Once the graph is built, find a hamiltonian path that traverses
# it. If such a path exists, that path is the solution.

# Hamiltonian path detection uses Bellman, Held, and Karp algorithm with time complexity O(2^n n^2). This gets really
# slow above n=19. It would probably be faster to use a backtracking search (Iwama, Kazuo; Nakashima, Takuya (2007),
# "An improved exact algorithm for cubic graph TSP)

from math import sqrt
from collections import defaultdict

def is_square(n):
    return sqrt(n).is_integer()

# Bellman, Held, and Karp
# for a subset S, check if hamiltonian path exists that ends at vertex v, for all v in S
# such a path exists if v has a neighbor w where subset S-v has a path that ends in w

def print2dBool(array):
    print('0 1 2 3 4 5 6 7 8 9 A B C D E F ')
    for i in array:
        for j in i:
            if j:
                print(1,end=' ')
            else:
                print(0,end=' ')
        print()

def build_graph():
    # build the graph by comparing every number 1-n to every number 1-n to see if they sum to a square and adding edges
    # for those that do. for example, for n=4, { 1: [3], 3: [1] }
    graph = defaultdict(list)
    for number in range(1, n + 1):
        for otherNumber in range(1, n + 1):
            if number == otherNumber:
                continue
            else:
                if is_square(number + otherNumber):
                    # print(number,otherNumber)
                    if number in graph:
                        graph[number].append(otherNumber)
                    else:
                        graph[number] = [otherNumber]
    return graph

def check_hamiltonian(graph,n):
    # initialize dynamic programming boolean matrix size n by 2**n to false. Each column is a subset of vertices, so
    # column 3 (binary 11) is the subset containing vertices 0 and 1, while column 4 (101) contains vertices 0 and 2.
    # elements of array[i][j] are true if the subset j contains a path that ends at vertex i.
    dp = [[False for i in range(2**n)] for j in range(n)]
    result = []
    # set elements [i][2**i] to true. Column 1 (subset{0}) contains a path that ends at vertex 0.
    for i in range(n):
        dp[i][2**i] = True
    # for each subset...
    for i in range(2**n): # i is mask
        for j in range(n): # j is row
            if i&(1<<j): # jth bit set in i/ is j in subset masked by i?
                for k in range(n):
                    # look at other nodes in subset (kth bit set, and k != j)
                    # if j is adjacent to k (j+1 in graph[k+1] or k+1 in graph[j+1])
                    #    (numbers start at 1, but indexing starts at 0, so when converting
                    #     index to number, add 1)
                    # and subset - j has path that ends at k
                    if i&(1<<k) and k != j and j+1 in graph[k+1] and dp[k][i ^ (1 << j)]:
                        dp[j][i] = True
                        break

    #print2dBool(dp)
    for i in range(n):
        # look at each row of last column. If one of those is true, there is a hamiltonian path
        mask = (1<<n)-1
        if dp[i][mask]:
            # extract path here
            extract_path(dp, graph, i, mask, result)
            #print(result)
            break
    return result


def extract_path(dp, graph, i, mask, result):
    if (mask):
        #print('mask', bin(mask))
        result.append(i + 1)
        # take that node off mask, and compare rows of connected nodes to new mask to find next node
        mask -= (1 << i)
        #print('new mask', bin(mask))
        #print(graph[i + 1])
        for next in graph[i + 1]:
            if dp[next - 1][mask]:
                extract_path(dp, graph, next-1, mask, result)
                break
    else:
        # base case: no remaining nodes in mask
        return

################### main ###################

n = int(input('enter N: '))

graph = build_graph()

#print(graph)
answer =  check_hamiltonian(graph,n)
if len(answer):
    print(answer)
else:
    print('there is no solution')
