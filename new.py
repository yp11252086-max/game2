import random
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Game Configuration
GRID_SIZE = 10
NUM_MINES = 15


class Minesweeper:

    def __init__(self):
        self.size = GRID_SIZE
        self.num_mines = NUM_MINES
        self.reset()

    def reset(self):
        # Initialize an empty board (0 = empty)
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.mines = set()
        self._place_mines()
        self._calculate_numbers()

    def _place_mines(self):
        while len(self.mines) < self.num_mines:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)
            if (r, c) not in self.mines:
                self.mines.add((r, c))
                self.board[r][c] = "M"

    def _calculate_numbers(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == "M":
                    continue

                # Count mines in the 8 neighboring cells
                mine_count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.size and 0 <= nc < self.size:
                            if self.board[nr][nc] == "M":
                                mine_count += 1
                self.board[r][c] = mine_count


game = Minesweeper()


@app.route("/")
def index():
    # Renders the HTML file
    return render_template("index.html")


@app.route("/api/new_game", methods=["POST"])
def new_game():
    game.reset()
    return jsonify({"status": "ready", "size": game.size})


@app.route("/api/reveal", methods=["POST"])
def reveal():
    data = request.json
    r = data.get("r")
    c = data.get("c")

    if (r, c) in game.mines:
        return jsonify(
            {
                "result": "game_over",
                "mines": list(game.mines),
                "value": "M",
            }
        )

    return jsonify({"result": "safe", "value": game.board[r][c]})


if __name__ == "__main__":
    # Start the local Flask web server
    app.run(debug=True)
