# Simpele inlezer voor sudoku's, neemt een input van 81 nummers, waarbij 0 een leeg vak betekent
# Later voeg ik verschillende opties om in te voeren toe


def readsudoku(input):
    nestedArr = []

    if len(input) is not 81:
        return 0

    for i in range(0, 9):
        arr = []
        x = i*9
        y = x + 9
        for char in input[x:y]:
            arr.append(int(char))
        nestedArr.append(arr)

    return nestedArr
