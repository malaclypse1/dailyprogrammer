#!/usr/bin/env python
# python 3.60
# /r/dailyprogrammer challenge for 1/29/18
# Description
#
# You own a nice tiny mini-market that sells candies to children. You need to know if you'll be able to give the change
# back to those little cute creatures and it happens you don't know basic math because when you were a child you were
# always eating candies and did not study very well. So you need some help from a little tool that tell you if you can.
# Input Description
#
# On the line beginning "Input:" be given a single number that tells you how much change to produce, and then a list of
# coins you own. The next line, beginning with "Output:", tells you the number of coins to give back to achieve the
# change you need to give back (bounded by the number of coins you have). Here's one that says "give the customer 3 or
# fewer coins". Example:
#
# Input: 10 5 5 2 2 1
# Output: n <= 3
#
# Output Description
#
# Your progam should emit the coins you would give back to yield the correct value of change, if possible. Multiple
# solutions may be possible. If no solution is possible, state that. Example:
#
# 5 5
#
# Challenge Input
#
# Input: 150 100 50 50 50 50
# Output: n < 5
#
# Input: 130 100 20 18 12 5 5
# Output: n < 6
#
# Input: 200 50 50 20 20 10
# Output: n >= 5
#
# Bonus
#
# Output the minimum number of coins needed:
#
# Input: 150 100 50 50 50 50
# Output: 2
#
# Input: 130 100 20 18 12 5 5
# Output: 3
#
# Challenge
#
# Input: 150 1 1 ... 1 (1 repeated 10000 times)
# Output: 150
#
# Note
#
# This is the subset sum problem with a twist, a classic computational complexity problem which poses fun questions
# about efficient calculation and lower bounds of complexity.
# Credit
#
# This challenge was suggested by use /u/Scara95, many thanks. If you have a challenge idea, please share it on
# /r/dailyprogrammer_ideas and there's a good chance we'll use it.
import itertools


def GetInput():
    # returns a tuple consisting of quantity (amount of change to return), a list of coins you have, and minimum and
    # coins to return
    userInput = input('Input: ').split()
    try:
        userInput = list(map(int, userInput))
    except ValueError:
        print("Input should be a space delimited list of integers")
        raise SystemExit
    #print(userInput)

    # userOutput should have 2 items: a comparator and an integer
    validComparators = ['<', '>', '<=', '>=', '=']
    userOutput = input('Output: n ').split()
    if len(userOutput) == 2 and userOutput[0] in validComparators:
        try:
            n = int(userOutput[1])
            comparator = userOutput[0]
        except ValueError:
            print("Output should be a comparator (<, >, <=, >=, =) and an integer")
            raise SystemExit
    else:
        print("Output should be a comparator (<, >, <=, >=, =) and an integer")
        raise SystemExit

    if comparator == '<':
        max = n - 1
        min = 0
    elif comparator == '<=':
        max = n
        min = 0
    elif comparator == '>':
        max = len(userInput)-1
        min = n+1
    elif comparator == '>=':
        max = len(userInput)-1
        min = n
    elif comparator == '=':
        max = n
        min = n
    else:
        print("error: comparator not found")

    return (userInput[0], userInput[1:], min, max)

def printList(outputList):
    for item in outputList:
        print(item,end=" ")
    print("")

(value, coins, min, max) = GetInput()
results = []
print(value, coins, min, max)
# brute force idea: find permutations of list, sum min to max indices of each permutation, output result if sum == value
# cons: brute force is slow, doesn't account for repeats of coins so we need to remove duplicate results
perms = itertools.permutations(coins, max)
for i in perms:
    #print(i)
    sum = 0
    index = 0
    for n in i:
        sum += n
        index += 1
        #print('sum: ', sum, 'index: ', index)
        if index >= min and sum == value:
            results.append(sorted(i[:index], reverse=True))
# check if solution possible
if not results:
    print('No solution possible')
else:
    # remove duplicates
    results = set(tuple(result) for result in results)
    for result in results:
        printList(result)