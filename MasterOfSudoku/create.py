from MasterOfSudoku.sudoku import Sudoku, Box
from MasterOfSudoku.shuffle import randarray
import MasterOfSudoku.solve as solve
import random
from MasterOfSudoku.visual import visual


def pattern():
    # Maak een lege sudoku aan
    new = Sudoku()

    # En vul de lege squares op de diagonaal willekeurig
    for i in range(0, 3):
        square = new.squares[i*4]
        arr = randarray()

        for j in range(0, len(square)):
            new.SetDigit(square[j], arr[j], True)

    # Nu hebben we een startpunt om te zoeken naar een pattern, via een variant van de bruteforce
    def step(sudoku):
        # Probeer zover te solven als we kunnen met naked singles
        try:
            solve.singles(sudoku)
        except Exception as e:
            print("Couldn't solve while creating pattern", e)
            # Sudoku is dus niet legaal
            return None

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
            return sudoku

        # Het kan ook zijn dat we een pivot vinden met len(pivot.legal) = 0.
        # In dat geval is de huidige sudoku niet legaal en returnen we niks
        if len(pivot.legal) == 0:
            return None

        # Itereer door de verschillende opties willekeurig
        # (omdat we maar 1 patroon kiezen, willen we dat deze willekeurig is)
        shuf = random.sample(pivot.legal, len(pivot.legal))
        for num in shuf:
            # Maak eerst een kopie aan
            copy = Sudoku()
            copy.Copy(sudoku)
            copy.SetDigit(copy.grid[pivot.index], num, True)
            # Roep vervolgens step weer aan (recursief)
            copy = step(copy)

            # Nu is copy of empty (als er geen legal optie uit komt) en zoeken we verder
            if copy is None:
                continue
            # Of hij is solved (dan zijn we klaar)
            else:
                return copy
        # Als we de forloop uitkomen, dan is er nog geen copy gereturned.
        # Return daarom None, zodat verder gezocht kan worden
        return None

    new = step(new)

    return new


def puzzle(patt, diff="easy"):
    # Maak van een pattern, een sudoku met passende clues, afhankelijk van de moeilijkheidsgraad
    removed = 0

    # Bepaal een symmetrievariant willekeurig en vul een array hiervoor
    symm = random.randint(0, 4)
    sets = []

    x = 5
    y = 5
    if symm in {0, 3}:
        x = 9
    if symm is 2:
        y = 9

    for i in range(0, x):
        for j in range(0, y):
            buddies = set()
            buddies.add((i, j))
            if symm < 2:
                # Als symm 0 of 1, dan hor symm
                buddies.add((i, 8 - j))
            if symm in range(1, 3):
                # Als symm 1 of 2, dan vert symm
                buddies.add((8 - i, j))
            if symm > 2 or symm == 1:
                # Als symm 3 of 4, dan 180² symm, als 1 dan ook
                buddies.add((8 - i, 8 - j))
            if symm == 4:
                # Als symm 4, dan ook 90² symm
                buddies.add((8 - j, i))
                buddies.add((j, 8 - i))
            if i == 5 or j == 5:
                if buddies in sets:
                    continue
            sets.append(buddies)

    def remove(check, sudoku):
        copy = Sudoku()
        copy.Copy(sudoku, True)

        for coord in check:
            box = copy.grid[coord[0] + coord[1] * 9]
            copy.SetDigit(box, 0, True)

        return copy

    def easy(check, sudoku):
        # Remove's digits die te vinden zijn met hidden single's
        copy = remove(check, sudoku)
        new = Sudoku()
        new.Copy(copy)
        viable = solve.hidsingles(new)

        if viable:
            return copy
        return viable

    def medium(check, sudoku):
        # Remove's digits die te vinden zijn met alle singles
        copy = remove(check, sudoku)
        new = Sudoku()
        new.Copy(copy)
        viable = solve.singles(new)

        if viable:
            return copy
        return viable

    def hard(check, sudoku):
        # Remove's digits die te vinden zijn met naked pair's
        copy = remove(check, sudoku)
        new = Sudoku()
        new.Copy(copy)
        viable = solve.nakedpairs(new)

        if viable:
            return copy
        return viable

    def expert(check, sudoku):
        # Remove's digits die te vinden zijn met alle pairs en candidate lines
        copy = remove(check, sudoku)
        new = Sudoku()
        new.Copy(copy)
        viable = solve.pairs(new)

        if viable:
            return copy
        return viable

    def fiendish(check, sudoku):
        # Remove's digits die te vinden zijn met triples
        copy = remove(check, sudoku)
        new = Sudoku()
        new.Copy(copy)
        viable = solve.triples(new)

        if viable:
            return copy
        return viable

    def diabolic(check, sudoku):
        # Remove's digits die te vinden zijn met quads en brute-force (depth max 1)
        copy = remove(check, sudoku)
        new = Sudoku()
        new.Copy(copy)
        viable = solve.bruteforce(new, 1)

        if viable:
            return copy
        return viable

    def nightmare(check, sudoku):
        # Remove's digits die te vinden zijn met brute-force (depth mag wat dieper)
        # Dient uiteindelijk uitgebreid met andere solving-techniques
        copy = remove(check, sudoku)
        new = Sudoku()
        new.Copy(copy)
        viable = solve.bruteforce(new, 5)

        if viable:
            return copy
        return viable

    # Stel de goede functie in aan de hand van opgegeven moeilijkheid
    f = easy
    modifier = 0
    if diff == "medium":
        f = medium
        modifier = 1
    elif diff == "hard":
        f = hard
        modifier = 2
    elif diff == "expert":
        f = expert
        modifier = 3
    elif diff == "fiendish":
        f = fiendish
        modifier = 4
    elif diff == "diabolic":
        f = diabolic
        modifier = 5
    elif diff == "nightmare":
        f = nightmare
        modifier = 6

    def initial(sudoku):
        rem = 0
        # Remove de eerste ~20-30 digits
        initcheck = random.sample(sets, len(sets))

        for check in initcheck:
            copy = easy(check, sudoku)
            if copy:
                sets.remove(check)
                sudoku.Copy(copy)
                rem += len(check)

            if rem >= 10 + modifier:
                break

        return rem

    removed += initial(patt)

    # Probeer vervolgens een sudoku te vinden met sub-30 clues.
    # Als niet, backtrack dan
    z = len(sets)
    sets = random.sample(sets, z)
    stack = [[patt, removed, -1]]
    index = 0
    maxrem = removed
    maxsudo = patt
    print(removed, patt.Count(), symm)

    while True:
        prev = stack[-1]
        copy = f(sets[index], prev[0])

        if not copy:
            # Als deze kopie niet legaal is, dan voegen we hem niet toe, en verhogen we index met 1
            index += 1
            # Echter, als index nu >= z, dan willen we niet verder gaan
            if index >= z:
                # Controleer de removed count van vorige versie
                if prev[1] >= 41 + modifier * 2:
                    # Okey, prima, break
                    print("breaking cuz >51?", prev[0].Count())
                    maxrem = prev[1]
                    maxsudo = Sudoku()
                    maxsudo.Copy(prev[0], True)
                    break
                elif prev[1] > maxrem:
                    maxrem = prev[1]
                    maxsudo.Copy(prev[0], True)
                # En sws willen we nu deze van de stack halen
                s = stack.pop(-1)
                if len(stack) == 0:
                    print("Breaking cuz stack's empty", symm)
                    break
                index = s[2] + 1
                # print("resetting index", index)
            continue
        if copy:
            # Als de kopie wel legaal is
            new = [copy, prev[1] + len(sets[index]), index]
            index += 1
            # Echter, als index nu >= z, dan willen we niet verder gaan
            if index >= z:
                # Controleer de removed count van vorige versie
                if new[1] >= 41 + modifier * 2:
                    # Okey, prima, break
                    print("breaking cuz >51?", new[0].Count())
                    maxrem = new[1]
                    maxsudo = Sudoku()
                    maxsudo.Copy(prev[0], True)
                    break
                elif new[1] > maxrem:
                    maxrem = new[1]
                    maxsudo.Copy(new[0], True)
                # En sws willen we nu deze van de stack halen
                s = stack.pop(-1)
                if len(stack) == 0:
                    print("Breaking cuz stack's empty", symm)
                    break
                index = s[2] + 1
                # print("resetting index", index)
            else:
                stack.append(new)
            continue
        break

    patt = maxsudo
    return patt
