import constants as c

def bold_text(text):
    bold_chars = c.BOLD_D
    result = ""
    for ch in text:
        if ch in bold_chars:
            result += bold_chars[ch]
            
        else:
            result += ch
            
    
    return result

def convert_to_unicode(string: str):
    while "**" in string:
        word_start = string.find("**")
        word_end = string.find("**", word_start + 2)
        if word_end == -1:
            break
        word_end += 2  # To include the ending '**'
        bold_part = string[word_start + 2:word_end - 2]
        bold_unicode = bold_text(bold_part)
        string = string[:word_start] + bold_unicode + string[word_end:]
    return string