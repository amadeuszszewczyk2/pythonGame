from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

plansza = [[" " for _ in range(3)] for _ in range(3)]
gracz = "X"


@app.route("/")
def index():
    return render_template("index.html", plansza=plansza)


@app.route("/gra", methods=["POST"])
def wykonaj_ruch():
    global gracz
    wiersz = int(request.form["wiersz"])
    kolumna = int(request.form["kolumna"])

    if plansza[wiersz][kolumna] == " ":
        plansza[wiersz][kolumna] = gracz

        if czy_wygrana(plansza, gracz):
            return jsonify(
                {
                    "komunikat": f"Gracz {gracz} wygrał!",
                    "wygrana": True,
                    "plansza": plansza,
                }
            )

        if czy_remis(plansza):
            return jsonify({"komunikat": "Remis!", "remis": True, "plansza": plansza})

        gracz = "O" if gracz == "X" else "X"
        return jsonify(
            {"komunikat": "", "wygrana": False, "remis": False, "plansza": plansza}
        )
    else:
        return jsonify(
            {
                "komunikat": "To pole jest już zajęte.",
                "wygrana": False,
                "remis": False,
                "plansza": plansza,
            }
        )


def czy_wygrana(plansza, znak):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if (plansza[i][0] == plansza[i][1] == plansza[i][2] == znak) or (
            plansza[0][i] == plansza[1][i] == plansza[2][i] == znak
        ):
            return True

    if (plansza[0][0] == plansza[1][1] == plansza[2][2] == znak) or (
        plansza[0][2] == plansza[1][1] == plansza[2][0] == znak
    ):
        return True

    return False


def czy_remis(plansza):
    for i in range(3):
        for j in range(3):
            if plansza[i][j] == " ":
                return False
    return True


if __name__ == "__main__":
    app.run(debug=True)
