import numpy as np

def gaussian_elimination(matrix):
    """Performs Gaussian elimination on a matrix."""
    matrix = np.array(matrix, dtype=float)
    rows, cols = matrix.shape
    row = 0
    for col in range(cols):
        if row >= rows:
            break
        pivot_row = row
        while pivot_row < rows and matrix[pivot_row, col] == 0:
            pivot_row += 1
        if pivot_row == rows:
            continue
        matrix[[row, pivot_row]] = matrix[[pivot_row, row]]
        matrix[row] /= matrix[row, col]
        for i in range(rows):
            if i != row:
                matrix[i] -= matrix[i, col] * matrix[row]
        row += 1
    return matrix

def gauss_jordan_elimination(matrix):
    """Performs Gauss-Jordan elimination on a matrix."""
    matrix = np.array(matrix, dtype=float)
    rows, cols = matrix.shape
    row = 0
    for col in range(cols):
        if row >= rows:
            break
        pivot_row = row
        while pivot_row < rows and matrix[pivot_row, col] == 0:
            pivot_row += 1
        if pivot_row == rows:
            continue
        matrix[[row, pivot_row]] = matrix[[pivot_row, row]]
        matrix[row] /= matrix[row, col]
        for i in range(rows):
            if i != row:
                matrix[i] -= matrix[i, col] * matrix[row]
        row += 1
    return matrix

def determinant(matrix):
    """Calculates the determinant of a square matrix."""
    matrix = np.array(matrix, dtype=float)
    rows, cols = matrix.shape
    if rows != cols:
        raise ValueError("Matrix must be square to calculate determinant")
    if rows == 1:
        return matrix[0, 0]
    if rows == 2:
        return matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0]
    det = 0
    for i in range(cols):
        submatrix = np.delete(np.delete(matrix, 0, 0), i, 1)
        det += (-1) ** i * matrix[0, i] * determinant(submatrix)
    return det

def solve_matrix_system(matrix, method='gaussian'):
    """Solves a system of linear equations using Gaussian or Gauss-Jordan elimination."""
    matrix = np.array(matrix, dtype=float)
    rows, cols = matrix.shape
    if method == 'gaussian':
        reduced_matrix = gaussian_elimination(matrix)
    elif method == 'gauss-jordan':
        reduced_matrix = gauss_jordan_elimination(matrix)
    else:
        raise ValueError("Invalid method. Choose 'gaussian' or 'gauss-jordan'.")
    return reduced_matrix

