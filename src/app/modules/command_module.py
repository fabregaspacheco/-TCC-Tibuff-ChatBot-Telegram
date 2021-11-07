import json

import requests
from app.helpers.findFile_helper import findFile
from app.modules import chat_module
from config import BOT, BASE_URL_API


class Commands:
    def __init__(self):
        self.chat = chat_module.Chat
        self.findFile = findFile
        self.servicosList = json.loads(open("src/config/Servicos.json").read())

    # 0
    async def start(self, data):
        await BOT.send_message(data.id, self.findFile("start", "instruction"))
        return await BOT.send_message(data.id, self.findFile("cancelar", "instruction"))

    # 1
    async def pc(self, data):
        await BOT.send_message(data.id, self.findFile("pc", "instruction"))
        await BOT.send_message(data.id, self.findFile("cancelar", "instruction"))
        response_client = await self.chat.waitNewMessageClient(data.id)
        if not response_client:
            return await BOT.send_message(data.id, self.findFile("recomecar", "sucess"))

        if await self.chat.sendSupportMessage(data, response_client, "SUPPORT_CHANNEL_VENDAS"):
            return await BOT.send_message(data.id, self.findFile("pc", "sucess"))

    # 2
    async def promocao(self, data):
        await BOT.send_message(data.id, self.findFile("promocao", "instruction"))
        await BOT.send_message(data.id, self.findFile("cancelar", "instruction"))
        while True:
            response_client = await self.chat.waitNewMessageClient(data.id)
            response_client = response_client.lower()

            if response_client:
                if "1" in response_client or "procurar" in response_client:
                    await BOT.send_message(data.id, self.findFile("promocao_buscar", "instruction"))
                    search = await self.chat.waitNewMessageClient(data.id)
                    response = requests.post(
                        f"{BASE_URL_API}telegram/promocao?search={search}")
                    await BOT.send_message(data.id, response.json()["message"])
                    break
                elif "2" in response_client or "todas" in response_client:
                    response = requests.post(
                        f"{BASE_URL_API}telegram/promocao")
                    await BOT.send_message(data.id, response.json()["message"])
                    break

            await BOT.send_message(data.id, self.findFile("escolha_opcao", "error"))

        return await BOT.send_message(data.id, self.findFile("recomecar", "sucess"))

    # 3

    async def servicos(self, data):
        await BOT.send_message(data.id, self.findFile("servicos", "instruction"))
        await BOT.send_message(data.id, self.findFile("cancelar", "instruction"))

        servicos_pedidos = []

        while True:
            response_client = await self.chat.waitNewMessageClient(data.id)
            if not response_client:
                return await BOT.send_message(data.id, self.findFile("recomecar", "sucess"))

            if response_client.isnumeric():
                response_client = int(response_client)
                if response_client >= 1 and response_client <= len(self.servicosList):
                    for option in self.servicosList:
                        if option["key"] == response_client:
                            message = f"Produto:{option['name']}, descricao: {option['description']}"
                            servicos_pedidos.append(message)

                    await BOT.send_message(data.id, self.findFile("adicionar_outro", "instruction"))
                    adicionar_outro = await self.chat.waitNewMessageClient(data.id)

                    if adicionar_outro and "n" in adicionar_outro.lower() or "continuar" in adicionar_outro.lower():
                        break

            await BOT.send_message(data.id, self.findFile("escolha_opcao", "error"))

        if servicos_pedidos:
            servicos_pedidos_string = str("/n ").join(servicos_pedidos)
            while True:

                await BOT.send_message(data.id, self.findFile("acionar_time_de_vendas", "instruction"))
                response_client_send_to_team_vendas = await self.chat.waitNewMessageClient(data.id)
                response_client_send_to_team_vendas = response_client_send_to_team_vendas.lower()
                response = None

                if response_client_send_to_team_vendas:
                    if "s" in response_client_send_to_team_vendas:
                        response = self.findFile(
                            "acionar_time_de_vendas", "sucess")
                        send_to_support = await self.chat.sendSupportMessage(data, servicos_pedidos_string, "SUPPORT_CHANNEL_VENDAS")
                    elif "n" in response_client_send_to_team_vendas:
                        response = self.findFile(
                            "nao_adionar_time_de_vendas", "sucess")

                    if not send_to_support:
                        break

                    if response:
                        await BOT.send_message(data.id, response)
                        break

                    await BOT.send_message(data.id, self.findFile("sim_nao", "error"))
                else:
                    return await BOT.send_message(data.id, self.findFile("recomecar", "sucess"))

    # 4
    async def garantia(self, data):
        await BOT.send_message(data.id, self.findFile("garantia", "instruction"))
        await BOT.send_message(data.id, self.findFile("cancelar", "instruction"))

        while True:
            response_client = await self.chat.waitNewMessageClient(data.id)
            if not response_client:
                return await BOT.send_message(data.id, self.findFile("recomecar", "sucess"))

            response_client = response_client.lower()
            response = None

            if "s" in response_client:
                response = self.findFile("garantia_uberlandia", "sucess")
            elif "n" in response_client:
                response = self.findFile("garantia_fora", "sucess")

            if response:
                await BOT.send_message(data.id, response)
                break

            await BOT.send_message(data.id, self.findFile("sim_nao", "error"))

    # 5
    async def contato(self,  data):
        await BOT.send_message(data.id, self.findFile("contato", "instruction"))
        await BOT.send_message(data.id, self.findFile("cancelar", "instruction"))
        response_client = await self.chat.waitNewMessageClient(data.id)
        if not response_client:
            return await BOT.send_message(data.id, self.findFile("recomecar", "sucess"))

        if await self.chat.sendSupportMessage(data, response_client, "SUPPORT_CHANNEL_CONTATO"):
            return await BOT.send_message(data.id, self.findFile("contato", "sucess"))

    # 6
    async def suporte(self, data):
        await BOT.send_message(data.id, self.findFile("suporte", "instruction"))
        await BOT.send_message(data.id, self.findFile("cancelar", "instruction"))
        response_client = await self.chat.waitNewMessageClient(data.id)
        if not response_client:
            return await BOT.send_message(data.id, self.findFile("recomecar", "sucess"))

        if await self.chat.sendSupportMessage(data, response_client, "SUPPORT_CHANNEL_GERAL"):
            return await BOT.send_message(data.id, self.findFile("suporte", "sucess"))
