from importlib import reload

import bot


def affr(stuff):
    print("[HNDL] {}".format(stuff))


def askinput(stuff):
    return input("[HNDL] {} ".format(stuff))

tokenf = open('token/token', 'r')
token = tokenf.read().strip()
tokenf.close()

while True:
    act = askinput("Action?")
    if act == "r":
        reload(bot)
    elif act == "m":
        try:
            bot.main(token)
        except KeyboardInterrupt:
            pass
        affr("End of exec.")
    elif act == "q":
        affr("End of handler exec.")
        break

