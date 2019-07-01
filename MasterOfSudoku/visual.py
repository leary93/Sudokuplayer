# Simpele module om de sudoku te visualiseren


def thickline():
    # De dikke lijn tussen de squares
    for i in range(0, 19):
        if i % 6 is 0:
            print("----", end="")
        else:
            print("---", end="")
    print("")


def thinline():
    # De dunne lijn tussen de rest van de boxes
    for i in range(0, 19):
        if i % 6 is 0:
            print(" || ", end="")
        else:
            print(" - ", end="")
    print("")


def verline(row, sel=None):
    # De verticale lijn waarop getallen worden weergegeven
    for i in range(0, 19):
        if i % 6 is 0:
            print(" || ", end="")
        elif i % 2 is 0:
            print(" | ", end="")
        elif i % 2 is 1:
            digit = row[i // 2].digit
            if digit == 0:
                digit = " "
            if sel is not None:
                if sel == i // 2:
                    print(">", digit, "<", sep="", end="")
                    continue
            print("", digit, "", end="")

    print("")


def visual(sudoku, sel=(0, 0)):
    # Loop door de rijen heen en roep de correcte lijn aan
    for i in range(0, 19):
        if i % 6 is 0:
            thickline()
        elif i % 2 is 0:
            thinline()
        elif i % 2 is 1:
            if sel[1] == i // 2:
                verline(sudoku.rows[i // 2], sel[0])
            else:
                verline(sudoku.rows[i // 2])

    return
