from unittest import TestCase
from flask import session, json
from app import app

class FlaskBoggleTests(TestCase):

    def setUp(self):
        """Setup before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_game_page_html(self):
    
        with self.client as client:
            response = client.get('/game')  
            self.assertIn('board', session)
            self.assertIn(b'score:', response.data.lower())  
            self.assertIn(b'<span id=timer>', response.data)  
            self.assertIn(b'id="times-played"', response.data)  
            self.assertIn(b'id="highest-score"', response.data)  



    def test_valid_word_on_board(self):
        """Test submission of a valid word using a predefined board."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
            response = client.post('/check-word', json={'guess': 'cat'})
            self.assertEqual(response.get_json()['result'], 'ok')

    def test_word_not_on_board(self):
        """Test submission of a word not on the predefined board."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
            response = client.post('/check-word', json={'guess': 'dog'})
            self.assertEqual(response.get_json()['result'], 'not-on-board')

    def test_non_english_word(self):
        """Test submission of a non-English word on the predefined board."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
            response = client.post('/check-word', json={'guess': 'fsjdakfkldsfjdslkfjdlksf'})
            self.assertEqual(response.get_json()['result'], 'not-word')
