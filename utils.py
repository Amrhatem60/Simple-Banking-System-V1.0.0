# عايز اتاكد ان ال @ قبلها حجات وبعدها حجات 

def email_validation(email):

  if email == "":
    print("Invalid Email, email can't be empty.")
    # email = input("Please Enter Your Email: ")
    return False

  elif email.isdigit():
    print("Invalid Email, email can't be contain integers only.")
    # email = input("Please Enter Your Email Correctly: ")
    return False

  elif email.count("@") != 1:
    print("Invalid Email, email must contain exactly one @")
    # email = input("Please Enter Your Email Correctly [ex. username@domain.extension]: ")
    return False

  elif email.index("@") == 0:
    print("Invalid Email, email can't starts with @")
    # email = input("Please Enter Your Email Correctly [ex. username@domain.extension]: ")
    return False

  elif email.index("@") == len(email) - 1:
    print("Invalid Email, email can't end with @")
    # email = input("Please Enter Your Email Correctly [ex. username@domain.extension]: ")
    return False

  elif email.index(".") == len(email) - 1:
    print("Invalid Email, Please define the extension of email")
    return False

  elif email.index("@") + 1 == email.index("."):
    print("Invalid Email, Please define the domain of email")
    return False

  else:
    return True


def check_integer(message):
  while True:
    try:
      return int(input(message).strip())
      

    except ValueError:
      print("Invalid input, Only Numbers Allowed")





# def commit_and_close_db():
#   """Commit Changes and Close DataBase Connection"""
#   db.commit()
#   db.close()
#   print("Connection To Database Closed")