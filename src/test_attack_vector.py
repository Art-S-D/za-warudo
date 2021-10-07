import pickle
import sys
import time
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

from server import ADMIN_PASSWORD
from timing_attack import send_request

WRONG_PASSWORD = "jtyikjoyipodgdfi"


def test_attack_vector(iterations=100_000):
    correct_password_time = 0
    wrong_password_time = 0

    correct_times = []
    wrong_times = []

    with tqdm(range(iterations)) as pbar:
        for i in pbar:
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
    rounded = np.round(times, decimals=5)

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
    if "run" in sys.argv:
        c, w = test_attack_vector()
        with open("correct.data", "wb") as f:
            pickle.dump(c, f)
        with open("wrong.data", "wb") as f:
            pickle.dump(w, f)
    elif "plot" in sys.argv:
        c = []
        w = []
        with open("correct.data", "rb") as f:
            c = pickle.load(f)
        with open("wrong.data", "rb") as f:
            w = pickle.load(f)
        plot(c, w)
    else:
        print("need run or plot in program args")
