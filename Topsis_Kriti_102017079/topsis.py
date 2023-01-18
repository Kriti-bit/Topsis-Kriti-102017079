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

    data = pd.read_csv(sys.argv[1])

    # Error If number of columns is less than 3
    if len(data.columns) < 3:
        print("ERROR: Number of columns is less than 3")
        exit()

    # 2nd column of input file has non numeric values then encode it
    for i in range(1, len(data.columns)):
        pd.to_numeric(data.iloc[:, i], errors="coerce")
        data.iloc[:, i].fillna((data.iloc[:, i].mode()), inplace=True)

    # Read data from csv file
    topsis(data, sys.argv[4], weights, sys.argv[3].split(","))


def topsis(data, result_file, weights, impact):
    new_data = normalisation(data)
    new_data = weighted_sum(new_data, weights)
    best_solution = ideal_best_solution(new_data, impact)
    worst_solution = ideal_worst_solution(new_data, impact)
    euclidean_distances = calc_euclidean_distance(
        new_data, best_solution, worst_solution)
    new_data["Score"] = euclidean_distances
    new_data["Rank"] = new_data["Score"].rank(method="max", ascending=False)
    new_data = new_data.astype({"Rank": int})
    new_data.to_csv(result_file, index=False)


def calc_euclidean_distance(data, best_solution, worst_solution):
    # Euclidean distance
    euclidean_distances = []
    for i in range(len(data)):
        pos_euclidean_distance = 0
        neg_euclidean_distance = 0
        for j in data.columns:
            pos_euclidean_distance += (data[j][i] - best_solution[j][i])**2
            neg_euclidean_distance += (data[j][i] - worst_solution[j][i])**2
        pos_euclidean_distance, neg_euclidean_distance = pos_euclidean_distance**0.5, neg_euclidean_distance**0.5
        euclidean_distance = (neg_euclidean_distance /
                              (pos_euclidean_distance + neg_euclidean_distance))
        euclidean_distances.append(euclidean_distance)

    return euclidean_distances


def ideal_best_solution(data, impact):
    # Ideal best solution
    ideal_solution_data = data.copy()
    for i in data.columns:
        if impact[i] == "+":
            ideal_solution_data[i] = max(data[i])
        else:
            ideal_solution_data[i] = min(data[i])

    return ideal_solution_data


def ideal_worst_solution(data, impact):
    # Ideal worst solution
    ideal_solution_data = data.copy()
    for i in data.columns:
        if impact[i] == "+":
            ideal_solution_data[i] = min(data[i])
        else:
            ideal_solution_data[i] = max(data[i])

    return ideal_solution_data


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
