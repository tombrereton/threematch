class UpdateBag:
    """
    Contains all the information that needs to passed between
    the Game and GUI class.
    """

    def __init__(self, removals, bonuses, additions, movements, ice_removed, medals_removed, info, state=()):
        self.removals = removals
        self.bonuses = bonuses
        self.additions = additions
        self.movements = movements
        self.ice_removed = ice_removed
        self.medals_removed = medals_removed
        self.info = info
        self.state = state

    def __str__(self):
        return "Removals:\n" \
               "{}\n" \
               "Bonuses:\n" \
               "{}\n" \
               "Additions:\n" \
               "{}\n" \
               "Movements:\n" \
               "{}\n" \
               "Ice removed:\n" \
               "{}\n" \
               "Medals removed:\n" \
               "{}\n" \
               "Info:\n" \
               "{}".format(self.removals, self.bonuses, self.additions,
                           self.movements, self.ice_removed, self.medals_removed, self.info)

    def is_empty(self):
        """
        Return true if all attributes are empty lists.
        :return:
        """
        if self.removals == [] and self.bonuses == [] and self.additions == [] \
                and self.movements == [] and self.ice_removed == [] and self.medals_removed == [] and self.info == []:
            return True
        else:
            return False
