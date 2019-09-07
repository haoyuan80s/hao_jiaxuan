import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import listdir
import random
from matplotlib.patches import Rectangle
import pandas as pd
import numpy as np


IMAGE_FOLDER = '/home/ec2-user/Happy/kaggle/data/raw_data/train_images/'
LABEL_PATH = '/home/ec2-user/Happy/kaggle/data/raw_data/train.csv'


def main():
    data = Data(IMAGE_FOLDER, LABEL_PATH)
    data.sample_image(n=10, show_rectangle=True)


class Data():
    def __init__(self, image_folder, label_path):
        self.label = Label(label_path)
        self.image = Image(image_folder)

    def sample_image(self, n=1, show_rectangle=False):
        ids = self.image.sample_ids(n)
        for id_ in ids:
            if show_rectangle:
                rectangles = self.label.get_rectangles(id_)
            else:
                rectangles = None
            self.image.show_image(id_, rectangles)


class Label():
    def __init__(self, label_path):
        self.dic = self._get_dic(label_path)

    def _get_dic(self, path):
        return dict(pd.read_csv(path).values)

    def get_rectangles(self, imange_id):
        '''Get a list of all charactor rectangles for a given image'''
        if self.dic[imange_id]:
            image_label = self.dic[imange_id].split(' ')
        else:
            image_label = []
        return [np.array(image_label[i+1:i+5], dtype=float)
                for i in range(0, len(image_label), 5)]


class Image():
    def __init__(self, image_folder):
        self.folder = image_folder

    def sample_ids(self, n=1):
        return np.char.strip(random.sample(
            listdir(self.folder), n), chars='.jpg')

    def show_image(self, id_, rectangles=None):
        path = self.folder + id_ + '.jpg'
        img = mpimg.imread(path)
        plt.imshow(img)
        if rectangles:
            for rect in rectangles:
                self._add_rectangle(rect)
        plt.show()

    def _add_rectangle(self, rect):
        x, y, w, h = rect
        rect = Rectangle((x, y), w, h,
                         linewidth=1,
                         edgecolor='r',
                         facecolor='none')
        plt.gca().add_patch(rect)


if __name__ == '__main__':
    main()
