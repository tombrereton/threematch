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
        return "Matches:\n" \
               "{}\n" \
               "Bonuses:\n" \
               "{}\n" \
               "Additions:\n" \
               "{}\n" \
               "Movements:\n" \
               "{}\n" \
               "Ice:\n" \
               "{}\n" \
               "Medals:\n" \
               "{}\n" \
               "Info:\n" \
               "{}".format(self.matches, self.bonuses, self.additions,
                           self.movements, self.ice, self.medals, self.info)
