import json
from app.modules.command_module import Commands
from unidecode import unidecode


class Check:
    def stopNext(dataMessage):
        stopNextMessages = json.loads(
            open("./src/config/StopNext.json").read())["keywords"]
        for word in stopNextMessages:
            if word == dataMessage.lower():
                return True

        return False

    def isCommand(name):
        command = Commands()
        if hasattr(command, name.lower()):
            return getattr(command, name.lower())

    def findContext(dataMessage):
        Options = json.loads(
            open("./src/config/Commands.json").read())

        dataMessage = unidecode(dataMessage).lower()

        for Option in Options:
            if Option["index"] == dataMessage:
                return Check.isCommand(Option["command"])

            for wordOption in Option["keysWords"]:
                if wordOption in dataMessage:
                    return Check.isCommand(Option["command"])
