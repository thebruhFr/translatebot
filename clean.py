import re

def clean_and_format_card(card_entry):
    match = re.search(r"(\d{16})[:|\/\r\n\n ](\d{1,2})[:|\/\r\n\n ](\d{2,4})[:|\/\r\n\n ](\d{3,4})", card_entry)
    
    if match:
        cc = match.group(1)
        mes = match.group(2)
        ano = match.group(3)
        cvv = match.group(4)

        if len(mes) == 1:
            mes = "0" + mes
        if len(ano) == 2:
            ano = "20" + ano

        return f"Cleaned Card Information:\nCC: {cc}\nExpiration: {mes}/{ano}\nCVV: {cvv}"
    
    return "Couldn't extract valid card information."
