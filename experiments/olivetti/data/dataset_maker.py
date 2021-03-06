import math
import numpy as np
import sklearn.datasets as datasets
from rotators import *

def main():
    olivetti = datasets.fetch_olivetti_faces()
    inputs = olivetti['data']
    images = olivetti['images']
    targets = olivetti['target']

    repeat_images = 30 # the number of times we want to repeat each image
    n_images = images.shape[0] * repeat_images
    image_sz = images.shape[1]

    image_keep = int(math.sqrt(2) * image_sz/2)

    rotated_faces = np.zeros((n_images, image_keep, image_keep))
    all_targets = np.zeros(n_images)
    angles = np.pi * np.random.rand(n_images) - np.pi/2
    degrees = 180/np.pi * angles

    img_ind = 0
    for rpt in range(repeat_images):
        for face_ind in range(images.shape[0]):
            rotated_image = rotate_image(images[face_ind, :, :], degrees[img_ind])
            cropped_image = crop_around_center(rotated_image, image_keep, image_keep)
            all_targets[img_ind] = targets[face_ind]

            rotated_faces[img_ind, :, :] = cropped_image
            img_ind += 1

    ## separate training data out ##
    n_people = 40
    n_train_people = 30

    ## randomly select the 30 people for training and 10 for test
    shuffle_people = np.random.permutation(n_people)
    train_people = shuffle_people[:n_train_people]
    test_people = shuffle_people[n_train_people:]

    train_images = np.zeros((1, image_keep, image_keep))
    train_angles = np.zeros((1))
    for tp in train_people:
        keepers = np.where(all_targets == tp)[0]
        keep_imgs = rotated_faces[np.ix_(keepers), :, :].squeeze()
        keep_angles = degrees[np.ix_(keepers)]
        train_images = np.concatenate((train_images, keep_imgs), 0)
        train_angles = np.concatenate((train_angles, keep_angles))

    train_images = np.expand_dims(train_images[1:, :, :], 1)
    train_angles = train_angles[1:]


    test_images = np.zeros((1, image_keep, image_keep))
    test_angles = np.zeros((1))
    for tp in test_people:
        keepers = np.where(all_targets == tp)[0]
        keep_imgs = rotated_faces[np.ix_(keepers), :, :].squeeze()
        keep_angles = degrees[np.ix_(keepers)]
        test_images = np.concatenate((test_images, keep_imgs), 0)
        test_angles = np.concatenate((test_angles, keep_angles))

    test_images = np.expand_dims(test_images[1:, :, :], 1)
    test_angles = test_angles[1:]

    np.savez("./rotated_faces_data.npz",
             train_images=train_images, train_angles=train_angles,
             test_images=test_images, test_angles=test_angles)

if __name__ == '__main__':
    main()
