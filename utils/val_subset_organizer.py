import argparse
import os

from tqdm import tqdm

if __name__ == "__main__":
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Organize the validation subset")
    parser.add_argument("--val_dir", type=str, help="Path to the validation directory")
    parser.add_argument("--labels_file", type=str, help="Path to the labels file")
    parser.add_argument("--classes_file", type=str, help="Path to the classes file")

    args = parser.parse_args()

    # Read the labels file
    with open(args.labels_file, "r") as f:
        labels = f.readlines()

    the_set = set()
    for label in labels:
        the_set.add(int(label.strip().split(" ")[1]))
    print(the_set)
    print(len(the_set))

    # Read and prepare json for class names
    with open(args.classes_file, "r") as f:
        class_names = f.readlines()

    # Remove new line at the end of each line and only keep every third line
    class_names = [name.strip() for name in class_names][0::3]

    # Extract actual class name
    class_names = [
        "n" + name[name.find("'id': '") + 7 : name.find("-n'")] for name in class_names
    ]

    for i in tqdm(range(len(labels))):
        # Get full image name, label, and class name
        image_name = "ILSVRC2012_val_" + str(i + 1).zfill(8) + ".JPEG"
        label = int(labels[i].strip().split(" ")[1])

        # Check if class directory already exists; create otherwise
        class_dir = args.val_dir + "/" + class_names[label]
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)

        # Move the image to the corresponding class directory
        os.rename(
            args.val_dir + "/" + image_name,
            class_dir + "/" + image_name,
        )
