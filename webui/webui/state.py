import os
import time
#import openai
import pynecone as pc

#openai.api_key = os.environ["OPENAI_API_KEY"]
import os
import sys

current_dir = os.path.abspath(__file__)
two_levels_up_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
print(two_levels_up_dir)
sys.path.append(two_levels_up_dir)
#print(sys.path)

import g4f

class QA(pc.Base):
    """A question and answer pair."""

    question: str
    answer: str


class State(pc.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = {
        "Intros": [QA(question="What is your name?", answer="Pynecone")],
    }
    messages: list[dict[str, str]] = [{"role": "user", "content": "What is your name?"},
                                      {"role": "assistant", "content": "Pynecone"}]
    # The current chat name.
    current_chat = "Intros"

    # The currrent question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    # Whether the drawer is open.
    drawer_open: bool = False

    # Whether the modal is open.
    modal_open: bool = False

    def create_chat(self):
        """Create a new chat."""
        # Insert a default question.
        self.chats[self.new_chat_name] = [
            QA(question="What is your name?", answer="Pynecone")
        ]
        self.current_chat = self.new_chat_name

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        """Toggle the drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = {
                "New Chat": [QA(question="What is your name?", answer="Pynecone")]
            }
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name
        self.toggle_drawer()

    @pc.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    
    async def process_question(self, form_data: dict[str, str]):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        # Check if we have already asked the last question or if the question is empty
        self.question = form_data["question"]
        if (
            self.chats[self.current_chat][-1].question == self.question
            or self.question == ""
        ):
            return

        # Set the processing flag to true and yield.
        self.processing = True
        

        # Start a new session to answer the question.
        # list comprehension with dict .dict()
        
        #print(session)
        #print(type(session))

        # Old OpenAI chat completion (to delete later)
        # session = openai.Completion.create(
        #     engine="text-davinci-003",
        #     prompt=self.question,
        #     max_tokens=100,
        #     n=1,
        #     stop=None,
        #     temperature=0.7,
        #     stream=True,  # Enable streaming
        # )
        
        qa = QA(question=self.question, answer="")
        self.chats[self.current_chat].append(qa)
        self.messages.append({"role": "user", "content": str(self.question)})
        yield
        yield
        

        # streamed completion
        response = g4f.ChatCompletion.create(model="gpt-4", messages=self.messages, stream=True)
         

        # self.chat.append({'question': self.question, 'answer': answer_text})
        # self.chats[self.current_chat][-1].answer += answer_text
        # self.chats = self.chats


        #print(self.chats[self.current_chat])
        # Stream the results, yielding after every word.
        for message in response:
            print(message)
            answer_text = message
            self.chats[self.current_chat][-1].answer += answer_text
            self.chats = self.chats
            yield
        self.messages.append({"role": "assistant", "content": self.chats[self.current_chat][-1].answer})
        
        # this print statement is a check (it can be deleted later)
        print(self.messages)
        # Toggle the processing flag.
        self.processing = False
