# I totally scooped this up from someone, but I can't
# remember where... sorry... I wasn't thinking at the time

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode(num, alphabet=BASE62):
    """
    Encode a positive number in Base62

    This function must return a str because alphabet contains non-int chars

    :param num: The integer to encode
    :type: int

    :param alphabet: The alphanumeric string used for encoding
    :type alphabet: str

    :return str
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def decode(string, alphabet=BASE62):
    """
    Decode a Base X encoded string into the number

    string must be a str because alphabet includes non int characters

    :param string: The encoded string
    :type string: str

    :param alphabet: The alphanumeric string used for encoding
    :type alphabet: str

    :return int
    """
    base = len(alphabet)
    str_len = len(string)
    num = 0

    for idx, char in enumerate(string):
        power = (str_len - (idx + 1))
        num += alphabet.index(char) * (base ** power)

    return num
