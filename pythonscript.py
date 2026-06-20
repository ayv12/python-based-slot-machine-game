import tkinter as tk
from tkinter import messagebox
import random

# Slot symbols
SLOT_SYMBOLS = ["❄", "🌼", "🔥"]

# Initialize global variables
current_bet = 0
loss_count = 0
quiz_attempted = False
repower_used = False
score = {"wins": 0, "losses": 0, "current_bet": 0}

# Dictionary to store player scores by email
player_scores = {}

# Function to place a bet
def place_bet():
    global current_bet, player_email

    # Get the player's email
    player_email = email_entry.get().strip()
    if not player_email:
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return
    
    if player_email not in player_scores:
        player_scores[player_email] = {"wins": 0, "losses": 0}

    try:
        bet_amount = float(bet_entry.get())
        if bet_amount < 10:
            messagebox.showerror("Invalid Bet", "Bet amount cannot be less than 10.")
        elif bet_amount > 100:
            messagebox.showerror("Invalid Bet", "Bet amount cannot be more than 100.")
        else:
            current_bet = bet_amount
            score["current_bet"] = current_bet
            messagebox.showinfo("Bet Placed", f"You have successfully placed a bet of ${current_bet}.")
            bet_entry.delete(0, tk.END)  
            bet_page.pack_forget()  
            game_page.pack(fill="both", expand=True) 
            update_scoreboard()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the bet.")

# Function to play the slot machine
def play_slot_machine():
    global current_bet, loss_count, quiz_attempted, repower_used

    if current_bet <= 0:
        if repower_used:
            messagebox.showerror("Game Over", "You have already used your repower chance. Game over!")
            show_final_scoreboard()  
            root.quit()  
        else:
            messagebox.showinfo("Game Over", "You have one chance to solve the quiz and repower!")
            game_page.pack_forget()
            math_quiz_page.pack(fill="both", expand=True)
        return

    # Spin the slots
    slot1 = random.choice(SLOT_SYMBOLS)
    slot2 = random.choice(SLOT_SYMBOLS)
    slot3 = random.choice(SLOT_SYMBOLS)

    # Update the slot display
    slot1_label.config(text=slot1)
    slot2_label.config(text=slot2)
    slot3_label.config(text=slot3)

    # Check for win condition
    if slot1 == slot2 == slot3:
        player_scores[player_email]["wins"] += 1
        score["wins"] += 1
        current_bet += 5
        result_label.config(text=f"You won! Bet increased to ₹{current_bet}", fg="green")
    else:
        current_bet -= 5
        player_scores[player_email]["losses"] += 1
        score["losses"] += 1
        result_label.config(text=f"You lost! Bet decreased to ₹{current_bet}", fg="red")
        loss_count += 1  # Increment loss count

    score["current_bet"] = current_bet
    update_scoreboard()

# Function to update the scoreboard
def update_scoreboard():
    scoreboard_label.config(
        text=f"Wins: {score['wins']} | Losses: {score['losses']} | Current Bet: ₹{score['current_bet']}"
    )

# Function to handle math quiz page
def check_answers():
    global current_bet, quiz_attempted, repower_used

    correct_answers = 0
    # Check each answer
    for i in range(5):
        user_answer = answer_entries[i].get()
        if user_answer.isdigit() and int(user_answer) == answers[i]:
            correct_answers += 1

    if correct_answers == 5:
        current_bet += 100
        score["current_bet"] = current_bet
        messagebox.showinfo("Quiz Passed", f"Correct! You've received 100 more bet points.\nYour new bet is: ₹{current_bet}.")
        quiz_attempted = True  # Marking the quiz as attempted
        repower_used = True  # Marking the repower as used
        math_quiz_page.pack_forget()
        game_page.pack(fill="both", expand=True)
        update_scoreboard()
    else:
        messagebox.showerror("Quiz Failed", "You did not answer all questions correctly. Game over!")
        show_final_scoreboard()  
        root.quit() 

### Function to show the final scoreboard
def show_final_scoreboard():
    # Create a new window for the final scoreboard
    game_page.destroy()
    final_scoreboard_window = tk.Frame(root, bg="black")
    root.iconbitmap("das1.ico")
    
    player_score = player_scores.get(player_email, {"wins": 0, "losses": 0})

    header = tk.Label(root, text="Score Board ", bg="pink", fg="black", font=("Helvetica", 18, "bold"))
    header.pack(fill=tk.X, pady=(0, 10))

    scoreboard_text =f"\nEmail: {player_email}\n\nWins: {player_score['wins']}\n\nLosses: {player_score['losses']}"
    scoreboard_label = tk.Label(root, text=scoreboard_text,bg="black",fg="pink", font=("Helvetica", 14))
    scoreboard_label.pack(pady=20)
    

    close_button = tk.Button(root, text="close", bg="pink", fg="black", font=("Helvetica", 12),command=root.destroy)
    close_button.pack(pady=10)

##    rebet_button = tk.Button(root, text="Go Back To Bet Page", bg="pink", fg="black", font=("Helvetica", 12),command=re_bet())
##    rebet_button.pack(pady=10)
##
##
##
##def re_bet():
##        final_scoreboard_window.pack_forget()
##        bet_page.pack(fill="both", expand=True)
##           
        

# Function to go back to betting page from game
def go_back_to_bet_page():
    game_page.pack_forget()
    bet_page.pack(fill="both", expand=True)

# Create main window
root = tk.Tk()
root.title("CASINO.PY")
root.geometry("600x500")
root.configure(bg="black")
root.iconbitmap("das1.ico")

# --- Bet Page ---
bet_page = tk.Frame(root, bg="black")
root.iconbitmap("das1.ico")

header = tk.Label(bet_page, text="Place Your ₹₹₹", bg="pink", fg="black", font=("Helvetica", 18, "bold"))
header.pack(fill=tk.X, pady=(0, 10))

instruction_label = tk.Label(bet_page, text="RULES\n\nyou must bet between 10 to 100\nOnce you lose you have to answer 5 questions\nIf correct, you get 100 points.\nIf you lose again, the game ends.\n\n\nEnter your bet amount (10 - 100):", bg="black", fg="white", font=("Helvetica", 12))
instruction_label.pack(pady=(10, 0))

bet_entry = tk.Entry(bet_page, font=("Helvetica", 14))
bet_entry.pack(pady=(10, 0))

email_label = tk.Label(bet_page, text="Enter your email:", bg="black", fg="white", font=("Helvetica", 12))
email_label.pack(pady=(10, 0))

email_entry = tk.Entry(bet_page, font=("Helvetica", 14))
email_entry.pack(pady=(10, 0))

bet_button = tk.Button(bet_page, text="Place Bet", bg="pink", fg="black", font=("Helvetica", 14), command=place_bet)
bet_button.pack(pady=(20, 0))

bet_page.pack(fill="both", expand=True)

# --- Game Page ---
game_page = tk.Frame(root, bg="black")
root.iconbitmap("das1.ico")

game_header = tk.Label(game_page, text="Slot Machine", bg="pink", fg="black", font=("Helvetica", 18, "bold"))
game_header.pack(fill=tk.X, pady=(0, 10))

scoreboard_label = tk.Label(game_page, text="Wins: 0 | Losses: 0 | Current Bet: ₹0", bg="black", fg="white", font=("Helvetica", 14))
scoreboard_label.pack(pady=(10, 0))

slot_frame = tk.Frame(game_page, bg="black")
slot_frame.pack(pady=30)

slot1_label = tk.Label(slot_frame, text="❄", bg="black", fg="white", font=("Helvetica", 48), relief=tk.RIDGE, width=4, height=2)
slot1_label.pack(side=tk.LEFT, padx=10)

slot2_label = tk.Label(slot_frame, text="🌼", bg="black", fg="white", font=("Helvetica", 48), relief=tk.RIDGE, width=4, height=2)
slot2_label.pack(side=tk.LEFT, padx=10)

slot3_label = tk.Label(slot_frame, text="🔥", bg="black", fg="white", font=("Helvetica", 48), relief=tk.RIDGE, width=4, height=2)
slot3_label.pack(side=tk.LEFT, padx=10)

handle_button = tk.Button(game_page, text="Punch To Play", bg="pink", fg="black", font=("Helvetica", 14), command=play_slot_machine)
handle_button.pack(pady=20)

result_label = tk.Label(game_page, text="", bg="black", fg="white", font=("Helvetica", 14))
result_label.pack(pady=10)

back_button = tk.Button(game_page, text="Go Back to Bet Page", bg="pink", fg="black", font=("Helvetica", 12), command=go_back_to_bet_page)
back_button.pack(pady=10)

# --- Math Quiz Page ---
math_quiz_page = tk.Frame(root, bg="black")
root.iconbitmap("das1.ico")

quiz_header = tk.Label(math_quiz_page, text="Quiz", bg="pink", fg="black", font=("Helvetica", 18, "bold"))
quiz_header.pack(fill=tk.X, pady=(0, 10))

questions = [
    "5 + 3 = ?", "12 - 4 = ?", "7 * 2 = ?", "15 / 3 = ?", "9 + 6 = ?"
]
answers = [8, 8, 14, 5, 15]
answer_entries = []

for question in questions:
    question_label = tk.Label(math_quiz_page, text=question, bg="black", fg="white", font=("Helvetica", 12))
    question_label.pack(pady=5)

    answer_entry = tk.Entry(math_quiz_page, font=("Helvetica", 14))
    answer_entry.pack(pady=5)
    answer_entries.append(answer_entry)

submit_button = tk.Button(math_quiz_page, text="Submit Answers", bg="pink", fg="black", font=("Helvetica", 14), command=check_answers)
submit_button.pack(pady=20)

# Run the application
root.mainloop()

