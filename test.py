from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import json




class AppTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

    def test_game_board(self):
        """Test game page launch"""
        with app.test_client() as client:
            res = client.get('/boggle')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<label for="submitted-word">Submit Word:</label><br>',html)


    def test_handle_highScore(self):
        """test highscore handling"""
        with app.test_client() as client:
            data = {'score': 15}
            headers = {'Content-Type': 'application/json'}
            res = client.post('/game-end', data=json.dumps(data), headers=headers)
            response_data = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertIn('brokeRecord', response_data)


    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-word')


    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')





    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')


    def test_word_submit(self):
        """test word submission"""
        self.client.get('/')
        res = self.client.get('/check-word?word=bacon')

        self.assertEqual(res.status_code, 200)

