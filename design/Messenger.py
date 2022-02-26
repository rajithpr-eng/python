# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

'''
SOLID principles are applied
S - Single Responsibility Principle(SRP)
O - Open Close Principle(OCP)
L - Liskov Substitution Principle(LSP)
I - Interface Segregation Principle(ISP)
D - Dependency Inversion Principle(DIP)
'''

'''
Problem Statement: A Rudimentary Messenger in Python, which dispatches incoming text messages to the Console 
(read, web intrface), and stores the message in a Database.
We simulate this execution using a few fixed text messages, and there are a few pre-defined Users to whom 
these messages can be sent.
Three message types are supported: Plain, Response, and Mention.
Two types of message attributes are available in Plain messages: Tags and Anchors.
'''

import random

message_type = {
    'PLAIN_POST': 0,
    'RESPONSE_POST': 1,
    'MENTION_POST': 2,
    'MAX_POST': 3
}

message_attribute = {
    'TAG': 0,
    'ANCHOR': 1,
    'MAX_ATTR': 2
}

texts = [
    'Veni, Vidi, Vici',
    'Eureka! Eureka!',
    'The Eagle Has Landed!',
    'Let Them Have Cake',
    'Swaraj Is My Birthright!'
]

users = [
    (1001, 'Charles'),
    (1002, 'Jane'),
    (1003, 'Mary')
]

class Message:
    def __init__(self, text):
        self.text = text


class PlainMessage(Message):
    def __init__(self, text, msg_attribute):
        super().__init__(text)
        self.msg_attribute = msg_attribute


class ResponseMessage(Message):
    pass


class MentionMessage(Message):
    def __init__(self, text, target_user):
        super().__init__(text)
        self.target_user = target_user

    def get_target_user(self):
        return self.target_user


class Logger:
    def log(self, message):
        pass


class ErrorLogger(Logger):
    def log(self, message):
        print('Exception occurred while posting message:' + message.text)


class FormattedLogger(Logger):
    def log(self, message):
        print('ALERT!!! Exception occurred while posting MESSAGE: **' + message.text +  '**')


class Console:
    def display(self, message):
        print('DISPLAYING ON WEB INTERFACE: <<' + message.text + '>>')


class Database:
    def insert(self, message):
        print('INSERTING DOCUMENT INTO DATABASE: %%' + message.text + '%%]')


class User:
    def __init__(self, identity, name):
        self.identity = identity
        self.name = name

    def notify(self, alert):
        print('User' + self.name +  'with ID' + str(self.identity) + 'received NOTIFICATION:' + alert)

    def superpose(self, message):
        print('User' + self.name + 'with ID' + str(self.identity) + 'SUPERPOSED with message:' + message.text)


class Engine:
    def __init__(self, console, database, logger, file):
        self.console        = console
        self.database       = database
        self.error_logger   = logger
        self.file           = file

    def dispatch(self, message):
        try:
            self.console.display(message)
            self.database.insert(message)
        except Exception:
            self.error_logger.log(message)
            self.file.backup(message)

    def add(self, message, reg_msg):
        self.dispatch(message)
        reg_msg.do_post_processing(message)


class File:
    def backup(self, message):
        print('WRITING BACKUP RECORD INTO FILE:' + '$$' + message + '$$')


class RegularPost:
    def __init__(self, engine):
        self.engine = engine

    def create_post(self, message):
        self.engine.add(message)

    def do_post_processing(self, message):
        pass


class TaggedPost(RegularPost):
    def create_post(self, message):
        text = "ADDING AS A TAG:" + message.text
        message.text = text
        self.engine.add(message, self)


class AnchorPost(RegularPost):
    def create_post(self, message):
        text = "ADDING AS A ANCHOR:" + message.text
        message.text = text
        self.engine.add(message, self)


class ResponsePost(RegularPost):
    def create_post(self, message):
        text = "POSTING AS A ANCHOR:" + message.text
        message.text = text
        self.engine.add(message, self)


class MentionPost(RegularPost):
    def notify_user(self, user):
        alert = "Creating a Mention!"
        user.notify(alert)

    def superpose_mention(self, user, message):
        user.superpose(message)

    def do_post_processing(self, message):
        user = message.get_target_user()
        self.notify_user(user)
        self.superpose_mention(user, message)

    def create_post(self, message):
        self.engine.add(message, self)


class MessageStream:
    def __init__(self):
        file     = File()
        logger   = ErrorLogger()
        console  = Console()
        database = Database()
        self.engine   = Engine(console, database, logger, file)

    def get_next_message(self):
        target_user = None
        post = None
        message = None
        msg_type   = random.randint(0, message_type['MAX_POST'] - 1)
        text_index = random.randint(0, len(texts) - 1)
        if msg_type == message_type['MENTION_POST']:
            index = random.randint(0, len(users) - 1)
            target_user = User(users[index][0], users[index][1])
            message = MentionMessage(texts[text_index], target_user)
            post    = MentionPost(self.engine)
        elif msg_type == message_type['PLAIN_POST']:
            ind = random.randint(0, message_attribute['MAX_ATTR'] - 1)
            message = PlainMessage(texts[text_index], ind)
            if ind == message_attribute['TAG']:
                post = TaggedPost(self.engine)
            else:
                post = AnchorPost(self.engine)
        elif msg_type == message_type['RESPONSE_POST']:
            message = ResponseMessage(texts[text_index])
            post = ResponsePost(self.engine)
        return post, message


class Messenger:
    def process_message(self, post, message):
        post.create_post(message)


# Client Code
if __name__ == '__main__':
    message_stream = MessageStream()
    messenger = Messenger()
    for count in range(1, 10):
        post, message = message_stream.get_next_message()
        messenger.process_message(post, message)
