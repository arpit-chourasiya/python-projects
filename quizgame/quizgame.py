import bcrypt, json, os, re, sys, random
import quizquestions as qq

#program starting menu
def start_options():
    print("\nWelcome to the Quiz Game! Please Select:\n1. Login\n2. Registration \n3. Play Quiz Game\n4. Exit from the game!")
    while True:
        try:
            choice = int(input("Please select a valid choice only from (1/2/3/4): "))
            if choice in [1,2,3,4]:
                return choice
        except ValueError:
            print("\nInvalid input! Please choose a number only from (1/2/3/4).")

#player login
def player_login(players_data):
    count1 = 1
    print("\nEnter details for login.")
    while count1 <= 5:
        valid_username = input("Enter your @username: ")
        for player_idx, player_key in enumerate(players_data):
            if valid_username == player_key.get("username"):
                count2 = 1
                while count2 <= 5:
                    valid_password = input("Enter your login password: ")
                    hashed_password = players_data[player_idx].get("Password")
                    password_checking = bcrypt.checkpw(valid_password.encode(), hashed_password.encode())
                    if password_checking:
                        print(f"\nLogin Successfully! Hello @{valid_username}")
                        return quiz_play(players_data, True, player_idx)
                    else:
                        print("\nInvalid password! Enter correct one.")
                    count2 += 1
                return exit_game(2) 
        else:
            print("\nInvalid @username, doesn't exist! Try again.")
        count1 += 1
    return exit_game(2) 

#player registration
def player_registration(players_data):
    counter =1
    while counter<=5:
        players_data_keys = ["Name", "Score", "Level"]
        print("\nEnter details:")
        players_data_values = [input(f"Enter your {key}: ")if key=="Name" else 0 for key in players_data_keys]
        players_data_values[2] = "Basic"
        if players_data_values[0] != "" and 3<=len(players_data_values[0])<=20:
            vaild_username = username_check(players_data)
            player_password = set_password()
            players_data_keys.extend(["username", "Password"])
            players_data_values.extend([vaild_username, player_password])
            players_data.append({players_data_keys[idx]: players_data_values[idx] for idx in range(len(players_data_keys))})
            svp_result = save_players_data(players_data)
            if svp_result =="success":
                print("\nRegistration Completed Successfully.")
                return player_login(players_data)
            else:
                print("\nSomething went wrong to save data! Try again.")
            count +=1
        else:
            print("Please set a valid name! Try to set between 2-20 character.")
        counter +=1
    else:
        return exit_game(1)
        
def quiz_play(player_data, is_loggedin, player_idx=None):
    count1 =1
    if is_loggedin != False:
        while count1<=5:
            choice = int(input("\nDo you want to continue? Select:\n1. Play Quiz Game \n2. Exit from the Quiz Game!\nSelect a choice (1/2): "))
            if choice ==2:
                return exit_game(3)
            elif choice==1:
                break
            else:
                print("\nPlease select a valid choice from (1/2/).")
            count1 +=1
    if count1>5: return exit_game(4)
    random_value = random.sample(range(0,25),25)
    player_level, print_score, player_username =  ((player_data[player_idx].get('Level') , player_data[player_idx].get('Score'), players_data[player_idx].get('username')) if is_loggedin==True else ("Basic", 0, "The Game"))
    
    attempted_correct, attempted_wrong = 0,0
    print(f"\nLets Play {player_username}! | Level: {player_level} | Score: {print_score}")
    question_number =1
    for iter in range(0,25):
        if player_level=="Basic":
            print(f"\n{question_number}. {qq.basic_ques[random_value[iter]].get('question')}")
        elif player_level=="Intermediate":
            print(f"\n{question_number}. {qq.intermediate_ques[random_value[iter]].get('question')}")
        elif player_level=="Advanced":
             print(f"\n{question_number}. {qq.advanced_ques[random_value[iter]].get('question')}")
        elif player_level=="Legend":
            print(f"\n{question_number}. {qq.legend_ques[random_value[iter]].get('question')}")
        elif player_level == "ALL LEVEL ACHIEVED":
            choice_opt = exit_game(6)
            if choice_opt == 1:
                player_data[player_idx]['Score'] = 0
                player_data[player_idx]['Level'] = "Basic"
                print("Profile Reset Successfully.")
                svp_result = save_players_data(players_data)
                return exit_game(3)
        else:
            exit_game(5)
        
        player_score , correct_answer, wrong_answer =  quiz_result(iter, random_value, player_level, print_score)
        if is_loggedin: 
            players_data[player_idx]['Score'] = player_score
            svp_result = save_players_data(players_data)
        attempted_correct + correct_answer 
        attempted_wrong + wrong_answer

        if question_number ==25:
            count2=1
            if is_loggedin:
                if player_level=="Basic":
                    player_level ="Intermediate"
                elif player_level =="Intermediate":
                    player_level = "Advanced"
                elif player_level == "Advanced":
                    player_level = "Legend"
                elif player_level == "Legend":
                    player_level = "ALL LEVEL ACHIEVED"
                print(f"\nCongratulation You Attemp all {player_level} quiz's | Total Attemted Questions: 25\n Attemped Correct: {attempted_correct} | Attemped Wrong: {attempted_wrong} | Score: {player_score}\nDo you want to continue?\n1. Play the Next Level\n2. Save Progress & Exit!")
                players_data[player_idx]['Level'] = player_level
                while count2<=5:
                    player_choice = int(input("Select a choice from (1/2): "))
                    if player_choice == 1:
                        svp_result = save_players_data(players_data)
                        if player_level == "ALL LEVEL ACHIEVED":
                            choice_opt = exit_game(6)
                            if choice_opt == 1:
                                player_data[player_idx]['Score'] = 0
                                player_data[player_idx]['Level'] = "Basic"
                                print("Profile Reset Successfully.")
                                svp_result = save_players_data(players_data)
                                return exit_game(3)

                    elif player_choice == 2:
                        
                        exit_game(0)
                    else:
                        print("Please select a valid choice from (1/2).")
                    count2+=1
                else:
                    exit_game(4)

            
            elif (is_loggedin) !=True:
                user_select = int(input("\nSave your progress. For Play more you need to login or register to the Quiz Game! Select:\n1. Login\n2. Registration\n3. Exit from the game"))
                if user_select==1:
                    return player_login(players_data)
                elif user_select==2:
                    return player_registration(players_data)
                else:
                    return exit_game(0)
        question_number +=1

def quiz_result(iter, random_value, player_level, player_score):
    if player_level=="Basic":
        correct_mark = 5
        negative_mark = -1
        quiz_answer, quiz_options = (qq.basic_ques[random_value[iter]].get('answer'), qq.basic_ques[random_value[iter]].get('options'))
    elif player_level=="Intermediate":
        correct_mark = 10
        negative_mark = -2
        quiz_answer, quiz_options = ((qq.intermediate_ques[random_value[iter]].get('answer')), qq.intermediate_ques[random_value[iter].get('options')])
    elif player_level=="Advanced":
        correct_mark = 15
        negative_mark = -3
        quiz_answer, quiz_options = ((qq.advanced_ques[random_value[iter]].get('answer')), qq.advanced_ques[random_value[iter].get('options')])
    elif player_level=="Legend":
        correct_mark = 20
        negative_mark = -4
        quiz_answer, quiz_options = ((qq.legend_ques[random_value[iter]].get('answer')), qq.legend_ques[random_value[iter].get('options')])
    else:
        exit_game(5)

    opt1, opt2, opt3, = quiz_options
    random_idx = random.sample([quiz_answer, opt1, opt2, opt3], 4)
    print(f"\nA. {random_idx[0]}\nB. {random_idx[1]}\nC. {random_idx[2]}\nD. {random_idx[3]}")
    count = 1
    while count<=5:
        player_answer = input("\nSelect a option: ").strip().upper()
        if player_answer in ["A", "B", "C", "D"]:
            if player_answer == "A":
                player_answer = random_idx[0]
            elif player_answer =="B":
                player_answer = random_idx[1]
            elif player_answer == "C":
                player_answer = random_idx[2]
            elif player_answer =="D":
                player_answer = random_idx[3]
            else:
                return exit_game(5)
            
            def check_option():
                for idx_value in random_idx:
                    if quiz_answer == idx_value: return random_idx.index(idx_value)
            correct_option = check_option()
            if correct_option ==0:
                correct_option ="A."
            elif correct_option== 1:
                correct_option ="B."
            elif correct_option == 2:
                correct_option = "C."
            elif correct_option ==3:
                correct_option = "D."
            else:
                return exit_game(5)
            
            attempted_correct, attempted_wrong = 0,0
            if player_answer == quiz_answer:
                player_score +=correct_mark
                attempted_correct+=1
                print(f"Correct Answer! Score: {player_score}")
                return player_score, attempted_correct, attempted_wrong
            elif player_answer != quiz_answer:
                player_score += negative_mark
                print(f"Wrong Answer! Correct option is: {correct_option} {quiz_answer}")
                return player_score, attempted_correct, attempted_wrong
            else:
                return exit_game(5)   
        else:
            print("\nPlease select a valid option from (A/B/C/D).")
        count+=1
    else:
        return exit_game(4)

def exit_game(value):
    
    if value==1:
        print("\nLimit Exceeded, Registration Process Failed! Try again.\n")
    elif value==2:
        print("\nLimit Exceeded, Login Process Failed! Try again.\n")
    elif value==3:
        print("\nThanks for comming! See you soon...\n")
    elif value==4:
        print("\nLimit Exceeded! Try again.\n")
    elif value==5:
        print("Something went wrong! Try again.\n")
    elif value==6:
        count =0
        print("\nYou Achieved all levels! Do you want to reset your profile?\n1. Yes \n2. Exit from the game!")
        while count<=5:
            count +=1
            choice = input("Select a valid choice from (1/2): ")
            if choice == 1:
                return choice
            else:
                return exit_game(0)
        else:
            return exit_game(4)
        
    else:
        print("\nThanks for playing! Goodbye.\n")
    sys.exit(0)

# JSON data functions 
def load_players_data():
    if os.path.exists("playersdata.json") and os.path.getsize("playersdata.json")>2:
        with open("playersdata.json", "r") as file:
            file_data = json.load(file)
            return file_data
    else:
        return []

def save_players_data(players_data):
    with open("playersdata.json", "w") as file:
        json.dump(players_data,file, indent=4)
        return "success"

# helper functions
def username_check(players_data):
    count=1
    while count<=5:
        user_input = input("Set your @username: ")
        if 5<=len(user_input)<=10 and re.match(r'^[A-Za-z0-9_]*$', user_input):
            if any(player.get("username") == user_input for player in players_data):
                print("\nThis @username was already taken! Try something different.")
            else:
                return user_input
        else: 
            print("\nPlease set a valid @username! Only allow: [A-Za-z0-9_] or try between 05 to 10 character.")
        count +=1           
    else:
        return exit_game(1)

def set_password():
    count = 1
    while count<=5:
        player_password = input("Set the password: ").strip()
        if 6<=len(player_password)<=15 and re.match(r'^\S+$', player_password):
            hashed_password = bcrypt.hashpw(player_password.encode(), bcrypt.gensalt())
            hashed_password_str = hashed_password.decode()
            return hashed_password_str
        else:
            print("\nEntered password not allowed! No space or try between 06 to 15 character.")
        count +=1
    else:
        return exit_game(1)
   

# program starting
players_data = load_players_data()
isplaying = start_options()
if isplaying==1: 
    player_login(players_data)
elif isplaying==2:
    player_registration(players_data)
elif isplaying==3:
    is_loggedin= False
    quiz_play(players_data, False)
else:
    exit_game(3)






















