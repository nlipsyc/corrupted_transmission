from typing import Tuple
from decimal import Decimal


class Coordinate:
    def __repr__(self):
        return f"<Coordinate: {round(self.x,3)}, {round(self.y, 3)}>"

    def __init__(self, y, x):
        self.y = Decimal(y)
        self.x = Decimal(x)

    def __sub__(self, subtrahend: "Coordinate") -> Decimal:
        """Get the distance in degrees as the crow flies between two coordinates.

        Because this is absolute, order of the operands doesn't matter (it's commutative).

        This is a silly unit of measure, but will work for a human to triangulate their position.
        """
        difference_y = self.y - subtrahend.y
        difference_x = self.x - subtrahend.x

        # Pythagorean theorem
        distance_from_subtrahend = (difference_x ** 2 + difference_y ** 2).sqrt()

        return distance_from_subtrahend
