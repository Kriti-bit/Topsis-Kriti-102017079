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

    # Error if file is not csv
    if not sys.argv[1].endswith(".csv"):
        print("ERROR: {} is not a csv file".format(sys.argv[1]))
        exit()

    # Error if file has no data
    if pd.read_csv(sys.argv[1]).empty:
        print("ERROR: File has no data")
        exit()

    # Error if weights are not given
    if sys.argv[2] == "":
        print("ERROR: Weights not given")
        exit()

    # Error if weights are not equal to number of columns
    if len(sys.argv[2].split(",")) != len(pd.read_csv(sys.argv[1]).columns):
        print("ERROR: Number of weights not equal to number of columns")
        exit()

    # Error if weights are not numbers
    try:
        weights = [float(i) for i in sys.argv[2].split(",")]
    except ValueError:
        print("ERROR: Weights are not numbers")
        exit()

    # Error if impacts are not given
    if sys.argv[3] == "":
        print("ERROR: Impacts not given")
        exit()

    # Error if impacts are not equal to number of columns
    if len(sys.argv[3].split(",")) != len(pd.read_csv(sys.argv[1]).columns):
        print("ERROR: Number of impacts not equal to number of columns")
        exit()

    # Error if impacts are not + or -
    if not all(i in ["+", "-"] for i in sys.argv[3].split(",")):
        print("ERROR: Impacts are not + or -")
        exit()

    # Error if Result file is not given
    if sys.argv[4] == "":
        print("ERROR: Result file not given")
        exit()

    # Error if result file is not csv
    if not sys.argv[4].endswith(".csv"):
        print("ERROR: {} is not a csv file".format(sys.argv[4]))
        exit()

    # Read data from csv file
    data = pd.read_csv(sys.argv[1])


def normalisation(data):
    # Normalisation
    normalised_data = data.copy()
    for i in data.columns:
        column_sum_of_squares = 0

        for j in data[i]:
            column_sum_of_squares += j*j

        column_sum_of_squares = column_sum_of_squares**0.5

        for k in range(len(data[i])):
            normalised_data[i][k] = data[i][k]/column_sum_of_squares

    return normalised_data


def weighted_sum(normalised_data, weights):
    # Weighted sum
    weighted_sum_data = normalised_data.copy()
    for i in normalised_data.columns:
        for j in range(len(normalised_data[i])):
            weighted_sum_data[i][j] = normalised_data[i][j]*weights[j]

    return weighted_sum_data


if __name__ == "__main__":
    main()
