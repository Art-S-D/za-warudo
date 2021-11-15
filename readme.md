# Timing attack

This project tries to do a timing attack to get the admin password on a local server.

## How it works

The server has an endpoint at /admin/login that sends back 200 if the password passed to it is the correct admin password and 401 otherwise.

Passing the correct password would be _theoratically_ take more time to the server to process, since python string comparison stops at soon as it finds different characters in the two strings.
If the server is slow enough, there should be a few milliseconds of difference.

Simply compare strings with the hmac.compare_digest function to protect against this sort of attack.

You can read [rapport.pdf](https://github.com/Art-S-D/za-warudo/blob/master/rapport.pdf) for more infos.

## Run the project:

```bash
python src/server.py
python src/timing_attack.py # on another terminal
```

If there it's not reliable enough, you can try to slow down the server.

```bash
cpulimit -f -c 1 -l 1 -- python src/server.py
```
