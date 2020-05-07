from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_train=len(y)
    num_class=W.shape[1]
    flag = True

    for i in range(num_train):
        unnorm_p = X[i].dot(W)
        unnorm_p -= np.argmax(unnorm_p)
        exp_unnorm_p = np.exp(unnorm_p)
        sum_exp_unnorm_p=np.sum(exp_unnorm_p)
        exp_norm_p = exp_unnorm_p / sum_exp_unnorm_p
        loss -= np.log(exp_norm_p[y[i]])
        if not flag:
            for j in range(num_class): 
                if j == y[i]:
                    dW[:,j] += -X[i] + X[i]*exp_norm_p[j]
                else:
                    dW[:,j] += X[i]*exp_norm_p[j]
        else:
            dW += X[i].reshape(-1,1).dot(exp_norm_p.reshape(1,-1))
            dW[:,y[i]] -= X[i]


    loss /= num_train
    dW /= num_train
    loss += reg * np.sum( W * W )
    dW += 2 * reg * W



    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_train=len(y)
    num_class= W.shape[1]

    unnorm_p = X.dot(W)
    unnorm_p -= np.argmax(unnorm_p,axis=1).reshape(-1,1)
    exp_unnorm_p = np.exp(unnorm_p)
    sum_exp_unnorm_p = np.sum(exp_unnorm_p,axis=1).reshape(-1,1)

    exp_norm_p = exp_unnorm_p / sum_exp_unnorm_p

    norm_p = - np.log(exp_norm_p)
    loss += np.sum(norm_p[np.arange(num_train),y]) / num_train + reg * np.sum( W * W )

    exp_norm_p[np.arange(num_train),y] -= 1

    dW += X.T.dot(exp_norm_p)/num_train + 2 * reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
