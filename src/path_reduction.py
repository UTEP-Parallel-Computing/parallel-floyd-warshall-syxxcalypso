#!/usr/bin/env python3
####################################
#
# Jennifer Harrison
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
size = comm.Get_size()

def path_reduce(d):
    for k in range(d.rows):
        for i in range(d.cols):
            for j in range(d.rows):
                d.table[i][j] = min(d.table[i][j], d.table[i][k] + d.table[k][j])

if __name__ == '__main__':
    rpt = 8/size
    tpr = size/8

    row_start = int(rpt * rank)
    row_end = int(rpt * (size+1))

    d = matrix.ParallelMatrix(8, 8)

    for k in range(d.rows):
        d.table[k] = comm.bcast(d.table[k], root=int(tpr*k))
        for i in range(d.cols):
            for j in range(d.rows):
                d.table[i][j] = min(d.table[i][j], d.table[i][k] + d.table[k][j])

    if rank == 0:
        #--- Some arbitrary and very large integer weight
        z = 2**8
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
        #--- Weight Matrix
        w = matrix.ParallelMatrix.from_list(graph)
        #--- Distance Matrix (Solution Matrix)
        d = matrix.ParallelMatrix.from_list(graph)

        for k in range(row_end, d.rows):
            d.table[k] = comm.recv(source=int(tpr*k), tag=k)
    else:
        for k in range(row_start, row_end):
            comm.Send(d.table[k], dest=0, tag=k)




    start = time.time()
    path_reduce(d)
    end = time.time()
    print(w)
    print('   Example Transform\n          |\n          v\n\n')
    print(d)
    print('Time Taken: %.20fs' % (end-start))
