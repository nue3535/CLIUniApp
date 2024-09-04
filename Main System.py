class Bank:
    def __init__(self, name, balance) -> None: #Constructor
        self.balance = balance # Add balance to bank
        self.name = name

    def mainMenu(self):
        userInput = input("Start banking (d/w/s/x): ")
        print(userInput)
        counter = 0
        while (userInput.lower() != 'x'):
            match userInput:
                case 'd':
                    deposit = float(input("Amount to deposit $"))
                    print(f"Amount {deposit} deposited")
                    self.balance += deposit
                case 'w':
                    withdraw = float(input("Amount to withdraw $"))
                    if (withdraw <= self.balance):
                        self.balance -= withdraw
                        print(f"Amount {withdraw} withdrawn, current balance is {self.balance}")
                    else:
                        print("Insufficient funds")
                case 's':
                    print(f"Current balance is ${self.balance:.2f}")
                case _:
                    print(f"Please enter d, w, s, or x!")

            userInput = input("Continue banking (d/w/s/x): ")

if __name__ == '__main__': # Return True if you execute this script
    bankObject1 = Bank("ANZ", 1000)
    bankObject1.mainMenu()
