# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

'''
Problem Statement: In this simulation of the messenger translation feature, we consider an English keyboard,
and support for three target languages to render final text:
French
German
Spanish
We also define three standard greeting messages in English, and their translations to the above three languages:
Suppose an independent software vendor designs classes to simulate rendering of these standard English greetings,
in French, German, and Spanish.
The aim is to translate the given greeting to the user's language of choice (among the three above).
'''

rendering_language = {
    'ENGLISH': 0,
    'FRENCH': 1,
    'GERMAN': 2,
    'SPANISH': 3,
}

standard_greeting_type = {
    'HELLO': 0,
    'THANKS': 1,
    'GOODBYE': 2
}

english_greetings = {
    'HELLO': 'Hello!',
    'THANKS': 'Thanks!',
    'GOODBYE': 'Goodbye!'
}

french_greetings = {
    'HELLO': 'Bonjour!',
    'THANKS': 'Merci!',
    'GOODBYE': 'Au revoir!'
}

german_greetings = {
    'HELLO': 'Hallo!',
    'THANKS': 'Vielen Dank!',
    'GOODBYE': 'Auf Wiedersehen!'
}

spanish_greetings = {
    'HELLO': 'Hola!',
    'THANKS': 'Gracias!',
    'GOODBYE': 'Adios!'
}


class RenderingLanguage:
    def render_text(self, typed_text):
        pass


class FrenchRendering(RenderingLanguage):
    def render_text(self, typed_text, greeting_type):
        text = ''

        if greeting_type == standard_greeting_type['HELLO']:
            text = french_greetings['HELLO']
        elif greeting_type == standard_greeting_type['THANKS']:
            text = french_greetings['THANKS']
        elif greeting_type == standard_greeting_type['GOODBYE']:
            text = french_greetings['GOODBYE']
        else:
            print('Incompatible greeting type passed!')
            return

        print(f'Translated to French: {text}')


class GermanRendering(RenderingLanguage):
    def render_text(self, typed_text, greeting_type):
        text = ''

        if greeting_type == standard_greeting_type['HELLO']:
            text = german_greetings['HELLO']
        elif greeting_type == standard_greeting_type['THANKS']:
            text = german_greetings['THANKS']
        elif greeting_type == standard_greeting_type['GOODBYE']:
            text = german_greetings['GOODBYE']
        else:
            print('Incompatible greeting type passed!')
            return

        print(f'Translated to German: {text}')


class SpanishRendering(RenderingLanguage):
    def render_text(self, typed_text, greeting_type):
        text = ''

        if greeting_type == standard_greeting_type['HELLO']:
            text = spanish_greetings['HELLO']
        elif greeting_type == standard_greeting_type['THANKS']:
            text = spanish_greetings['THANKS']
        elif greeting_type == standard_greeting_type['GOODBYE']:
            text = spanish_greetings['GOODBYE']
        else:
            print('Incompatible greeting type passed!')
            return

        print(f'Translated to Spanish: {text}')


class RenderingAdapter:
    def __init__(self):
        self.rendering_languages = []

    def register_language(self, rendering_language, language_type):
        self.rendering_languages.append((language_type, rendering_language))

    def unregister_language(self, language_type):
        for language_entry in self.rendering_languages:
            if language_type == language_entry[0]:
                self.rendering_languages.remove(language_entry)

    def translate_rendering(self, typed_text, greeting_type, language_type):
        rendering_language = None

        for language_entry in self.rendering_languages:
            if language_type == language_entry[0]:
                rendering_language = language_entry[1]
                break

        if not rendering_language:
            print(f'Remain in English: {typed_text}')
            return

        rendering_language.render_text(typed_text, greeting_type)


class EnglishKeyboard:
    def __init__(self, rendering_adapter):
        self._typed_text = ''
        self._greeting_type = -1
        self.rendering_adapter = rendering_adapter

    @property
    def typed_text(self):
        return self._typed_text

    @typed_text.setter
    def typed_text(self, typed_text):
        self._typed_text = typed_text

    @property
    def greeting_type(self):
        return self._greeting_type

    @greeting_type.setter
    def greeting_type(self, greeting_type):
        self._greeting_type = greeting_type

    def input_text(self, typed_text, greeting_type):
        self.typed_text = typed_text
        self.greeting_type = greeting_type

    def display_text(self, language_type):
        print(f'Greeting in English: {self.typed_text}')

        self.rendering_adapter.translate_rendering(self.typed_text, self.greeting_type, language_type)


# Client Context
if __name__ == '__main__':

    rendering_adapter = RenderingAdapter()
    rendering_adapter.register_language(FrenchRendering(), rendering_language['FRENCH'])
    rendering_adapter.register_language(GermanRendering(), rendering_language['GERMAN'])
    rendering_adapter.register_language(SpanishRendering(), rendering_language['SPANISH'])

    english_keyboard = EnglishKeyboard(rendering_adapter)

    english_keyboard.input_text(english_greetings['HELLO'], standard_greeting_type['HELLO'])
    english_keyboard.display_text(rendering_language['FRENCH'])

    english_keyboard.input_text(english_greetings['THANKS'], standard_greeting_type['THANKS'])
    english_keyboard.display_text(rendering_language['SPANISH'])

    english_keyboard.input_text(english_greetings['GOODBYE'], standard_greeting_type['GOODBYE'])
    english_keyboard.display_text(rendering_language['GERMAN'])

    english_keyboard.input_text(english_greetings['GOODBYE'], standard_greeting_type['GOODBYE'])
    english_keyboard.display_text(rendering_language['ENGLISH'])