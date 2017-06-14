class UpdateBag:
    """
    Contains all the information that needs to passed between
    the Game and GUI class.
    """

    def __init__(self, matches, bonuses, additions, movements, ice, medals, info):
        self.matches = matches
        self.bonuses = bonuses
        self.additions = additions
        self.movements = movements
        self.ice = ice
        self.medals = medals
        self.info = info

    def __str__(self):
        print("Matches:")
        print(self.matches)
        print("Bonuses:")
        print(self.bonuses)
        print("Additions:")
        print(self.additions)
        print("Movements:")
        print(self.movements)
        print("Ice:")
        print(self.ice)
        print("Medals:")
        print(self.medals)
        print("Info:")
        print(self.info)
