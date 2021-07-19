from django.test import TestCase

from django.urls import reverse


class StartPointTest(TestCase):
    def test_happy_path(self):
        """Should serve linked location if proper coords passed"""
        response = self.client.get(reverse("calibration:start-point"), {"y": "43.54", "x": "-80.26"})
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
