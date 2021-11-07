from fer import FER
import cv2
from os import listdir, sep
from os.path import isfile, join
from main import Politician
# Recreate the csv file as appropriate. 
DIRS = ["nicola", "keith"]

def get_files():
    files_by_politicians = {}
    for dir in DIRS:
        static_path = ".." + sep + "static" + sep + dir
        files_by_politicians[dir] = [f for f in listdir(dir) if isfile(join(dir, f))]

def evaluate_emotions():
    politicians = []


if __name__ == "__main__":
    files = get_files()
    