class PartyAnimal :
	x = 0

    def party(self) :
        self.x += 1
        print("So far :", self.x)


# >>> an = PartyAnimal()
# >>> an.party()
# So far : 1
# >>> an.party()
# So far : 2
# >>> PartyAnimal.party(an)
# So far : 3
# >>> an.party()
# So far : 4
# >>> 
