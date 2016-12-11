from sys import stdin

from textblob.classifiers import NaiveBayesClassifier, DecisionTreeClassifier, MaxEntClassifier

from brainy.tasks import definetask, directionstask


COMMANDS = {
    'define': definetask,
    'directions': directionstask
}
DEBUG = False


def build_classifier():
    """ Build a classifier that's pretty good with all the examples.
    """
    train_data = []
    test_data = []
    for name, module in COMMANDS.iteritems():
        for question in module.SAMPLE_QUESTIONS:
            train_data.append((question.lower(), name))
        for question in module.TEST_QUESTIONS:
            test_data.append((question.lower(), name))

    best_score = 0
    best_classifier = None
    for classifier in [NaiveBayesClassifier, DecisionTreeClassifier]:
        cl = classifier(train_data)
        accuracy = cl.accuracy(test_data)
        if DEBUG:
            print classifier, 'got accuracy', accuracy
        if accuracy > best_score:
            best_score = accuracy
            best_classifier = cl

    if DEBUG:
        print 'Using', best_classifier
    return best_classifier


def main(argv):
    # Build the classifiers
    cl = build_classifier()
    while True:
        print 'Enter a command: ',
        command = stdin.readline().strip().lower()
        if command == '':
            continue
        module_name = cl.classify(command)
        if DEBUG:
            print module_name
        COMMANDS[module_name].handle(command)


if __name__ == '__main__':
    from sys import argv
    main(argv)
