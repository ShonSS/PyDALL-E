# boost_art_prompt_thread.py
import logging
from PyQt6.QtCore import QThread, pyqtSignal
import openai

logger = logging.getLogger(__name__)


class BoostArtPromptThread(QThread):
    promptBoosted = pyqtSignal(str)
    progressChanged = pyqtSignal(int)

    def __init__(self, prompt, selected_aesthetic):
        super().__init__()
        self.prompt = prompt
        self.selected_aesthetic = selected_aesthetic

    def run(self):
        logger.info("Starting art prompt boosting")
        boosted_prompt = self.boost_art_prompt(self.prompt, self.selected_aesthetic)
        self.progressChanged.emit(100)  # Simulate progress completion
        logger.info("Art prompt boosting completed")
        self.promptBoosted.emit(boosted_prompt)

    def boost_art_prompt(self, prompt, selected_aesthetic):
        # Define the boost instruction with the selected aesthetic if available
        if selected_aesthetic:
            boost_instruction = f"Craft an art prompt for DALL-E by transforming the following text into a powerful catalyst for awe-inspiring {selected_aesthetic} art:"
        else:
            boost_instruction = "Craft an art prompt for DALL-E by transforming the following text into a powerful catalyst for awe-inspiring art:"

        # Combine the boost instruction with the existing prompt
        combined_prompt = f"{boost_instruction} {prompt}"

        logger.debug("Generated boost instruction: %s", boost_instruction)

        # Use OpenAI to rewrite the art prompt and engineer the best prompt
        boosted_prompt = openai.Completion.create(
            engine="text-davinci-003",
            prompt=combined_prompt,
            max_tokens=256,
            n=1,
            stop=None,
            temperature=1.2,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        ).choices[0].text.strip()

        logger.debug("Boosted prompt: %s", boosted_prompt)

        return boosted_prompt