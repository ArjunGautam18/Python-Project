import random

b = random.randint(1, 100)  
guesses = 0
n = -1

print("Guess the number between 1 and 100!")

while n != b:
    n = int(input("Enter your guess: "))
    guesses += 1
    if n < b:
        print("Higher number please!!")
    elif n > b:
        print("Lower number please!!")
    else:
        print(f"You have guessed the correct number in {guesses} guesses!!!")
