import numpy as np
from src.helper import sigmoid, relu

def init_weights(p, U, L, seed=0):
    np.random.seed(seed)
    
    weights = []
    for i in range(L):
        if i == 0 and L == 1:
            weights.append(np.random.rand(1, p))                # Randomly initialise input layer weight matrix of shape    W(1) = (p, 1)
        elif i == 0:
            weights.append(np.random.rand(U[i], p))             # Randomly initialise input layer weight matrix of shape    W(1) = (p, U)
        elif i == L-1:
            weights.append(np.random.rand(1, U[i-1]))           # Randomly initialise output layer weight matrix of shape   W(L) = (1, UL-1)
        else:
            weights.append(np.random.rand(U[i], U[i-1]))        # Randomly initialise hidden layer weight matrix of shape   W(l) = (Ul, Ul-1)
    return weights

def init_biases(U, L, seed=0):
    np.random.seed(seed)
    biases = []
    if L == 1:
        biases.append(np.random.rand())
    else:
        for i in range(L):
            biases.append(np.random.rand(U[i]))
    return biases

# h = activation function
# W = weights
# x = input
# b = bias
# p = number of features
# U = number of hidden layer neurons
# L = number of layers

def nn_matrix(data, rand_U=True, seed=0, L=1, U_limit=10):
    # Calculate variables for input layer
    p = data.shape[1]                               # Number of features set to number of spectroscopy columns
    x = data                                        # Initialise x matrix as column vector

    np.random.seed(seed)    
    if rand_U:
        U = np.random.randint(1, U_limit-1, L-1)    # Randomly initialise U in shape [U1, ..., UL-1] if rand_U is True
        U = np.append(U, 1)                         # Add 1 to the end of U to match the output layer

    # Initialise weights and bias
    # Randomly initialise weight matrix W. W(1) has dimensions of U1 x p, W(l) has dimensions of Ul x Ul-1. W(L) has dimensions of 1 x UL.
    weights = init_weights(p, U, L, seed)
    biases = init_biases(U, L, seed)

    # q(l) = h(W(l) * q(l-1) + b(l))
    q = x
    for i in range(L):
        q = np.dot(weights[i], q.T).T + biases[i]
        q = relu(q)

    return q