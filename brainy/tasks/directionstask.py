"""
The DirectionsTask is used to get directions to a place.
"""

import re
import urllib
import webbrowser

from brainy.utils import get_noun_phrase


# The sample questions that Brainy will use to learn when to run this task.
SAMPLE_QUESTIONS = [
    'Where is Sacramento?',
    'Where is New York?',
    'Where is South Africa?',
    'Where is Russia?',
    "Where's San Francisco?",
    "Where's London?",
    "Where's Canada?",
    "Where's my house?",
    'how do i get to burger king?',
    'how do i get to Eureka?',
    'how do i get to Six Flags?',
    'give me directions to Marin',
    'give me directions to San Diego'
]

# The test questions Brainy will use to see if it can tell if it learned correctly.
TEST_QUESTIONS = [
    'Where is Philidelphia?',
    'Where is Oak Ridge?',
    'Where is Taco Bell?',
    'Where is Spain?',
    "Where's Rhode Island?",
    "Where's Paris?",
    "Where's Denver?",
    "Where's Krispy Kreme?",
    'how do i get to my house?',
    'how do i get to Vallejo?',
    'how do i get to Roam Burger?',
    'give me directions to Portland',
    'give me directions to Yellowstone'
]

COMMON_REGEX = re.compile(".*?(where('s|\s+is)|how\s+(can|do)\s+(i|we|you)\s+(get|go)\s+to|directions\s+(for|to))\s+(.*?)\??$")

def handle(command):
    regex_match = COMMON_REGEX.match(command)
    get_directions = False
    if regex_match and regex_match.groups()[6]:
        request = regex_match.groups()[6]
        first_group = regex_match.groups()[0]
        get_directions = (first_group == 'directions to' or first_group.startswith('how'))
    else:
        get_directions = ('directions' in command)
        request = get_noun_phrase(command)

    if request is None:
        # Parsing failed :(
        print "Sorry, I don't know what you mean."
        return
    
    if get_directions:
        request = 'directions to ' + request
    
    url_part = urllib.quote(request.replace(' ', '+'))
    webbrowser.open_new_tab('https://www.google.com/maps/search/' + url_part)
