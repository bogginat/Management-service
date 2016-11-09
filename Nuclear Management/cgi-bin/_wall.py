#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import time


class Wall:
    USERS = 'users/users.json'
    WALL = 'wall/wall.json'
    COOKIES = 'cookies/cookies.json'
    DATA = 'data_users/data_users.json'

    def __init__(self):
        """Создаём начальные файлы, если они не созданы"""
        try:
            with open(self.USERS, 'r', encoding='utf-8'):
                pass
        except IOError:
            with open(self.USERS, 'w', encoding='utf-8') as f:
                json.dump({}, f)

        try:
            with open(self.WALL, 'r', encoding='utf-8'):
                pass
        except IOError:
            with open(self.WALL, 'w', encoding='utf-8') as f:
                json.dump({"posts": []}, f)

        try:
            with open(self.COOKIES, 'r', encoding='utf-8'):
                pass
        except IOError:
            with open(self.COOKIES, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def register(self, user, password, adm):
        """Регистриует пользователя. Возвращает True при успешной регистрации"""
        if self.find1(user):
            return False  # Такой пользователь существует
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        users[user] = [password, adm]
        with open(self.USERS, 'w', encoding='utf-8') as f:
            json.dump(users, f)
        return True

    def register1 (self, user, fam, im, otch, job):
        """Регистриует пользователя. Возвращает True при успешной регистрации"""
        if self.find(user):
            return False  # Такой пользователь существует
        with open(self.DATA, 'r', encoding='utf-8') as f:
            users = json.load(f)
        users[user] = [fam, im, otch, job]
        with open(self.DATA, 'w', encoding='utf-8') as f:
            json.dump(users, f)
        return True

    def set_cookie(self, user):
        """Записывает куку в файл. Возвращает созданную куку."""
        with open(self.COOKIES, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        cookie = str(time.time()) + str(random.randrange(10**14))  # Генерируем уникальную куку для пользователя
        cookies[cookie] = user
        with open(self.COOKIES, 'w', encoding='utf-8') as f:
            json.dump(cookies, f)
        return cookie

    def find_cookie(self, cookie):
        """По куке находит имя пользователя"""
        with open(self.COOKIES, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        return cookies.get(cookie)

    def find(self, user, password=None):
        """Ищет пользователя по имени или по имени и паролю"""
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        if user in users and (password == users[user][0]):
            return True
        return False


    def find1(self, user):
        """Ищет пользователя по имени или по имени и паролю"""
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        if user in users:
            return True
        return False


    def del_cookie(self, cookie):
        with open(self.COOKIES, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        cookies.pop(cookie)
        with open(self.COOKIES, 'w', encoding='utf-8') as f:
            json.dump(cookies, f)
        return True

    def adminust(self, user):
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        if users[user][1] == "yes":
            return True
        else:
            return False

