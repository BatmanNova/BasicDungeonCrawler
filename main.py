import random


# These are the players base stats, Health points, Energy, Attack Power
class MyPlayer:
    def __init__(self):
        self.maxHP = 10
        self.HP = self.maxHP
        self.EN = 3
        self.AP = 2
        self.row = 0
        self.col = 0

    def getPosition(self):
        return self.row, self.col

    def setPosition(self, row, col):
        self.row = row
        self.col = col

    def takeDamage(self, damage):
        self.HP -= damage
        if self.dead():
            print("you have died, game over!")
            exit()

    def heal(self):
        if self.HP + 3 > self.maxHP:
            self.HP = self.maxHP
        else:
            self.HP += 3

    def dead(self):
        return True if self.HP <= 0 else False

# enemy health will be generated based upon the floor depth they are on
class Enemy:

    def __init__(self, floorValue):
        if floorValue == 1:
            self.HP = 8
            self.damage = 2
        elif floorValue == 2:
            self.HP = 12
            self.damage = 3
        else:
            self.HP = 16
            self.damage = 4

    def takeDamage(self, damage):
        self.HP -= damage

    def dead(self):
        return True if self.HP <= 0 else False


class Boss(Enemy):
    def __init__(self, floorValue):
        if floorValue == 1:
            self.HP = 10
            self.damage = 5
        elif floorValue == 2:
            self.HP = 15
            self.damage = 7
        else:
            self.HP = 25
            self.damage = 9


# The floor sizes are going to be manually set, layer 1 is 3x2
# layer 2 is going to be 3x3, and the final layer will be 3x4
class Floor:
    layer = 0
    rows, cols = (0, 0)

    def __init__(self, layer):
        self.layer = layer
        self.cleared = False

        if layer == 1:
            self.rows, self.cols = (3, 2)
            self.rooms = [[0] * self.cols] * self.rows
        elif layer == 2:
            self.rows, self.cols = (3, 3)
            self.rooms = [[0] * self.cols] * self.rows
        else:
            self.rows, self.cols = (3, 4)
            self.rooms = [[0] * self.cols] * self.rows

    def displayFloor(self):
        for x in range(0, 3):
            print(self.rooms[x])

    # the rooms will be filled with their room value, their room value will
    # determine if they are a loot (2), monster(1) or empty(0), or (3) for boss.
    def fillRooms(self):
        if self.layer == 1:
            self.rooms = [[random.randint(0, 2) for x in range(0, 2)] for y in range(0, 3)]
        elif self.layer == 2:
            self.rooms = [[random.randint(0, 2) for x in range(0, 3)] for y in range(0, 3)]
        elif self.layer == 3:
            self.rooms = [[random.randint(0, 2) for x in range(0, 4)] for y in range(0, 3)]

    def setBoss(self):
        # This will set the boss room, or the room with the staircase in it to go down
        if self.layer == 1:
            self.rooms[(random.randint(0, 2))][(random.randint(0, 1))] = 3
        elif self.layer == 2:
            self.rooms[(random.randint(0, 2))][(random.randint(0, 2))] = 3
        elif self.layer == 3:
            self.rooms[(random.randint(0, 2))][(random.randint(0, 3))] = 3

    def placePlayer(self):
        # This will recursively call themselves in case the random number they generated
        # is a boss room, to prevent the boss room from being deleted

        if self.layer == 1:
            rows, cols = (random.randint(0, 2), random.randint(0, 1))
            if self.rooms[rows][cols] == 3:
                self.placePlayer()
            else:
                self.rooms[rows][cols] = 4
                player1.setPosition(rows, cols)
        elif self.layer == 2:
            rows, cols = (random.randint(0, 2), random.randint(0, 2))
            if self.rooms[rows][cols] == 3:
                self.placePlayer()
            else:
                self.rooms[rows][cols] = 4
                player1.setPosition(rows, cols)
        elif self.layer == 3:
            rows, cols = (random.randint(0, 2), random.randint(0, 3))
            if self.rooms[rows][cols] == 3:
                self.placePlayer()
            else:
                self.rooms[rows][cols] = 4
                player1.setPosition(rows, cols)

    def updatePlayerPos(self, player):
        self.rooms[player.row][player.col] = 4


def getInput(floor, player):
    validInput = False
    floor.displayFloor()

    while not validInput:
        print("Please input which direction you'd like to go:(up, down, left, right): ")
        direction = input()

        if direction == "left" or direction == "right" or direction == "up" or direction == "down":
            validInput = validateInput(direction, floor, player)
        else:
            print("invalid input, please try again.")

    movePlayer(direction, floor, player)


def validateInput(direction, floor, player):

    if direction == "left" or direction == "right":
        if direction == "left" and player.col - 1 < 0 or direction == "right" and player.col + 1 > floor.cols - 1:
            print("That would put you out of bounds.")
            return False
        else:
            return True
    elif direction == "up" or direction == "down":
        if direction == "down" and player.row + 1 > floor.rows - 1 or direction == "up" and player.row - 1 < 0:
            print("That would put you out of bounds.")
            return False
        else:
            return True


def movePlayer(direction, floor, player):
    #setting the room they were in to empty
    floor.rooms[player.row][player.col] = 0

    if direction == "left":
        #grabs the number (or what is assigned to that room)
        roomMovedTo = floor.rooms[player.row][player.col - 1]
        player.col -= 1
        floor.updatePlayerPos(player)
    elif direction == "right":
        roomMovedTo = floor.rooms[player.row][player.col + 1]
        player.col += 1
        floor.updatePlayerPos(player)
    elif direction == "up":
        roomMovedTo = floor.rooms[player.row - 1][player.col]
        player.row -= 1
        floor.updatePlayerPos(player)
    else:
        roomMovedTo = floor.rooms[player.row + 1][player.col]
        player.row += 1
        floor.updatePlayerPos(player)

    resolveRoom(roomMovedTo, floor, player)


def resolveRoom(currentRoom, floor, player):
    playerEnergy = player.EN

    if currentRoom == 0:
        print("This room is empty.")
    if currentRoom == 1:
        # combat loop
        print("You have entered a room with a monster! There is no turning back now!")
        print("Healing costs 3 Energy, attacking costs 1 energy. You currently have:", player.EN)

        enemy1 = Enemy(floor.layer)

        while not enemy1.dead():
            print("You have entered the boss room, BEWARE! He hits hard!")
            playerAction = input(
                "What would you like to do? enter 'heal' (or h) to heal, or 'attack' (or a) to attack: ")
            playerAction.lower()
            if playerAction == "h" or playerAction == "heal":
                if playerEnergy >= 3:
                    player.heal()
                    playerEnergy -= 3
                else:
                    print("You do not have enough energy to heal.")
            elif playerAction == "a" or playerAction == "attack":
                enemy1.takeDamage(player.AP)
                print("You deal damage to the monster, their HP is: ", enemy1.HP)
                playerEnergy -= 1
            else:
                print("not a valid input.")

            if playerEnergy <= 0:
                if not enemy1.dead():
                    print("Enemy attacks, you get dealt: ", enemy1.damage)
                    player.takeDamage(enemy1.damage)
                    print("Your current HP: ", player.HP)
                    playerEnergy = player.EN

        lootObtained(player)

    if currentRoom == 2:
        lootObtained(player)
    if currentRoom == 3:
        boss1 = Boss(floor.layer)

        while not boss1.dead():
            playerAction = input(
                "What would you like to do? enter 'heal' (or h) to heal, or 'attack' (or a) to attack: ")
            playerAction.lower()
            if playerAction == "h" or playerAction == "heal":
                if playerEnergy >= 3:
                    player.heal()
                    playerEnergy -= 3
                else:
                    print("You do not have enough energy to heal.")
            elif playerAction == "a" or playerAction == "attack":
                boss1.takeDamage(player.AP)
                print("You deal damage to the boss, his HP is: ", boss1.HP)
                playerEnergy -= 1

            else:
                print("not a valid input.")

            if playerEnergy <= 0:
                if not boss1.dead():
                    print("Boss attacks, you get dealt: ", boss1.damage)
                    player.takeDamage(boss1.damage)
                    print("Your current HP: ", player.HP)
                    playerEnergy = player.EN

        print("You have killed the boss, proceeding to the next floor....")
        lootObtained(player)
        floor.cleared = True


def lootObtained(player):
    lootObtained = False

    while not lootObtained:
        playerAction = input("You have defeated the monster, please select the potion you want.\n"
                             "1. Attack Potion (increases attack by 1)\n"
                             "2. Energy Potion (increases energy by 1)\n"
                             "3. Heal Potion (increases max HP by 2, performs a heal action)\n")
        if playerAction == "1":
            player.AP += 1
            lootObtained = True
            print("You have selected the attack potion, you attack is now: ", player.AP)
        elif playerAction == "2":
            player.EN += 1
            lootObtained = True
            print("You have selected the energy potion, you energy is now: ", player.EN)
        elif playerAction == "3":
            player.maxHP += 2
            player.heal()
            lootObtained = True
            print("You have selected the Heal potion, you maxHP is now: ", player.maxHP)
            print("Your current HP is: ", player.HP)
        else:
            print("invalid input.")


if __name__ == '__main__':
    player1 = MyPlayer()

    print("Welcome adventurer, you have found your way into my dungeon!\n"
          "The only way to get out, is to kill the final boss on the final floor.\n"
          "Here is a map:")
    print(" ---------- Floor 1 ------------")
    floor1 = Floor(1)
    floor1.fillRooms()
    floor1.setBoss()
    floor1.placePlayer()
    floor1.displayFloor()
    print("-----------------------------------")

    print("You will notice that there are various numbers assigned to each room.\n"
          "Your location is marked with a number 4, so go ahead and find yourself.\n"
          "rooms that are empty are marked with a 0. They are simply storage rooms unused.\n"
          "Rooms that have monsters in them that need killing are marked with a 1,\n"
          "feel free kill them or avoid them, but be informed, upon killing a monster\n"
          "they will drop loot!\n"
          "Rooms marked with a 2 are free loot! Feel free to go grab them.\n"
          "And finally rooms marked with a 3 are the floor boss! You must defeat\n"
          "this boss in order to progress. There are 3 bosses, 3 floors in total.\n"
          "goodluck Adventurer! Try not to be my dungeons afternoon snack.")
    print("---------------------------------------------------------------------")
    print("I know that is a lot of information, so here is a legend for your map:\n"
          "0 = empty\n"
          "1 = Enemy\n"
          "2 = Loot\n"
          "3 = Boss\n"
          "4 = you\n")
    #floor 1 game loop

    while not floor1.cleared:
        getInput(floor1, player1)


    #floor 2 game loop
    print(" ------------ Floor 2 --------------")
    floor2 = Floor(2)
    floor2.fillRooms()
    floor2.setBoss()
    floor2.placePlayer()
    floor2.displayFloor()
    print("-----------------------------------")
    while not floor2.cleared:
        getInput(floor2, player1)

    # floor 3 game loop
    print(" ------------ Floor 3 --------------")
    floor3 = Floor(3)
    floor3.fillRooms()
    floor3.setBoss()
    floor3.placePlayer()
    floor3.displayFloor()
    print("-----------------------------------")
    while not floor3.cleared:
        getInput(floor3, player1)

    print("Congratulations you have cleared all 3 floors!")
