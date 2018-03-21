# RohBot
[![Build Status](https://travis-ci.org/DasNeuling/RohBot.svg?branch=master)](https://travis-ci.org/DasNeuling/RohBot) 
[![Maintainability](https://api.codeclimate.com/v1/badges/bd6db20a062abff2f5b4/maintainability)](https://codeclimate.com/github/DasNeuling/RohBot/maintainability)
[![codecov](https://codecov.io/gh/DasNeuling/RohBot/branch/master/graph/badge.svg)](https://codecov.io/gh/DasNeuling/RohBot)



## Setup
1. Add token for bot to the Config file by replacing *xxxx*
2. Install dependencies with `pip install -r requirements.txt`
3. Load the language model used by this Bot via   
`python -m spacy download en`
4. Depending on your configuration you may need to type this in your terminal before running:   
`export LC_ALL="en_US.UTF-8"`  
`export LC_CTYPE="en_US.UTF-8"`
5. Run the bot with `python RohBot/RohBot.py`
