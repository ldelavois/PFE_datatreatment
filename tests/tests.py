# coding: utf-8

import argparse
import matplotlib.pyplot as plt
import csv
import numpy as np
import datetime
import sys
import unittest
import random

class Tests(unittest.TestCase):

    def test_choice(self):
        
        liste = list(range(10))
        elt = random.choice(liste)
        # Vérifie que 'elt' est dans 'liste'
        self.assertIn(elt, liste)

unittest.main()
