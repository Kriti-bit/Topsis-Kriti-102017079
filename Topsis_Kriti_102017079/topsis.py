import sys
import os
import pandas as pd


def main():
    # Number of arguments
    n = len(sys.argv)
    # If number of arguments is not equal to 5
    if n != 5:
        print("ERROR: Invalid number of arguments")
        exit()

    # If file does not exist
    if not os.path.exists(sys.argv[1]):
        print("ERROR: {} does not exist".format(sys.argv[1]))
        exit()


if __name__ == "__main__":
    main()
