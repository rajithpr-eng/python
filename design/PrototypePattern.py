# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

'''
Problem Statement: In this messenger, a user can post a caption on a message group, or to a contact.
A caption consists of an emotion that drives it.
A caption consists of text typed in by the user, a system generated caption based on the emotion expressed,
and a suitable emoticon.
The system has a Keyboard class to input the text message, and an indication of the emotion behind it.
There are three standard emotions supported:
Happy
Sad
Angry
'''

import copy
import random

standard_emotion = {
    'HAPPY': 0,
    'SAD': 1,
    'ANGRY': 2,
    'MAX': 3
}

texts = [
    'Veni, Vidi, Vici',
    'Eureka! Eureka!',
    'The Eagle Has Landed!',
    'Let Them Have Cake',
    'Swaraj Is My Birthright!'
]

class Emoticon:
    def __init__(self, emotion):
        self._emotion = emotion

    def __str__(self):
        pass

    @property
    def emotion(self):
        return self._emotion

    @emotion.setter
    def emotion(self, emotion):
        self._emotion = emotion

    def clone(self):
        pass


class Happy(Emoticon):
    def __init__(self):
        super().__init__(':-)')
        self.happy = None

    def __str__(self):
        print(f'{self.emotion}')

    def clone(self):
        if not self.happy:
            self.happy = Happy()

        new_happy = copy.deepcopy(self.happy)
        return new_happy


class Angry(Emoticon):
    def __init__(self):
        super().__init__(';-#')
        self.angry = None

    def __str__(self):
        print(f'{self.emotion}')

    def clone(self):
        if not self.angry:
            self.angry = Angry()

        new_angry = copy.deepcopy(self.angry)
        return new_angry


class Sad(Emoticon):
    def __init__(self):
        super().__init__(':-(')
        self.sad = None

    def __str__(self):
        print(f'{self.emotion}')

    def clone(self):
        if not self.sad:
            self.sad = Sad()

        new_sad = copy.deepcopy(self.sad)
        return new_sad


class CaptionText:
    def __init__(self, text):
        self._text = text

    def __str__(self):
        print(f'{self.text}')

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def clone(self):
        pass


class HappyCaption(CaptionText):
    def __init__(self):
        super().__init__('What a beautiful day!')
        self.happy = None

    def clone(self):
        if not self.happy:
            self.happy = HappyCaption()

        new_happy = copy.deepcopy(self.happy)
        return new_happy


class SadCaption(CaptionText):
    def __init__(self):
        super().__init__('The world is so difficult!')
        self.sad = None

    def clone(self):
        if not self.sad:
            self.sad = SadCaption()

        new_sad = copy.deepcopy(self.sad)
        return new_sad


class AngryCaption(CaptionText):
    def __init__(self):
        super().__init__('I will put an end to all misery!')
        self.angry = None

    def clone(self):
        if not self.angry:
            self.angry = AngryCaption()

        new_angry = copy.deepcopy(self.angry)
        return new_angry


class Keyboard:
    def __init__(self):
        self._typed_text = ''
        self._emotion = -1

    @property
    def typed_text(self):
        return self._typed_text

    @typed_text.setter
    def typed_text(self, typed_text):
        self._typed_text = typed_text

    @property
    def emotion(self):
        return self._emotion

    @emotion.setter
    def emotion(self, emotion):
        self._emotion = emotion

    def input(self, input_text, emotion):
        self.typed_text = input_text
        self.emotion = emotion


class CaptionTextFactory:
    def __init__(self):
        self.happy_caption = HappyCaption()
        self.sad_caption = SadCaption()
        self.angry_caption = AngryCaption()

    def get_caption_text(self, emotion):
        if emotion == standard_emotion['HAPPY']:
            return self.happy_caption.clone()
        elif emotion == standard_emotion['SAD']:
            return self.sad_caption.clone()
        elif emotion == standard_emotion['ANGRY']:
            return self.angry_caption.clone()
        else:
            return None


class EmoticonFactory:
    def __init__(self):
        self.happy_emoticon = Happy()
        self.sad_emoticon = Sad()
        self.angry_emoticon = Angry()

    def get_emoticon(self, emotion):
        if emotion == standard_emotion['HAPPY']:
            return self.happy_emoticon.clone()
        elif emotion == standard_emotion['SAD']:
            return self.sad_emoticon.clone()
        elif emotion == standard_emotion['ANGRY']:
            return self.angry_emoticon.clone()
        else:
            return None


class CaptionBuilder:
    def __init__(self, keyboard, caption_text_factory, emoticon_factory):
        self.keyboard = keyboard
        self.caption_text_factory = caption_text_factory
        self.emoticon_factory = emoticon_factory

    def build_message(self):
        full_message = ''
        full_message += self.keyboard.typed_text
        full_message += '\n'

        caption_text = self.caption_text_factory.get_caption_text(self.keyboard.emotion)
        if not caption_text:
            print('Unsupported Emotion Experienced!')
            return

        full_message += caption_text.text
        full_message += '\n'

        emoticon = self.emoticon_factory.get_emoticon(self.keyboard.emotion)
        if not emoticon:
            print('Unsupported Emotion Experienced!')
            return

        full_message += emoticon.emotion

        print(f'{full_message}')

class MessageStream:

    def get_next_message(self):
        emotion   = random.randint(0, standard_emotion['MAX'] - 1)
        text_index = random.randint(0, len(texts) - 1)
        return texts[text_index], emotion

# Client Code
if __name__ == '__main__':
    keyboard = Keyboard()
    caption_text_factory = CaptionTextFactory()
    emoticon_factory = EmoticonFactory()
    caption_builder = CaptionBuilder(keyboard, caption_text_factory, emoticon_factory)
    message_stream = MessageStream()
    for count in range(1, 10):
        msg, emotion = message_stream.get_next_message()
        keyboard.input(msg, emotion)
        caption_builder.build_message()