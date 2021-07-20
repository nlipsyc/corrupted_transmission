from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from corrupted_transmission.utils import Coordinate
from decimal import Decimal


from .views import _generate_equilateral_triangle_around_point, triangulation


class StartPointTest(TestCase):
    def test_happy_path(self):
        """Should serve linked location if proper coords passed"""
        response = self.client.get(
            reverse("calibration:start-point"), {"y": str(settings.CITY_LOCATION.y), "x": str(settings.CITY_LOCATION.x)}
        )
        # TODO check for the link unsing reverse()
        self.assertIn("<a href", str(response.content))
        self.assertIn("Location acquired, commence triangulation", str(response.content))

    def test_no_coords(self):
        """Should serve the null island hint"""
        response = self.client.get(reverse("calibration:start-point"))
        self.assertIn("Null island does not exist", str(response.content))

    def test_default_coords(self):
        """Should serve the null island hint"""
        response = self.client.get(reverse("calibration:start-point"), {"y": "0.00", "x": "0.00"})
        self.assertIn("Null island does not exist", str(response.content))

    def test_incorrect_coords(self):
        """Should serve the incorrect location hint."""
        response = self.client.get(reverse("calibration:start-point"), {"y": "40.71", "x": "-74.00"})
        self.assertIn("does not match background stelar data", str(response.content))


class TriangulationTest(TestCase):
    def test_generate_triangle(self):
        # I miss pytest.parametrize...
        a, b, c = _generate_equilateral_triangle_around_point(Coordinate(-50, 10), Decimal(15))
        side = b.x - c.x
        import pdb

        pdb.set_trace()
        self.assertAlmostEqual(side, Decimal(17.32), places=2)

        # a is above bc
        self.assertGreater(a.y, b.y)
        # a is on the midpoint of bc
        self.assertEquals(a.x, c.x + side / 2)

        # b is to the right of c
        self.assertGreater(b.x, c.x)
        # bc is horizontal
        self.assertEqual(b.y, c.y)
