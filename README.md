# Wagic Deck Builder

This is a Magic the Gathering deck builder tool for Wololo's [Wagic](https://github.com/WagicProject/wagic) a homebrew MTG game. The decks are plain text and can also be used for personal archival means.

/Wagic/User/profiles/<Name> is the default decks directory. Use a .env file containing the line ```WAGIC_PLAYER=<Name>``` where <Name> is your Wagic profile name. To set up that profile, if you haven't already, is done through the settings. Inside settings, there is a tab for profile, which is named "Default". Choose "New profile", provide a name, and then that will be your WAGIC_PLAYER=THAT_NAME_HERE.

## Prerequisits

 - [Wagic](https://github.com/WagicProject/wagic): Have this installed somewhere locally on the computer you run this program on. It requires some files to check things not handled by API calls
 - [Python 3.^](https://www.python.org/): At least python 3, although not tested for any specific release
   - python-dotenv: Run ```pip install python-dotenv```
   - consolemenu: Run ```pip install consolemenu```
 - [MTGSDK](https://docs.magicthegathering.io/#documentationsdks) for Python: A wrapper of the API calls

## Preview

![screenshot of version 1.0.6](deck_builder_v-1-0-6.png "Example of V.1.0.6")

## Operations

Currently being worked on. Changes are likely, but currently works as a minimum function.

### Menu
In the menu screen, type the number option and hit enter. To exit the program, type ```!quit```

### Deck Setup
There are 2 questions to this screen. First, type out a name for the deck and hit enter. Then type out a description for the deck and hit enter.

### Card Search
Search cards by name. Capilization doesn't matter except on Basic Land cards. Searches don't need to be fully spelled out, but it helps to narrow down the returned results. Just typing "she" looking for "Sheoldred, Whispering One" is going to give all prints of that card, plus all prints of any other card that contains "she" anywhere in the text of the card's name.

Once a card has been found, it will print out the results after some filters. Now select which result to add, or type ```!none``` to return to another search. If you chose one of the results, then answer how many copies you wish to add. Default limit is 1-4, but certain cards like Basic Lands and Relentless Rats have no limit.

While being prompted to search, you may either type ```!save``` or ```!quit```. This will save or return to the main menu, respectively.

Side note in regards to Basic Lands. Until I fix this issue, Basic Lands need to be typed in verbatum as "Plains","Forest","Swamp","Mountain", or "Island". They will default to 10E (tenth edition). This is arbitrarily chosen.

Alternative saving location can be set by setting a .env variable ```SAVE_LOCATION=relative|wagic```. No variable, or really anything but "relative" will result in the default Wagic location.

## Considerations about deck building
 - (*) denotes default set (perhaps 2ED?)
 - \# is to comment out a line
 - cards can be added directly via multiverse id
 - each call of "#DESC:" in the description is a new line

 ## Example of a deck file

![screenshot of a deck file](example_deck_file.png "screenshot of a deck file")

## For use as AI decks
### HINT
 - dontattackwith(<card name>)

## Troubleshooting

 - Use on Windows. For your on use, you can change the Wagic directory line to wherever you saved it. (ie 'C:\Users\YourName\Downloads\Wagic'). Or you can set a variable in the .env file. (ie. HOME="C:\Users\YourName")
 - At this time, the wagic available filter check is flawed. /set/_cards.dat does not seem to actually contain only valid cards. At worst, if you don't unzip the /Res/WagicCore.zip, it won't even access that file.
