import os
import glob
import random
import shutil
import numpy as np
from PIL import Image


def resetDir(name):
    if name not in os.listdir(os.path.join('data', 'custom')):
        os.mkdir(os.path.join('data', 'custom', name))
    else:
        shutil.rmtree(os.path.join('data', 'custom', name))
        os.mkdir(os.path.join('data', 'custom', name))


def generate(images, name, type, frame_length=400):

    for image in images:
        new_image = Image.new('RGBA', (frame_length, frame_length),
                              (255, 255, 255))

        label_idx = image[1].split('/')[-1][0]
        image = image[0]

        width, height = image.size
        width = round(width / frame_length, 8)
        height = round(height / frame_length, 8)
        x, y = random.uniform(0, 1 - width), random.uniform(0, 1 - height)
        x_center = round(x + width / 2, 8)
        y_center = round(y + height / 2, 8)

        new_image.paste(
            image,
            (int(round(x * frame_length)), int(round(y * frame_length))))
        label_text = str(label_idx) + ' ' + str(x_center) + ' ' + str(
            y_center) + ' ' + str(width) + ' ' + str(height)

        new_image.save(os.path.join('data', 'custom', 'images', name + '.png'))
        with open(os.path.join('data', 'custom', 'labels', name + '.txt'),
                  'w') as label_file:
            label_file.write(label_text)


def main():

    resetDir('images')
    resetDir('labels')

    images_name = glob.glob(os.path.join('data', 'custom', 'origin', '*.png'))
    train_text, valid_text = '', ''

    count = 0

    images = []
    # Generate one object on each image
    for image_name in images_name:
        with Image.open(image_name) as image:
            images = [(image, image_name)]
            for i in range(80):
                count += 1
                generate(images, str(count), 'train')
                train_text += 'data/custom/images/' + str(count) + '.png\n'
            for i in range(20):
                count += 1
                generate(images, str(count), 'valid')
                train_text += 'data/custom/images/' + str(count) + '.png\n'

    with open(os.path.join('data', 'custom', 'train.txt'), 'w') as train_file:
        train_file.write(train_text)
    with open(os.path.join('data', 'custom', 'valid.txt'), 'w') as valid_file:
        valid_file.write(valid_text)


if __name__ == '__main__':
    main()
