try:
    import pymp
except ImportError:
    print("PyMP Failed to import, is it install?")
    sys.exit(1)

class MatrixIncompatibleError(Exception):
    def __init__(self, message):
        super().__init__(message)

class ParallelMatrix(object):
    __doc__ = ''''''
    def __init__(self, rows, cols, pthreads=1, fill_random=False):
        self.rows = rows
        self.cols = cols
        self.table = pymp.shared.array((rows,cols), dtype='int')
        if fill_random:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.table[i][j] = random.randint(1,6)

    @classmethod
    def from_list(cls, multilist, pthreads=1):
        cols = len(multilist[0])
        for row in multilist:
            if len(row) != cols:
                raise TypeError("Multidimensional list must be rectangular!")
        m = cls(len(multilist), cols, pthreads)
        for i in range(m.rows):
            for j in range(m.cols):
                m.table[i][j] = multilist[i][j]
        return m

    def __matmul__(self, obj):
        if not self.rows == obj.cols:
            raise MatrixIncompatibleError("Matrix row count does not match target Matrix column count!\n")
        result_matrix = Matrix(self.rows, obj.cols)
        with pymp.Parallel(pthreads) as p:
            for _row in p.range(self.rows):
                for col in range(obj.cols):
                    for row in range(obj.rows):
                        result_matrix.table[_row][col] += self.table[_row][row] * obj.table[row][col]
        return result_matrix

    def __str__(self):
        result_matrix_s = ''
        for row in self.table:
            for i in row:
                if i >= 2**16:
                    result_matrix_s += ' . '
                else:
                    result_matrix_s += '{:2d} '.format(i)
            result_matrix_s += ' \n'
        return result_matrix_s
