class CanvasOptions:
    def __init__(self):
        # what pitches should have stem orientation randomized 50:50
        self.randomize_stem_flips_for_pitches = [-2, -1, 0, 1, 2]

        # do barlines point up, above the staff?
        self.barlines_up = False

        # do barlines point down, below the staff?
        self.barlines_down = False

        # probability that a random space between symbols will be inserted
        # (a relatively large space meant to make the trained model more robust)
        self.random_space_probability = 0.03

        # size range for the random space in pixels
        # (size in addition to the regular horizontal padding space)
        self.random_space_size = (50, 300)

    @staticmethod
    def get_empty():
        """Returns empty options, ready for overriding"""
        opts = CanvasOptions()
        for key in vars(opts).keys():
            setattr(opts, key, None)
        return opts

    def override_values_from(self, other):
        """
        Overrides local values by those in the other object that
        are not set to None.
        """
        if other is None:
            return

        for key, val in vars(other).items():
            if val is not None:
                setattr(self, key, val)
