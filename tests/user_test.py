import logging

from flaskApp import db
from flaskApp.db.models import User, Song


def test_adding_user(application, add_user):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 1
        assert db.session.query(Song).count() == 0
        #showing how to add a record
        #create a record
        #user = User('keith@webizly.com', 'testtest')
        #add it to get ready to be committed
        #db.session.add(user)
        #call the commit
        #db.session.commit()
        #assert that we now have a new user
        #assert db.session.query(User).count() == 1

        #finding one user record by email
        user = User.query.filter_by(email='kc446@njit.edu').first()
        log.info(user)
        #asserting that the user retrieved is correct
        assert user.email == 'kc446@njit.edu'
        #this is how you get a related record ready for insert
        user.songs= [Song("test", "Someone"),Song("test2", "Someone Else")]
        #commit is what saves the songs
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='test',artist='Someone').first()
        assert song1.title == "test"
        assert song1.artist == "Someone"
        #changing the title of the song
        song1.title = "SuperSongTitle"
        song1.artist = "Someone Else"
        #saving the new title of the song
        db.session.commit()
        song2 = Song.query.filter_by(title='SuperSongTitle',artist='Someone Else').first()
        assert song2.title == "SuperSongTitle"
        assert song2.artist == "Someone Else"
        #checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0




