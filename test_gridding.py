import unitest
import regular_gridding

class RegularGriddingTestCase(unitest.TestCase):

	#Do any setup if necessary. Run a takedown after tests if a setup was used.
	#def setup(self):
	#	self.results = regularlyGridRandom()
			
	def tearDown(self):


	def runTest(self):
		self.results = regularlyGridRandom()
		xi = self.results[0]
		yi = self.results[1]
		zi = self.results[2]
		self.assert(


if __name__=="__main__":
	unittest.main()
