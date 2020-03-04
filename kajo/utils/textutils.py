# -*- coding: utf-8 -*-

import re
from urllib.parse import urlparse


RE_SPACES = re.compile(r'\s+')
RE_DIGITS = re.compile(r'\[[0-9]*\]')
RE_SPECIALSYMB = re.compile(r'[^a-zA-Z0-9]')
RE_AZ09 = re.compile(r'[^a-zA-Z0-9/]')
RE_URLS = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class TextCleaner:
    """A simple text cleaning util."""
    def __init__(self, text):
        """
        :param text: <str>
        """
        self.text = text
        self.text_clean = self.cleanup()

    def cleanup(self):
        """
        Soft cleanup - leave text intact, but remove
        repeated '\n' and spaces, and finally strip.
        """
        text = ''
        try:
            self.text.split('\n')
        except AttributeError:
            return text

        for par in self.text.split('\n'):
            par = par.strip()
            if par == '':
                continue

            par = RE_SPACES.sub(' ', par)
            text += par + '\n'

        return text.strip()

    def cleanup_hard(self):
        """
        Hard cleanup - leave only text without digits,
        special symbols and spaces.
        """
        text = RE_DIGITS.sub(' ', self.text)
        text = RE_SPECIALSYMB.sub(' ', text)
        return RE_SPACES.sub(' ', text).strip()

    def extract_urls(self, distinct=True):
        """
        Extracts and cleans up all urls from self.text.

        :param distinct: <bool>
        :return: <list>
        """
        urls = RE_URLS.findall(self.text.lower())
        clean_urls = []
        for url in urls:
            # Get the last character.
            last_char = url[-1]

            # Check if the last character is not an alphabet,
            # or a number, or a '/' (some websites may have that).
            if bool(RE_AZ09.match(last_char)):
                url = url[:-1]
            clean_urls.append(url)

        if distinct:
            clean_urls = list(set(clean_urls))

        return clean_urls
