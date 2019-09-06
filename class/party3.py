class PartyAnimal :
    x = 0
    name = ""

    def __init__(self, name) :
        self.name = name
        print(self.name, "constructed")

    def party(self) :
        self.x += 1
        print(self.name, "party count :", self.x)

    def __del__(self) :
        print(self.name, "destructed")

s = PartyAnimal("Sally")    # Sally constructed
j = PartyAnimal("Jim")      # Jim constructed
print()

s.party()                   # Sally party count : 1
j.party()                   # Jim party count : 1
s.party()                   # Sally party count : 2
PartyAnimal.party(s)        # Sally party count : 3
PartyAnimal.party(j)        # Jim party count : 2
s.party()                   # Sally party count : 4
j.party()                   # Jim party count : 3

print()
del(s)                      # Sally destructed
del(j)                      # Jim destructed
print("-" * 40)

class FootballFan(PartyAnimal) :
    points = 0

    # if use script below, will be overwritten
    # def __init__(self, name) :
    #     self.points += 1
    #     PartyAnimal.__init__(self, name)  # if no this line, name variable is not set.

    def touchdown(self) :
        self.points = self.points + 7
        self.party()
        print(self.name, "points", self.points)

s = PartyAnimal("Sally")    # Sally constructed
s.party()                   # Sally party count : 1
print()

j = FootballFan("Jim")      # Jim constructed
j.party()                   # Jim party count : 1
j.touchdown()               # Jim party count : 2
                            # Jim points 7
print()
del(s)                      # Sally destructed
del(j)                      # Jim destructed
