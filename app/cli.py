import os
import dotenv
from app.tweet_reporter import trigger_tweet_report

def run():
    """ Triggers the tweet analyser."""

    dotenv_path='.env'
    config = dotenv.dotenv_values(dotenv_path)
    config_check = check_config_file(dotenv_path, config)
    if config_check:
        dotenv.set_key(dotenv_path, 'RUN', 'True')
        trigger_tweet_report(config)

    return True

def check_config_file(dotenv_path, config):
    """ Check if all values in the config file exist.
    :param dotenv_path: Path to the config file.
    """
    for key in config.keys():
        if config[key] == '':
            
            return False

    return True

def add_boring_word() -> bool:
    """ Add a boring word to the boring list."""

    word = input("Please enter a boring word: ")
    with open('app/datafiles/boring_words.txt', 'a') as f:
        f.write(word)
    
    return True

def show_config_file():
    """ Show the config file."""

    if os.path.exists('.env'):
        dotenv_path='.env'
        config = dotenv.dotenv_values(dotenv_path)
        for key in config.keys():
            print(f'{key} : {config[key]}')
    else:
        print('Config file not found')

    return True

def create_config_file():
    """ Create a config file with the minimum required fields."""

    config = {'API_KEY' : '', 
              'API_KEY_SECRET' : '',
              'BEARER_TOKEN' : '',
              'ACCESS_TOKEN' : '',
              'ACCESS_SECRET' : '',
              'CLIENT_SECRET' : '',
              'LIST_ID' : '',
              'SENDER_EMAIL' : '',
              'RECEIVER_EMAIL' : '',
              'EMAIL_PASSWORD' : '',
              'NTWEETS' : 1000,
              'RUN' : 'True'
              }
    
    if os.path.exists('.env'):
        print('Config file already exists')
    else:
        print('Config file not found, creating a new one')
        for key in config.keys():
            if config[key] == '':
                answer=input(f'Please fill the {key} value in the config file: ')
                dotenv.set_key('.env', key, answer)
        print('Config file created')

    return True

def start() -> bool:
    """ Start the tweet analyser."""

    input("Welcome to the tweeter analyser. Let me check if the config file is ready")

    if os.path.exists('.env'):
        dotenv_path='.env'
        config = dotenv.dotenv_values(dotenv_path)
        config_check = check_config_file(dotenv_path, config)
        runtime=24
    else:
        create_config_file()
    
    if config_check  == True:
        print("Config file is ready, triggering a run now, next run will be in {} hours".format(runtime))
        dotenv.set_key(dotenv_path, 'RUN', 'True')
        run()
    else:
        for key in config.keys():
            if config[key] == '':
                answer=input(f'Please fill the {key} value in the config file: ')
                dotenv.set_key(dotenv_path, key, answer)
        print("Config file is ready, triggering a run now, next run will be in {} hours".format(runtime))
    
    return True

def set_parameter() -> bool:
    """ Set a parameter in the config file."""

    dotenv_path='.env'
    config = dotenv.dotenv_values(dotenv_path)
    config_check = check_config_file(dotenv_path, config)
    
    if config_check  == True:
        for key in config.keys():
            print(key)
        answer=input('Please select the parameter you want to change: ')
        if answer in config.keys():
            new_value=input('Please enter the new value: ')
            dotenv.set_key(dotenv_path, answer, new_value)
            print("Parameter has been changed")
        else:
            print("Parameter does not exist")
    else:
        print("Config file is not ready, please run the start command first")
    return True

def stop() -> bool:
    """"Set the Running argument to false"""
    dotenv_path='.env'
    config = dotenv.dotenv_values(dotenv_path)
    config_check = check_config_file(dotenv_path, config)
    
    if config_check  == True:
        dotenv.set_key(dotenv_path, 'Running', 'False')
        print("The tweet analyser has been stopped")
    else:
        print("Config file is not ready, please run the start command first")
    return True