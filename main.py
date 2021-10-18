import hodlBot
from time import sleep


def main():
    bot = hodlBot.HodlBot()
    while True:
        sleep(2)
        bot.start_loading_information()


main()
