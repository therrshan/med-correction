import random

PHONETIC_CONFUSIONS = {
    'क': ['ख', 'ग', 'क़'], 'ख': ['क', 'ग'], 'ग': ['क', 'घ'], 'घ': ['ग', 'ख'],
    'च': ['छ', 'ज'], 'छ': ['च', 'ज'], 'ज': ['च', 'झ', 'ज़'], 'झ': ['ज', 'छ'],
    'ट': ['ठ', 'ड'], 'ठ': ['ट', 'ड'], 'ड': ['ट', 'ढ'], 'ढ': ['ड', 'ठ'],
    'त': ['थ', 'द', 'ट'], 'थ': ['त', 'द'], 'द': ['त', 'ध'], 'ध': ['द', 'थ'],
    'प': ['फ', 'ब'], 'फ': ['प', 'ब', 'फ़'], 'ब': ['प', 'भ'], 'भ': ['ब', 'फ'],
    'स': ['श', 'ष'], 'श': ['स', 'ष'], 'ष': ['स', 'श'],
    'न': ['ण', 'म'], 'ण': ['न'], 'म': ['न'],
    'इ': ['ई', 'ए'], 'ई': ['इ'], 'उ': ['ऊ', 'ओ'], 'ऊ': ['उ'],
    'ए': ['ऐ', 'इ'], 'ऐ': ['ए'], 'ओ': ['औ', 'उ'], 'औ': ['ओ'],
    'र': ['ड़', 'ल'], 'ड़': ['र', 'ढ़'], 'ल': ['र', 'ळ'],
}

VISUAL_CONFUSIONS = {
    'र': ['ड'], 'व': ['ब'], 'ध': ['घ'], 'भ': ['म'],
    'ष': ['स'], 'न': ['ण'], 'ड': ['र'], 'घ': ['ध'],
}

MATRA_CONFUSIONS = {
    'ा': [''], 'ि': ['ी', ''], 'ी': ['ि', ''], 'ु': ['ू', ''], 'ू': ['ु', ''],
    'े': ['ै', ''], 'ै': ['े', ''], 'ो': ['ौ', ''], 'ौ': ['ो', ''],
    'ं': ['', 'ँ'], 'ँ': ['', 'ं'], '्': [''],
}

MEDICAL_TERMS = {
    'दर्द': ['दरद', 'डर्ड', 'दर्दे', 'दर्द़'],
    'पेट': ['पेन', 'पेत', 'पैट', 'पेठ'],
    'सिर': ['सि र', 'सीर', 'सर', 'शिर'],
    'खांसी': ['काशी', 'खासी', 'खाँसी', 'कांसी'],
    'बुखार': ['बूखार', 'बुकार', 'बखार', 'बुखर'],
    'गले': ['गाले', 'गल', 'गळे', 'गल्ले'],
    'जलन': ['जालन', 'ज़लन', 'जलान', 'जल्लन'],
    'चक्कर': ['चकर', 'चक्र', 'चाकर', 'चक्कार'],
    'सूजन': ['सुजन', 'सूज़न', 'शूजन', 'सूजान'],
    'कमजोरी': ['कमज़ोरी', 'कमजोरि', 'कमज़ोरि', 'कमजोर'],
    'थकान': ['थाकान', 'ठकान', 'थकन', 'थाकन'],
    'नाक': ['नक', 'नाख', 'नाग', 'नक़'],
    'कान': ['कन', 'कान', 'खान', 'कान्'],
    'आंख': ['आख', 'अंख', 'आँख', 'अखं'],
    'पैर': ['परै', 'पाइर', 'पायर', 'पेर'],
    'हाथ': ['हथ', 'हात', 'हाथ्', 'हाठ'],
    'उल्टी': ['उलटी', 'उलती', 'उल्टि', 'ऊल्टी'],
    'दस्त': ['दास्त', 'दस्ते', 'दस', 'दस्त्'],
    'खुजली': ['कुचली', 'खुजलि', 'खूजली', 'खुज़ली'],
    'ऐंठन': ['बेंठन', 'अंठन', 'ऐठन', 'ऐंठान'],
}

def corrupt_char(char, phonetic=True):
    if phonetic and char in PHONETIC_CONFUSIONS:
        return random.choice(PHONETIC_CONFUSIONS[char] + [char])
    elif not phonetic and char in VISUAL_CONFUSIONS:
        return random.choice(VISUAL_CONFUSIONS[char] + [char])
    return char

def corrupt_matra(text):
    result = []
    for char in text:
        if char in MATRA_CONFUSIONS and random.random() < 0.2:
            result.append(random.choice(MATRA_CONFUSIONS[char]))
        else:
            result.append(char)
    return ''.join(result)

def mess_with_spacing(text):
    words = text.split()
    if len(words) < 2:
        return text
    
    result = []
    i = 0
    while i < len(words):
        if i < len(words) - 1 and random.random() < 0.1:
            result.append(words[i] + words[i+1])
            i += 2
        elif len(words[i]) > 4 and random.random() < 0.1:
            split_pos = len(words[i]) // 2
            result.append(words[i][:split_pos])
            result.append(words[i][split_pos:])
            i += 1
        else:
            result.append(words[i])
            i += 1
    return ' '.join(result)

def corrupt_medical_word(word):
    for term, corruptions in MEDICAL_TERMS.items():
        if term in word and random.random() < 0.4:
            return word.replace(term, random.choice(corruptions))
    return word

def corrupt_word(word, intensity=0.15):
    if random.random() < 0.3:
        corrupted = corrupt_medical_word(word)
        if corrupted != word:
            return corrupted
    
    if random.random() < intensity:
        r = random.random()
        
        if r < 0.4:
            chars = list(word)
            if chars:
                idx = random.randint(0, len(chars) - 1)
                chars[idx] = corrupt_char(chars[idx], phonetic=True)
            word = ''.join(chars)
        elif r < 0.6:
            chars = list(word)
            if chars:
                idx = random.randint(0, len(chars) - 1)
                chars[idx] = corrupt_char(chars[idx], phonetic=False)
            word = ''.join(chars)
        elif r < 0.8:
            word = corrupt_matra(word)
        else:
            chars = list(word)
            for i in range(len(chars)):
                if random.random() < 0.15:
                    chars[i] = corrupt_char(chars[i], phonetic=random.choice([True, False]))
            word = ''.join(chars)
    
    return word

def add_noise(text, intensity=0.12, multiplier=1.0):
    actual_intensity = intensity * multiplier
    words = text.split()
    corrupted = [corrupt_word(w, actual_intensity) for w in words]
    result = ' '.join(corrupted)
    
    if random.random() < 0.15:
        result = mess_with_spacing(result)
    
    return result

def create_curriculum_samples(clean_text, num_variants=3):
    samples = []
    intensities = [0.5, 1.0, 1.5]
    
    for i in range(num_variants):
        mult = intensities[i % len(intensities)]
        noisy = add_noise(clean_text, intensity=0.12, multiplier=mult)
        if noisy != clean_text:
            samples.append((noisy, clean_text))
    
    return samples