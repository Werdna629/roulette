from enum import Enum
import random

class Color(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2

class Parity(Enum):
    EVEN = 0
    ODD = 1

class Zone(Enum):
    FIRST12 = 0
    SECOND12 = 1
    THIRD12 = 2
    FIRST18 = 3
    SECOND18 = 4
    FIRSTCOL = 5
    SECONDCOL = 6
    THIRDCOL = 7

class Space:
    def __init__(self, number: int):
        self.number = number
        if self.number in [0, 37]:
            self.color = Color.GREEN
        elif self.number % 2 == 0:
            self.color = Color.BLACK
        else:
            self.color = Color.RED

    def getNumber(self):
        # Returns string of number
        if self.number == 37:
            return '00'
        else:
            return str(self.number)

    def __repr__(self):
        return "({}, {})".format(self.getNumber(), self.color)

    def __eq__(self, rSpace):
        return self.number == rSpace.number

class Bet:
    def __init__(self, *args):
        '''Possible Bet Types:
        Color: Bet(Color.BLACK, 10)
        Parity: Bet(Parity.ODD, 10)
        Space: Bet(Space(1), 10)
        Zone: Bet(Zone.FIRST12, 10)
        Two Spaces (Pair): Bet(Space(1), Space(2), 10)
        Four Spaces (Corner): Bet(Space(1), Space(2), Space(4), Space(5), 10)
        '''

        self.space = None
        self.spaces = []
        self.amount = None
        self.type = None
        
        if len(args) == 2:
            if type(args[0]) == Color:
                #Adds all of the specified colored spaces
                self.type = 'color'
                self.spaces = [Space(s) for s in range(0, 38) if Space(s).color==args[0]]
            elif type(args[0]) == Parity:
                self.type = 'parity'
                #Adds all of the specified parity spaces
                self.spaces = [Space(s) for s in range(1, 37) if s%2==args[0].value]
            elif type(args[0]) == Space:
                self.type = 'space'
                self.space = args[0]
            elif type(args[0]) == Zone:
                self.type = 'zone'
                if args[0] == Zone.FIRST12:
                    self.spaces = [Space(s) for s in range(1, 13)]
                elif args[0] == Zone.SECOND12:
                    self.spaces = [Space(s) for s in range(13, 25)]
                elif args[0] == Zone.THIRD12:
                    self.spaces = [Space(s) for s in range(25, 37)]
                elif args[0] == Zone.FIRST18:
                    pass
                elif args[0] == Zone.SECOND18:
                    pass
                elif args[0] == Zone.FIRSTCOL:
                    pass
                elif args[0] == Zone.SECONDCOL:
                    pass
                elif args[0] == Zone.THIRDCOL:
                    pass
            
            self.amount = args[1]
            
        if len(args) == 3:
            self.type = 'pair'
            self.spaces = [args[0], args[1]]
            self.amount = args[2]
            
        if len(args) == 5:
            self.type = 'corner'
            self.spaces = [args[0], args[1], args[2], args[3]]
            self.amount = args[4]


class Wheel:
    def __init__(self, mode: str):
        # Mode being American or European
        self.mode = mode
        self.spaces = []
        for x in range(0, 4):
            self.spaces.append(Space(x))
        if self.mode == 'US':
            self.spaces.append(Space(37))

    def spin(self):
        # Randomly pick a space from self.spaces, return info on space (number, color)
        return random.choice(self.spaces)


class Game:
    def __init__(self, mode: str, money: int):
        # Mode being American or European
        self.mode = mode
        self.history = []
        self.money = 1000
        self.wheel = Wheel(mode)

    def processBet(self, result: Space, bets: [Bet]):
        #return int with money gained/lost (positive for gained, negative for lost)
        total = -sum([bet.amount for bet in bets])
        for bet in bets:
            if bet.type == 'space':
                if result == bet.space:
                    total += 2*bet.amount
                    
            elif bet.type in ['color', 'parity']:
                if result in bet.spaces:
                    total += 2*bet.amount

            elif bet.type == 'pair':
                if result in bet.spaces:
                    total += 4*bet.amount
                
            elif bet.type == 'corner':
                if result in bet.spaces:
                    total += 8*bet.amount

            elif bet.type == 'zone':
                if len(bet.spaces) == 12: #FIRST12, SECOND12, THIRD12
                    pass
            
        return total

    def playRound(self, bets: [Bet]):
        result = self.wheel.spin()
        change = self.processBet(result, bets)
        self.money += change
        print("Result was {}. You {} ${}".format(result, 'won' if change >= 0 else 'lost', abs(change)))
        return None

g = Game('US', 1000)

