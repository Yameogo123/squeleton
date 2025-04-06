
from {{ cookiecutter.package_slug }}.models.llm.LLM import LLM
from groq import Groq
from {{ cookiecutter.package_slug }}.utils.utils import Utils
from decouple import config

class GroqLLM(LLM):
    
    def __init__(self):
        super().__init__()
        if Utils.not_all_in_env(["GROQ_API_KEY", "GROQ_MODEL"]):
            raise Exception("Environment variables not set")
        self.setAPIKey(config("GROQ_API_KEY"))
        self.setModelName(config("GROQ_MODEL"))
        self.setSystemPrompt(Utils.MedecialAdvice())
        self.__client = Groq(api_key=config("GROQ_API_KEY"))

    
    def retrieve_message(self, user_prompt:str, context:str = ""):
        """
            Retrieves a message by using the Groq LLM to generate response from a given prompt.

            Args:
                user_prompt (str): The input prompt.

            Returns:
                str: The generated code as a string
        """
        messages = [
            {"role": "system", "content": self.getSystemPrompt() + "\n" + context},
            {
                "role": "user",
                "content": " Voici ma question: " + str(user_prompt),
            },
        ]
        completion = self.__client.chat.completions.create(
            model=self.getModelName(), messages=messages,
            temperature=0.9, max_completion_tokens=1024,
            top_p=1, stream=False, stop=None
        )
        return completion.choices[0].message.content.replace("`", "")

        