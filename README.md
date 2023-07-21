# Wagic Deck Builder

This is a Magic the Gathering deck builder tool for Wololo's [Wagic](https://github.com/WagicProject/wagic) a homebrew MTG game. The decks are plain text and can also be used for personal archival means.

/Wagic/User/profiles/<Name> is the default decks directory. Use a .env file containing the line ```WAGIC_PLAYER=<Name>``` where <Name> is your Wagic profile name.

## Prerequisits

 - [Wagic](https://github.com/WagicProject/wagic): Have this installed somewhere locally on the computer you run this program on. It requires some files to check things not handled by API calls
 - [Python 3.^](https://www.python.org/): At least python 3, although not tested for any specific release
   - python-dotenv: Run ```pip install python-dotenv```
 - [MTGSDK](https://docs.magicthegathering.io/#documentationsdks) for Python: A wrapper of the API calls


## Operations

Currently being worked on. Changes are likely, but currently works as a minimum function.

Type "1" to select the create a deck option. Fill out a name and small description. At it's current state, basic lands are returning something in the API call that causes a crash. So please type the full name and capitalize the first letter. ie ```Plains```,```Forrest```,```Swamp```, etc. The fix is bypassing the API call and thus also the set lookup. The set marker that will be saved is the wildcard.

## Considerations about deck building
 - (*) denotes any set or maybe most recent set?
 - \# is to comment out a line
 - cards can be added directly via multiverse id
 - each call of "#DESC:" in the description is a new line

## For use as AI decks
### HINT
 - dontattackwith(<card name>)

## Troubleshooting

 - Use on Windows. For your on use, you can change the Wagic directory line to wherever you saved it. (ie 'C:\Users\YourName\Downloads'). The os.environ isn't strictly linux, but less likely to work out of the box.
