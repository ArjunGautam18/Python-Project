import random

# Random choice for computer (1=rock, 2=paper, 3=scissor)
computer = random.randint(1, 3)

# Mapping number to string
choice_dict = {1: 'rock', 2: 'paper', 3: 'scissor'}

# User input
choice = int(input("Enter any one number among 1 (rock), 2 (paper), 3 (scissor): "))
you = choice_dict[choice]
comp = choice_dict[computer]

print(f"\nYou chose: {you}")
print(f"Computer chose: {comp}")

# Game logic
if you == comp:
    print("It's a draw!")
elif (you == 'rock' and comp == 'scissor') or \
     (you == 'paper' and comp == 'rock') or \
     (you == 'scissor' and comp == 'paper'):
    print("CONGRATULATION !!! , You won!")
else:
    print("You lose!!!!!")
