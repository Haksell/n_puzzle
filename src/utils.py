import re
import sys


def panic(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def clamp(x, mini, maxi):
    return mini if x < mini else maxi if x > maxi else x


def parse_size(s):
    if re.fullmatch(r"\d+", s):
        size = int(s)
        if size >= 2:
            return size, size
    elif fullmatch := re.fullmatch(r"(\d+)x(\d+)", s):
        height = int(fullmatch.group(1))
        width = int(fullmatch.group(2))
        if height >= 2 and width >= 2:
            return height, width
    panic(f"Invalid size: {s}")


def read_file(filename, max_file_size=50_000):
    try:
        content = open(filename).read(max_file_size)
        assert len(content) != max_file_size, f"file too big (max={max_file_size})"
    except Exception as e:
        panic(f"Failed to read puzzle '{filename}': {e}")
    return content
