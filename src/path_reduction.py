#!/usr/bin/env python3
####################################
#
# Jennifer Harrison
# ID: 
# Class: 
#
####################################
import os, sys, time, matrix

def path_reduce(w, d):
    for k in range(w.rows):
        for i in range(w.cols):
            for j in range(w.rows):
                d.table[i][j] = min(d.table[i][j], d.table[i][k] + d.table[k][j])


#--- Some arbitrary and very large integer
z = 2**16

#--- Weighted symmetrical graph
#         0   1   2   3   4   5   6   7
#         A   B   C   D   E   F   G   H
graph = [[0,  4,  z,  z,  z,  z,  7,  4],  # A  0
         [z,  0,  9,  z,  z,  6,  8,  1],  # B  1
         [z,  z,  0,  z, 10,  z,  z,  z],  # C  2
         [z,  z,  z,  0,  z,  z,  z,  z],  # D  3
         [z,  z,  8,  6,  0,  5,  z,  z],  # E  4
         [z,  z,  z,  z,  6,  0,  z,  z],  # F  5
         [z,  4,  z,  z,  z,  7,  0,  z],  # G  6
         [z,  z,  3,  z,  z,  z,  z,  0]]  # H  5



#--- Create weight and solution matrices from graph
W = matrix.ParallelMatrix.from_list(graph, 2)
D = matrix.ParallelMatrix.from_list(graph, 2)

if __name__ == '__main__':
    start = time.time()
    path_reduce(W, D)
    end = time.time()
    print(W)
    print('   Example Transform\n          |\n          v\n\n')
    print(D)
    print('Time Taken: %.20fs' % (end-start))

# At this commit stage, the program is still using pymp, please look to further commits for use of mpi
