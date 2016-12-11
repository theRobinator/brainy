"""
The DefineTask is used to define words or phrases through the use of a dictionary or Wikipedia.
"""

import re
import urllib
import urllib2

from lxml import html as htmlparser
from textblob import TextBlob

from brainy.utils import get_noun_phrase


# The sample questions that Brainy will use to learn when to run this task.
SAMPLE_QUESTIONS = [
    'What is love?',
    'What is a house?',
    'What is an ampersand?',
    "What's a computer?",
    "What's an underscore?",
    'Define pedantic',
    'Define enigma',
    'Define transparency',
    "What's the definition of consciousness?",
    "What's the definition of telepathy?"
]

# The test questions Brainy will use to see if it can tell if it learned correctly.
TEST_QUESTIONS = [
    'What is sadness?',
    'What is a banana?',
    'What is an albatross?',
    "What's a duck?",
    "What's an elephant?",
    'Define undulations',
    'Define alternation',
    'Define bees',
    "What's the definition of disco?",
    "What's the definition of available?"
]

COMMON_REGEX = re.compile("(what('s|\s+is)?\s+the\s+definition\s+(of|for)|what('s|\s+is)?|define)(\s+an?)?\s+?(.*?)\??$")
REPLACE_REFS_REGEX = re.compile('\[\d+\]')

def handle(command):
    regex_match = COMMON_REGEX.match(command)
    if regex_match and regex_match.groups()[5]:
        request = regex_match.groups()[5]
    else:
        request = get_noun_phrase(command)

    if request is None:
        # Parsing failed :(
        print "Sorry, I don't know what you mean."
        return
    
    answer = None
    source_url = None
    
    # Now that we know what we want, look it up on Wikipedia
    try:
        wikipedia_name = urllib.quote(request.replace(' ', '_'))
        wiki_url = 'https://en.wikipedia.org/wiki/' + wikipedia_name
        wiki_html = urllib2.urlopen(wiki_url).read()
        html_tree = htmlparser.fromstring(wiki_html)
        p_elements = html_tree.xpath("//div[@id='mw-content-text']/p[1]")
        if p_elements and len(p_elements):
            answer = re.sub(REPLACE_REFS_REGEX, '', p_elements[0].text_content())
        
        # Disambiguation pages and incomplete responses shouldn't be displayed
        if answer and answer[-1] == ':':
            answer = None
        else:
            source_url = wiki_url
            
    except urllib2.URLError, e:
        # Not on wikipedia!
        pass
    
    if answer is None:
        # Wikipedia failed, try looking this up in the dictionary if it's a single word
        textblob = TextBlob(request)
        if len(textblob.words) == 1:
            definitions = textblob.words[0].definitions
            if definitions and len(definitions):
                word = str(textblob.words[0])
                if len(definitions) == 1:
                    answer = 'The word "%s" means:\n%s' % (word, definitions[0])
                else:
                    answer_parts = ['%s has %d definitions:' % (word, len(definitions))]
                    for i in xrange(len(definitions)):
                        answer_parts.append('%d. %s' % (i+1, definitions[i]))
                    answer = '\n'.join(answer_parts)
        
    if answer is None:
        print "Sorry, I don't know what you mean."
    else :
        print '#' * 50
        print answer
        if source_url:
            print
            print 'For more information, see', source_url
        print '#' * 50
    