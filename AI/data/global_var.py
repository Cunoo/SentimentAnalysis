import re

# Slovak stopwords
STOP_WORDS_SK = {
    "a", "aby", "aj", "ak", "akej", "akejže", "ako", "akom", "akomže", "akou",
    "akouže", "akože", "aká", "akáže", "aké", "akého", "akéhože", "akému", "akémuže", "akéže",
    "akú", "akúže", "aký", "akých", "akýchže", "akým", "akými", "akýmiže", "akýmže", "akýže",
    "ale", "alebo", "ani", "asi", "avšak", "až", "ba", "bez", "bezo", "bol",
    "bola", "boli", "bolo", "bude", "budem", "budeme", "budete", "budeš", "budú", "buď",
    "by", "byť", "cez", "cezo", "dnes", "do", "ešte", "ho", "hoci", "i", 
    "iba", "ich", "im", "inej", "inom", "iná", "iné", "iného", "inému", "iní", 
    "inú", "iný", "iných", "iným", "inými", "ja", "je", "jeho", "jej", "jemu", 
    "ju", "k", "kam", "kamže", "každou", "každá", "každé", "každého", "každému", "každí", 
    "každú", "každý", "každých", "každým", "každými", "kde", "kej", "kejže", "keď", "keďže", 
    "kie", "kieho", "kiehože", "kiemu", "kiemuže", "kieže", "kinematografia", "koho", "kom", "komu", 
    "kou", "kouže", "kto", "ktorej", "ktorou", "ktorá", "ktoré", "ktorí", "ktorú", "ktorý", 
    "ktorých", "ktorým", "ktorými", "ku", "ká", "káže", "ké", "kéže", "kú", "kúže", 
    "ký", "kýho", "kýhože", "kým", "kýmu", "kýmuže", "kýže", "lebo", "leda", "ledaže", 
    "len", "ma", "majú", "mal", "mala", "mali", "mať", "medzi", "mi", "mne", 
    "mnou", "moja", "moje", "mojej", "mojich", "mojim", "mojimi", "mojou", "moju", "možno", 
    "mu", "musia", "musieť", "musí", "musím", "musíme", "musíte", "musíš", "my", "má", 
    "mám", "máme", "máte", "máš", "môcť", "môj", "môjho", "môže", "môžem", "môžeme", 
    "môžete", "môžeš", "môžu", "mňa", "na", "nad", "nado", "najmä", "nami", "naša", 
    "naše", "našej", "naši", "našich", "našim", "našimi", "našou", "ne", "nech", "neho", 
    "nej", "nejakej", "nejakom", "nejakou", "nejaká", "nejaké", "nejakého", "nejakému", "nejakú", "nejaký", 
    "nejakých", "nejakým", "nejakými", "nemu", "než", "nich", "nie", "niektorej", "niektorom", "niektorou", 
    "niektorá", "niektoré", "niektorého", "niektorému", "niektorú", "niektorý", "niektorých", "niektorým", "niektorými", "nielen", 
    "niečo", "nim", "nimi", "nič", "ničoho", "ničom", "ničomu", "ničím", "no", "nám", 
    "nás", "náš", "nášho", "ním", "o", "od", "odo", "on", "ona", "oni", 
    "ono", "ony", "oň", "oňho", "po", "pod", "podo", "podľa", "pokiaľ", "popod", 
    "popri", "potom", "poza", "pre", "pred", "predo", "preto", "pretože", "prečo", "pri", 
    "práve", "s", "sa", "seba", "sebe", "sebou", "sem", "si", "sme", "snímka", 
    "snímky", "so", "som", "ste", "svoj", "svoja", "svoje", "svojho", "svojich", "svojim", 
    "svojimi", "svojou", "svoju", "svojím", "sú", "ta", "tak", "takej", "takejto", "taká", 
    "takáto", "také", "takého", "takéhoto", "takému", "takémuto", "takéto", "takí", "takú", "takúto", 
    "taký", "takýto", "takže", "tam", "teba", "tebe", "tebou", "teda", "tej", "tejto", 
    "ten", "tento", "ti", "tie", "tieto", "tiež", "to", "toho", "tohoto", "tohto", 
    "tom", "tomto", "tomu", "tomuto", "toto", "tou", "touto", "tu", "tvoj", "tvoja", 
    "tvoje", "tvojej", "tvojho", "tvoji", "tvojich", "tvojim", "tvojimi", "tvojím", "ty", "tá", 
    "táto", "tí", "títo", "tú", "túto", "tých", "týchto", "tým", "tými", "týmto", 
    "u", "už", "v", "vami", "vaša", "vaše", "vašej", "vaši", "vašich", "vašim", 
    "vaším", "veď", "viac", "vo", "vy", "vám", "vás", "váš", "vášho", "však", 
    "všetci", "všetka", "všetko", "všetky", "všetok", "z", "za", "začo", "začože", "zo", 
    "áno", "čej", "či", "čia", "čie", "čieho", "čiemu", "čiu", "čo", "čoho", 
    "čom", "čomu", "čou", "čože", "čí", "čím", "čími", "ďalšia", "ďalšie", "ďalšieho", 
    "ďalšiemu", "ďalšiu", "ďalšom", "ďalšou", "ďalší", "ďalších", "ďalším", "ďalšími", "ňom", "ňou", 
    "ňu", "že"
}

def simple_slovak_stemmer(word):
    """A rule-based stemmer for Slovak"""
    word = word.lower()
    
    # Remove case endings for nouns, adjectives, etc.
    suffixes = ['ovi', 'ová', 'ovej', 'ových', 'ovým', 'ami', 'ách', 'iach', 
                'och', 'iam', 'om', 'am', 'emu', 'ého', 'ej', 'ou', 'ho',
                'ými', 'ými', 'ých', 'ého', 'ému', 'ými', 'ým', 'ím', 'im',
                'ov', 'mi', 'ia', 'ie', 'iu', 'í', 'ý', 'á', 'é', 'i', 'e', 
                'o', 'u', 'y', 'a']
    
    # Verb suffixes
    verb_suffixes = ['úvať', 'ívať', 'avať', 'ovať', 'úvam', 'ívam', 'avam',
                   'ujem', 'uješ', 'uje', 'ujeme', 'ujete', 'ujú',
                   'ím', 'íš', 'í', 'íme', 'íte', 'ia',
                   'il', 'ila', 'ili', 'ilo']
    
    # Try verb suffixes first
    for suffix in sorted(verb_suffixes, key=len, reverse=True):
        if len(word) > len(suffix) + 2 and word.endswith(suffix):
            return word[:-len(suffix)]
    
    # Then try other suffixes
    for suffix in sorted(suffixes, key=len, reverse=True):
        if len(word) > len(suffix) + 3 and word.endswith(suffix):
            return word[:-len(suffix)]
    
    return word

def clean_text(sentence, stop_words=STOP_WORDS_SK):
    """Clean and preprocess Slovak text"""
    # Remove URLs
    sentence = re.sub(r'https?:\/\/[^\s]+', '', sentence)
    
    # Remove HTML tags
    sentence = re.sub(r'<[^>]+>', '', sentence)
    
    # Remove words that contain digits
    sentence = re.sub(r'\b\w*\d\w*\b', '', sentence)
    
    # Remove whitespaces
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    
    # Remove digits
    sentence = re.sub(r'\b\d+\b', '', sentence)
    
    # Remove whitespaces again
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    
    # Remove punctuation
    sentence = re.sub(r'[^\w\s]', '', sentence)
    
    # Remove whitespaces again
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    
    # Convert to lowercase
    sentence = sentence.lower()
    
    # Remove stop words
    tokens = []
    for token in sentence.split():
        if token not in stop_words:
            tokens.append(token)
    
    return " ".join(tokens)

def handle_negations(text):
    """Mark words that follow negation words"""
    # Tokenize the text
    tokens = text.split()
    
    # Slovak negation words
    negation_words = ["nie", "ne", "nebudem", "nemám", "nemá", "nebude", 
                     "nechcem", "nechce", "bez", "ani"]
    
    negated_tokens = []
    negation_active = False
    
    for token in tokens:
        if token in negation_words or token.startswith("ne"):
            negation_active = True
            negated_tokens.append(token)
        elif token in [".", "!", "?", ";", ","]:  # Reset negation at punctuation
            negation_active = False
            negated_tokens.append(token)
        elif negation_active:
            # Mark words following negation
            negated_tokens.append("NEG_" + token)
        else:
            negated_tokens.append(token)
    
    return " ".join(negated_tokens)

def preprocess_for_sentiment(text, apply_stemming=True):
    """Complete preprocessing pipeline for Slovak sentiment analysis"""
    # First clean the text
    cleaned_text = clean_text(text)
    
    # Handle negations
    negation_handled_text = handle_negations(cleaned_text)
    
    if not apply_stemming:
        return negation_handled_text
    
    # Apply stemming
    tokens = negation_handled_text.split()
    stemmed_tokens = []
    
    for token in tokens:
        if token.startswith("NEG_"):
            # Handle negated tokens
            stem = simple_slovak_stemmer(token[4:])
            stemmed_tokens.append("NEG_" + stem)
        else:
            # Normal tokens
            stem = simple_slovak_stemmer(token)
            stemmed_tokens.append(stem)
    
    return " ".join(stemmed_tokens)

