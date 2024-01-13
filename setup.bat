@echo off
python -m venv venv
call venv\Scripts\activate
pip install nltk
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
call venv\Scripts\deactivate
pause
