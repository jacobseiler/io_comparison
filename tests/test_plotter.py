from io_comparison.plot import Plotter

import unittest
import pytest

class TestPlotter(unittest.TestCase):

    def get_class(self) -> Plotter:
        return Plotter()

    def test_load(self) -> None:
        plotter = self.get_class()
