# 6.00 Problem Set 5
# RSS Feed Filter

import string
import time

import feedparser
from project_util import translate_html
from news_gui import Popup


#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link


#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word

    def is_word_in(self, text):
        text = text.lower()
        for char in string.punctuation:
            text = text.replace(char, " ")
        words = text.split(" ")
        return self.word.lower() in words


# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)

    def evaluate(self, story):
        return self.is_word_in(story.get_title())


# TODO: SubjectTrigger
class SubjectTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)

    def evaluate(self, story):
        return self.is_word_in(story.get_subject())


# TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)

    def evaluate(self, story):
        return self.is_word_in(story.get_summary())



# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)



# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger_1, trigger_2):
        self.trigger_1 = trigger_1
        self.trigger_2 = trigger_2

    def evaluate(self, story):
        return self.trigger_1.evaluate(story) and self.trigger_2.evaluate(story)



# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger_1, trigger_2):
        self.trigger_1 = trigger_1
        self.trigger_2 = trigger_2

    def evaluate(self, story):
        return self.trigger_1.evaluate(story) or self.trigger_2.evaluate(story)


# Phrase Trigger
# Question 9

# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        return self.phrase in story.get_subject() \
               or self.phrase in story.get_summary() \
               or self.phrase in story.get_title()



#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    stories_containing_triggers = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                stories_containing_triggers.append(story)
                break
    return stories_containing_triggers



#======================
# Part 4
# User-Specified Triggers
#======================


def make_trigger(trigger_type, parameters, trigger_dictionary):
    print trigger_dictionary
    if trigger_type == "TITLE":
        trigger = TitleTrigger(parameters)
    elif trigger_type == "SUBJECT":
        trigger = SubjectTrigger(parameters)
    elif trigger_type == "SUMMARY":
        trigger = SummaryTrigger(parameters)
    elif trigger_type == "NOT":
        trigger = NotTrigger(trigger_dictionary[parameters])
    elif trigger_type == "AND":
        trigger = AndTrigger(trigger_dictionary[parameters[0]], trigger_dictionary[parameters[1]])
    elif trigger_type == "OR":
        trigger = OrTrigger(trigger_dictionary[parameters[0]], trigger_dictionary[parameters[1]])
    elif trigger_type == "PHRASE":
        trigger = PhraseTrigger(parameters)
    else:
        return None
    return trigger



def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    trigger_dictionary = {}
    added_triggers = []

    for line in lines:
        split_line = line.split(" ")
        trigger_name = split_line[0]
        trigger_type = split_line[1]
        parameters = split_line[2:]

        if split_line[0] == "ADD":
            for trigger in split_line[1:]:
                trigger_to_add = trigger_dictionary[trigger]
                added_triggers.append(trigger_to_add)

        elif split_line[1] == "AND" or split_line[1] == "OR":
            trigger_dictionary[trigger_name] = make_trigger(trigger_type, parameters, trigger_dictionary)

        elif split_line[1] == "NOT":
            trigger_dictionary[trigger_name] = make_trigger(trigger_type, parameters, trigger_dictionary)

        elif split_line[1] == "PHRASE":
            trigger_dictionary[trigger_name] = make_trigger(trigger_type, " ".join(parameters), trigger_dictionary)

        else:
            trigger_dictionary[trigger_name] = make_trigger(trigger_type, parameters[0], trigger_dictionary)

    return added_triggers



import thread

def main_thread(p):
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []

    while True:
        print "Polling . . .",

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)

        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            print ". . .",
            if story.get_guid() not in guidShown:
                newstories.append(story)
        print ". . ."
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)


SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

