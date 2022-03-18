#!/usr/bin/env python3

import os
import glob
import argparse
import shutil

TRAIN_PCT=0.80

TRAIN_NAME='train'
TEST_NAME='test'

train_counter = 0
test_counter = 0

def test_train_split(input_path: str):
    global train_counter
    global test_counter

    train_path="{}/{}".format(input_path, TRAIN_NAME)
    test_path="{}/{}".format(input_path, TEST_NAME)

    input_glob=input_path + '/*.png'

    globbed = glob.glob(input_glob)

    num_files = len(globbed)

    train_waterline = TRAIN_PCT * num_files

    if not globbed:
        raise(ValueError(f"Empty folder, there are no .png files in {input_path}."))

    for idx, file in enumerate(glob.glob(input_path + '/*.png')):
        print(file)
        file_name = file.split('/')[-1]
        item_name = file_name.split('.')[0]
        print("Image/Anno Pair Name: {}".format(file.split('.')[0]))
        if idx < train_waterline:
            shutil.copy2("{}/{}.png".format(input_path, item_name), "{}/{}.png".format(train_path, item_name))
            shutil.copy2("{}/{}.txt".format(input_path, item_name), "{}/{}.txt".format(train_path, item_name))
            train_counter += 1
        else:
            shutil.copy2("{}/{}.png".format(input_path, item_name), "{}/{}.png".format(test_path, item_name))
            shutil.copy2("{}/{}.txt".format(input_path, item_name), "{}/{}.txt".format(test_path, item_name))
            test_counter += 1
    print("Train Count {}, Test Count {}".format(train_counter, test_counter))

def parser() -> None:
    parser = argparse.ArgumentParser(description="Test train split for Face Mask Detection dataset (darknet style).")
    parser.add_argument("--input", type=str, default="", help="The path with the iamges and annotations to split. Files/annotations must have same name.")
    return parser.parse_args()

def check_arguments_errors(args : argparse.Namespace) -> None:
    if not os.path.exists(args.input):
        raise(ValueError("Invalid input folder path: {}".format(os.path.abspath(args.input))))

def main() -> None:
    args = parser()
    check_arguments_errors(args)   
    test_train_split(args.input)

if __name__ == "__main__":
    main()