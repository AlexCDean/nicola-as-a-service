from fer import FER, exceptions
import cv2
from os import listdir
import os
from os.path import isfile, join
from collections import namedtuple
Politician = namedtuple('Politician', ['name', 'picture_name', 'emotion', 'emotion_strength'])
# Recreate the csv file as appropriate. 
DIRS = ["nicola", "keith"]
SCRIPT_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(SCRIPT_DIR, f"..{os.sep}static")

def get_files():
    files_by_politicians = {}
    for dir in DIRS:
        ABS_DIR = os.path.join(STATIC_DIR, dir)
        files_by_politicians[dir] = [f for f in listdir(ABS_DIR) if isfile(join(ABS_DIR, f))]
    return files_by_politicians

def evaluate_emotions(politician_files):
    politicians = []
    detector = FER()
    for name, list_files in politician_files.items():
        for file in list_files:
            img = cv2.imread(os.path.join(SCRIPT_DIR, name, file))
            try:
                emotion, score = detector.top_emotion(img)
            except exceptions.InvalidImage:
                print(f"{file} is not valid")
            politicians.append(
                Politician(name, file, emotion, score)
            )
    return politicians

if __name__ == "__main__":
    files = get_files()
    politicians = evaluate_emotions(files)
    