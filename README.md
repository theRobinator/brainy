Brainy
======

Brainy is my take on a helpful "assistant AI" like Siri or Google Now. It's meant to be a way for me to play around with
machine learning concepts like NLP and voice synthesis, and different kinds of IO like audio or chatbots.


Installation
------------

```
virtualenv .
pip install -r requirements.txt
python -m textblob.download_corpora  # For the NLP library
```

Then you can run it with `python brainy`.


Implementation State
--------------------

Brainy currently supports only command-line text IO, and the ability to define words and get directions. As I get better
at all of these concepts, it'll hopefully expand into all sorts of useful tools.


Creating New Commands
---------------------

If you want to make a new command, there are two steps:

1. Create a new module under `brainy.tasks` that defines `SAMPLE_QUESTIONS`, `TEST_QUESTIONS`, and `handle(command)`.
   Check out one of the previously existing tasks for examples.
2. Add your module to the `COMMANDS` dictionary at the top of `main.py`.


Things to Do
------------

- Figure out semantic analysis so I can parse "places" out of directions questions
- Split out input and output into separate layers to connect to different systems
- Hook up speech-to-text and vice versa
- Make a Slack bot IO system
- Hook up AppleScripts on OSX
- Read stuff from Wolfram Aplha maybe?
