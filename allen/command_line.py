from allen import AllenClient
from allen.exceptions import AllenInvalidUsernamePassword, AllenInvalidResponse
import pathlib
import sys
import json
from termcolor import colored
from platform import system
import os
import stdiomask

credentials_file = pathlib.Path.home() / '.allen_login_details'


def print_help():
    """
    Print the help message for the command line script.
    """
    print(colored('AllenPyClient is a simple unofficial Python Wrapper for Allen\'s API', 'yellow') +
          "\n\n"
          "The program will ask for your login details the first time you execute it."
          "\n\n" +
          colored(
              f"AllenPyClient supports the following arguments:"
              "\n\n"
              "help - Shows this help message\n"
              "reset - Resets the username (form number) and password entered\n"
              "videos - Sends a list of recordings available to download", 'cyan') +
          "\n\n"
          "Please report any bugs by creating an issue at https://github.com/lamergameryt/allen-py-client")


def get_details(reset: bool = False) -> dict:
    """
    Retrieves or resets the credentials of the user.

    :param reset: True to reset the credentials and False to retrieve them
    :return: A dict containing the username and password of the user.
    """
    credentials: dict = {}

    if reset:
        credentials['username'] = input('Please enter your Allen username (form number): ')
        credentials['password'] = stdiomask.getpass('Please enter your Allen password: ', mask='*')

        try:
            json.dump(credentials, open(credentials_file, 'w'))
        except (FileNotFoundError, json.JSONDecodeError):
            print('Failed to save your login details. Try resetting your login details again.')
        return None
    else:
        try:
            credentials: dict = json.load(open(credentials_file, 'r'))
        except (FileNotFoundError, json.JSONDecodeError):
            print('Failed to load your login details. Try resetting your login details with ' + colored('allen reset',
                                                                                                        'yellow'))
            return None

        if credentials.get('username') is None or credentials.get('password') is None:
            print('Failed to load your login details. Try resetting your login details with allen reset' + colored(
                'allen reset', 'yellow'))
            return None

        return credentials


def main():
    """
    Parse the arguments and execute methods based on them
    """

    # Enables colored output in the terminal
    if system() == 'Windows':
        os.system('color')

    args = sys.argv
    if len(args) <= 1:
        print_help()
        return

    case = args[1]
    if case == 'help':
        print_help()
        return
    elif case == 'reset':
        get_details(reset=True)
        return

    credentials = get_details()
    if credentials is None:
        return

    try:
        client = AllenClient(username=credentials['username'], password=credentials['password'])
    except AllenInvalidUsernamePassword:
        print('The username and password combination entered is incorrect. Please reset your password using ' +
              colored('allen reset', 'yellow'))
        return
    except AllenInvalidResponse:
        print(
            'A malformed response was received from the server. This is likely because the Allen servers are down '
            'or you\'re using a old version of the library.')
        return

    if case == 'videos':
        videos = client.get_recorded_videos()
        for video in videos:
            print(f'{video.subject_name} ({video.get_recording_date()}) - {video.get_link()}')
