import random

class GuessGame:
    def _init_(self):
        self.secret_number = random.randint(1, 10)

    def play(self):
        guess = int(input("Guess a number between 1 and 10: "))

        if guess == self.secret_number:
            print("You won! 🎉")
        else:
            print("Wrong guess!")
            print("The number was:", self.secret_number)


game1 = GuessGame()
game1.play()