import sqlite3

db = sqlite3.connect("user.db")
cr = db.cursor()


def create_tables():
    cr.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            username TEXT,
            email TEXT,
            password TEXT,
            mobile_no TEXT,
            pin TEXT,
            balance INTEGER
        )
    """)

    db.commit()



def save_user(name, username, email, password, mobile_phone, bank_pin, balance):
    cr.execute("SELECT user_id FROM users")
    users = cr.fetchall()
    if not users:
        new_user_id = "user1"
    else:
        last_number = 0
        for user in users:
            user_id = user[0]
            number = int(user_id.replace("user", ""))
            if number > last_number:
                last_number = number
        new_user_id = f"user{last_number + 1}"
    cr.execute("""
        INSERT INTO users
        (user_id, name, username, email, password, mobile_no, pin, balance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
    """, (
        new_user_id,
        name,
        username,
        email,
        password,
        mobile_phone,
        bank_pin,
        balance
    ))
    db.commit()
    print(f"User Created Successfully! Your ID is: {new_user_id}")




def check_login(username, password):
    cr.execute("""
        SELECT user_id
        FROM users
        WHERE username = ? AND password = ?
    """, (username, password))
    user = cr.fetchone()
    if user:
        return user # (userId,)
    else:
        return None




def get_user_details(user_id):
    cr.execute("""
        SELECT name, username, email, password, mobile_no, pin, balance
        FROM Users
        WHERE user_id = ?
        """, (user_id,))
    user = cr.fetchone()
    return user # (name, username, email, password, mobile_no, pin, balance) ==> Tuble



def make_deposit(user_id, added_balance):
    cr.execute("SELECT balance FROM Users WHERE user_id = ?", (user_id,))
    old_user_balance = cr.fetchone()
    new_balance = old_user_balance[0] + added_balance
    cr.execute(f"UPDATE Users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    db.commit()
    return new_balance



def make_withdraw(user_id, withdraw_balance):
    cr.execute("SELECT balance FROM Users WHERE user_id = ? ", (user_id,))
    old_user_balance = cr.fetchone() # Tuple => (balance,)
    new_balance = old_user_balance[0] - withdraw_balance
    cr.execute("UPDATE Users SET balance = ? WHERE user_id = ? ", (new_balance, user_id))
    db.commit()
    return new_balance




def get_recevier_id(user_id, mobile_no):
    cr.execute("SELECT user_id, username FROM Users WHERE mobile_no = ? ", (mobile_no, ))
    recevier = cr.fetchone() # (user_id, username)
    if recevier:
        if user_id == recevier[0]:
            print("Operation Cancelled, You Can't Transfere To Your Self")
            return False
        else:
            print(f"Okay, You Want To Transfere To {recevier[1]}")
            return True
    else:
        print("Operation Cancelled, We Can't Find This User In System\n Please check From Recevier Information.")
        return False




def check_transfere_balance(user_id, transfere_balance):
    cr.execute("SELECT balance FROM Users WHERE user_id = ? ", (user_id))
    sender = cr.fetchone() # (balance,)
    
    if sender:
        current_sender_balance = sender[0]
        if transfere_balance <= 0:
            print("Operation Cancelled, Balance Must Be Higher Than 0 EGP")
            return False
        elif current_sender_balance < transfere_balance:
            print(f"Insufficient Balance, You Want To Transfere {transfere_balance} EGP,\n But Your Balance Is {current_sender_balance} EGP")
            return False
        else:
            print("Okay, Your Balance Is Sufficient")
            return True
    else:
        print("Sender Not Found")
        return False




def make_transfere(sender_user_id, receiver_phone_number, transfere_balance):
    cr.execute("SELECT user_id, name, username, balance FROM Users WHERE mobile_no = ?", (receiver_phone_number,))
    recevier = cr.fetchone() # (user_id, name, username, balance)
    current_recevier_balance = recevier[3] # Current Receiver Balance
    # if recevier:
    #     current_recevier_balance = recevier[3] # Current Receiver Balance
    # else:
    #     return None
    # if recevier:
    #     if recevier[0] == sender_user_id:
    #         return "Operation Cancelled, You Can't Transfere To Your Self"
    #     else:
    #         recevier_balance = recevier[3]

    # if recevier:
    #     recevier_balance = recevier[3] # Receiver Current Balance



    # else:
        # print("Recevier Is Not Found In System, Please Try Again With The Correct Data")
        # return f"Recevier Whose Phone Number {receiver_phone_number} Is Not Found In System, Please Try Again With The Correct Data"
    
    cr.execute("SELECT name, username, balance FROM Users WHERE user_id = ? ", (sender_user_id,))
    sender = cr.fetchone() # (name, username, balance)
    current_sender_balance = sender[2] # Current Sender Balance
    # if sender:
    
    # else:
    #     return None
    # if transfere_balance > sender_balance:
    #     print(f"Insufficient Balance, You Want To Transfere {transfere_balance}EGP,\n But Your Balance Is {sender_balance}EGP")
    # else:
    new_recevier_balance_after_transfere = current_recevier_balance + transfere_balance 
    new_sender_balance_after_transfere = current_sender_balance - transfere_balance 
    try:
        cr.execute("UPDATE Users SET balance = ? WHERE user_id = ? ", (new_recevier_balance_after_transfere, recevier[0]))
        cr.execute("UPDATE Users SET balance = ? WHERE user_id = ? ", (new_sender_balance_after_transfere, sender_user_id))
        db.commit()
        cr.execute("SELECT balance FROM Users WHERE user_id = ? ", (sender_user_id))
        new_sender_balance = cr.fetchone() # (balance,)
        return new_sender_balance[0]
    except Exception as e:
        db.rollback()
        # print("There Is Error Happen During Transfere,\nTransfere Operation Not Completed")
        return -1
    
    # cr.execute("SELECT balance FROM Users WHERE mobile_no = ? ", (receiver_phone_number,))
    # new_recevier_balance = cr.fetchone() # (balance,)
    # # new_recevier_balance = balance[0]
    # cr.execute("SELECT balance FROM Users WHERE user_id = ? ", (sender_user_id))
    # new_sender_balance = cr.fetchone() # (balance,)
    
    
    # if new_recevier_balance[0] == current_recevier_balance + transfere_balance and new_sender_balance[0] == current_sender_balance - transfere_balance:
    #     # print(f"Transfere Operation Is Completed, Your Balance Now Is: {new_recevier_balance_after_transfere}")
    #     return new_sender_balance[0]
    # else:
    #     # print("Operation Cancelled, Maybe There Is An Invalid Data Entered, Please Try Again")
    #     return False
    # # return recevier_balance, sender_balance
