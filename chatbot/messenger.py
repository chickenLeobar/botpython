import os

from fbmessenger import BaseMessenger
from fbmessenger.templates import GenericTemplate
from fbmessenger import elements, templates, sender_actions

from utils import find_all_words , similar
from bot.initialize import chat_bot
import requests
import  os
import json
from fbmessenger.thread_settings import (
    GreetingText,
    GetStartedButton,
    PersistentMenuItem,
    PersistentMenu
)

print(os.path.abspath("chatbot/data.json"))

def match_words(words: list, sentence):
    return len(find_all_words(words, sentence)) > 0


def respond_products(client: BaseMessenger):
    def get_element_product(pr: dict) -> elements.Element:
        btn = elements.Button(title='Comprar', button_type="web_url", url='http://facebook.com')
        elems = elements.Element(
            title=pr['name'],
            item_url=pr['url'],
            image_url=pr['image'],
            subtitle=pr['description'],
            buttons=[
                btn
            ]
        )
        return elems

    with open(os.path.abspath("chatbot/data.json"),'r') as my_file:
        data = json.loads(my_file.read())

    products = data['products']
    template = templates.GenericTemplate(elements=[get_element_product(product) for product in products])

    client.send(template.to_dict())


def initialize_menu():
    btn = elements.Button(title='ver productos 📦', button_type="postback", payload="show_products")
    btn2 = elements.Button(title='Hablar con un bot 🤖 ', button_type="postback", payload="talking_bot")
    elems = elements.Element(
        title='Aquinomas',
        item_url='http://facebook.com',
        image_url='https://source.unsplash.com/random',
        subtitle='Elige la acción que mas te parezca',
        buttons=[
            btn,
            btn2,
        ]
    )
    res = templates.GenericTemplate(elements=[elems])
    return res.to_dict()


def only_text(text, cliente: BaseMessenger):
    print("text here")
    print(text)
    print(similar("muestrame los productos" , text))
    if match_words(['salir', "menu" , "Empezar"], text):
        cliente.send(initialize_menu(), 'RESPONSE')

    elif match_words(['productos' , "reomindame productos" , "tienda"] , text):
        respond_products(cliente)
    else:
        typing_on = sender_actions.SenderAction(sender_action="typing_on")
        cliente.send(typing_on.to_dict())
        resp = chat_bot.get_response(text)
        typing_off = sender_actions.SenderAction(sender_action="typing_off")
        cliente.send(typing_off.to_dict())
        cliente.send(elements.Text(str(resp)).to_dict())


class Messenger(BaseMessenger):
    def __init__(self, page_access_token):
        self.page_access_token = page_access_token

        super(Messenger, self).__init__(self.page_access_token)
        self.init_bot()

    def message(self, message):
        print(message)
        if 'text' in message['message']:
            text = message['message']['text']
            only_text(str(text), self)

        # if match_words([''])

    def delivery(self, message):
        pass

    def read(self, message):
        pass

    def account_linking(self, message):
        pass

    def postback(self, message):
        print("post back detected")
        payload = message['postback']['payload']
        print(payload)
        if 'talking_bot' in payload:
            print("payload exist")
            txt = "Desde ahora, se econtrara hablando con nuestro bot 🤖Para salir del hilo use las palabra clave : salir"
            self.send(elements.Text(txt).to_dict(), 'RESPONSE')
        if 'show_products' in payload:
            respond_products(self)


    def optin(self, message):
        pass

    def init_bot(self):

        self.add_whitelisted_domains('https://facebook.com/')
        greeting = GreetingText(text='Bienvenido a  mi bot :)')
        self.set_messenger_profile(greeting.to_dict())
        get_started = GetStartedButton(payload='start')
        self.set_messenger_profile(get_started.to_dict())

        menu_item_1 = PersistentMenuItem(
            item_type='postback',
            title='Productos',
            payload='show_products',
        )
        menu_item_2 = PersistentMenuItem(
            item_type='postback',
            title='Hablar con un bot',
            payload="talking_bot"
        )
        persistent_menu = PersistentMenu(menu_items=[
            menu_item_1,
            menu_item_2
        ])

        res = self.set_messenger_profile(persistent_menu.to_dict())
