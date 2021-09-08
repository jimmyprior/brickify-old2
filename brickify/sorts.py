#imports?


class LocationSorted:
	#creates a matrix filled with everything

	def __init__(self, mosaic_size, fits):

		self.mborder = mosaic_size
		self.pborder = fits[0].size  #add this method
		self.sorted = []

		#shorten this with * or something probs
		for y in range(self.mborder[1]):
			row = []
			for x in range(self.mborder[0]):
				row.append(None)

			self.sorted.append(row)

		for fit in fits:
			self.add_fit(fit)

		#store this stuff as a matrix?

	def add_fit(self, fit):
		#have to initially fill the list with nones cause yeah preserve indexes i guess

		#index in the list will be the y * the x border of the mosaic + the x
		location = fit.location

		self.sorted[location[1]][location[0]] = fit
		#check and make sure x,y coordinate alligns with location within

	def get_affected(self, fit):
		#account for orientation

		#generates indexes of impacted pieces and retursn the fits at the indexes

		x, y = fit.location
		minX = x - self.pborder[0] + 1 
    #low bound x pborder is just the regular size for the piece all these fits share.
		maxX = x + fit.size[0]  
    #never exceed boundary cause already a check for that when create

		minY = y - self.pborder[1] + 1  # low bound y
		maxY = y + fit.size[1]  # i think i actuall

		if minX < 0:  #confrim not off left side
			minX = 0

		if minY < 0:
			minY = 0

		#some edge detection on the left border
		# never will go past right

		#x coordinate - width of the self piece + 1
		#x oordinate + width of the piece
		#y coordinate - height of the self piece + 1
		#y coordinate + height of the piece

		#returns list of fits
		#uses quick maths to easily find the indexes
		#create the x, y coordinates : index?

		#maybe just change this to a matrix for ease of use? yeah, that would save a lot of code

		overlap = []

		for y in range(minY, maxY):
			for x in range(minX, maxX):
				overlap.append(self.sorted[y][x])

		return overlap


class ScoreSorted:
	def __init__(self, fits):
		#removing is very fast because this uses a dictionary to quick remove

		self.sorted = sorted(fits)  #rearanges the current list... does not create a new one
    
		self.create_lookup_dict()

		self.index = 0

		#keep track of the last fit that != none so that not loop trhough the start everytime
		#nvm that cause that assumes that piece was placed which is not necessarily true actually, wait we can sue that we just need to check that piece again. S

	def create_lookup_dict(self):
		#hashmap for speed
		self.lookup = {}
		for val in range(len(self.sorted)):
			key = self.sorted[val]
			self.lookup[key] = val
			#shorted this after debug

		#run during init
		#set as param

	def remove_fit(self, fit):
		#returns true or false specifiying whether or not the fit was removed
		#this way fits_score can be kept track of

		#fit is not actually removed, it is set to none to preserve the indexes of the list.

		index = self.lookup.get(fit, None)
		#this means it was not in the dict
		if index != None:
			self.sorted[index] = None
			self.lookup.pop(fit)
			return True

		return False

	def get_best_fit(self):
		#returns the first list in sorted that is not none, or none if there are not more fits in sorted.
		#THIS DOES NOT REMOVE
		#REMOVE WILL BE DONE AFTER IN ADUSTMENT PHASE
		#THIS DOES MOVE INDEX THOUGH

		#idk if i need the minus one, figure it out
		for index in range(self.index, len(self.sorted)):
			if self.sorted[index]:
				self.index = index
				return self.sorted[index]
