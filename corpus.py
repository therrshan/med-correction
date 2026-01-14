import random

SYMPTOM_TEMPLATES = [
    "मुझे {body_part} में {pain_type} है",
    "{body_part} में {pain_type} हो रहा है",
    "मेरे {body_part} में बहुत {pain_type} है",
    "{body_part} में तेज {pain_type} है",
    "कल से {body_part} में {pain_type} शुरू हो गया",
    "{time} से {body_part} में {pain_type} है",
    "मुझे {symptom} हो रहा है",
    "{symptom} की समस्या है",
    "{time} से {symptom} है",
    "बहुत {symptom} महसूस हो रहा है",
    "मुझे {symptom1} और {symptom2} है",
    "{body_part} में {pain_type} और {symptom} है",
    "{symptom1} के साथ {symptom2} भी है",
    "{body_part} में हल्की {pain_type} है",
    "{body_part} में बहुत तेज {pain_type} है",
    "कभी-कभी {body_part} में {pain_type} होता है",
    "दो दिन से {symptom} है",
    "सुबह से {body_part} में {pain_type} है",
    "रात को {symptom} बढ़ जाता है",
    "खाना खाने के बाद {body_part} में {pain_type} होता है",
    "पिछले हफ्ते से {body_part} में {pain_type} है और {symptom} भी हो रहा है",
    "{body_part} में {pain_type} है जो {body_part2} तक फैल रहा है",
    "जब {action} करता हूं तो {body_part} में {pain_type} होता है",
    "नहीं, मुझे {symptom} नहीं है",
    "हां, {body_part} में {pain_type} है",
    "अभी तो {symptom} नहीं है",
    "{body_part} {adjective} लग रहा है",
    "त्वचा पर {skin_symptom} हो गई है",
    "{body_part} सूजा हुआ है",
    "क्या यह {disease} हो सकता है",
    "{symptom} के लिए क्या दवा लूं",
    "यह समस्या कब तक रहेगी",
]

BODY_PARTS = [
    "पेट", "सिर", "गला", "गले", "छाती", "पीठ", "कमर",
    "पैर", "पैरों", "हाथ", "हाथों", "नाक", "कान", "आंख", "आंखों",
    "दांत", "मसूड़ों", "जीभ", "गर्दन", "कंधा", "कंधों", "घुटना", "घुटनों",
    "उंगली", "उंगलियों", "कलाई", "टखना", "पीठ", "छाती",
]

PAIN_TYPES = [
    "दर्द", "तेज दर्द", "जलन", "खुजली", "सूजन", "ऐंठन",
    "भारीपन", "कड़ापन", "झनझनाहट", "सुन्नपन",
]

SYMPTOMS = [
    "बुखार", "खांसी", "सर्दी", "जुकाम", "उल्टी", "दस्त",
    "चक्कर", "कमजोरी", "थकान", "सांस लेने में तकलीफ",
    "भूख नहीं लगना", "नींद नहीं आना", "पसीना आना",
    "बेचैनी", "घबराहट", "वजन कम होना", "वजन बढ़ना",
]

ADJECTIVES = [
    "भारी", "हल्का", "सूजा हुआ", "लाल", "पीला", "सख्त",
    "नरम", "गर्म", "ठंडा", "सुन्न",
]

SKIN_SYMPTOMS = [
    "दाने", "खुजली", "लाली", "सूजन", "घाव", "चकत्ते", "फोड़े",
]

TIME_EXPRESSIONS = [
    "कल से", "परसों से", "तीन दिन से", "एक हफ्ते से",
    "सुबह से", "शाम से", "रात से", "दोपहर से",
]

ACTIONS = [
    "चलता", "खाता", "सोता", "बैठता", "खड़ा होता",
    "काम करता", "सीढ़ी चढ़ता",
]

DISEASES = [
    "डेंगू", "मलेरिया", "टाइफाइड", "निमोनिया", "अस्थमा",
]

COMPLETE_SENTENCES = [
    "मुझे पेट में दर्द है", "सिर में बहुत दर्द हो रहा है", "खांसी और बुखार है",
    "गले में खराश है", "नाक बह रही है", "उल्टी जैसा महसूस हो रहा है",
    "चक्कर आ रहे हैं", "बहुत कमजोरी महसूस हो रही है", "रात को नींद नहीं आती",
    "खाना खाने के बाद पेट में दर्द होता है", "दो दिन से बुखार है", "छाती में जलन हो रही है",
    "पीठ में बहुत दर्द है", "घुटनों में सूजन है", "त्वचा पर दाने हो गए हैं",
    "आंखों में जलन है", "कान में दर्द है", "दांत में दर्द हो रहा है",
    "हाथों में झनझनाहट है", "पैरों में सूजन है", "गर्दन में अकड़न है",
    "सांस लेने में तकलीफ हो रही है", "पेट में भारीपन महसूस हो रहा है", "सिर घूम रहा है",
    "बुखार के साथ ठंड लग रही है", "पूरे शरीर में दर्द है", "भूख बिल्कुल नहीं लग रही",
    "बहुत थकान महसूस हो रही है", "रात को बुखार बढ़ जाता है", "खाना हजम नहीं हो रहा",
    "पेट फूला हुआ लग रहा है", "मुंह सूख रहा है", "गला बैठ गया है",
    "आवाज नहीं निकल रही", "नाक बंद है", "कफ आ रहा है",
    "सूखी खांसी है", "छींकें आ रही हैं", "आंखों से पानी आ रहा है",
    "जी मिचला रहा है", "पेट में मरोड़ है", "शरीर टूट रहा है",
    "बदन दर्द हो रहा है", "सिर भारी लग रहा है", "आंखों के सामने अंधेरा छा जाता है",
    "दिल की धड़कन तेज है", "सीने में जकड़न है", "पसीना बहुत आ रहा है",
    "हाथ-पैर ठंडे हो रहे हैं", "पेट में गैस बन रही है", "कब्ज की शिकायत है",
    "लूज मोशन हो रहे हैं", "उल्टी हो गई", "मितली आ रही है", "सिरदर्द बहुत तेज है",
    "माइग्रेन का दर्द है", "आंखों में धुंधलापन है", "कान बज रहे हैं", "नाक से खून आ रहा है",
    "मसूड़ों से खून आता है", "दांत में झनझनाहट है", "जीभ पर छाले हैं",
    "मुंह में छाले हो गए हैं", "गला सूज गया है", "तालू में दर्द है",
    "निगलने में तकलीफ है", "सांस फूलती है", "खांसते समय दर्द होता है",
    "छाती में भारीपन है", "दिल बैठ जाता है", "धड़कन अनियमित है",
    "ब्लड प्रेशर हाई है", "शुगर बढ़ी हुई है", "वजन तेजी से कम हो रहा है",
    "वजन बढ़ रहा है", "भूख बहुत लगती है", "प्यास बहुत लगती है",
    "बार-बार पेशाब आता है", "पेशाब में जलन है", "पेशाब रुक-रुक कर आता है",
    "पेशाब का रंग गहरा है", "शौच में खून आता है", "शौच सख्त है",
    "पेट दर्द के साथ दस्त हैं", "बुखार उतर नहीं रहा", "ठंड लगकर बुखार आता है",
    "शाम को बुखार आता है", "रात को पसीना आता है", "हथेलियां और तलवे जलते हैं",
    "जोड़ों में दर्द रहता है", "घुटने में सूजन और दर्द है", "कमर दर्द बहुत है",
    "रीढ़ में दर्द है", "गर्दन घुमाने में दर्द होता है", "कंधे में अकड़न है",
    "बाजू उठाने में तकलीफ है", "कोहनी में दर्द है", "कलाई में मोच आई है",
    "उंगलियों में सूजन है", "अंगूठे में दर्द है", "हथेली में झनझनाहट है",
    "पैर की उंगली में दर्द है", "एड़ी में दर्द होता है", "तलवों में जलन है",
    "पिंडलियों में दर्द है", "जांघ में खिंचाव है", "कूल्हे में दर्द है",
]

def fill_template(template):
    sentence = template
    if "{body_part}" in sentence:
        sentence = sentence.replace("{body_part}", random.choice(BODY_PARTS))
    if "{body_part2}" in sentence:
        sentence = sentence.replace("{body_part2}", random.choice(BODY_PARTS))
    if "{pain_type}" in sentence:
        sentence = sentence.replace("{pain_type}", random.choice(PAIN_TYPES))
    if "{symptom}" in sentence:
        sentence = sentence.replace("{symptom}", random.choice(SYMPTOMS))
    if "{symptom1}" in sentence:
        sentence = sentence.replace("{symptom1}", random.choice(SYMPTOMS))
    if "{symptom2}" in sentence:
        sentence = sentence.replace("{symptom2}", random.choice(SYMPTOMS))
    if "{adjective}" in sentence:
        sentence = sentence.replace("{adjective}", random.choice(ADJECTIVES))
    if "{skin_symptom}" in sentence:
        sentence = sentence.replace("{skin_symptom}", random.choice(SKIN_SYMPTOMS))
    if "{time}" in sentence:
        sentence = sentence.replace("{time}", random.choice(TIME_EXPRESSIONS))
    if "{action}" in sentence:
        sentence = sentence.replace("{action}", random.choice(ACTIONS))
    if "{disease}" in sentence:
        sentence = sentence.replace("{disease}", random.choice(DISEASES))
    return sentence

def generate_medical_sentences(count=5000):
    sentences = set()
    sentences.update(COMPLETE_SENTENCES)
    
    attempts = 0
    max_attempts = count * 5
    
    while len(sentences) < count and attempts < max_attempts:
        if random.random() < 0.6:
            template = random.choice(SYMPTOM_TEMPLATES)
            sentence = fill_template(template)
        else:
            sentence = random.choice(COMPLETE_SENTENCES)
        sentences.add(sentence)
        attempts += 1
    
    if len(sentences) < count:
        print(f"Got {len(sentences)} unique sentences, adding combos...")
        sentences_list = list(sentences)
        while len(sentences) < count and len(sentences_list) > 1:
            s1 = random.choice(sentences_list)
            s2 = random.choice(sentences_list)
            if s1 != s2:
                sentences.add(f"{s1} और {s2}")
    
    return list(sentences)