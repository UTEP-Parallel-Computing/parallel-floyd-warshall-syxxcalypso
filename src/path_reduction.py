#!/usr/bin/env python3
####################################
#
# Jennifer Harrison
# ID: 
# Class: 
#
####################################
import os, sys, time, matrix

try:
    from mpi4py import MPI
except ImportError:
    print("OpenMPI Failed to import, is it installed?")
    sys.exit(1)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

#--- Some arbitrary and very large integer weight
z = 2**10
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
W = matrix.ParallelMatrix.from_list(graph)
D = matrix.ParallelMatrix.from_list(graph)

def path_reduce(d):
    for k in range(d.rows):
        for i in range(d.cols):
            for j in range(d.rows):
                d.table[i][j] = min(d.table[i][j], d.table[i][k] + d.table[k][j])

def path_reduce_multi(d):
    for k in range(d.rows):
        d[k] = comm.bcast(d[k], root=0)
        for i in range(d.cols):
            for j in range(d.rows):
                d.table[i][j] = min(d.table[i][j], d.table[i][k] + d.table[k][j])

if __name__ == '__main__':
    '''
    if rank == 0:
        for k in range(D.rows):
            D[k] = comm.recv(source=0, tag=k)
    else:
        for k in range(D.rows):
            comm.Send(D[k], dest=0, tag=k)
    '''
    start = time.time()
    path_reduce(D)
    end = time.time()
    print(W)
    print('   Example Transform\n          |\n          v\n\n')
    print(D)
    print('Time Taken: %.20fs' % (end-start))
