import tensorflow as tf
import tensorflow.examples.tutorials.mnist.input_data as input_data


# data
mnist = input_data.read_data_sets("mnist_data/", one_hot=True)


def weight_variable(shape, name):
    initial = tf.random_normal(shape, stddev=0.1, name=name)
    return tf.Variable(initial)

def bias_variable(shape, name):
    initial = tf.constant(0.1, shape=shape, name=name)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x, name):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name=name)

# define placeholder
xs = tf.placeholder(tf.float32, [None, 784], name='x_input')
ys = tf.placeholder(tf.float32, [None, 10], name='y_input')
x_image = tf.reshape(xs, [-1, 28, 28, 1], name='data')


# conv1 layer
W_conv1 = weight_variable([5, 5, 1, 32], name='W_conv1')
b_conv1 = bias_variable([32], name='b_conv1')
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1, name='h_conv1')

#  pool1 layer
h_pool1 = max_pool_2x2(h_conv1, name='h_pool1')

# conv2 layer
W_conv2 = weight_variable([5, 5, 32, 64], name='W_conv2')
b_conv2 = bias_variable([64], name='b_conv2')
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2, name='h_conv2')

# pool2 layer
h_pool2 = max_pool_2x2(h_conv2, name='h_pool2')

# func1 layer
W_func1 = weight_variable([7 * 7 * 64, 1024], name='W_func1')
b_func1 = bias_variable([1024], name='b_func1')
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64], name='h_pool2_flat')

h_func1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_func1) + b_func1, name='h_func1')


# output layer
W_func2 = weight_variable([1024, 10], name='W_func2')
b_func2 = bias_variable([10], name='b_func2')
prediction = tf.nn.softmax(tf.matmul(h_func1, W_func2) + b_func2, name='prediction')

# cross entropy
cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction), reduction_indices=[1]))

with tf.name_scope("train"):
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

# accuracy
correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(ys, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# initial session
sess = tf.Session()
sess.run(tf.global_variables_initializer())

output_node_names = 'data,prediction'
# train
for step in range(3000):
    batch = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={xs:batch[0], ys:batch[1]})
    if step % 100 == 0:
        loss, acc = sess.run((cross_entropy, accuracy), feed_dict={xs:batch[0], ys:batch[1]})
        print('Current step: %d, loss: %s, accuracy: %s' % (step, loss, acc))

print(sess.run(accuracy, feed_dict={xs:mnist.test.images, ys:mnist.test.labels}))

# directly obatin frozen_model.pb without using freeze_graph.py
constant_graph = tf.graph_util.convert_variables_to_constants(sess, sess.graph_def, output_node_names.split(','))
with tf.gfile.GFile('trained_model/frozen_model.pb', "wb") as f:
    f.write(constant_graph.SerializeToString())


sess.close()


