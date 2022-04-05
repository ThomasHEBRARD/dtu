#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:56:42 2022

@author: abda
"""
# demo_forward

import numpy as np
import matplotlib.pyplot as plt
import make_data
#%% Create some points

n = 300
example_nr = 2
noise = 1.2

X, T, x, dim = make_data.make_data(example_nr, n, noise)
fig, ax = plt.subplots(1,1)
ax.scatter(X[0:n,0],X[0:n,1],c = 'red', alpha = 0.3, s = 15)
ax.scatter(X[n:2*n,0],X[n:2*n,1],c = 'green', alpha = 0.3, s = 15)
ax.set_aspect('equal', 'box')
plt.title('training')


#%% Before training, you should make data have zero mean

c = X.mean(axis = 0)
std = X.std(axis = 0)
x_c = (x - c)/std
X_c = (X - c)/std

# fig, ax = plt.subplots(1,1)
# ax.scatter(X_c[0:n,0],X_c[0:n,1],c = 'red', alpha = 0.3, s = 15)
# ax.scatter(X_c[n:2*n,0],X_c[n:2*n,1],c = 'green', alpha = 0.3, s = 15)
# ax.set_aspect('equal', 'box')
# plt.title('Zero mean training')



#%% Randomly initialize weights

W1 = np.random.randn(3,3)
W2 = np.random.randn(4,2)
# print(W1)
# print(W2)

#%% Make the forward pass (all points at once - you should later create a minibatch implementation)

z = np.c_[X_c, np.ones((X_c.shape[0],1))]@W1
h = np.maximum(z, 0)
y_hat = np.c_[h, np.ones((X_c.shape[0],1))]@W2
y = np.exp(y_hat)/np.sum(np.exp(y_hat), axis=1, keepdims=True)

# print((y<0).sum())


#%% Make the forward pass of regularly sampled points

z = np.c_[x_c, np.ones((x_c.shape[0],1))]@W1
h = np.maximum(z, 0)
y_hat = np.c_[h, np.ones((x_c.shape[0],1))]@W2
y_im = np.exp(y_hat)/np.sum(np.exp(y_hat), axis=1, keepdims=True)


#%% Make a function that implements the forward pass

W = [W1, W2]
def forward(x, W):
    z = np.c_[x, np.ones((x.shape[0],1))]@W[0]
    h = np.maximum(z, 0)
    y_hat = np.c_[h, np.ones((x.shape[0],1))]@W[1]
    y = np.exp(y_hat)/np.sum(np.exp(y_hat), axis=1, keepdims=True)
    return y, h

eta = 0.001

def backpropagate(y, h, W):
    y, h = forward(X_c, W) #10-by-2, 10k-by-3

    delta_2 = y - T # 10k-by-2

    Q_2 = np.transpose(np.c_[h, np.ones((X_c.shape[0],1))])@delta_2

    a_prime = np.where(h>0, 1, 0) # 3-by-10k

    delta_2_T = delta_2.T # 2-by-10k

    W_2_chap = W[1][:3,:] # 3-by-2
    right_member = W_2_chap@delta_2_T # 3-by-10k
    left_member = np.transpose(a_prime) # 10k-by-3

    delta_1 = np.multiply(left_member, right_member) # 3-by-10k

    Q_1 = np.transpose(np.c_[X_c, np.ones((X_c.shape[0],1))])@delta_1.T

    W_1 = W[0] - eta * Q_1
    W_2 = W[1] - eta * Q_2
    
    W = [W_1, W_2]

    return W

max_iter = 1000
i = 0
while i < max_iter:
    print(i)
    y, h = forward(X_c, W)
    W = backpropagate(y, h, W)
    i += 1

y, h = forward(x_c, W)
im = np.reshape(y, (100, 100, 2))
fig, ax = plt.subplots()
ax.imshow(im[:,:,0])
plt.show()

