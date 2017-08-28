import numpy as np
import math
import actions

def apply_mesh(matrix, mesh,size):
    shape = matrix.shape
    print(shape)
    if len(shape) > 2:
        out = np.zeros(shape,dtype=np.int16)
        for i in range(shape[2]):
            out[:, :, i] = apply_mesh_one_dimension(matrix[:, :, i], mesh, size)
        return out
    else:
        return apply_mesh_one_dimension(matrix,mesh,size)


def apply_mesh_one_dimension(matrix, mesh, size):
    out = np.zeros(matrix.shape, dtype=np.int16)
    radius = int(size / 2)
    shape = matrix.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if i >= shape[0] - radius or i < radius or j < radius or j >= shape[1] - radius:
                out[i, j] = matrix[i, j]
            else:
                out[i, j] = int(np.sum(mesh * matrix[i - radius:i + radius + 1, j - radius:j + radius + 1]))

    return out


def mean_filter(matrix, size):
    mesh = np.full((size, size), 1/(size*size), dtype=np.float32)
    return apply_mesh(matrix, mesh, size)


def weighted_mean_filter(matrix, size):
    mesh = [[1/16, 2/16, 1/16], [2/16, 4/16, 2/16], [1/16, 2/16, 1/16]]
    return apply_mesh(matrix, mesh, size)


def median_filter(matrix, size):
    shape = matrix.shape
    print(shape)
    if len(shape) > 2:
        out = np.zeros(shape, dtype=np.int16)
        for i in range(shape[2]):
            out[:, :, i] = apply_median_one_dimension(matrix[:, :, i], size)
        return out
    else:
        return apply_median_one_dimension(matrix, size)

def weighted_median_filter(matrix, size):
    shape = matrix.shape
    print(shape)
    if len(shape) > 2:
        out = np.zeros(shape, dtype=np.int16)
        for i in range(shape[2]):
            out[:, :, i] = apply_weighted_median_one_dimension(matrix[:, :, i], size)
        return out
    else:
        return apply_weighted_median_one_dimension(matrix, size)


def apply_weighted_median_one_dimension(matrix,size):
    out = np.zeros(matrix.shape, dtype=np.int16)
    radius = int(size / 2)
    mesh = [1, 2, 1, 2, 4, 2, 1, 2, 1]
    shape = matrix.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if i >= shape[0] - radius or i < radius or j < radius or j >= shape[1] - radius:
                out[i, j] = matrix[i, j]
            else:
                out[i, j] = np.median(np.repeat(matrix[i - radius:i + radius + 1, j - radius:j + radius + 1], mesh))

    return out

def apply_median_one_dimension(matrix,size):
    out = np.zeros(matrix.shape, dtype=np.int16)
    radius = int(size / 2)
    shape = matrix.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if i >= shape[0] - radius or i < radius or j < radius or j >= shape[1] - radius:
                out[i, j] = matrix[i, j]
            else:
                out[i, j] = np.median(matrix[i - radius:i + radius + 1, j - radius:j + radius + 1])

    return out


def gauss_filter(matrix, size, std):
    mesh = np.zeros((size, size))
    radius = int(size/2)
    cst = 1 / (2*math.pi*std*std)
    for i in range(-radius,radius+1):
        for j in range(-radius, radius+1):
            mesh[i+radius, j+radius] = cst*math.exp(-(j*j + i*i)/(2*std*std))
    print(np.sum(mesh))
    ma = apply_mesh(matrix, mesh, size)
    return ma


def highpass_filter(matrix,size):
    mesh = np.full((size,size), -1/(size*size), dtype=np.float32)
    radius = int(size/2)
    mesh[radius, radius] = (size*size - 1) / (size*size)
    print(mesh)
    return actions.linear_transform(apply_mesh(matrix, mesh, size))
