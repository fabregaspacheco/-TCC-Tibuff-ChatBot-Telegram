from app.modules.check_module import Check
from app.helpers.findFile_helper import findFile
from config import BOT, SUPPORT_CHANNEL_CONTATO, SUPPORT_CHANNEL_GERAL, SUPPORT_CHANNEL_VENDAS, BASE_URL_API
from telethon import events, types
import requests as Requests
import asyncio


class Chat:
    async def sendSupportMessage(data, data_message, channel):
        try:
            channel: int
            message = None
            link = f"[Visitar perfil de {data.first_name}](tg://user?id={data.id})"

            if "SUPPORT_CHANNEL_GERAL" == channel:
                _channel = SUPPORT_CHANNEL_GERAL
                message = f'''O usuário **{data.first_name}**, acabou de pedir a nossa ajuda:
                                    \n- Duvida: {data_message}
                                    \n- {link}
                                '''
            elif "SUPPORT_CHANNEL_CONTATO" == channel:
                _channel = SUPPORT_CHANNEL_CONTATO
                message = f'''O usuário **{data.first_name}**, esta realizando uma proposta:
                                    \n- Proposta:{data_message}
                                    \n- {link}
                                '''

            elif "SUPPORT_CHANNEL_VENDAS" == channel:
                _channel = SUPPORT_CHANNEL_VENDAS
                message = f'''O usuário **{data.first_name}**, esta precisando precisando de ajuda para comprar um de nossos servicos:
                                    \n- Contexto: {data_message}
                                    \n- {link}
                                '''

            if message and _channel:
                asyncio.create_task(BOT.send_message(
                    types.PeerChat(int(_channel)), message))
                return True

        except:
            Requests.post(
                f"{BASE_URL_API}telegram/off/{data.id}")
            await BOT.send_message(data.id, findFile("mensagem_suporte", "error"))

    async def waitNewMessageClient(chatId):
        try:

            async with BOT.conversation(int(chatId), timeout=60*15) as waitChatMessage:
                event = waitChatMessage.wait_event(
                    event=events.NewMessage(), timeout=60*15)
                resolvedEvent = await event
                chatResponse = resolvedEvent.raw_text

                if not Check.stopNext(chatResponse):
                    return chatResponse
        except:
            Requests.post(
                f"{BASE_URL_API}telegram/off/{chatId}")

    async def slashCommand(data):
        Requests.post(
            f"{BASE_URL_API}telegram/on/{data['client'].id}")

        commandName: str = data["dialog"].split()[0].replace("/", "")
        if len(commandName) >= 1:
            command = Check.isCommand(commandName)
            if command:
                await command(data["client"])

        return Requests.post(
            f"{BASE_URL_API}telegram/off/{data['client'].id}")

    async def contextCommand(data):
        Requests.post(
            f"{BASE_URL_API}telegram/on/{data['client'].id}")

        command = Check.findContext(data["dialog"])
        if command:
            await command(data["client"])

        return Requests.post(
            f"{BASE_URL_API}telegram/off/{data['client'].id}")
