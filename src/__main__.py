from app.modules.chat_module import Chat
from config import BOT, BOT_TOKEN, BASE_URL_API
from telethon import events
import requests as Requests


class TibuffBot:
    def __init__(self):
        try:
            print("Configurando...")
            if BOT == None or BOT_TOKEN == None:
                return print("É preciso configurar o bot!")

            BOT.start(bot_token=BOT_TOKEN)
            print("Configurado")
        except:
            return print("Houve um erro, tente rodar novamente, se o erro persistir entre em contato com antonio.oficialcontato@gmai.com, com assunto 'Sistema com erro persistente'.")

    def run(self):
        self.inicializeChat()
        BOT.run_until_disconnected()

    def inicializeChat(self):
        print("Inicicializado Sistema de obvervação de chat")

        @BOT.on(events.NewMessage)
        async def globalChatReader(event):
            data = {
                "dialog": event.raw_text,
                "client": await event.get_sender()
            }

            try:
                response = Requests.post(
                    f"{BASE_URL_API}telegram/check/{data['client'].id}")

                if response.json()["message"] != "User actived":
                    if "/" in data["dialog"][0]:
                        return await Chat.slashCommand(data)

                    return await Chat.contextCommand(data)

            except:
                Requests.post(
                    f"{BASE_URL_API}telegram/off/{data['client'].id}")
                return await BOT.send_message(data["client"].id, "Houve algum erro inesperado tente utilizar o comando novamente novamente, se o error persistir entre em contato, com  @Tibuff")


if __name__ == "__main__":
    TibuffBot().run()
