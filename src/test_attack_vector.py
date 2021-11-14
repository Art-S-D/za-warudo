import pickle
import sys
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import argparse

from server import ADMIN_PASSWORD
from timing_attack import send_request

"""
I was unsure at first if a timing attack would be possible so i tried
requesting the back with the full password and a wrong password to get
the maximum time difference possible
"""

WRONG_PASSWORD = "jtyikjoyipodgdfi"


def test_attack_vector(iterations=100_000):
    correct_password_time = 0
    wrong_password_time = 0

    correct_times = []
    wrong_times = []

    for i in tqdm(range(iterations)):
        _, t = send_request(ADMIN_PASSWORD)
        correct_password_time += t
        correct_times.append(t)
        _, t = send_request(WRONG_PASSWORD)
        wrong_times.append(t)
        wrong_password_time += t
    print("Correct password verification time: ",
          correct_password_time/iterations)
    print("Wrong password verification time: ", wrong_password_time/iterations)

    return correct_times, wrong_times


def plot_times(times, **kwargs):
    rounded = np.round(times, decimals=6)

    unique, counts = np.unique(
        rounded, return_counts=True)

    for i in range(len(counts)):
        if counts[i] < 50:
            np.delete(unique, i)
            np.delete(counts, i)

    plt.plot(unique, counts, **kwargs)


def plot(correct, wrong):
    print("correct median:{} average:{}".format(
        np.median(correct), np.average(correct)))
    print("wrong median:{} average:{}".format(
        np.median(wrong), np.average(wrong)))

    plot_times(correct, color="blue", linewidth=0.5)
    plot_times(wrong, color="red", linewidth=0.5)

    plt.savefig('test_attack.png')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A test on timing attacks.')
    parser.add_argument(
        "-c", "--command",
        help="either run to start sending requests or plot to plot the obtained results",
        default="run")
    parser.add_argument(
        "-r", "--requests", help="the number of requests to send",
        default=100_000, type=int)
    args = parser.parse_args()

    if args.command == "run":
        c, w = test_attack_vector(args.requests)
        with open("correct.data", "wb") as f:
            pickle.dump(c, f)
        with open("wrong.data", "wb") as f:
            pickle.dump(w, f)
    elif args.command == "plot":
        c = []
        w = []
        with open("correct.data", "rb") as f:
            c = pickle.load(f)
        with open("wrong.data", "rb") as f:
            w = pickle.load(f)
        plot(c, w)
    else:
        print("need a command")
