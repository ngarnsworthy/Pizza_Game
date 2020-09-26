class Monster(object):
    eats = 'food'
    def __init__(self,name):
        self.name = name
    def speak(self):
        print(self.name + ' speaks')
    def eat(self, meal):
        if meal == self.eats:
            print('yum')
        else:
            print('belch')
#my_monster = Monster('nick')
#my_monster.speak()
#my_monster.eat('food')

class FrankenBurger(Monster):
    eats = 'ham'
