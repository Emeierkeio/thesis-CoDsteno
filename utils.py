dict_months = {
    'gennaio': 'january',
    'febbraio': 'february',
    'marzo': 'march',
    'aprile': 'april',
    'maggio': 'may',
    'giugno': 'june',
    'luglio': 'july',
    'agosto': 'august',
    'settembre': 'september',
    'ottobre': 'october',
    'novembre': 'november',
    'dicembre': 'december',
}

def months_itatoeng(month):
    """
    Translates the month from italian to english.
    
    Args:
        month: month in italian.
    
    Returns:
        month: month in english.
    """
        
    return dict_months[month]



def format_text(text):
    """
    Formats the text of the intervention.
    
    Args:
        text: text of the intervention.
        
    Returns:
        text: formatted text of the intervention (without newlines and commas).
    """

    text = text.replace("\n", " ").replace(",", " ")
    
    return text