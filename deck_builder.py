from mtgsdk import Card
import os
from datetime import datetime
#import json
#import pprint

Wagic = "/home/laylong/Downloads/Wagic"

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
    modern_datetime = datetime.strptime("2006-01-01", "%Y-%m-%d")
    if set_datetime > modern_datetime:
        return True
    return False

def search_card():
    global Wagic
    search_term = input("Search: ")
    if search_term == "!quit":
        exit()
    cards = Card.where(name=search_term).all()
    formatted_results = []

    if len(cards) == 0:
        return "No such card in Magic"

    # TODO add validation for if card exists in Wagic
    cards[:] = [each for each in cards if (os.path.exists(f"{Wagic}/Res/sets/{each.set}"))]
    print("Filtered: Wagic available")
    

    # Filter stage, make these a settings change later
    cards[:] = [each for each in cards if (modern_set(each))]
    print("Filtered: Modern sets (2006+)")


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

def main():
    states = ["menu","add deck","add cards"]
    state = 0

    while(True):
        if states[state] == "menu":
            print "Add new decks or edit one to add cards"
            state = int(input("1. new deck"))
        valid_card = search_card()
        valid_quantity = request_quantity(valid_card)
        print(f"{valid_card[0]} ({valid_card[2]})   *{valid_quantity}")

main()