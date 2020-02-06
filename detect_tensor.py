from __future__ import print_function

import numpy as np
import pandas as pd
import tensorflow.compat.v1 as tf
from sklearn.preprocessing import LabelBinarizer
from sklearn.utils import shuffle
from sklearn.model_selection import KFold

tf.disable_v2_behavior()

# Import MNIST data
originalTrainingData = pd.read_csv('anaSampledForTraining.csv')
trainingData = shuffle(originalTrainingData)
X_trainingData = np.array(trainingData['wrdiff']).reshape(len(originalTrainingData), 1)
Y_trainingData = []
for data in trainingData['label']:
    if data is 0:
        Y_trainingData.append([1, 0])
    else:
        Y_trainingData.append([0, 1])
Y_trainingData = np.array(Y_trainingData).reshape(len(originalTrainingData), 2)

totalNumber = len(originalTrainingData.index)

# Parameters
learning_rate = 0.001
training_epochs = 150
batch_size = 100
display_step = 1

# Network Parameters
n_hidden_1 = 256  # 1st layer number of neurons
n_hidden_2 = 256  # 2nd layer number of neurons
n_input = 1  # MNIST data input (img shape: 28*28)
n_classes = 2  # MNIST total classes (0-9 digits)

# tf Graph input
X = tf.placeholder("float", [None, n_input])
Y = tf.placeholder("float", [None, n_classes])

weight_mean = {

}

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

saver = tf.train.Saver()


def cross_validate(session_, split_size=10):
    results = []
    count = 0
    kf = KFold(n_splits=split_size)
    for train_idx, val_idx in kf.split(X_trainingData, Y_trainingData):
        train_x = X_trainingData[train_idx]
        train_y = Y_trainingData[train_idx]
        val_x = X_trainingData[val_idx]
        val_y = Y_trainingData[val_idx]
        run_train(session_, train_x, train_y, val_x, val_y, count)
        count += 1
    return results


# Create model
def multilayer_perceptron(x):
    # Hidden fully connected layer with 256 neurons
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    # Hidden fully connected layer with 256 neurons
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    # Output fully connected layer with a neuron for each class
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer


# Construct model
logits = multilayer_perceptron(X)

# Define loss and optimizer
loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=logits, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))

# Initializing the variables
init = tf.global_variables_initializer()


def get_next_batch(i, total_batch):
    batch_size_ = totalNumber // batch_size
    if i < total_batch - 1:
        return X_trainingData[i * batch_size_:(i + 1) * batch_size_], Y_trainingData[
                                                                      i * batch_size_:(i + 1) * batch_size_]
    return X_trainingData[i * batch_size_:], Y_trainingData[i * batch_size_:]


def run_train(session_, train_x, train_y, val_x, val_y, count):
    for epoch in range(100):
        avg_cost = 0.
        total_batch = int(len(train_x) / batch_size)
        x_batches = np.array_split(train_x, total_batch)
        y_batches = np.array_split(train_y, total_batch)
        # Loop over all batches
        for i in range(total_batch):
            batch_x, batch_y = x_batches[i], y_batches[i]
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = session_.run([train_op, loss_op], feed_dict={X: batch_x, Y: batch_y})
            # Compute average loss
            avg_cost += c / total_batch
        # Display logs per epoch step
        # if epoch % display_step == 0:
        # print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(avg_cost))
    print("Optimization Finished!")

    # acc = np.mean([session_.run(accuracy, feed_dict={
    #     X: val_x[i],
    #     Y: val_y[i]})
    #               for i in range(len(val_x))]
    #               )
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy:", accuracy.eval({X: val_x, Y: val_y}))
    # print('weights1:', session_.run(weights))
    # saver.save(session_, save_path='models/count' + str(count) + '.ckpt')


with tf.Session() as session:
    session.run(init)
    result = cross_validate(session)
    print("Cross-validation result: %s" % result)
