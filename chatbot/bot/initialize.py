from chatterbot import ChatBot

from chatterbot.trainers import ListTrainer

chat_bot = ChatBot(
    'Charlie',
    default_response=['Lo siento no te he entendido,Sigo aprendiendo :(' ,'Puedes escribir menú, para ver que opciones tenemos para ti'],
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri="sqlite:///bd.sqlite",
    logic_adapters= [
        'chatterbot.logic.BestMatch',
        'bot.faq_adapter.TestLogicAdapter'
    ]
)

from chatterbot.trainers import ListTrainer

trainer = ListTrainer(chat_bot)


description = "Somos una tienda al servicio del cliente y de tu comunidad"
ubicacion = "Chiclayo Av. Tumbes 125as"
delivery = "Claro, hacemos delivery a todo el perú"
recomendation = str('Tenemos mucho que ofrecer😉, escribe la palabra "productos"  y te mostrare enseguida lo que tenemos para ti')
trainer.train([
    "Hola",
    "Hola, bienvenido a aquinomas",
    "información",
    description,
    "Acerca de",
    description,
    "quienes son?",
    description,
    "ubicacion",
    ubicacion,
    "Donde estan ubicados",
    ubicacion,
    "¿Donde se encuentran?",
    ubicacion,
    "Donde se encuentran",
     ubicacion,
    "¿Hacen delivery?",
    delivery,
    "delivery",
    delivery,
    "recomiendame algo",
    recomendation,
    "recomendación",
    recomendation,
    "polos",
    recomendation,
    "ropa",
    recomendation,
    "¿Quienes son?",
    ubicacion
])



