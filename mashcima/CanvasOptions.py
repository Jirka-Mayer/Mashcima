class CanvasOptions:
    def __init__(self):
        # what pitches should randomize note stem orientation
        self.randomize_stem_flips_for_pitches = [-2, -1, 0, 1, 2]

        # do barlines point up, above the staff?
        self.barlines_up = False

        # do barlines point down, below the staff?
        self.barlines_down = False

        # probability that a random space between symbols will be inserted
        self.random_space_probability = 0.03

        # size range for the random space in pixels
        self.random_space_size = (50, 300)
