import msvcrt, os
from MasterOfSudoku.visual import visual
# Kleine module om relevante key-presses te lezen

keys = {75: "left",  77: "right",  72: "up",  80: "down", 8: "del", 48: 0,
        49: 1, 50: 2, 51: 3, 52: 4, 53: 5, 54: 6, 55: 7, 56: 8, 57: 9, 27: "escape", 13: "enter"}
diffs = ["easy", "medium", "hard", "expert", "fiendish", "diabolic", "nightmare", "platinum blonde"]

menustrings = ["           Los een sudoku op            ",
               "         Vul zelf een sudoku in         ",
               "           Stop het programma           "]
diffstrings = ["                  Easy                  ",
               "                 Medium                 ",
               "                  Hard                  ",
               "                 Expert                 ",
               "                Fiendish                ",
               "                Diabolic                ",
               "                Nightmare               ",
               "             Platinum Blonde            ",
               "             Terug naar menu            "]
bar = "-------------------------------------------------------------"
footers = [" || Gebruik pijltjes om te navigeren, escape voor 't menu || ",
           " ||  1-9 om een getal in te vullen en 0 om leeg te maken  || "]
menu = ["Menu", "Solve", "Check", "Terug"]


def key():
    # Wacht tot een key word ingedrukt, vind deze en return
    while 1:
        if msvcrt.kbhit():
            a = ord(msvcrt.getch())
            if a:
                try:
                    a = keys[a]
                except:
                    a = "wrong key" + " " + a
                finally:
                    return a


def interface(mode="menu"):

    if mode == "menu":
        sel = 0
        while 1:
            os.system('cls')

            print("------------------------------------------")
            print("||   Welkom bij mijn sudoku programma   ||")
            print("|| Los een sudoku op, of maak er zelf 1 ||")
            print("||        Geniet, groeten Leroy         ||")
            print("------------------------------------------")

            for i in range(0, 3):
                if sel == i:
                    print(">", menustrings[i])
                else:
                    print(" ", menustrings[i])
            k = key()
            if k == "escape":
                return "quit"
            elif k == "up":
                sel = (sel - 1) % 3
            elif k == "down":
                sel = (sel + 1) % 3
            elif k == "enter":
                break
            else:
                print("Invalid key:", k)
        if sel == 2:
            return "quit"
        if sel == 1:
            return "insert"
        if sel == 0:
            return "select"
    if mode == "difficulty":
        sel = 0
        while 1:
            os.system('cls')

            print("------------------------------------------")
            print("||   Selecteer een moeilijkheidsgraad:  ||")
            print("------------------------------------------")
            for i in range(0, 9):
                if sel == i:
                    print(">", diffstrings[i])
                else:
                    print(" ", diffstrings[i])
            k = key()
            if k == "escape":
                return "menu"
            elif k == "up":
                sel = (sel - 1) % 9
            elif k == "down":
                sel = (sel + 1) % 9
            elif k == "enter":
                break
            else:
                print("Invalid key:", k)
        if sel == 8:
            return "menu"
        else:
            return diffs[sel]
    else:
        return "break"


def play(sudoku, header, message="", sel=(0, 0)):
    esc = False
    opt = 0
    while 1:

        os.system('cls')
        print(bar)
        print(header)
        visual(sudoku, sel)

        if not esc:
            # Als we in de sudoku navigeren
            for foot in footers:
                print(foot)
            print(message)
            print(bar)
            k = key()
            if k == "escape":
                esc = True
                continue
            elif k == "up":
                sel = (sel[0], (sel[1] - 1) % 9)
            elif k == "down":
                sel = (sel[0], (sel[1] + 1) % 9)
            elif k == "left":
                sel = ((sel[0] - 1) % 9, sel[1])
            elif k == "right":
                sel = ((sel[0] + 1) % 9, sel[1])
            elif k == "enter":
                continue
            elif k in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}:
                return [k, sel]
            else:
                print("Invalid key:", k)
        if esc:
            # Als we het menu wilden zien
            print(" ||    ", end="")
            for i in range(0, 4):
                if opt == i:
                    print("  >", menu[i], "  ", end="")
                else:
                    print("   ", menu[i], "  ", end="")
            print("    ||")
            k = key()
            if k == "left":
                opt = (opt - 1) % 4
            elif k == "right":
                opt = (opt + 1) % 4
            elif k == "enter":
                # Doe iets met de geselecteerde optie
                if opt == 0:
                    return "break"
                if opt == 1:
                    return "solve"
                if opt == 2:
                    return "check"
                if opt == 3:
                    esc = False
                    continue
            if k == "escape":
                esc = False
                continue
            else:
                print("Invalid key:", k)

