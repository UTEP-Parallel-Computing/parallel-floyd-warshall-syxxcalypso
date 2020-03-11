import numpy # Required by mpi4py so cannot reasonably be considered an additional library!

class MatrixIncompatibleError(Exception):
    def __init__(self, message):
        super().__init__(message)

class ParallelMatrix(object):
    __doc__ = ''''''
    def __init__(self, rows, cols, fill_random=False):
        self.rows = rows
        self.cols = cols
        self.table = numpy.array((rows,cols), dtype=numpy.short)
        if fill_random:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.table[i][j] = random.randint(1,6)

    @classmethod
    def from_list(cls, multilist):
        cols = len(multilist[0])
        for row in multilist:
            if len(row) != cols:
                raise TypeError("Multidimensional list must be rectangular!")
        m = cls(len(multilist), cols)
        m.table = numpy.array(multilist, dtype=numpy.short)
        return m

    def __str__(self):
        result_matrix_s = ''
        for row in self.table:
            for i in row:
                if i >= 2**10:
                    result_matrix_s += ' . '
                else:
                    result_matrix_s += '{:2d} '.format(i)
            result_matrix_s += ' \n'
        return result_matrix_s
