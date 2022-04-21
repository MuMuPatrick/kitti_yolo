# kitti_train_val.py
import glob
path = 'kitti_data/'
def generate_train_and_val(image_path, txt_file):
    with open(txt_file, 'w') as tf:
        for jpg_file in glob.glob(image_path + '*.png'):
            tf.write(jpg_file + '\n')
#generate_train_and_val(path + 'train_images/', path + 'train.txt') 
generate_train_and_val(path + 'val_images/', path + 'valid.txt') 
