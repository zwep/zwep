# encoding: utf-8

"""


"""

import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


def tsne_plot(data, color):
    """
    Caluclate TSNE clustering
    :param data:
    :param color:
    :return:
    """
    tsne = TSNE(perplexity=50, n_components=2, init='pca', n_iter=1000, method='exact')
    tsne_document = tsne.fit_transform(data)

    plt.figure(figsize=(9, 9))  # in inches
    for i_index, i_color in enumerate(color):
        x, y = tsne_document[i_index, :]
        plt.scatter(x, y, color=i_color)

    plt.show()


def generate_error_plot(loss_value, epoch_list):
    """
    Used to show the relation between iterations and loss value
    :param loss_value:
    :param epoch_list:
    :return:
    """
    plt.figure(1)
    plt.plot(epoch_list, loss_value)
    name_file = "plot_error_rate" + ".png"
    plt.savefig(name_file)
    plt.gcf().clear()


def generate_gif():
    """
    Used to create a gif from the generated prediction-plots
    :return:
    """
    import glob
    import imageio

    images = []
    filenames = glob.glob("linreg*png")
    for filename in filenames:
        images.append(imageio.imread(filename))

    imageio.mimsave('convergence.gif', images)


def plot_with_labels(low_dim_embs, labels, filename):
    """
    Function to draw visualization of distance between embeddings.

    :param low_dim_embs:
    :param labels:
    :param filename:
    :return:
    """
    assert low_dim_embs.shape[0] >= len(labels), 'More labels than embeddings'
    plt.figure(figsize=(18, 18))  # in inches
    for i, label in enumerate(labels):
        x, y = low_dim_embs[i, :]
        plt.scatter(x, y)
        plt.annotate(label,
                     xy=(x, y),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.savefig(filename)
