import ollama
import logging 
from shortterm_memory.ChatbotMemory import ChatbotMemory
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"
logging.basicConfig(filename="app.log" , filemode="w", level=logging.DEBUG)

class Bot:
    def __init__(self, model:str="mistral:latest", ollama_options=None):
        self.model = model
        self._ollama_option = ollama_options if ollama_options else {'temperature': 1}
        # self._ollama_options.update({'temperature': 1})
        self.memory = ChatbotMemory()
        self.running = False
        self.response = ""
        
    
    def ans(self, user_input:str):
        self.running = True
        self.response = ""
        # TODO : Mettre RAG en place
        context = "" # 
        
        prompt = (
            "Vous êtes un assistant intelligent. Utilisez les informations suivantes pour aider l'utilisateur.\n\n"
            "Mémoire du chatbot (à ne pas montrer à l'utilisateur) :\n"
            f"{self.memory.get_memory()}\n\n"
            "Contexte pertinent :\n"
            f"{context}\n\n"
            "Question de l'utilisateur :\n"
            f"{user_input}\n\n"
            "Répondez de manière claire et CONCISE et avec une mise en forme lisible et structuré :\n"
        )
        result = ollama.generate(
            model=self.model,
            prompt=prompt,
            stream=True,
            options=self._ollama_option
        )
        # print(f"Response generated. with model : {self.model}")
        logging.info(f"Response generated. with model : {self.model}")
        
        self.response = ""
        for chunk in result:
            self.response += chunk['response']
            yield chunk['response']
         
        self.memory.update_memory(user_input, self.response)
        self.running = False

def main():
    bot = Bot()
    
    print("Bienvenue dans le chat terminal ! Tapez '/quit' pour quitter.")
    
    while True:
    
        user_input = input("Vous: ")
        
        if user_input.strip().lower() == "/quit":
            print("Fin de la conversation. À bientôt!")
            break
        
        response_generator = bot.ans(user_input)
        
        print("Bot:", end=" ")
    
        for chunk in response_generator:
            print(chunk, end="", flush=True)
        print() 

if __name__ == "__main__":
    main()
