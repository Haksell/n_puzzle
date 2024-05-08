import sys


def panic(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def clamp(x, mini, maxi):
    return mini if x < mini else maxi if x > maxi else x
