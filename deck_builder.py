from mtgsdk import Card
import os
from datetime import datetime
from dotenv import load_dotenv
#import json
#import pprint

Wagic = f"{os.environ.get('HOME')}/Downloads/Wagic"
VERSION = "1.0.4"
load_dotenv()

def modern_set(each):
    global Wagic
    try:
        set_info = open(f"{Wagic}/Res/sets/{each.set}/_cards.dat")
    except:
        print(f"Failed to find/open '{each.set}/_cards.dat")

    for line in set_info:
        if "year=" in line:
            set_date = line[5:15]
            each.set_year = line[5:9]
            break

    set_datetime = datetime.strptime(set_date,"%Y-%m-%d")
    modern_datetime = datetime.strptime("2004-01-01", "%Y-%m-%d")
    if set_datetime > modern_datetime:
        return True
    return False

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
        return [search_term, "Basic Land","*"]

    cards = Card.where(name=search_term).all()
    formatted_results = []

    if len(cards) == 0:
        print("No such card in Magic")
        return "stop"

    cards[:] = [each for each in cards if (os.path.exists(f"{Wagic}/Res/sets/{each.set}"))]
    print("Filtered: Wagic available")
    

    # Filter stage, make these a settings change later
    cards[:] = [each for each in cards if (modern_set(each))]
    print("Filtered: Modern sets (2004+)")

    if len(cards) <= 0:
        print("No results after filters")
        return "stop"

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
    current_decks.remove("stats")
    current_decks.sort()
    last_deck = current_decks[-1].replace("deck" ,"").replace(".txt", "")
    this_deck = int(last_deck) + 1

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
        elif (valid_card != "stop"):
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


    save_file = open(f"{Wagic}/User/profiles/{os.environ.get('WAGIC_PLAYER')}/deck{deck_number}.txt", "w")
    print(10 * "-")
    for each in write_lines:
        print(each[:-1]) # cut only the last newline
        save_file.write(each)
    print(10 * "-")
    print(f"Saving to deck{deck_number}.txt")

def main():
    states = ["menu","new deck","edit deck"]
    state = 0

    while(True):
        if states[state] == "menu":
            print("Add new decks or edit one to add cards")
            state = input("1. new deck\n>")
            if state == "!quit":
                exit()
            else:
                state = int(state)
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