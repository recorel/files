#!/usr/bin/env python

# Save parameters every a few SGD iterations as fail-safe
SAVE_PARAMS_EVERY = 5000

import glob
import os.path as op
import pickle
import random

import numpy as np

# from utils.gradcheck import gradcheck_naive
# from utils.utils import softmax

import json

import numpy as np


def dump(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f)


def load(path):
    with open(path) as f:
        obj = json.load(f)

    return obj


def normalize_rows(x):
    """ Row normalization function

    Implement a function that normalizes each row of a matrix to have
    unit length.
    """
    N = x.shape[0]
    x /= np.sqrt(np.sum(x ** 2, axis=1)).reshape((N, 1)) + 1e-30
    return x


def softmax(x):
    """Compute the softmax function for each row of the input x.
    It is crucial that this function is optimized for speed because
    it will be used frequently in later code. 

    Arguments:
    x -- A D dimensional vector or N x D dimensional numpy matrix.
    Return:
    x -- You are allowed to modify x in-place
    """
    orig_shape = x.shape

    if len(x.shape) > 1:
        # Matrix
        tmp = np.max(x, axis=1)
        x -= tmp.reshape((x.shape[0], 1))
        x = np.exp(x)
        tmp = np.sum(x, axis=1)
        x /= tmp.reshape((x.shape[0], 1))
    else:
        # Vector
        tmp = np.max(x)
        x -= tmp
        x = np.exp(x)
        tmp = np.sum(x)
        x /= tmp

    assert x.shape == orig_shape
    return x


def sigmoid(x):
  """
  Compute the sigmoid function for the input here.
  Arguments:
  x -- A scalar or numpy array.
  Return:
  s -- sigmoid(x)
  """

  ### START CODE HERE
  s = 1 / (1 + np.exp(-x))
  ### END CODE HERE

  return s

def naive_softmax_loss_and_gradient(center_word_vec,outside_word_idx,outside_vectors,dataset):
  """ Naive Softmax loss & gradient function for word2vec models

  Implement the naive softmax loss and gradients between a center word's 
  embedding and an outside word's embedding. This will be the building block
  for our word2vec models.

  Arguments:
  center_word_vec -- numpy ndarray, center word's embedding
                  (v_c in the pdf handout)
  outside_word_idx -- integer, the index of the outside word
                  (o of u_o in the pdf handout)
  outside_vectors -- outside vectors (rows of matrix) for all words in vocab
                    (U in the pdf handout)
  dataset -- needed for negative sampling, unused here.

  Return:
  loss -- naive softmax loss
  grad_center_vec -- the gradient with respect to the center word vector
                   (dJ / dv_c in the pdf handout)
  grad_outside_vecs -- the gradient with respect to all the outside word vectors
                  (dJ / dU)
                  
   Note:
   - we usually use column vector convention (i.e., vectors are in column form) for vectors in matrix U and V (in the handout)
   but for ease of implementation/programming we usually use row vectors (representing vectors in row form).
   - A softmax() function provided (utils/utils.py) which takes as input a vector/matrix of values and returns the softmax for each value in the vector, relative to the others.

  """

  ### Please use the provided softmax function (imported earlier in this file)
  ### This numerically stable implementation helps you avoid issues pertaining
  ### to integer overflow.
  
  ### START CODE HERE

  # print(20*"*")
  # print("Center word: ", center_word_vec)
  # print(20*"*")
  # print("outsdie vectors: ", outside_vectors)
  # # print(20*"*")
  # print(outside_word_idx)
  # print(20*"*")
  # print(outside_vectors[2])
  print(20*"#")
  # print(outside_vectors * center_word_vec)

  # gradient w/r to center vector

  outside_word_vec = outside_vectors[outside_word_idx]

  rows, _ = np.shape(outside_vectors)
  y = np.zeros((rows,)).astype(float)


  y[outside_word_idx] = 1

  print("y:", y)
  
  y_hat = np.matmul(
            softmax(np.matmul(outside_vectors, center_word_vec)), 
            outside_vectors
            )

  grad_center_vec = np.dot(
     outside_word_vec, 
     np.subtract(y_hat, y)
     )
  grad_outside_vecs = np.dot(
     center_word_vec,
     np.subtract(y_hat, y)
     )
  
  loss = - np.dot(outside_word_vec, center_word_vec)  + \
    np.log( np.sum(np.exp( np.matmul(outside_vectors, center_word_vec))))
  
  
  '''
      'test_naivesoftmax': {
        'center_word_vec': np.array([-0.27323645, 0.12538062, 0.95374082]).astype(float),
        'outside_word_idx': 3,
        'outside_vectors': np.array([[-0.6831809, -0.04200519, 0.72904007],
                                    [0.18289107, 0.76098587, -0.62245591],
                                    [-0.61517874, 0.5147624, -0.59713884],
                                    [-0.33867074, -0.80966534, -0.47931635],
                                    [-0.52629529, -0.78190408, 0.33412466]]).astype(float)
  

  output:

    'test_naivesoftmax': {
        'loss': 2.217424877675181,
        'dj_dvc': np.array([-0.17249875, 0.64873661, 0.67821423]).astype(float),
        'dj_du': np.array([[-0.11394933, 0.05228819, 0.39774391],
                           [-0.02740743, 0.01257651, 0.09566654],
                           [-0.03385715, 0.01553611, 0.11817949],
                           [0.24348396, -0.11172803, -0.84988879],
                           [-0.06827005, 0.03132723, 0.23829885]]).astype(float)

  '''

  ### END CODE HERE

  return loss, grad_center_vec, grad_outside_vecs


def main():
  print("bbb")
  center_word_vec =np.array([-0.27323645, 0.12538062, 0.95374082]).astype(float)
  outside_word_idx = 3
  outside_vectors = np.array([[-0.6831809, -0.04200519, 0.72904007],
                              [0.18289107, 0.76098587, -0.62245591],
                              [-0.61517874, 0.5147624, -0.59713884],
                              [-0.33867074, -0.80966534, -0.47931635],
                              [-0.52629529, -0.78190408, 0.33412466]]).astype(float)
          
  print(naive_softmax_loss_and_gradient(center_word_vec,outside_word_idx,outside_vectors, None))

if __name__ == "__main__":
   main()
