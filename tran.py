from googletrans import Translator

translator = Translator()

# Translate from English to Spanish
translation = translator.translate('broken heart!', dest='my')

print(translation.text)
