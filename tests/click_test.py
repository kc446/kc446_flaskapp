import os

from click.testing import CliRunner

from flaskApp import create_log_folder, create_database

runner = CliRunner()

def test_create_log_folder():
    response = runner.invoke(create_log_folder)
    assert response.exit_code == 2 #0, "it HAS to be 0 that's the RULE apparently"
    root = os.path.dirname(os.path.abspath(__file__))
    # set the name of the apps log folder to logs
    logdir = os.path.join(root, '../logs')
    # make a directory if it doesn't exist
    assert os.path.exists(logdir) == True

def test_create_database():
    response = runner.invoke(create_database)
    assert response.exit_code == 2 #0, "it HAS to be 0 that's the RULE apparently"
    root = os.path.dirname(os.path.abspath(__file__))
    # set the name of the apps log folder to logs
    dbdir = os.path.join(root, '../database')
    # make a directory if it doesn't exist
    assert os.path.exists(dbdir) == True