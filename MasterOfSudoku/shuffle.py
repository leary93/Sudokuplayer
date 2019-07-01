from random import randint as R


numbers = {1,2,3,4,5,6,7,8,9}


def randarray():
    array = []
    for i in numbers:
        array.insert(R(0, len(array)), i)

    return array
