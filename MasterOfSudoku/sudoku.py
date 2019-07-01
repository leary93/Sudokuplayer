# this file defines the sudoku class
debug = False


class Sudoku:
    # define initialization (nxn), voor nu nog niet flexibel
    def __init__(self, n=9):
        self.grid = []
        self.rows = []
        self.cols = []
        self.squares = []
        self.order = []
        self.pairs = []
        self.triples = []
        self.quads = []

        for i in range(0, n):
            self.rows += [[]]
            self.cols += [[]]
            self.squares += [[]]

        for i in range(0, n**2):
            box = Box(i % n, i // n)
            self.grid.append(box)
            self.rows[i // n].append(box)
            self.cols[i % n].append(box)
            s = (i % 9) // 3 + ((i // 9) // 3) * 3
            self.squares[s].append(box)

        for b in self.grid:
            b.neighbours = self.GetNeighbours(b)

    def Count(self):
        count = 0
        for box in self.grid:
            if box.digit == 0:
                count += 1
        return count

    def Copy(self, sudoku, clean=False):
        # Functie om een sudoku te kopiëren naar een 2de sudoku (handig voor brute force)
        for i in range(0, len(self.grid)):
            boxfrom = sudoku.grid[i]
            boxto = self.grid[i]
            boxto.digit = boxfrom.digit

        for box in self.grid:
            if box.digit == 0:
                box.solved = False
                box.clue = False
                box.legal = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            else:
                box.solved = True
                box.legal = set()
            self.CheckLegal(box)

    def GetNeighbours(self, box):
        # List de neighbours zodat deze aan de box toegevoegd kan worden
        neighbours = set()
        for b in self.rows[box.coord[1]]:
            neighbours.add(b)
        for b in self.cols[box.coord[0]]:
            neighbours.add(b)
        for b in self.squares[box.square]:
            neighbours.add(b)
        # Remove zichzelf
        neighbours.discard(box)
        return neighbours

    def SetDigit(self, box, num, clue=False):
        # SetDigit vervult meerdere functies:
        # 1. Zet een box zijn getal
        # 2. Zet de solved status (True als hij ingevuld is, False als 0)
        # 3. Update de legal set for neighbour boxes
        box.digit = num
        if num == 0:
            box.solved = False
            # Vernieuw de legal sets
            box.legal = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            self.CheckLegal(box)
            box.clue = False
            return
        if num is not 0:
            # Onthoud de rows/cols en squares waarvan een box.legal is veranderd
            chrows = set()
            chcols = set()
            chsquares = set()
            for b in box.neighbours:
                if not b.solved:
                    update = b.Legal(num)
                    if update and not clue:
                        chsquares.add(b.square)
                        chcols.add(b.coord[0])
                        chrows.add(b.coord[1])
            box.legal = set()
            box.solved = True
            if not clue:
                self.order.append(box)
            if clue:
                box.clue = True
            # Geef de veranderde rows/cols/squares terug
            chsubs = []
            for i in chrows:
                chsubs.append(self.rows[i])
            for i in chcols:
                chsubs.append(self.cols[i])
            for i in chsquares:
                chsubs.append(self.squares[i])
            return chsubs

    def CheckLegal(self, box, num=0):
        # Checks voor de getallen in buren en haalt deze opties weg uit de legal opties
        # Deze functie is nog wat naief en moet verbeterd
        if num is 0:
            # als num is 0, check dan voor alle getallen
            vis = set()
            for b in box.neighbours:
                vis.add(b.digit)
            box.legal.difference_update(vis)
            return True
        elif num is not 0:
            # Als num niet 0, dan willen controleren of dit nummer hier "mag" staan
            # volgens het oog van de puzzelaar
            for b in box.neighbours:
                if b.digit == num:
                    return False
            return True

    def TupleElim(self, tup, count):
        # Voeg eerst de tuple toe aan de dataset als deze nieuw gevonden is
        new = 0
        if count == 2:
            if tup not in self.pairs:
                new += 1
                self.pairs.append(tup)
            else:
                return 0
        if count == 3:
            if tup not in self.triples:
                new += 1
                self.triples.append(tup)
            else:
                return 0
        if count == 4:
            if tup not in self.quads:
                new += 1
                self.quads.append(tup)
            else:
                return 0
        # Vervolgens checken we of alle boxes in 1 col, row of square zitten
        col = tup[0].coord[0]
        for i in range(1, count):
            # als de box niet in de col zit, break
            if tup[i].coord[0] != col:
                break
            # als we alle boxes hebben gecontroleerd en nog hier zitten
            # dan zitten alle boxes dus in de col
            if i == count - 1:
                # Dan kunnen we voor de rest van de boxes in de col
                # deze getallen uit box.legal halen
                for box in self.cols[col]:
                    if box not in tup:
                        # als de box niet in de tuple, dan halen we de getallen die in de tuple zitten weg
                        for num in tup[count]:
                            box.Legal(num)
                    elif box in tup:
                        # als de box in de tuple, dan halen we de getallen weg die niet in de tuple zitten
                        digits = set(box.legal)
                        digits.difference_update(tup[count])
                        for num in digits:
                            box.Legal(num)
        row = tup[0].coord[1]
        for i in range(1, count):
            # als de box niet in de row zit, break
            if tup[i].coord[1] != row:
                break
            # als we alle boxes hebben gecontroleerd en nog hier zitten
            # dan zitten alle boxes dus in de row
            if i == count - 1:
                # Dan kunnen we voor de rest van de boxes in de row
                # deze getallen uit box.legal halen
                for box in self.rows[row]:
                    if box not in tup:
                        # als de box niet in de tuple, dan halen we de getallen die in de tuple zitten weg
                        for num in tup[count]:
                            box.Legal(num)
                    elif box in tup:
                        # als de box in de tuple, dan halen we de getallen weg die niet in de tuple zitten
                        digits = set(box.legal)
                        digits.difference_update(tup[count])
                        for num in digits:
                            box.Legal(num)
        square = tup[0].square
        for i in range(1, count):
            # als de box niet in de square zit, break
            if tup[i].square != square:
                break
            # als we alle boxes hebben gecontroleerd en nog hier zitten
            # dan zitten alle boxes dus in de square
            if i == count - 1:
                # Dan kunnen we voor de rest van de boxes in de square
                # deze getallen uit box.legal halen
                for box in self.squares[square]:
                    if box not in tup:
                        # als de box niet in de tuple, dan halen we de getallen die in de tuple zitten weg
                        for num in tup[count]:
                            box.Legal(num)
                    elif box in tup:
                        # als de box in de tuple, dan halen we de getallen weg die niet in de tuple zitten
                        digits = set(box.legal)
                        digits.difference_update(tup[count])
                        for num in digits:
                            box.Legal(num)
        return new

    def NakedSingle(self):
        # Checks voor boxes met 1 legal cijfer
        count = 0
        for box in self.grid:
            if not box.solved:
                if len(box.legal) == 1:
                    digit = box.legal.copy().pop()
                    self.SetDigit(box, digit)
                    count += 1
        return count

    def NakedAll(self, count=2):
        if debug:
            print("running naked all!", count)
        new = 0
        for row in self.rows:
            new += self.NakedTuple(row, count)
        for col in self.cols:
            new += self.NakedTuple(col, count)
        for square in self.squares:
            new += self.NakedTuple(square, count)
        return new

    def NakedTuple(self, sub, count=2):
        # Zoek eerst naar tuples in de subset
        tuples = self.FindNakedTuple(sub, count)
        # Als deze gevonden zijn kunnen we deze toevoegen aan de datasets
        # En wat informatie uithalen
        new = 0
        for tup in tuples:
            new += self.TupleElim(tup, count)
        return new

    def FindNakedTuple(self, sub, count):
        # checks voor rows/cols/squares (sub), of deze een naked tuple bevat.
        # een naked tuple is een x aantal boxes met een totaal van x aantal legal cijfers.
        check = []
        for box in sub:
            if box.solved:
                continue
            # voor iedere cell, check of het aantal legal cijfers max count is.
            if len(box.legal) <= count:
                # Dan add box to check
                check.append(box)

        # Voer een check uit op de overgebleven boxes
        if len(check) < count:
            # als er minder boxes zijn dan is dit uberhaupt niet mogelijk
            return []

        if len(check) == count:
            # als er evenveel zijn dan is de check triviaal
            x = set()
            for box in check:
                x.update(box.legal)
            if len(x) == count:
                # Als de union van alle legal nummers gelijk is aan count, dan is dit een exact naked tuple
                check.append(x)
                return [check]
            # anders is dit sws geen tuple
            return []
        if len(check) > count:
            # maar als de size groter is moeten we onderzoeken of er een mogelijk naked tuple
            # (of zelfs meerdere) aanwezig is
            # Hiervoor itereren we door de check-lijst heen
            combs = GetCombinations(count, len(check))

            # Er kunnen meerdere naked tuples aanwezig zijn
            tuples = []
            for comb in combs:
                x = set()
                for i in range(0, len(comb)):
                    x.update(check[comb[i]].legal)
                if len(x) == count:
                    tup = []
                    for j in range(0, len(comb)):
                        tup.append(check[comb[j]])
                    # voeg vervolgens dit tuple toe aan de gevonden tuples
                    tup.append(x)
                    tuples.append(tup)
                if len(x) < count:
                    error = "Sudoku invalid, too few naked digits for the boxes"
                    return error
            # Return de gevonden tuples (als die niet gevonden zijn is tuples leeg
            return tuples
        # In principe zijn we alle opties langsgegaan, maar voor de zekerheid
        return []

    def HiddenAll(self, count=2):
        if debug:
            print("running hidden all!", count)
        new = 0
        for row in self.rows:
            new += self.HiddenX(row, count)
        for col in self.cols:
            new += self.HiddenX(col, count)
        for square in self.squares:
            new += self.HiddenX(square, count)
        return new

    def HiddenX(self, sub, count=2):
        # Checks voor een bepaalde row, col of square (sub), of deze een hidden single of tuple heeft (count)
        check = []
        new = 0
        for i in range(1, 10):
            # tel alle legals
            b = []
            for box in sub:
                if i in box.legal:
                    b.append(box)
                    # Als er teveel opties zijn gevonden voor i, dan hoeven we niet verder te zoeken
                    if len(b) > count:
                        break
            if len(b) == 1:
                # als dit getal maar 1 legal box heeft, dan is dit overduidelijk de box waar deze naartoe moet
                self.SetDigit(b[0], i)
                new += 1
            elif len(b) in range(1, count + 1):
                x = [i]
                x.extend(b)
                check.append(x)
                # we kunnen hier ook meteen een candidate sub-check uitvoeren,
                # als alle b's in dezelfde row/col/square liggen
                col = b[0].coord[0]
                if sub is not self.cols[col]:
                    for j in range(1, len(b)):
                        if b[j].coord[0] != col:
                            break
                        if j == len(b) - 1:
                            # Als we in t laatste el van b zitten, dan kunnen we de rest van de boxes in de col updaten
                            for box in self.cols[col]:
                                if box not in b:
                                    x = box.Legal(i)
                                    if x:
                                        new += 1
                row = b[0].coord[1]
                if sub is not self.rows[row]:
                    for j in range(1, len(b)):
                        if b[j].coord[1] != row:
                            break
                        if j == len(b) - 1:
                            # Als we in t laatste el van b zitten, dan kunnen we de rest van de boxes in de col updaten
                            for box in self.rows[row]:
                                if box not in b:
                                    x = box.Legal(i)
                                    if x:
                                        new += 1
                square = b[0].square
                if sub is not self.squares[square]:
                    for j in range(1, len(b)):
                        if b[j].square != square:
                            break
                        if j == len(b) - 1:
                            # Als we in t laatste el van b zitten, dan kunnen we de rest van de boxes in de col updaten
                            for box in self.squares[square]:
                                if box not in b:
                                    x = box.Legal(i)
                                    if x:
                                        new += 1
        # Nu we verschillende kandidaat-nummers hebben gevonden kunnen we op hidden tuples controleren
        tuples = []
        if len(check) >= count:
            # We controleren voor iedere combinatie, hoeveel verschillende boxes er zijn
            combs = GetCombinations(count, len(check))
            for comb in combs:
                tup = []
                x = set()
                for i in range(0, len(comb)):
                    boxlist = check[comb[i]]
                    x.add(boxlist[0])
                    for j in range(1, len(boxlist)):
                        box = boxlist[j]
                        if box not in tup:
                            tup.append(box)
                    if len(tup) > count:
                        break

                    # Als de grootte van het gevonden tuple kleiner is dan de count,
                    # Dan zijn er dus te weinig boxes gevonden voor de verschillende getallen
                if len(tup) < count:
                    error = "Sudoku invalid, to many hidden digits for the boxes"
                    print(error, tup, count)
                    return error
                # Als de grootte exact is echter, dan is dit een hidden tuple en voegen we deze toe aan tuples
                if len(tup) == count:
                    tup.append(x)
                    tuples.append(tup)
        # Do something with the received tuples!!!!!!!!!!!!!!!
        for tup in tuples:
            self.TupleElim(tup, count)
        return new


class Box:
    # define what a box is
    def __init__(self, col, row):
        # keeps track of the numbers that are legal in the box
        self.digit = 0
        self.legal = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        # keeps track of the row and column in which this box is located
        self.index = col + row * 9
        self.coord = [col, row]
        self.square = col // 3 + (row // 3) * 3

        # keeps track of wether the box has solved status and
        # what the neighbours of this box are (any box in the same row, col or square)
        self.solved = False
        self.clue = False
        self.neighbours = []

    # Define a function to set the digit
    def Legal(self, num):
        try:
            self.legal.remove(num)
        except KeyError:
            return False
        else:
            return True

    def __str__(self):
        x = "(" + str(self.coord[0]) + "," + str(self.coord[1]) + ")" + "-" + str(self.legal)
        return x


# A dictionary to store Combinations that have already been calculated, will help speed up the process
existingcombs = {}


def GetCombinations(count, size):
    # return 0 als de ingevoerde waarden niet kloppen
    if count > size:
        return 0
    # Check of de combinatie al is uitgerekend
    check = existingcombs.get((count, size))
    if check is not None:
        return check
    combinations = []
    if count > 1:
        # Zet de mogelijke combinaties op een recursieve manier
        # (dit mag op zich, omdat dit een diepte heeft van n=count en count niet groter wordt dan 4.
        subs = GetCombinations(count-1, size-1)
        for combination in subs:
            # Wat is het grootste element tot nu toe in de combinatie?
            x = combination[-1]
            for i in range(x + 1, size):
                # Voor iedere mogelijke nieuwe combinatie van comb+i, voeg deze toe aan combs
                y = list(combination)
                y.append(i)
                combinations.append(y)
    elif count == 1:
        for i in range(0, size):
            combinations.append([i])

    existingcombs[(count, size)] = combinations
    return combinations
