class TxtParser:

    @staticmethod
    def next_word_after_phrase(text, phrase):
        start_index = text.find(phrase)

        if start_index != -1:
            next_word_start = start_index + len(phrase)
            text_after_phrase = text[next_word_start:]
            next_word_end = text_after_phrase.find(" ")
            if next_word_end == -1:
                next_word = text_after_phrase
            else:
                next_word = text_after_phrase[:next_word_end]
            return next_word
        return None
