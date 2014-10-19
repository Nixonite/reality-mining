reality-mining
==============

Python code for [parsing the RealityMining dataset in Python using numpy/scipy.](http://jeremykun.com/2014/01/21/realitymining-a-case-study-in-the-woes-of-data-processing/)

This code is a fork, so it builds and stems away from it somehow. This branch detects bluetooth proximity events (when two people are close to each other and are thus detected via bluetooth scans every 6 minutes or so) and makes a guess about their friendship based on how many events take place at certain times such as holidays, weekeends, whatever. 
