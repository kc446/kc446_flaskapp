def test_development_config(application):
    application.config.from_object('flaskApp.config.DevelopmentConfig')

    assert application.config['DEBUG']
    assert not application.config['TESTING']

def test_testing_config(application):
    application.config.from_object('flaskApp.config.TestingConfig')
    assert application.config['DEBUG']
    assert application.config['TESTING']
    assert not application.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert application.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///'

def test_production_config(application):
    application.config.from_object('flaskApp.config.ProductionConfig')
    assert not application.config['DEBUG']
    assert not application.config['TESTING']