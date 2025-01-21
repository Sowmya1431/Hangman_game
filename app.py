from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session management

# Words dataset
words = ['apple', 'banana', 'grape', 'orange', 'mango', 
         'strawberry', 'blueberry', 'kiwi', 'pineapple', 
         'watermelon', 'peach', 'apricot', 'coconut',
         'pomegranate', 'blackberry', 'raspberry', 'cherry',
         'coil', 'coin', 'coke', 'cola', 'cold', 'colt', 
         'coma', 'comb', 'come', 'cone', 'conk', 'cons', 
         'cony', 'cook', 'cool', 'font', 'food', 'fool', 
         'foot', 'full', 'fume', 'fund', 'funs', 'joys', 
         'judo', 'jugs', 'sofa', 'soft', 'soil', 'sold', 
         'sole', 'solo', 'some', 'song', 'sons', 'soon', 
         'piece', 'pipes', 'price', 'roams', 'roans', 
         'roars', 'roast', 'robes', 'robed', 'robin', 
         'robot', 'rocks', 'rocky', 'skirt', 'skits', 
         'yummy', 'angers', 'angina', 'angled', 'angler', 
         'angles']

# Route: Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Route: Start Game
@app.route("/start")
def start_game():
    word = random.choice(words)
    guessed = ["_" for _ in word]
    guessed_letters = []
    attempts = 6

    # Reveal two random letters
    for _ in range(2):
        index = random.randint(0, len(word) - 1)
        guessed[index] = word[index]

    # Store game state in session
    session["word"] = word
    session["guessed"] = guessed
    session["guessed_letters"] = guessed_letters
    session["attempts"] = attempts

    return redirect(url_for("game"))

# Route: Game Page
@app.route("/game", methods=["GET", "POST"])
def game():
    if request.method == "POST":
        guess = request.form.get("guess").lower()
        guessed_letters = session.get("guessed_letters", [])
        word = session.get("word", "")
        guessed = session.get("guessed", [])
        attempts = session.get("attempts", 6)

        if guess in guessed_letters:
            message = "You already guessed that letter!"
        else:
            guessed_letters.append(guess)
            if guess in word:
                for index, letter in enumerate(word):
                    if letter == guess:
                        guessed[index] = guess
                message = "Good guess!"
            else:
                attempts -= 1
                message = "Wrong guess!"

        # Update session
        session["guessed_letters"] = guessed_letters
        session["guessed"] = guessed
        session["attempts"] = attempts

        if "_" not in guessed:
            return render_template("game.html", guessed=guessed, attempts=attempts, message="You win!", word=word)
        elif attempts == 0:
            return render_template("game.html", guessed=guessed, attempts=0, message="Game over!", word=word)

        return render_template("game.html", guessed=guessed, attempts=attempts, message=message)

    # GET request: Display game page
    return render_template("game.html",guessed=session.get("guessed", []), attempts=session.get("attempts", 6),message="")

if __name__ == "__main__":
    app.run(debug=True)
