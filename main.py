import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
import requests
import random

class ResultDialog(QDialog):
    """
    Dialog to display the result.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Result')
        self.layout = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # Add fade-in animation for the result dialog
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(1000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)
        self.anim.start()

    def set_result(self, result):
        """
        Set the result text.

        Args:
            result (str): The text to be displayed.
        """
        self.label.setText(result)


class ChessInfoApp(QWidget):
    """
    Main application widget.
    """
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI.
        """
        layout = QVBoxLayout()

        # Chess.com Username Label
        self.username_label = QLabel('Chess.com Username:', self)
        self.username_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Entry field for username
        self.username_entry = QLineEdit(self)

        # Button to get info
        self.btn_get_info = QPushButton('Get Info', self)
        self.btn_get_info.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px 20px; border: none;"
            "border-radius: 5px;")

        # Button to suggest tactic
        self.btn_suggest_tactic = QPushButton('Suggest Tactic', self)
        self.btn_suggest_tactic.setStyleSheet(
            "background-color: #FFC107; color: white; font-weight: bold; padding: 10px 20px; border: none;"
            "border-radius: 5px;")

        self.btn_get_info.clicked.connect(self.get_user_info)
        self.btn_suggest_tactic.clicked.connect(self.suggest_tactic)

        layout.addWidget(self.username_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.btn_get_info, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_suggest_tactic, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # Add fade-in animation for the main widget
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(1000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)
        self.anim.start()

        # Add animation for the button
        self.anim_button = QPropertyAnimation(self.btn_get_info, b"geometry")
        self.anim_button.setDuration(200)
        self.anim_button.setStartValue(self.btn_get_info.geometry())
        self.anim_button.setEndValue(self.btn_get_info.geometry().adjusted(-10, -10, 10, 10))

    def get_user_info(self):
        """
        Get and display the user's info when the button is clicked.
        """
        username = self.username_entry.text()

        if not username:
            self.show_error_message("Please enter a username")
            return

        url = f"https://api.chess.com/pub/player/{username}/stats"

        headers = {
            "User-Agent": "MyChessApp (fla2021)"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            rating = data['chess_blitz']['last']['rating']
            self.show_result(f"The rating for {username} is {rating}")
        else:
            self.show_error_message(f"Error {response.status_code}")

    def suggest_tactic(self):
        """
        Suggest a tactic based on user's ratings.
        """
        username = self.username_entry.text()

        if not username:
            self.show_error_message("Please enter a username")
            return

        url = f"https://api.chess.com/pub/player/{username}/stats"

        headers = {
            "User-Agent": "MyChessApp (robfertoyan)"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            bullet_rating = data['chess_bullet']['last']['rating']
            blitz_rating = data['chess_blitz']['last']['rating']

            tactic = self.get_tactic(bullet_rating, blitz_rating)
            self.show_result(f"Suggested Tactic: {tactic}")
        else:
            self.show_error_message(f"Error {response.status_code}")

    def get_tactic(self, bullet_rating, blitz_rating):
        """
        Get a tactic suggestion based on ratings.

        Args:
            bullet_rating (int): The user's bullet rating.
            blitz_rating (int): The user's blitz rating.

        Returns:
            str: The suggested tactic.
        """
        opening_suggestions = {
            "Aggressive": [
                "1.e4 e5 2.Nf3 Nc6 3.Bb5 f5 (Ruy Lopez, Morphy Defense)",
                "1.e4 e5 2.Nf3 Nc6 3.d4 exd4 4.Bc4 (Scotch Game)"
            ],
            "Stable": [
                "1.e4 e5 2.Nf3 Nc6 3.d4 exd4 (Scotch Game)",
                "1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Ba4 Nf6 (Ruy Lopez, Berlin Defense)"
            ]
        }

        if blitz_rating > bullet_rating:
            tactic_type = "Aggressive"
        elif blitz_rating < bullet_rating:
            tactic_type = "Stable"
        else:
            return "No specific opening suggestion"

        return random.choice(opening_suggestions[tactic_type])

    def show_result(self, result):
        """
        Display the result in a dialog.

        Args:
            result (str): The result text.
        """
        dialog = ResultDialog(self)
        dialog.set_result(result)
        dialog.exec_()

    def show_error_message(self, message):
        """
        Display an error message in a dialog.

        Args:
            message (str): The error message.
        """
        dialog = ResultDialog(self)
        dialog.set_result(message)
        dialog.exec_()

    def resizeEvent(self, event):
        """
        Adjust button animation on resize.

        Args:
            event: The resize event.
        """
        self.anim_button.setStartValue(self.btn_get_info.geometry())
        self.anim_button.setEndValue(self.btn_get_info.geometry().adjusted(-10, -10, 10, 10))
        self.anim_button.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChessInfoApp()

    # Set a fixed window size
    ex.setFixedSize(400, 200)

    ex.setWindowTitle('Chess.com Info')
    ex.show()
    sys.exit(app.exec_())
