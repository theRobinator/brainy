from textblob import TextBlob


def get_noun_phrase(command):
    # Use NLP to look for noun phrases
    textblob = TextBlob(command)
    phrases = textblob.noun_phrases
    if len(phrases):
        return phrases[-1]
    else:
        # Fall back to just looking for any nouns at all
        for i in xrange(len(textblob.tags)):
            if textblob.tags[i][1][0] == 'N':
                return ' '.join(textblob.words[i:])

    return None
