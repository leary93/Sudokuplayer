from MasterOfSudoku.sudoku import Sudoku, Box
from MasterOfSudoku.visual import visual

# In deze module belopen we algoritmen die de verschillende technieken gebruiken.
debug = False


def hidsingles(sudoku):
    # Deze functie beloopt alleen hidden singles
    c = 1
    fullsolve = False
    while c > 0:
        cur = len(sudoku.order)

        x = sudoku.HiddenAll(1)

        c = len(sudoku.order) - cur
        c += x

        cont = False
        for box in sudoku.grid:
            if not box.solved:
                cont = True
        if not cont:
            fullsolve = True
            break

    return fullsolve


def singles(sudoku):
    # Deze functie beloopt alleen singles, genoeg om meeste sudoku's up to hard op te lossen
    c = 1
    fullsolve = False

    while c > 0:
        cur = len(sudoku.order)

        x = sudoku.NakedSingle()
        x += sudoku.HiddenAll(1)

        c = len(sudoku.order) - cur
        c += x

        cont = False
        for box in sudoku.grid:
            if not box.solved:
                cont = True
        if not cont:
            fullsolve = True

            break

    return fullsolve


def pairs(sudoku):
    # Deze functie beloopt singles en pairs, genoeg om meeste sudoku's up to tricky op te lossen.
    c = 1
    fullsolve = False

    while c > 0:
        cur = len(sudoku.order)
        while True:

            x = sudoku.NakedSingle()
            x += sudoku.HiddenAll(1)
            if x is 0:
                break

        x = sudoku.HiddenAll(2)
        c = len(sudoku.order) - cur
        c += x

        c += sudoku.NakedAll(2)

        cont = False
        for box in sudoku.grid:
            if not box.solved:
                cont = True
        if not cont:
            fullsolve = True

            break

    return fullsolve


def nakedpairs(sudoku):
    # Deze functie beloopt singles en pairs, genoeg om meeste sudoku's up to tricky op te lossen.
    c = 1
    fullsolve = False

    while c > 0:
        cur = len(sudoku.order)
        while True:

            x = sudoku.NakedSingle()
            x += sudoku.HiddenAll(1)
            if x is 0:
                break

        c = len(sudoku.order) - cur
        c += sudoku.NakedAll(2)

        cont = False
        for box in sudoku.grid:
            if not box.solved:
                cont = True
        if not cont:
            fullsolve = True

            break

    return fullsolve


def triples(sudoku):
    # Deze functie beloopt alle naked en hidden tuples, alswel candidate lines en multiple lines. Genoeg om bijna alle
    # fiendish sudoku's op te lossen
    c = 1
    fullsolve = False

    while c > 0:
        cur = len(sudoku.order)
        while True:

            x = sudoku.NakedSingle()
            x += sudoku.HiddenAll(1)
            if x is 0:
                break

        x = sudoku.HiddenAll()
        c = len(sudoku.order) - cur
        c += x

        c += sudoku.NakedAll()

        if c is 0:
            c = sudoku.NakedAll(3)
            c += sudoku.HiddenAll(3)

        cont = False
        for box in sudoku.grid:
            if not box.solved:
                cont = True
        if not cont:
            fullsolve = True

            break

    return fullsolve


def fulltuples(sudoku):
    # Deze functie beloopt alle naked en hidden tuples, alswel candidate lines en multiple lines. Genoeg om bijna alle
    # fiendish sudoku's op te lossen
    c = 1
    fullsolve = False

    while c > 0:
        cur = len(sudoku.order)
        while True:

            x = sudoku.NakedSingle()
            x += sudoku.HiddenAll(1)
            if x is 0:
                break

        x = sudoku.HiddenAll()
        c = len(sudoku.order) - cur
        c += x

        c += sudoku.NakedAll()

        if c is 0:
            c = sudoku.NakedAll(3)
            c += sudoku.HiddenAll(3)
        if c is 0:
            c = sudoku.NakedAll(4)
            c += sudoku.HiddenAll(4)
        cont = False
        for box in sudoku.grid:
            if not box.solved:
                cont = True
        if not cont:
            fullsolve = True

            break

    return fullsolve


def bruteforce(sudoku, max=81, f=fulltuples, depth=0):
    if debug:
        # visual(sudoku)
        print("bruteforce launch with", depth)
    # Deze functie lost de sudoku gegarandeert op, al dan niet met brute-force, en geeft alle oplossingen terug.
    brutesolved = []

    # Probeer zover te solven als we kunnen met de aangegeven techniek
    f(sudoku)

    # Selecteer vervolgens een box met zo min mogelijk legal opties, dit wordt onze pivot
    leg = 10
    pivot = None

    for box in sudoku.grid:
        if box.digit > 0:
            # Skip boxes die al een nummer hebben
            continue

        if len(box.legal) >= leg:
            # Skip boxes met meer legal opties dan die eerder gevonden
            continue

        leg = len(box.legal)
        pivot = box
        if leg == 2:
            break

    # Note, het kan zijn dat we geen Pivot hebben gevonden, in dit geval hadden alle boxes een getal
    # en kunnen we de huidige oplossing teruggeven
    if pivot is None:
        return [sudoku]

    # Het kan ook zijn dat we een pivot vinden met len(pivot.legal) = 0.
    # In dat geval is de huidige sudoku niet legaal en returnen we een lege array
    # Tevens geven we een lege array terug als de maximale diepte is bereikt
    if len(pivot.legal) == 0 or depth >= max:
        return []

    # Als we vervolgens een pivot hebben gevonden, maken we voor iedere optie een nieuwe sudoku aan
    brutesudokus = []
    for num in pivot.legal:
        copy = Sudoku()
        copy.Copy(sudoku)
        copy.SetDigit(copy.grid[pivot.index], num, True)
        brutesudokus.append(copy)

    # Vervolgens hebben we een array aan copies (die ieder een ander nummer voor de pivot hebben
    # Hier kunnen we bruteforce weer voor aanroepen (recursief dus)

    for sudo in brutesudokus:
        try:
            check = bruteforce(sudo, max, f, depth + 1)
            if check is False:
                return False
            brutesolved.extend(check)
        except Exception as e:
            continue

    # Check eerst hoeveel oplossingen er zijn:
    sol = len(brutesolved)
    if sol > 2:
        # Als we nu al meerdere oplossingen hebben gevonden dan is dit een probleem
        if debug:
            print("Sudoku has multiple solutions")
        return False
    if depth == 0:
        # Als de depth 0 is, dan is dit dus de bovenste laag.
        if sol == 1:
            # En als er dan een oplossing gevonden is, dan is dit een enkele
            if debug:
                print("Sudoku has a single solution")
            sudoku.Copy(brutesolved[0])
            return True
        if sol == 0:
            # Anders hebben we er geen gevonden!
            if debug:
                print("Sudoku has no solutions")
            return False

    return brutesolved
