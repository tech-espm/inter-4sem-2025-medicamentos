from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot(
    "",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///chatbot.sqlite3",
    logic_adapters=[
        {"import_path": "chatterbot.logic.BestMatch"},
        {"import_path": "chatterbot.logic.MathematicalEvaluation"},
        {"import_path": "chatterbot.logic.TimeLogicAdapter"},
    ],
    read_only=False,
)

treinador = ListTrainer(bot)

dialogos = [
    "Oi",
    "Olá! Como posso te ajudar?",
    "Qual seu nome?",
    "Acredito que não sou capacitada para te responder essa pergunta. Recomendo que você procure um médico e marque uma consulta para questões mais complicadas.",
    "Obrigado",
    "De nada! 🙂",
]

treinador.train(dialogos)
print("Treinamento por lista concluído!")
