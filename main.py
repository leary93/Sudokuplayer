import MasterOfSudoku.readsudoku as read
from MasterOfSudoku.sudoku import Sudoku
import MasterOfSudoku.solve as solve
import cProfile as CP
import MasterOfSudoku.create as create
import MasterOfSudoku.interface as interface
from MasterOfSudoku.visual import visual
import MasterOfSudoku.shuffle as shuffle

diffs = ["easy", "medium", "hard", "expert", "fiendish", "diabolic", "nightmare", "platinum blonde"]
menumodes = {"menu", "select", "difficulty"}
headers = [" ||                                                       || ",
           " ||                     Los de sudoku op                  || ",
           " ||                   Maak je eigen sudoku                || "]
messges = [" ||                 !!  dat is een clue  !!               || ",
           " ||                   box is leeggemaakt                  || ",
           " ||                Alles lijkt goed te gaan               || ",
           " ||                 Er is iets fout gegaan                || "]

# Platinum blonde is bekend als een van de moeilijkste sudoku's bekend en zou een goede maatstaf moeten zijn voor de
# kracht van het brute-force algoritme
platinumBlonde = "000000012000000003002300400001800005060070800000009000008500000900040500470006000"


# In main regelen we dat alles gestart wordt.
def program(mode, sudoku):

    while mode in menumodes:
        # Menu control sectie
        command = interface.interface(mode)
        if command == "quit":
            mode = "exit"
            break
        if command == "select":
            mode = "difficulty"
        if command == "insert":
            mode = "create"
            break
        if command == "menu":
            mode = "menu"
        if command in diffs:
            mode = "play"
            diff = command
            print("Loading ...")
            if diff == "platinum blonde":
                # Lees de platinum blonde uit
                array = read.readsudoku(platinumBlonde)
                sudoku = Sudoku()

                for i in range(0, 9):
                    if array is 0:
                        x = shuffle.randarray()
                    else:
                        x = array[i]
                    for j in range(0, 9):
                        box = sudoku.rows[i][j]
                        sudoku.SetDigit(box, x[j], True)
            else:
                pattern = create.pattern()
                sudoku = create.puzzle(pattern, diff)
            break
        if command == "break":
            break
    while mode == "play":
        # Play control sectie
        solving = True
        message = ""
        sel = (0, 0)
        while solving:
            command = interface.play(sudoku, headers[1], message, sel)

            if len(command) == 2:
                sel = command[1]
                box = sudoku.grid[sel[0] + sel[1] * 9]

                if box.clue:
                    message = messges[0]
                elif command[0] == 0:
                    sudoku.SetDigit(box, 0)
                    message = messges[1]
                elif sudoku.CheckLegal(box, command[0]):
                    message = ""
                    sudoku.SetDigit(box, command[0])
                else:
                    message = " ||               !!  " + str(command[0]) + "mag daar niet  !!                 || "
                continue
            message = ""
            if command == "break":
                mode = "menu"
                solving = False
            if command == "solve":
                # Solve de sudoku en print deze
                print("Solving")
                solve.bruteforce(sudoku)
                continue
            if command == "check":
                # Check of je op de goede weg bent
                print("Checking")
                copy = Sudoku()
                copy.Copy(sudoku)
                good = solve.bruteforce(copy)
                if good:
                    message = messges[2]
                else:
                    message = messges[3]

    while mode == "create":

        creating = True
        sudoku = Sudoku()
        message = ""
        sel = (0, 0)
        while creating:
            command = interface.play(sudoku, headers[2], message, sel)
            if len(command) == 2:
                sel = command[1]
                box = sudoku.grid[sel[0] + sel[1] * 9]

                if box.clue:
                    message = messges[0]
                elif command[0] == 0:
                    sudoku.SetDigit(box, 0)
                    message = messges[1]
                elif sudoku.CheckLegal(box, command[0]):
                    message = ""
                    sudoku.SetDigit(box, command[0])
                else:
                    message = " ||               !!  " + str(command[0]) + "mag daar niet  !!                 || "
                continue
            message = ""
            if command == "break":
                mode = "menu"
                creating = False
            if command == "solve":
                # Kopiëer deze sudoku en probeer hem zelf op te lossen
                copy = Sudoku()
                copy.Copy(sudoku)
                mode = program("play", copy)
                return mode
            if command == "check":
                # Controleer of de sudoku legaal is
                print("checking")
                copy = Sudoku()
                copy.Copy(sudoku)
                good = solve.bruteforce(copy)
                if good:
                    message = messges[2]
                else:
                    message = messges[3]
                continue
    return mode


runmode = "menu"
runsudoku = Sudoku()
while runmode is not "exit":
    runmode = program(runmode, runsudoku)
    if runmode == "exit":
        break

print("Exiting")






