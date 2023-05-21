from unittest import TestCase
from app import app
from flask import session, request
from boggle import Boggle

app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]
app.app_context().push()
boggle_board = ""
word = ""
high_score = 23


class FlaskTests(TestCase):
    @classmethod
    def setUpClass(cls):
        with app.test_client() as client:
            global boggle_board
            boggle_board = [["A", "C", "B", "D", "E"], ["A", "C", "B", "D", "E"], [
                "A", "C", "B", "D", "E"], ["A", "C", "B", "D", "E"], ["H", "E", "L", "L", "O"]]
            global high_score
            high_score = 23
            global word
            word = "hello"
    # I tried session["board"] = what I have, session["high_score"] = 23!
    # Those didn't work and returned a "RuntimeError: Working outside of request context." error
    # I tried setUp and tearDown and now setUpClass

    # TODO -- write tests for every view function / feature!

    def test_check_work(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>BOGGLE TIME!!!!!!!!!!</h1>", html)

    def test_word_check(self):
        with app.test_client() as client:
            res = client.get("/")
            # html = res.get_data(as_text=True)
            request.args["word"] = "hello"
            
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.request.args["word"], "hello")

    def test_word_in_board(self):
        with app.test_client() as client:
            res = client.get("/")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(Boggle.check_valid_word(
                session["boggle_board"], word), request.args["word"])

    def test_highscore(self):
        with app.test_client() as client:
            res = client.get("/")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session["high_score"], 23)
