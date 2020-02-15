from __future__ import print_function

import numpy as np
import pandas as pd
import sklearn as sk
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
    # weights_mean = {
    #     'h1': tf.Variable(tf.zeros([n_input, n_hidden_1])),
    #     'h2': tf.Variable(tf.zeros([n_hidden_1, n_hidden_2])),
    #     'out': tf.Variable(tf.zeros([n_hidden_2, n_classes]))
    # }
    #
    # biases_mean = {
    #     'b1': tf.Variable(tf.zeros([n_hidden_1])),
    #     'b2': tf.Variable(tf.zeros([n_hidden_2])),
    #     'out': tf.Variable(tf.zeros([n_classes]))
    # }

    results = []
    count = 0
    kf = KFold(n_splits=split_size)
    for train_idx, val_idx in kf.split(X_trainingData, Y_trainingData):
        train_x = X_trainingData[train_idx]
        train_y = Y_trainingData[train_idx]
        val_x = X_trainingData[val_idx]
        val_y = Y_trainingData[val_idx]
        run_train(session_, train_x, train_y, val_x, val_y, count)
        # weights_mean = weights_step, weights_mean
        # biases_mean = tf.add(biases_step, biases_mean)
    # weights_mean = session_.run(tf.divide(weights_mean, split_size))
    # biases_mean = session_.run(tf.divide(biases_mean, split_size))
    # return weights_mean, biases_mean


# Create model
def multilayer_perceptron(x):
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['h1']), biases['b1']))
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['h2']), biases['b2']))
    out_layer = tf.nn.sigmoid(tf.matmul(layer_2, weights['out']) + biases['out'])
    return out_layer


# Construct model
logits = multilayer_perceptron(X)

# Define loss and optimizer
loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=logits, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

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
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(avg_cost))
    print("Optimization Finished!")
    # acc = np.mean([session_.run(accuracy, feed_dict={
    #     X: val_x[i],
    #     Y: val_y[i]})
    #               for i in range(len(val_x))]
    #               )
    # accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

    # the recall for good moves

    # good_x_index = tf.where(tf.equal(val_y, [0, 1]))
    good_moves_x = []
    good_moves_y = []

    bad_moves_x = []
    bad_moves_y = []

    # index = 0
    # for val in val_y:
    #     # print(val)
    #     if (val == [0, 1]).all():
    #         good_moves_y.append(val)
    #         good_moves_x.append(val_x[index])
    #     else:
    #         bad_moves_y.append(val)
    #         bad_moves_x.append(val_x[index])
    #     index += 1

    f1(session_, val_x, val_y, model='single')
    # f1(session_, bad_moves_x, bad_moves_y)

    # f_score(session_,)
    # the recall for bad moves


def f1(session_, val_x, y_true, model='multi'):

    # y_p = tf.arg_max(logits, 1)
    val_accuracy, y_hat = session_.run([accuracy, logits], feed_dict={X: val_x, Y: y_true})
    # y_true = np.argmax(val_y, 1)

    epsilon = 1e-7
    y_hat = tf.round(y_hat)  # 将经过sigmoid激活的张量四舍五入变为0，1输出
    print(y_hat.eval())

    tp = tf.reduce_sum(tf.cast(y_hat * y_true, 'float'), axis=0)
    # tn = tf.sum(tf.cast((1-y_hat)*(1-y_true), 'float'), axis=0)
    fp = tf.reduce_sum(tf.cast((1 - y_hat) * y_true, 'float'), axis=0)
    fn = tf.reduce_sum(tf.cast(y_hat * (1 - y_true), 'float'), axis=0)

    p = tp / (tp + fp + epsilon)  # epsilon的意义在于防止分母为0，否则当分母为0时python会报错
    r = tp / (tp + fn + epsilon)

    f1 = 2 * p * r / (p + r + epsilon)
    f1 = tf.where(tf.is_nan(f1), tf.zeros_like(f1), f1)

    print(f1.eval())

    if model == 'single':
        return f1
    if model == 'multi':
        return tf.reduce_mean(f1)

def f_score(session_, val_x, val_y, print_label=''):
    y_p = tf.arg_max(logits, 1)
    val_accuracy, y_pred = session_.run([accuracy, y_p], feed_dict={X: val_x, Y: val_y})
    # good moves
    y_true = np.argmax(val_y, 1)

    TP = tf.count_nonzero(y_pred * y_true, dtype=tf.float32)
    TN = tf.count_nonzero((y_pred - 1) * (y_true - 1), dtype=tf.float32)
    FP = tf.count_nonzero(y_pred * (y_true - 1), dtype=tf.float32)
    FN = tf.count_nonzero((y_pred - 1) * y_true, dtype=tf.float32)

    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * precision * recall / (precision + recall)

    print(precision)
    # the recall for total samples
    # print("%s Accuracy: %f" % (print_label, val_accuracy))
    # print("%s Precision: %f" % (print_label, precision))
    # print("%s Recall: %f" % (print_label, recall))
    # print("%s f1_score: %f" % (print_label, f1))


with tf.Session() as session:
    session.run(init)
    cross_validate(session)
    # accuracy_t = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    # print("Accuracy_model:", accuracy_t.eval({X: X_trainingData, Y: Y_trainingData}))
