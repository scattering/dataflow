import unittest
from reduction.common.regular_gridding import regularlyGridRandom

class RegularGriddingTestCase(unittest.TestCase):
    def setup(self):
        """Do any setup if necessary. Run a takedown after tests if a setup was used."""
        self.results = regularlyGridRandom()

    def tearDown(self):
        pass

    def runTest(self):
        self.results = regularlyGridRandom()
        xi = self.results[0]
        yi = self.results[1]
        zi = self.results[2]
        assert ()


if __name__ == "__main__":
    unittest.main()
