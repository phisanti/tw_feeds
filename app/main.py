import argparse
from app.cli import start, run, stop, set_parameter, stop, create_config_file, show_config_file, add_boring_word

def command_args():

    """Command line arguments for the tweet analyser"""

    # Set up the command line arguments
    parser = argparse.ArgumentParser(description='Tweet analyser')
    subparsers  = parser.add_subparsers(dest='command')
    parser.add_argument('-s', '--start', help='Start the tweet analyser', action='store_true')
    parser.add_argument('-set', '--set_parameter',help='Set a parameter in the config file', action='store_true')
    parser.add_argument('-sp', '--stop', help='Stop the tweet analyser', action='store_true')
    parser.add_argument('-r', '--run', help='Run the tweet analyser', action='store_true')
    parser.add_argument('-c', '--create_config', help='Create a config file', action='store_true')
    parser.add_argument('-show', '--show_config', help='Show the config file', action='store_true') 
    parser.add_argument('-add', '--add_boring_word', help='Add words to the ignore list', action='store_true') 

    args = parser.parse_args()

    # Run the command
    if args.start:
        start()
    elif args.run:
        run()
    elif args.create_config:
        create_config_file()
    elif args.show_config:
        show_config_file()
    elif args.set_parameter:
        set_parameter()
    elif args.stop:
        stop()
    elif args.add_boring_word:
        add_boring_word()
    else:
        print("Command not recognised")

if __name__ == "__main__":
    command_args()