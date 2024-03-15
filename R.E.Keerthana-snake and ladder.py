import time
import random
import sys
import mysql.connector as mc
from tabulate import tabulate

MAX_VALUE = 100 # winning point

# snake takes you down from 'key' to 'value'
snakes_at = {
    25:5,
    34:1,
    47:19,
    65:52,
    87:57,
    91:61,
    99:69
}

# ladder takes you up from 'key' to 'value'
ladders_at = {
    3:51,
    6:27,
    20:70,
    36:55,
    63:95,
    68:98
}
# messages when turns
turns = [
    "",
    "Go.",
    "Your turn.",
    "Lets win this.",
    "Are you ready?",
    "Please proceed."    
]
# messages when snake
snake_bite = [
    "dang",
    "bummer",
    "boohoo",
    "OHH NOOO",
    "snake bite"
]
# messages when ladder
ladder_climb = [
    "woww",
    "woohoo",
    "yaayyy"
    "nailed it",
    "HIP HIP HURRAY!"
]

# introduction
def welcome_msg():
    msg = """
    Welcome to The Snake and Ladder Game.
    Version: 1.0.0
    Developed by R.E.Keerthana.
    *****************************************************
    DISCLAIMER: This game is completely based on chance.
    *****************************************************
    HOW TO PLAY:
        1. Decide who goes first.
        2. Press Enter instead of rolling dice... ;)
        3. Climb UP ladders(when you reach them!) to win fast.
        4. Slide DOWN snakes... T_T
        5. Land exactly on the final position (100) to win.
    ALL THE BEST!
    """
    print(msg)

# taking player names
def get_player_names():
    player1_name = None
    while not player1_name:
        player1_name = input("Please enter a valid name for first player: ").strip()

    player2_name = None
    while not player2_name:
        player2_name = input("Please enter a valid name for second player: ").strip()

    print("\nMatch will be played between '" + player1_name + "' and '" + player2_name + "'\n")
    return player1_name, player2_name

# virtual method for rolling dice
def get_dice_value():
    time.sleep(1)
    dice_value = random.randint(1,6)
    print("Its a " + str(dice_value))
    return dice_value

# function used when snake
def got_snake_bite(old_value, current_value, player_name):
    print("\n" + random.choice(snake_bite).upper() + "  ~~~~~~~~~~>")
    print("\n" + player_name + " got a snake bite. Down from " + str(old_value) + " to " + str(current_value))

# function used when ladder
def got_ladder_climb(old_value, current_value, player_name):
    print("\n" + random.choice(ladder_climb).upper() + "    ##########")
    print("\n" + player_name + " climbed the ladder from " + str(old_value) + " to " + str(current_value))

# moving up or down acc. snake or ladder
def snake_ladder(player_name, current_value, dice_value):
    time.sleep(1)
    old_value = current_value
    current_value = current_value + dice_value

    if current_value > MAX_VALUE:
        print("You need " + str(MAX_VALUE - old_value) + " to win this game. Keep trying.")
        return old_value

    print("\n" + player_name + " moved from " + str(old_value) + " to " + str(current_value))
    if current_value in snakes_at:
        final_value = snakes_at.get(current_value)
        got_snake_bite(current_value, final_value, player_name)

    elif current_value in ladders_at:
        final_value = ladders_at.get(current_value)
        got_ladder_climb(current_value, final_value, player_name)

    else:
        final_value = current_value

    return final_value

# checking for winner
def check_win(player_name, position,looser):
    time.sleep(1)
    if MAX_VALUE == position:
        global pwd
        con = mc.connect(host = 'localhost', user = 'root', passwd = pwd)
        print("\n\n\nThats it.\n\n" + player_name + " won the game.")
        print("Congratulations! " + player_name)
        print("\nThank you for playing the game.")
        winner = player_name
        cur = con.cursor() # myql connection
        cur.execute('create database if not exists Snake_And_Ladder')
        cur.execute('use Snake_And_Ladder')
        cur.execute('create table if not exists Score_Board(Winner_History varchar(30) not null,Looser_History varchar(30) not null)')
        names = (winner,looser)
        query = "insert into score_board values(%s,%s)" # all previous game history of 
        cur.execute(query,names) # winners and loosers stored
        con.commit() # effecting change
        
        l = []
        query3 = "select * from score_board"
        cur.execute(query3)
        table = cur.fetchall()
        for row in table:
            row = list(row)
            l.append(row)
        print("\n")
        print("*"*39)
        print("|            SCORE_BORAD              |")
        print("-"*39)
        print(tabulate(l, headers=['Winner_History', 'Looser_History'],tablefmt='orgtbl'))
        print("-"*39)

        downloads = cur.rowcount # no. of record stored
        print('Total number of matches played as of now:',downloads)
        con.close()
        sys.exit(0) # exists

def main_game():
    welcome_msg()
    time.sleep(1)
    player1_name, player2_name = get_player_names()
    time.sleep(1)
    global pwd
    pwd = input("Please enter password of mysql:")
    try:
        con = mc.connect(host = 'localhost', user = 'root', passwd = pwd)
    except:
        print("Authentication Error Occurred.")
        print("Incorrect Password!")
        sys.exit(0)
    player1_current_position = 0
    player2_current_position = 0

    while True:
        time.sleep(1)
        input_1 = input("\n" + player1_name + ": " + random.choice(turns) + " Hit the enter to roll dice: ")
        print("\nRolling dice...")
        dice_value = get_dice_value()
        time.sleep(1)
        print(player1_name + " moving....")
        player1_current_position = snake_ladder(player1_name, player1_current_position, dice_value)

        check_win(player1_name, player1_current_position,player2_name)
        
        input_2 = input("\n" + player2_name + ": " + random.choice(turns) + " Hit the enter to roll dice: ")
        print("\nRolling dice...")
        dice_value = get_dice_value()
        time.sleep(1)
        print(player2_name + " moving....")
        player2_current_position = snake_ladder(player2_name, player2_current_position, dice_value)

        check_win(player2_name, player2_current_position,player1_name)
    

#main program or calling main function which contains all the subfunctions.
pwd = None
main_game()
