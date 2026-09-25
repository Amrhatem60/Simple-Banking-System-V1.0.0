# Import Section
from utils import email_validation, check_integer
from database import create_tables, save_user, check_login, get_user_details, make_deposit, make_transfere, make_withdraw, get_recevier_id, check_transfere_balance

# -----------------------------------------------------------------------------
# Create User Table In Database 
create_tables()



# -----------------------------------------------------------------------------
# Constants Section
VALID_EGY_PREFIX = ["10", "11", "12", "15"]


# -----------------------------------------------------------------------------
print("--------------------------------------------")
print("======== Hello, Happy To See You <3 ========")
print("--------------------------------------------")
print(
  """
  Overview About This Banking System
  This System is Closed To Our Big Banking System You Can Do Anything
  - Check Your Balance
  - Deposit
  - Withdraw
  - Transfer Money To anyone
  - Transaction History
  - Account Information
  * And Many Many Things
  """
)



while True:
  try:

    status_of_login = int(input("What Do You Want To Do ? \n [1] Sign Up \n [2] Login \n Choose [1] Or [2]:"))
    if status_of_login == 1:
      print(f"Great! You Choose To : Sign Up")
      break

    elif status_of_login == 2:
      print(f"Great! You Choose To : Login")
      break

  except ValueError:
    print("Please Enter A Number: 1 Or 2.")




if status_of_login == 1:

    name = input("Enter Your Name: ").strip().capitalize()
    # while name == "" or any(character.isdigit() for character in name) or name.isalpha() == False:
    while not name.isalpha(): # True -> False , False -> True
      print("Invalid input, name must be string Only and can't be empty")
      name = input("Please Enter Your Name As String Only: ").strip().capitalize()

    email = input("Enter Your Email: ").strip().lower()
    while not email_validation(email): # False -> Not False = True
      email = input("Please Enter Your Email Correctly [ex: amr123@gmail.com]: ").strip().lower()

    password = input("Enter Your Password Strong [Contains Characters & Integers & Symbols]: ").strip()
    while not any(character.isalpha() for character in password) or not any(character.isdigit() for character in password) or not any(not character.isdigit() and not character.isalpha() for character in password):
      print("Invalid Password, Password Must Contain String and Numbers and Symbols")
      password = input("Please Enter Your Password Strong")

    mobile_phone = input("Enter Your Phone Number : +20").strip()
    while not mobile_phone.isdigit() or len(mobile_phone) != 10 or mobile_phone[:2] not in VALID_EGY_PREFIX:
      if not mobile_phone.isdigit(): # abc123
        print("Invalid Number, Mobile Phone Must Be Numbers Only")
      elif len(mobile_phone) != 10:
        print("Invalid Number, Phone Number Must Contain 10 Number Without +20")
      elif mobile_phone[:2] not in VALID_EGY_PREFIX:
        print("Invalid Egy Number, Only Egypt Number Is Allowed")
      mobile_phone = input("Please Enter Your Mobile Phone :")

    bank_pin = input("Enter Your Account PIN [6 Integers]").strip()
    while not bank_pin.isdigit() or len(bank_pin) != 6:
      if not bank_pin.isdigit():
        print("Invalid Number, PIN Must Be Numbers Only")
      elif len(bank_pin) != 6:
        print("Invalid PIN, PIN Must Be 6 Integers")
      bank_pin = input("Please Enter Your PIN Correctly: ")

    balance = check_integer("Please Enter Your Opening balance [Must be Greater Than 500EGP]")
    while balance <= 500:
      print("Insufficient Balance, Opening Balance Must Be Greater Than 500 EGP")
      balance = check_integer("Please Enter Your Opening balance [Must be Greater Than 500EGP]")

    save_user(name, email[:email.index("@")], email, password, mobile_phone, bank_pin, balance)


elif status_of_login == 2:
    username_to_login = input("Enter Your Username : ").strip().lower()
    user_password_to_login = input("Enter Your Password: ").strip()
    user = check_login(username_to_login, user_password_to_login) # (userID,) --> Returned Tuple
    # user = (userID,), type --> Tuple

    if user:
      print(f"Login Successfully, Hello {username_to_login} Happy To See You Again <3")
      user_data = list(get_user_details(user[0])) # Returned Tuble Converted To List
      # user_data = [name, username, email, password, mobile_no, pin, balance]

      while True:
        try:
          menu = int(input("""
                      Okay, Now What Do You Want To Do ?\n
                      [1] Show Account Information\n
                      [2] View Your Balance\n
                      [3] Make A Transaction\n
                      [4] Deposit\n
                      [5] Logout
                      Choose From This Choices :
                  """).strip())


          if menu == 1:
            print(f"""
                Hello {user_data[1]} <3\n
                Your Account Details Shown Here:\n 
                Your Id Is: {user[0]}\n
                Your Name Is: {user_data[0]}\n
                Your Username Is: {user_data[1]}\n
                Your Email Is: {user_data[2]}\n
                Your Mobile Number Is: {user_data[4]}\n
                Your Current Balance Is: {user_data[6]}\n
                """)


          elif menu == 2:
            print(f"Your Current Balance Is: {user_data[6]}")


          elif menu == 3:
            transaction = int(input(f"""
                                  Great! {user_data[1]},\n
                                  You Want To Make A Transaction\n
                                  So, Please Choose What Do You Want To Do ?\n
                                  [1] Make A Transfere\n
                                  [2] Make A Withdraw\n
                                  Choose From This Choices :
                                  """))

            if transaction == 1:
              while True:
                try:
                  receiver_phone_num = input("Please Enter The Phone Number Of Receiver: +20 ").strip()
                  if receiver_phone_num == "":
                    print("Invalid Input, Input Can't Be Empty, Please Enter The Receiver Phone Numer.")
                    
                  elif not receiver_phone_num.isdigit():
                    print("Invalid Input, Phone Number Must Be Integers Only\n ex: +20 1277257856")
                    
                  elif len(receiver_phone_num) != 10:
                    print("The Phone Number Must Be 10 Integers\n ex: +20 1277257856")
                    
                  elif receiver_phone_num[:2] not in VALID_EGY_PREFIX:
                    print("Invalid Egy Number, Only Egypt Number Is Allowed\n ex: +20 1277257856")
                    
                  else:
                    result_from_get_recevier_func = get_recevier_id(user[0], receiver_phone_num)
                    if result_from_get_recevier_func:
                      transfere_balance = int(input(f"Now Enter The Balance You Want To Transfere: "))
                      # if transfere_balance:
                      result_from_check_func = check_transfere_balance(user[0], transfere_balance)
                      if result_from_check_func:
                        operation = make_transfere(user[0], receiver_phone_num, transfere_balance)
                        if operation == -1:
                          print("There Is Error Happen During Transfere,\nTransfere Operation Is Not Completed")
                          # print(f"Transfere Operation Is Completed")
                          # user_data[6] = operation
                          # break
                        elif operation >= 0:
                          # print("There Is Error Happen During Transfere,\nTransfere Operation Is Not Completed")
                          print(f"Transfere Operation Is Completed")
                          user_data[6] = operation
                          break
                          # print("There Is Error Happen During Transfere,\nTransfere Operation Is Not Completed")
                        # elif operation == 0:
                        #   print()
                      else:
                        # print("Operation Cancelled")
                        print("Operation Cancelled, Maybe There Is An Invalid Data Entered, Please Try Again")
                    # else:
                      
                      
                      # print("G/reate! Your Transfere Is Completed Successfully\n Check Your Balance Now.")
                except ValueError:
                  print("Invalid Input, Only Numbers Is Allowed.")

            elif transaction == 2:
              while True:
                try:
                  print("Great! You Want To Make A Withdraw Operation")
                  withdraw_balance = int(input("Please Enter The Balance Count You Want To Withdraw: ").strip())
                  if withdraw_balance <= 0:
                    print("Operation Cancelled, withdraw Balance Must Greater than 0 EGP")
                  
                  else:
                      if withdraw_balance > user_data[6]: 
                        print("This Operation Can't Done, Your Balance Is Insufficient To Withdraw It")
                      else:
                        user_data[6] = make_withdraw(user[0], withdraw_balance)
                        print("Greate! Your Withdraw Is Completed Successfully\n Check Your Balance Now.")
                        break
                      
                except ValueError:
                  print("Invalid Input, Only Numbers Is Allowed.")

            else:
              print("Invalid Choice, Please Choose From Choices.")


          elif menu == 4:
            print(f"Greate! {username_to_login},\n You Want To Make A Deposit.")

            while True:
              try:
                new_added_balance = int(input("Please Enter Your Balance You Want To Take/Deposit: ").strip())

                if new_added_balance <= 0:
                  print("Can't Make This Operation, Money To Deposit Must Be Greater Than 0")
                else:
                  user_data[6] = make_deposit(user[0], new_added_balance)
                  print("Greate! Your Deposit Is Completed Successfully\n Check Your Balance Now.")
                  break

              except ValueError:
                print("Invalid, Balance Must Be Numbers Only and More Than 0 EGP")


          elif menu == 5:
            print("You Logged Out, I Whish To See You Later <3")
            break


          else:
            print("Invalid Choice, Please Choose From Choices In Menu (ex: 1 or 2 or ....) : ")


        except ValueError:
          print("Invalid Input, String Is Not Allowed, Please Choose From Choices.")


    else:
      print(f"Login Failed, Username -> {username_to_login}, Is Not Found \n Maybe Username or Password Is Wrong")






















