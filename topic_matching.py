import tokenization as tk
import keys_loader

def topic_related(text : str) -> bool: # check if the keys are contained in the tokens list of the text

    keys = keys_loader.load('keys.txt')
    text_tokens = tk.tokenization_process(text)

    for x in keys:
        if x in text_tokens:
            return True

    return False