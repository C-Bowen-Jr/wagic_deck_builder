from mtgsdk import Card, Set
import os
from datetime import datetime
from dotenv import load_dotenv
import consolemenu
#from consolemenu.items import *
#import json
#import pprint

load_dotenv()
Wagic = f"{os.environ.get('HOME')}/Downloads/Wagic"
print(Wagic)
VERSION = "1.0.6"

def modern_set(each):
    # Perhaps better approach than raw date comparison, exclusionary list method
    exclusion_list = ["LEA","LEB","2ED","3ED","4ED","5ED","6ED","7ED","8ED","9ED","ARN","ATQ","LEG","DRK","FEM","ICE","HML","ALL","MIR","VIS","WTH","TMP","STH","EXO","USG","ULG","UDS","MMQ","NEM","PCY","INV","PLS","APC","ODY","TOR","JUD","ONS","LGN","SCG","POR","PO2","P3K","S99","S00","CHR","ATH","BRB","DKM","UGL","UNH","UST","UND","UNF","SUM","PWOS","PTC","O90P","FBB","CEI","CED","4BB"]

    from_set = Set.find(f"{each.set}")
    each.set_year = from_set.release_date[:4]

    if each.set in exclusion_list:
        return False
    return True

def search_card():
    global Wagic

    # loop rather than return on stops to try again, except quit
    search_term = input("Search: ")
    if search_term == "!save":
        return "save"
    elif search_term == "!quit":
        return "stop"

    if search_term in "Plains Forest Mountain Swamp Island":
        # temporary fix, something isn't valid in the response on these from the API
        return [search_term, "Basic Land","10E"]

    cards = Card.where(name=search_term).all()
    formatted_results = []

    if len(cards) == 0:
        print("No such card in Magic")
        return "none"

    #cards[:] = [each for each in cards if (os.path.exists(f"{Wagic}/Res/sets/{each.set}"))]
    #print("Filtered: Wagic available")
    print("Wagic filter skipped")
    

    # Filter stage, make these a settings change later
    cards[:] = [each for each in cards if (modern_set(each))]
    print("Filtered: Modern sets (2004+)")

    if len(cards) <= 0:
        print("No results after filters")
        return "none"

    elif len(cards) == 1:
        print(f"Only one result: {cards[0].name} ({cards[0].set})")
        return [cards[0].name,cards[0].types[0],cards[0].set]
        print(f"{cards[0]}")

    result_number = 0
    for each in cards:
        print(f"Result {result_number}: ")
        print(f"-Name:        {each.name}")
        print(f"-Type:        {each.types[0]}")
        print(f"-Set (Abrv.): {each.set_name} ({each.set})")
        print(f"-Year:        {each.set_year}\n")
        formatted_results.append([each.name,each.types[0],each.set])
        result_number += 1

    choice = -1
    while not choice in range(len(formatted_results)):
        choice = input(f"Which result: (0-{len(formatted_results)-1})")
        if choice == "!none":
            return "none"
        try:
            choice = int(choice)
        except:
            print("Please enter a number")

    return formatted_results[choice]
    #print(json.dumps(cards, indent=2))
    #pprint.pprint(vars(each))
    #print("\n")

def request_quantity(card_selected):
    max_copies = 4
    if card_selected[0] == "Relentless Rats":
        max_copies = 100
    if card_selected[1].find("Basic Land") > -1:
        max_copies = 100

    choice = 0
    while not choice in range(1,max_copies + 1):
        choice = input(f"How many copies: (1-{max_copies})")
        try:
            choice = int(choice)
        except:
            print("Please enter a number")

    return choice

def create_deck():
    global Wagic
    current_decks = os.listdir(f"{Wagic}/User/profiles/{os.environ.get('WAGIC_PLAYER')}")
    current_decks.remove("options.txt")
    current_decks.remove("tasks.dat")
    current_decks.remove("collection.dat")
    current_decks.remove("stats")
    if current_decks:
        current_decks.sort()
        last_deck = current_decks[-1].replace("deck" ,"").replace(".txt", "")
        this_deck = int(last_deck) + 1
    else:
        this_deck = 1

    lands = []
    creatures = []
    permanents = [] # Covers enchantments and equipment
    spells = [] # Covers instants and sorceries
    deck_name = input("Deck name?\n>")
    description = input("Description?\n>")

    card_count = 0
    while (True):
        valid_card = search_card()
        if (valid_card == "save"):
            save(this_deck, deck_name,description,lands,creatures,spells,permanents)
            break
        elif (valid_card == "stop"):
            break
        elif (valid_card == "none"):
            pass
        else:
            valid_quantity = request_quantity(valid_card)
            card_count += valid_quantity
            quantity_buffer = 32 - len(valid_card[0])
            print(f"(Adding {valid_card[0]}...{card_count}/60)\n")

            if ("Land" in valid_card[1]):
                lands.append(f"{valid_card[0]} ({valid_card[2]}) {quantity_buffer*' '}*{valid_quantity}")
        
            elif ("Creature" in valid_card[1]):
                creatures.append(f"{valid_card[0]} ({valid_card[2]}) {quantity_buffer*' '}*{valid_quantity}")
        
            elif (valid_card[1] == "Instant" or valid_card[1] == "Sorcery"):
                spells.append(f"{valid_card[0]} ({valid_card[2]}) {quantity_buffer*' '}*{valid_quantity}")

            else:
                permanents.append(f"{valid_card[0]} ({valid_card[2]}) {quantity_buffer*' '}*{valid_quantity}")
    
def save(deck_number, deck_name,description,lands,creatures,spells,permanents):
    global VERSION
    write_lines = []

    write_lines.append(f"#NAME:{deck_name}\n")
    write_lines.append(f"#DESC:{description}\n#DESC:\n#DESC:Constructed using WagicDeckBuilder v.{VERSION}\n\n")
    
    if (len(creatures) > 0): 
        write_lines.append("#/--- CREATURES ---/\n")
        for each in creatures:
            write_lines.append(f"{each}\n")
        write_lines.append("\n")
    if (len(permanents) > 0): 
        write_lines.append("#/--- PERMANENTS---/\n")
        for each in permanents:
            write_lines.append(f"{each}\n")
        write_lines.append("\n")
    if (len(spells) > 0): 
        write_lines.append("#/---   SPELLS   ---/\n")
        for each in spells:
            write_lines.append(f"{each}\n")
        write_lines.append("\n")
    if (len(lands) > 0): 
        write_lines.append("#/---   LANDS   ---/\n")
        for each in lands:
            write_lines.append(f"{each}\n")
        write_lines.append("\n")

    # TODO: save_location options between A:B, relative/Decks or Wagic/Path
    save_choice = os.environ.get('SAVE_LOCATION') # relative | wagic, load from .env
    if save_choice == "relative":
        save_file = open(f"./Decks/{deck_name}.txt", "w")
        print(f"Saving to local as {deck_name}.txt")
    else:
        save_file = open(f"{Wagic}/User/profiles/{os.environ.get('WAGIC_PLAYER')}/deck{deck_number}.txt", "w")
        print(f"Saving to Wagic as {deck_number}.txt")
    print(10 * "-")
    for each in write_lines:
        print(each[:-1]) # cut only the last newline
        save_file.write(each)
    print(10 * "-")
    print(f"Save complete")

def main():
    global VERSION
    menu = consolemenu.ConsoleMenu("Wagic Deck Buildler",f"WDB v[{VERSION}]\nSelect an option")

    #new_deck = Items.MenuItem("Create a new deck")
    #edit_deck = Items.MenuItem("Edit a deck")

    #menu.append_item(new_deck)
    #menu.append_item(edit_deck)

    #menu.show()

    states = ["menu","new deck","edit deck"]
    state = 0

    while(True):
        if states[state] == "menu":
            print("Add new decks or edit one to add cards")
            state = input("1. new deck\n>")
            if state == "!quit":
                exit()
            else:
                try:
                    state = int(state)
                except:
                    print("Not a number")
            if not state in range(1,len(states)):
                print("Not a valid menu option")
                state = 0

        if states[state] == "new deck":
            create_deck()
            state = 0
        if states[state] == "edit deck":
            print("Not implemented")
            state = 0
        #valid_card = search_card()
        #valid_quantity = request_quantity(valid_card)
        #print(f"{valid_card[0]} ({valid_card[2]})   *{valid_quantity}")

main()