import pygame
import math

pygame.init()


class Button:
    def __init__(self, pos_x, pos_y, width, height, color, text):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('Arial', 20)

    def getRect(self):
        return self.rect

    def addText(self):
        displayWindow.blit(self.font.render(self.text, True, (0, 0, 0)),
                           (self.pos_x + self.width / 2 - 10, self.pos_y))
        pygame.display.update()


class Unit(Button):
    def __init__(self, pos_x, pos_y, width, height, color, text):
        super().__init__(pos_x, pos_y, width, height, color, text)


class GUIButton(Button):
    def __init__(self, pos_x, pos_y, width, height, color, text):
        super().__init__(pos_x, pos_y, width, height, color, text)

    def chooseButton(self):
        if self.color == red:
            self.color = lightRed
        elif self.color == blue:
            self.color = lightBlue
        elif self.color == darkRed:
            self.color = red

    def uncheckButton(self):
        if self.color == lightRed:
            self.color = red
        elif self.color == lightBlue:
            self.color = blue
        elif self.color == red:
            self.color = darkRed


displayWidth = 800
displayHeight = 600
fieldSize = 20  # liczba kratek


blue = pygame.Color("#00AAB2")
lightBlue = pygame.Color("#4da6ff")
lightRed = pygame.Color("#ff6666")
red = pygame.Color("red")
darkRed = pygame.Color("#b30000")
green = pygame.Color("#33cc33")

menuX = min(displayWidth, displayHeight)

displayWindow = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Battleground Simulator")
clock = pygame.time.Clock()
displayWindow.fill(pygame.Color("white"))

infantryRed = GUIButton(menuX + 20, 20, menuX / fieldSize, menuX / fieldSize, red, "I")
infantryBlue = GUIButton(menuX + 40 + menuX / fieldSize,
                         20,
                         menuX / fieldSize,
                         menuX / fieldSize,
                         blue, "I")
archerRed = GUIButton(menuX + 20,
                      20 + 20 + menuX / fieldSize,
                      menuX / fieldSize,
                      menuX / fieldSize,
                      red, "A")
archerBlue = GUIButton(menuX + 40 + menuX / fieldSize,
                       20 + 20 + menuX / fieldSize,
                       menuX / fieldSize,
                       menuX / fieldSize,
                       blue, "A")
cavalryRed = GUIButton(menuX + 20,
                       20 + 40 + 2 * menuX / fieldSize,
                       menuX / fieldSize,
                       menuX / fieldSize,
                       red, "C")
cavalryBlue = GUIButton(menuX + 40 + menuX / fieldSize,
                        20 + 40 + 2 * menuX / fieldSize,
                        menuX / fieldSize,
                        menuX / fieldSize,
                        blue, "C")
deleteButton = GUIButton(menuX + 20 + menuX / fieldSize,
                         20 + 40 + 4 * menuX / fieldSize,
                         3 * menuX / fieldSize,
                         menuX / fieldSize,
                         darkRed, "Del")
startButton = GUIButton(menuX + 20 + menuX / fieldSize,
                        20 + 40 + 7 * menuX / fieldSize,
                        3 * menuX / fieldSize,
                        menuX / fieldSize,
                        green, "Start")

menuButtons = [infantryRed, infantryBlue, archerRed, archerBlue, cavalryRed, cavalryBlue]
extraButtons = [deleteButton, startButton]
Units = {}
chosenButton = deleteButton
mode = "None"  # "Add" - dodawanie, "Del" - usuwanie
currentColor = red
currentType = "None"


def drawGrid(number):
    blockSize = min(displayHeight, displayWidth) / number
    for x in range(number):
        for y in range(number):
            rect = pygame.Rect(x * blockSize, y * blockSize,
                               blockSize, blockSize)
            pygame.draw.rect(displayWindow, pygame.Color("black"), rect, 1)


def addUnit(keyX, keyY, width):
    x = keyX * width
    y = keyY * width
    Units[keyX, keyY] = Unit(x, y, width, width, currentColor, currentType)
    print("added at", keyX, keyY)


def removeUnit(keyX, keyY):
    Units.pop((keyX, keyY), None)
    print("del at", keyX, keyY, len(Units))
    displayWindow.fill(pygame.Color("white"))


def convert_to_hex(rgba_color):
    red = rgba_color[0]
    green = rgba_color[1]
    blue = rgba_color[2]
    return '0x{r:02x}{g:02x}{b:02x}'.format(r=red, g=green, b=blue)


def getString():
    for (x, y), unit in Units.items():
        line = ""
        line += str(x)
        line += ","
        line += str(y)
        line += ","
        line += unit.text
        line += ",#"
        tmp = convert_to_hex(unit.color)
        line += tmp[2:]
        line += "\n"
    return line

finished = False

while not finished:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                print(mouseX, mouseY)
                if mouseX > menuX:
                    for button in menuButtons:
                        if button.pos_x <= mouseX <= button.pos_x + button.width:
                            if button.pos_y <= mouseY <= button.pos_y + button.height:
                                mode = "Add"
                                currentColor = button.color
                                currentType = button.text
                                chosenButton.uncheckButton()
                                chosenButton = button
                                button.chooseButton()
                                break
                    for button in extraButtons:
                        if button.pos_x <= mouseX <= button.pos_x + button.width:
                            if button.pos_y <= mouseY <= button.pos_y + button.height:
                                if button.text == "Del":
                                    mode = "Del"
                                    chosenButton.uncheckButton()
                                    chosenButton = button
                                    button.chooseButton()
                                    break
                                else:
                                    finished = True  # start main program
                else:
                    if mode == "Add":
                        addUnit(math.floor(mouseX / (menuX / fieldSize)),
                                math.floor(mouseY / (menuX / fieldSize)),
                                menuX / fieldSize)
                    elif mode == "Del":
                        removeUnit(math.floor(mouseX / (menuX / fieldSize)),
                                   math.floor(mouseY / (menuX / fieldSize)))

        for button in menuButtons:
            pygame.draw.rect(displayWindow, button.color, button.getRect(), 0)
            button.addText()

        for button in extraButtons:
            pygame.draw.rect(displayWindow, button.color, button.getRect(), 0)
            button.addText()

        for unit in Units.values():
            pygame.draw.rect(displayWindow, unit.color, unit.getRect(), 0)
            unit.addText()

        drawGrid(fieldSize)
        pygame.display.update()
        clock.tick(30)
print(getString())
print("quitting...")
pygame.quit()
