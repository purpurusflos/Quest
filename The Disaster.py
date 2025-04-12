from tkinter import *
import json
from random import randint

master = Tk()
master.geometry("250x200")

title_label = Label(master, text="The Disaster")
title_label.pack()
button_start = Button(master, text="Start")
button_start.pack()

ok_button = Button(master, text="ok")
ok_button.pack_forget()

# Класс Gamer имеет атрибуты nickname, health_level и location,
# соответствующие имени, уровню здоровья и местоположению игрока.
# Местоположение в начале игры всегда третья локация.
class Gamer:
    def __init__(self, login, health, location):
        self.nickname = login
        self.health_level = health
        self.location = 2

    def __str__(self):
        return f"Your name is {self.nickname}"

# Метод heal позволяет восстановить определенное количество очков здоровья,
    # по умолчанию - 10 очков, если уровень здоровья не превышает 100.
    def heal(self, health_points=10):
        self.health_level += health_points
        if self.health_level > 100:
            self.health_level = 100
            return "Can't heal more than 100 health points."
        return f'User {self.nickname} has {self.health_level} health points.'

# Метод damage позволяет отнять у игрока определенное количество очков здоровья,
    # по умолчанию - 10 очков, если уровень здоровья не меньше 0.
    def damage(self, damage_points=10):
        self.health_level -= damage_points
        if self.health_level <= 0:
            return "You're temporarily dead."
        return f'User {self.nickname} has {self.health_level} health points.'

# Метод find возвращает информацию о том, где находится игрок в данный момент
    def find(self):
        return str(locations[self.location])

# Метод go позволяет игроку перемещаться из локации в локацию. Выбор локации осуществляется игроком,
    # для этого он должен ввести порядковый номер локации.
    # После перемещения будет выведена информация о текущем местоположении игрока
    def go(self, choice):
        self.location = (choice - 1)
        return str(locations[self.location])


# Класс Location содержит атрибуты name, description, items и NPCs,
# соответствующие названию локации, ее описанию, предметам и неиграбельным персонажам в этой локации.
class Location:
    def __init__(self, name, description, items, NPCs):
        self.name = name
        self.description = description
        self.items = list()
        self.NPCs = list()
        for item in items:
            self.items.append(Item(item['name'], item['weight']))
        for character in NPCs:
            self.NPCs.append(NPC(character['name'], character['lines']))

    def __str__(self):
        return f"You're in a {self.description}."


# Класс NPC содержит атрибуты name и lines,
# соответствующие имени персонажа и фразам, которые он говорит.
class NPC:
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines

    def __str__(self):
        return self.name

# С помощью метода talk персонаж произносит одну случайную фразу из имеющихся у него фраз.
    def talk(self):
        phrase = randint(0, len(self.lines) - 1)
        return f'{self.name} says: "{self.lines[phrase]}"'


# Класс Item имеет атрибуты name и weight, соответствующие названию данного предмета и его весу.
class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __str__(self):
        return self.name

    def __del__(self):
        return f"{self.name} was destroyed."


# Класс Inventory имеет атрибуты items и volume,
# соответствующие списку предметов, находящихся в инвентаре, и свободному месту в инвентаре, или его объему.
class Inventory:
    def __init__(self, items_list=[], volume=10):
        self.items = items_list
        self.volume = volume

    def __str__(self):
        items_names = ', '.join([str(i) for i in self.items])
        if items_names == "":
            items_names = "nothing"
        return f"There's {items_names} in the bag. Space left: {self.volume}"

# Метод put позволяет игроку добавить предмет из локации в инвентарь в случае, если в инвентаре достаточно места,
# при этом предмет удаляется из локации. Для этого игрок должен ввести порядковый номер предмета в локации.
# Место в инвентаре уменьшается на вес предмета.
    def put(self, coordinates):
        item = locations[gamers.location].items[coordinates - 1]
        if (self.volume - item.weight) < 0:
            return f"The bag is full. You can't put {item.name}"
        else:
            self.items.append(item)
            self.volume -= item.weight
            locations[gamers.location].items.remove(locations[gamers.location].items[coordinates - 1])
            items_names = ', '.join([str(i) for i in self.items])
            return f"There's {items_names} in the bag."

# Метод take позволяет игроку добавить предмет из инвентаря в локацию,
# при этом предмет удаляется из инветаря. Для этого игрок должен ввести порядковый номер предмета в инвентаре.
# Место в инвентаре увеличивается на вес убранного предмета.
    def take(self, coordinates):
        item = self.items[coordinates - 1]
        if item in self.items:
            locations[gamers.location].items.append(item)
            self.volume += item.weight
            self.items.remove(item)
            items_names = ', '.join([str(i) for i in self.items])
            if items_names == "":
                items_names = "nothing"
            return f"There's {items_names} in the bag."

# Метод take позволяет уничтожить предмет. Для этого игрок должен ввести порядковый номер предмета в инвентаре.
# Место в инвентаре увеличивается на вес уничтоженного предмета.
    def destroy(self, coordinates):
        item = self.items[coordinates - 1]
        self.volume += item.weight
        self.items.remove(item)
        return f"You've destroyed the {item.name}."


with open("my_locations.json") as f:
    config_locations = json.load(f)
locations = list()
for L in config_locations["locations"]:
    locations.append(Location(L["name"], L["description"], L["items"], L["NPC"]))


with open("my_gamers.json") as f:
    config = json.load(f)
gamers = Gamer(config["gamers"][0]["login"], int(config["gamers"][0]["health_level"]), config["gamers"][0]["location"])

bag = Inventory()

text1 = Label(master, text='You wake up in a quiet room.')
text1.pack_forget()

e = Entry(master)
e.insert(0, "Type command ")
e.pack_forget()


def actions(event):
    comm = e.get()
    if comm == "heal":
        text1["text"] = gamers.heal()
    elif comm == "damage":
        text1["text"] = gamers.damage()
    elif "put" in comm:
        items_names = ', '.join([str(i) for i in locations[gamers.location].items])
        text1["text"] = f"There are {items_names}."
        if len(comm) > 3:
            text1["text"] = bag.put(int(comm[-1]))
            e.delete(0, 'end')
            e.insert(0, "Type command ")
    elif "take out" in comm:
        items_names = ', '.join([str(i) for i in bag.items])
        text1["text"] = f"There are {items_names}."
        if len(comm) > 8:
            text1["text"] = bag.take(int(comm[-1]))
            e.delete(0, 'end')
            e.insert(0, "Type command ")
    elif "destroy" in comm:
        items_names = ', '.join([str(i) for i in bag.items])
        text1["text"] = f"There are {items_names}."
        if len(comm) > 8:
            text1["text"] = bag.destroy(int(comm[-1]))
            e.delete(0, 'end')
            e.insert(0, "Type command ")
    elif comm == "What's in my bag?":
        text1["text"] = str(bag)
    elif comm == "Where am I?":
        text1["text"] = gamers.find()
    elif comm == "Who am I?":
        text1["text"] = str(gamers)
    elif "go" in comm:
        locations_names = ', '.join([str(i.name) for i in locations])
        text1["text"] = f"You can go to {locations_names}"
        if len(comm) > 2:
            text1["text"] = gamers.go(int(comm[-1]))
            e.delete(0, 'end')
            e.insert(0, "Type command ")
    elif "talk" in comm:
        NPCs_names = ', '.join([str(i) for i in locations[gamers.location].NPCs])
        text1["text"] = f"There are {NPCs_names}."
        if len(comm) > 4:
            text1["text"] = locations[gamers.location].NPCs[int(comm[-1]) - 1].talk()
            e.delete(0, 'end')
            e.insert(0, "Type command ")


menu = Menu(master)
master.config(menu=menu)
actions_menu = Menu(menu)
menu.add_cascade(label='List of actions', menu=actions_menu)
actions_menu.add_command(label='Who am I?')
actions_menu.add_command(label='Where am I?')
actions_menu.add_command(label="What's in my bag?")
actions_menu.add_command(label='go')
actions_menu.add_command(label='talk')
actions_menu.add_command(label='put')
actions_menu.add_command(label='take out')
actions_menu.add_command(label='destroy')
actions_menu.add_command(label='heal')
actions_menu.add_command(label='damage')
help_menu = Menu(menu)
menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='How to choose an item/location/NPC')
help_menu.add_separator()
help_menu.add_command(label='Exit', command=master.quit)


def help_choose():
    text1["text"] = "To choose an item, location or an NPC, type \
     the number of the chosen object from the list of all possible options\
      right after the command you've typed. \
      Example: You can go to School, City, Theatre. Type 'go 3' to go to the theatre."


def hide(widget):
    widget.pack_forget()


def appear(widget):
    widget.pack()


def start_screen(event):
    hide(button_start)
    hide(title_label)
    appear(text1)
    appear(e)
    appear(ok_button)


button_start.bind('<Button-1>', start_screen)
ok_button.bind('<Button-1>', actions)
# help_menu.entryconfig(0, command=help_choose)

mainloop()
