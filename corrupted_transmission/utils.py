from decimal import Decimal


class Coordinate:
    def __repr__(self):
        return f"<Coordinate: {self.x}, {self.y}>"

    def __init__(self, y, x):
        self.y = Decimal(y)
        self.x = Decimal(x)
