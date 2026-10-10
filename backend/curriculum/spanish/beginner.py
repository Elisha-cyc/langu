"""
Spanish - Beginner level
50 lessons, fully written as the content template for the app.
Schema matches generate_scaffold.py.
"""

lessons = [
    {
        "lesson_number": 1,
        "title": "Greetings and Introductions",
        "vocabulary": [
            {"word": "Hola", "translation": "Hello", "pronunciation": "OH-lah"},
            {"word": "Buenos días", "translation": "Good morning", "pronunciation": "BWEH-nos DEE-as"},
            {"word": "Buenas tardes", "translation": "Good afternoon", "pronunciation": "BWEH-nas TAR-des"},
            {"word": "Me llamo", "translation": "My name is", "pronunciation": "meh YAH-mo"},
            {"word": "Mucho gusto", "translation": "Nice to meet you", "pronunciation": "MOO-cho GOOS-to"},
        ],
        "grammar": {
            "topic": "Basic sentence structure",
            "explanation": "Spanish greetings often stand alone as full sentences. 'Me llamo' literally means 'I call myself', using the reflexive verb 'llamarse'.",
        },
        "example_sentences": [
            {"target_language": "Hola, me llamo Ana.", "english": "Hello, my name is Ana."},
            {"target_language": "Buenos días, mucho gusto.", "english": "Good morning, nice to meet you."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'Good afternoon, my name is Carlos.'", "answer": "Buenas tardes, me llamo Carlos."},
            {"type": "fill_in_blank", "prompt": "Hola, ___ Sofía. (My name is)", "answer": "me llamo"},
        ],
    },
    {
        "lesson_number": 2,
        "title": "The Spanish Alphabet and Pronunciation",
        "vocabulary": [
            {"word": "a, e, i, o, u", "translation": "the five vowels", "pronunciation": "ah, eh, ee, oh, oo"},
            {"word": "ñ", "translation": "'enye' letter, unique to Spanish", "pronunciation": "EN-yeh"},
            {"word": "rr", "translation": "rolled/trilled r", "pronunciation": "strong rolled r"},
            {"word": "j", "translation": "like English 'h'", "pronunciation": "hard H sound"},
            {"word": "h", "translation": "always silent", "pronunciation": "silent"},
        ],
        "grammar": {
            "topic": "Vowel and consonant sounds",
            "explanation": "Spanish vowels have one consistent sound each, unlike English. Stress usually falls on the second-to-last syllable unless marked with an accent (á, é, í, ó, ú).",
        },
        "example_sentences": [
            {"target_language": "El perro corre rápido.", "english": "The dog runs fast (notice the rolled 'rr')."},
            {"target_language": "La niña se llama Begoña.", "english": "The girl's name is Begoña (notice the 'ñ')."},
        ],
        "exercises": [
            {"type": "multiple_choice", "prompt": "Which letter is silent in Spanish?", "answer": "h", "options": ["h", "j", "rr", "ñ"]},
            {"type": "translation", "prompt": "How many vowels does Spanish have?", "answer": "Five: a, e, i, o, u."},
        ],
    },
    {
        "lesson_number": 3,
        "title": "Numbers 0-20",
        "vocabulary": [
            {"word": "cero", "translation": "zero", "pronunciation": "SEH-ro"},
            {"word": "cinco", "translation": "five", "pronunciation": "SEEN-ko"},
            {"word": "diez", "translation": "ten", "pronunciation": "dee-EHZ"},
            {"word": "quince", "translation": "fifteen", "pronunciation": "KEEN-seh"},
            {"word": "veinte", "translation": "twenty", "pronunciation": "VAYN-teh"},
        ],
        "grammar": {
            "topic": "Counting basics",
            "explanation": "Numbers 16-19 combine 'dieci-' with the unit (dieciséis, diecisiete, dieciocho, diecinueve), and are written as one word.",
        },
        "example_sentences": [
            {"target_language": "Tengo veinte años.", "english": "I am twenty years old."},
            {"target_language": "Hay quince estudiantes.", "english": "There are fifteen students."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Write the number 17 in Spanish.", "answer": "diecisiete"},
            {"type": "fill_in_blank", "prompt": "Tengo ___ (5) hermanos.", "answer": "cinco"},
        ],
    },
    {
        "lesson_number": 4,
        "title": "Days of the Week",
        "vocabulary": [
            {"word": "lunes", "translation": "Monday", "pronunciation": "LOO-nes"},
            {"word": "miércoles", "translation": "Wednesday", "pronunciation": "mee-EHR-koh-les"},
            {"word": "viernes", "translation": "Friday", "pronunciation": "vee-EHR-nes"},
            {"word": "sábado", "translation": "Saturday", "pronunciation": "SAH-bah-doh"},
            {"word": "domingo", "translation": "Sunday", "pronunciation": "doh-MEEN-go"},
        ],
        "grammar": {
            "topic": "Days are not capitalized",
            "explanation": "Unlike English, days of the week in Spanish are lowercase and are all masculine, using 'el' (el lunes, el martes).",
        },
        "example_sentences": [
            {"target_language": "El lunes tengo clase de español.", "english": "On Monday I have Spanish class."},
            {"target_language": "Los sábados no trabajo.", "english": "On Saturdays I don't work."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'I rest on Sundays.'", "answer": "Descanso los domingos."},
            {"type": "fill_in_blank", "prompt": "Hoy es ___ (Wednesday).", "answer": "miércoles"},
        ],
    },
    {
        "lesson_number": 5,
        "title": "Months and Seasons",
        "vocabulary": [
            {"word": "enero", "translation": "January", "pronunciation": "eh-NEH-ro"},
            {"word": "julio", "translation": "July", "pronunciation": "HOO-lee-oh"},
            {"word": "primavera", "translation": "spring", "pronunciation": "pree-mah-VEH-rah"},
            {"word": "verano", "translation": "summer", "pronunciation": "veh-RAH-no"},
            {"word": "invierno", "translation": "winter", "pronunciation": "een-vee-EHR-no"},
        ],
        "grammar": {
            "topic": "Talking about dates",
            "explanation": "To express a date, Spanish uses 'el' + number + 'de' + month: 'el 5 de mayo' (May 5th). Months are also lowercase.",
        },
        "example_sentences": [
            {"target_language": "Mi cumpleaños es el 3 de julio.", "english": "My birthday is on July 3rd."},
            {"target_language": "En invierno hace mucho frío.", "english": "In winter it's very cold."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'Summer is my favorite season.'", "answer": "El verano es mi estación favorita."},
            {"type": "fill_in_blank", "prompt": "Hoy es el primero de ___ (January).", "answer": "enero"},
        ],
    },
    {
        "lesson_number": 6,
        "title": "Colors",
        "vocabulary": [
            {"word": "rojo", "translation": "red", "pronunciation": "ROH-ho"},
            {"word": "azul", "translation": "blue", "pronunciation": "ah-SOOL"},
            {"word": "verde", "translation": "green", "pronunciation": "VEHR-deh"},
            {"word": "amarillo", "translation": "yellow", "pronunciation": "ah-mah-REE-yoh"},
            {"word": "negro", "translation": "black", "pronunciation": "NEH-groh"},
        ],
        "grammar": {
            "topic": "Adjective agreement with colors",
            "explanation": "Colors ending in -o change to -a for feminine nouns (rojo/roja), and add -s for plural. Colors ending in other letters (verde, azul) usually don't change for gender.",
        },
        "example_sentences": [
            {"target_language": "La casa es azul.", "english": "The house is blue."},
            {"target_language": "Tengo dos camisas rojas.", "english": "I have two red shirts."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "El coche es ___ (black).", "answer": "negro"},
            {"type": "translation", "prompt": "Translate: 'The flowers are yellow.'", "answer": "Las flores son amarillas."},
        ],
    },
    {
        "lesson_number": 7,
        "title": "Family Members",
        "vocabulary": [
            {"word": "madre", "translation": "mother", "pronunciation": "MAH-dreh"},
            {"word": "padre", "translation": "father", "pronunciation": "PAH-dreh"},
            {"word": "hermano/a", "translation": "brother/sister", "pronunciation": "ehr-MAH-noh/nah"},
            {"word": "abuela", "translation": "grandmother", "pronunciation": "ah-BWEH-lah"},
            {"word": "primo/a", "translation": "cousin", "pronunciation": "PREE-moh/mah"},
        ],
        "grammar": {
            "topic": "Possessive adjectives (mi, tu, su)",
            "explanation": "'Mi', 'tu', and 'su' (my, your, his/her) don't change for gender, only for number: mi hermano, mis hermanos.",
        },
        "example_sentences": [
            {"target_language": "Mi madre es doctora.", "english": "My mother is a doctor."},
            {"target_language": "Tus primos viven en México.", "english": "Your cousins live in Mexico."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'My grandmother cooks well.'", "answer": "Mi abuela cocina bien."},
            {"type": "fill_in_blank", "prompt": "___ hermana es alta. (My)", "answer": "Mi"},
        ],
    },
    {
        "lesson_number": 8,
        "title": "Subject Pronouns",
        "vocabulary": [
            {"word": "yo", "translation": "I", "pronunciation": "yoh"},
            {"word": "tú", "translation": "you (informal)", "pronunciation": "too"},
            {"word": "él / ella", "translation": "he / she", "pronunciation": "ehl / EH-yah"},
            {"word": "nosotros/as", "translation": "we", "pronunciation": "noh-SOH-trohs"},
            {"word": "ellos/as", "translation": "they", "pronunciation": "EH-yohs"},
        ],
        "grammar": {
            "topic": "Formal vs informal 'you'",
            "explanation": "Spanish distinguishes 'tú' (informal) from 'usted' (formal) for 'you' singular. Subject pronouns are often dropped since the verb ending shows who is speaking.",
        },
        "example_sentences": [
            {"target_language": "Nosotros somos estudiantes.", "english": "We are students."},
            {"target_language": "¿Usted es el profesor?", "english": "Are you (formal) the teacher?"},
        ],
        "exercises": [
            {"type": "multiple_choice", "prompt": "Which pronoun is used for 'they' (all women)?", "answer": "ellas", "options": ["ellos", "ellas", "nosotras", "ustedes"]},
            {"type": "translation", "prompt": "Translate: 'She is my friend.'", "answer": "Ella es mi amiga."},
        ],
    },
    {
        "lesson_number": 9,
        "title": "Ser vs Estar (Introduction)",
        "vocabulary": [
            {"word": "ser", "translation": "to be (permanent)", "pronunciation": "sehr"},
            {"word": "estar", "translation": "to be (temporary/location)", "pronunciation": "ehs-TAHR"},
            {"word": "soy", "translation": "I am (ser)", "pronunciation": "soy"},
            {"word": "estoy", "translation": "I am (estar)", "pronunciation": "ehs-TOY"},
            {"word": "cansado/a", "translation": "tired", "pronunciation": "kahn-SAH-doh"},
        ],
        "grammar": {
            "topic": "Choosing ser or estar",
            "explanation": "Use 'ser' for identity, characteristics, origin, and time (Soy de España). Use 'estar' for location, temporary states, and feelings (Estoy cansado).",
        },
        "example_sentences": [
            {"target_language": "Soy alto y soy de Perú.", "english": "I am tall and I am from Peru."},
            {"target_language": "Estoy en la biblioteca.", "english": "I am at the library."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "___ cansada hoy. (estar, I am)", "answer": "Estoy"},
            {"type": "translation", "prompt": "Translate: 'He is a doctor.'", "answer": "Él es doctor."},
        ],
    },
    {
        "lesson_number": 10,
        "title": "Present Tense of -AR Verbs",
        "vocabulary": [
            {"word": "hablar", "translation": "to speak", "pronunciation": "ah-BLAHR"},
            {"word": "trabajar", "translation": "to work", "pronunciation": "trah-bah-HAHR"},
            {"word": "estudiar", "translation": "to study", "pronunciation": "ehs-too-dee-AHR"},
            {"word": "cantar", "translation": "to sing", "pronunciation": "kahn-TAHR"},
            {"word": "bailar", "translation": "to dance", "pronunciation": "bye-LAHR"},
        ],
        "grammar": {
            "topic": "-AR verb conjugation",
            "explanation": "Drop -ar and add: -o, -as, -a, -amos, -áis, -an. Example: hablar → hablo, hablas, habla, hablamos, habláis, hablan.",
        },
        "example_sentences": [
            {"target_language": "Yo hablo español y ella habla inglés.", "english": "I speak Spanish and she speaks English."},
            {"target_language": "Nosotros trabajamos los lunes.", "english": "We work on Mondays."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Ellos ___ (bailar) salsa.", "answer": "bailan"},
            {"type": "translation", "prompt": "Translate: 'I study every day.'", "answer": "Estudio todos los días."},
        ],
    },
    {
        "lesson_number": 11,
        "title": "Present Tense of -ER Verbs",
        "vocabulary": [
            {"word": "comer", "translation": "to eat", "pronunciation": "koh-MEHR"},
            {"word": "beber", "translation": "to drink", "pronunciation": "beh-BEHR"},
            {"word": "leer", "translation": "to read", "pronunciation": "leh-EHR"},
            {"word": "aprender", "translation": "to learn", "pronunciation": "ah-prehn-DEHR"},
            {"word": "correr", "translation": "to run", "pronunciation": "koh-RREHR"},
        ],
        "grammar": {
            "topic": "-ER verb conjugation",
            "explanation": "Drop -er and add: -o, -es, -e, -emos, -éis, -en. Example: comer → como, comes, come, comemos, coméis, comen.",
        },
        "example_sentences": [
            {"target_language": "Tú comes mucha fruta.", "english": "You eat a lot of fruit."},
            {"target_language": "Aprendemos español juntos.", "english": "We learn Spanish together."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Yo ___ (beber) agua.", "answer": "bebo"},
            {"type": "translation", "prompt": "Translate: 'They read books.'", "answer": "Ellos leen libros."},
        ],
    },
    {
        "lesson_number": 12,
        "title": "Present Tense of -IR Verbs",
        "vocabulary": [
            {"word": "vivir", "translation": "to live", "pronunciation": "vee-VEER"},
            {"word": "escribir", "translation": "to write", "pronunciation": "ehs-kree-BEER"},
            {"word": "abrir", "translation": "to open", "pronunciation": "ah-BREER"},
            {"word": "recibir", "translation": "to receive", "pronunciation": "reh-see-BEER"},
            {"word": "decidir", "translation": "to decide", "pronunciation": "deh-see-DEER"},
        ],
        "grammar": {
            "topic": "-IR verb conjugation",
            "explanation": "Drop -ir and add: -o, -es, -e, -imos, -ís, -en. Example: vivir → vivo, vives, vive, vivimos, vivís, viven.",
        },
        "example_sentences": [
            {"target_language": "Vivimos en Madrid.", "english": "We live in Madrid."},
            {"target_language": "Ella escribe una carta.", "english": "She writes a letter."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Yo ___ (abrir) la puerta.", "answer": "abro"},
            {"type": "translation", "prompt": "Translate: 'You (informal) decide.'", "answer": "Tú decides."},
        ],
    },
    {
        "lesson_number": 13,
        "title": "Definite and Indefinite Articles",
        "vocabulary": [
            {"word": "el", "translation": "the (masc. sing.)", "pronunciation": "ehl"},
            {"word": "la", "translation": "the (fem. sing.)", "pronunciation": "lah"},
            {"word": "un", "translation": "a/an (masc.)", "pronunciation": "oon"},
            {"word": "una", "translation": "a/an (fem.)", "pronunciation": "OO-nah"},
            {"word": "los / las", "translation": "the (plural)", "pronunciation": "lohs / lahs"},
        ],
        "grammar": {
            "topic": "Article agreement",
            "explanation": "Articles must agree in gender and number with the noun: el libro, la mesa, los libros, las mesas.",
        },
        "example_sentences": [
            {"target_language": "El libro está en la mesa.", "english": "The book is on the table."},
            {"target_language": "Quiero un café y una agua.", "english": "I want a coffee and a water."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "___ (the) casa es grande.", "answer": "La"},
            {"type": "translation", "prompt": "Translate: 'The students (plural) study.'", "answer": "Los estudiantes estudian."},
        ],
    },
    {
        "lesson_number": 14,
        "title": "Gender of Nouns",
        "vocabulary": [
            {"word": "chico/a", "translation": "boy/girl", "pronunciation": "CHEE-koh/kah"},
            {"word": "ciudad", "translation": "city (feminine)", "pronunciation": "see-oo-DAHD"},
            {"word": "problema", "translation": "problem (masculine, exception)", "pronunciation": "proh-BLEH-mah"},
            {"word": "mano", "translation": "hand (feminine, exception)", "pronunciation": "MAH-noh"},
            {"word": "día", "translation": "day (masculine, exception)", "pronunciation": "DEE-ah"},
        ],
        "grammar": {
            "topic": "Rules and exceptions",
            "explanation": "Most nouns ending in -o are masculine and -a are feminine, but there are exceptions like 'el día' and 'la mano'. Words ending in -ción, -sión, -dad are almost always feminine.",
        },
        "example_sentences": [
            {"target_language": "El problema es difícil.", "english": "The problem is difficult."},
            {"target_language": "La ciudad es hermosa.", "english": "The city is beautiful."},
        ],
        "exercises": [
            {"type": "multiple_choice", "prompt": "Which article goes with 'mano'?", "answer": "la", "options": ["el", "la", "los", "las"]},
            {"type": "translation", "prompt": "Translate: 'The day is long.'", "answer": "El día es largo."},
        ],
    },
    {
        "lesson_number": 15,
        "title": "Plural of Nouns",
        "vocabulary": [
            {"word": "libro / libros", "translation": "book / books", "pronunciation": "LEE-broh(s)"},
            {"word": "lápiz / lápices", "translation": "pencil / pencils", "pronunciation": "LAH-pees / LAH-pee-sehs"},
            {"word": "mujer / mujeres", "translation": "woman / women", "pronunciation": "moo-HEHR(-ehs)"},
            {"word": "flor / flores", "translation": "flower / flowers", "pronunciation": "flohr(-ehs)"},
            {"word": "papel / papeles", "translation": "paper / papers", "pronunciation": "pah-PEHL(-ehs)"},
        ],
        "grammar": {
            "topic": "Pluralization rules",
            "explanation": "Add -s to words ending in a vowel; add -es to words ending in a consonant. Words ending in -z change to -ces (lápiz → lápices).",
        },
        "example_sentences": [
            {"target_language": "Tengo tres lápices.", "english": "I have three pencils."},
            {"target_language": "Las mujeres trabajan aquí.", "english": "The women work here."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Give the plural of 'flor'.", "answer": "flores"},
            {"type": "fill_in_blank", "prompt": "Compro dos ___ (papel, plural).", "answer": "papeles"},
        ],
    },
    {
        "lesson_number": 16,
        "title": "Adjective Agreement",
        "vocabulary": [
            {"word": "alto/a", "translation": "tall", "pronunciation": "AHL-toh/tah"},
            {"word": "bonito/a", "translation": "pretty/nice", "pronunciation": "boh-NEE-toh/tah"},
            {"word": "inteligente", "translation": "intelligent (invariable)", "pronunciation": "een-teh-lee-HEHN-teh"},
            {"word": "grande", "translation": "big (invariable)", "pronunciation": "GRAHN-deh"},
            {"word": "pequeño/a", "translation": "small", "pronunciation": "peh-KEH-nyoh/nyah"},
        ],
        "grammar": {
            "topic": "Adjectives agree in gender and number",
            "explanation": "Adjectives ending in -o/-a change for gender and add -s for plural. Adjectives ending in -e (like 'inteligente') stay the same for both genders.",
        },
        "example_sentences": [
            {"target_language": "La casa es pequeña y bonita.", "english": "The house is small and pretty."},
            {"target_language": "Los chicos son inteligentes.", "english": "The boys are intelligent."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Ella es muy ___ (tall).", "answer": "alta"},
            {"type": "translation", "prompt": "Translate: 'The dogs are big.'", "answer": "Los perros son grandes."},
        ],
    },
    {
        "lesson_number": 17,
        "title": "Numbers 21-100",
        "vocabulary": [
            {"word": "veintiuno", "translation": "twenty-one", "pronunciation": "vayn-tee-OO-noh"},
            {"word": "treinta", "translation": "thirty", "pronunciation": "TRAYN-tah"},
            {"word": "cincuenta", "translation": "fifty", "pronunciation": "seen-KWEHN-tah"},
            {"word": "setenta", "translation": "seventy", "pronunciation": "seh-TEHN-tah"},
            {"word": "cien", "translation": "one hundred", "pronunciation": "see-EHN"},
        ],
        "grammar": {
            "topic": "Compound numbers",
            "explanation": "From 31 onward, numbers are written as three words with 'y': treinta y uno, cuarenta y dos. Note: 'cien' is used alone, but 'ciento' before other numbers (ciento uno).",
        },
        "example_sentences": [
            {"target_language": "Tengo cuarenta y cinco años.", "english": "I am forty-five years old."},
            {"target_language": "Hay cien personas aquí.", "english": "There are one hundred people here."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Write '67' in Spanish.", "answer": "sesenta y siete"},
            {"type": "fill_in_blank", "prompt": "Necesito ___ (30) minutos.", "answer": "treinta"},
        ],
    },
    {
        "lesson_number": 18,
        "title": "Telling Time",
        "vocabulary": [
            {"word": "¿Qué hora es?", "translation": "What time is it?", "pronunciation": "keh OH-rah ehs"},
            {"word": "en punto", "translation": "on the dot / sharp", "pronunciation": "ehn POON-toh"},
            {"word": "media", "translation": "half (past)", "pronunciation": "MEH-dee-ah"},
            {"word": "cuarto", "translation": "quarter", "pronunciation": "KWAR-toh"},
            {"word": "de la mañana / tarde / noche", "translation": "in the morning/afternoon/night", "pronunciation": "deh lah mah-NYAH-nah"},
        ],
        "grammar": {
            "topic": "Es la / Son las",
            "explanation": "Use 'Es la una' for 1:00, and 'Son las' for all other hours: Son las tres, Son las cinco y media.",
        },
        "example_sentences": [
            {"target_language": "Son las tres y cuarto de la tarde.", "english": "It's 3:15 in the afternoon."},
            {"target_language": "Es la una en punto.", "english": "It's exactly one o'clock."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'It's 8:30 at night.'", "answer": "Son las ocho y media de la noche."},
            {"type": "fill_in_blank", "prompt": "Son las diez y ___ (quarter).", "answer": "cuarto"},
        ],
    },
    {
        "lesson_number": 19,
        "title": "Question Words",
        "vocabulary": [
            {"word": "qué", "translation": "what", "pronunciation": "keh"},
            {"word": "quién", "translation": "who", "pronunciation": "kee-EHN"},
            {"word": "dónde", "translation": "where", "pronunciation": "DOHN-deh"},
            {"word": "cuándo", "translation": "when", "pronunciation": "KWAHN-doh"},
            {"word": "por qué", "translation": "why", "pronunciation": "pohr keh"},
        ],
        "grammar": {
            "topic": "Question word accents",
            "explanation": "Question words always carry a written accent when used in questions (qué, quién) to distinguish them from relative pronouns without accents (que, quien).",
        },
        "example_sentences": [
            {"target_language": "¿Dónde vives?", "english": "Where do you live?"},
            {"target_language": "¿Por qué estudias español?", "english": "Why do you study Spanish?"},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'When is the party?'", "answer": "¿Cuándo es la fiesta?"},
            {"type": "fill_in_blank", "prompt": "¿___ es tu profesor? (who)", "answer": "Quién"},
        ],
    },
    {
        "lesson_number": 20,
        "title": "Basic Food Vocabulary",
        "vocabulary": [
            {"word": "pan", "translation": "bread", "pronunciation": "pahn"},
            {"word": "agua", "translation": "water", "pronunciation": "AH-gwah"},
            {"word": "carne", "translation": "meat", "pronunciation": "KAR-neh"},
            {"word": "fruta", "translation": "fruit", "pronunciation": "FROO-tah"},
            {"word": "verdura", "translation": "vegetable", "pronunciation": "vehr-DOO-rah"},
        ],
        "grammar": {
            "topic": "Uncountable nouns with 'un poco de'",
            "explanation": "Use 'un poco de' (a little) before uncountable foods: un poco de pan, un poco de agua.",
        },
        "example_sentences": [
            {"target_language": "Quiero un poco de pan y fruta.", "english": "I want a little bread and fruit."},
            {"target_language": "No como carne los viernes.", "english": "I don't eat meat on Fridays."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'I like vegetables.'", "answer": "Me gustan las verduras."},
            {"type": "fill_in_blank", "prompt": "Bebo ___ (water) todos los días.", "answer": "agua"},
        ],
    },
    {
        "lesson_number": 21,
        "title": "Ordering at a Restaurant",
        "vocabulary": [
            {"word": "la cuenta", "translation": "the bill", "pronunciation": "lah KWEHN-tah"},
            {"word": "el menú", "translation": "the menu", "pronunciation": "ehl meh-NOO"},
            {"word": "quisiera", "translation": "I would like", "pronunciation": "kee-see-EH-rah"},
            {"word": "para beber", "translation": "to drink", "pronunciation": "PAH-rah beh-BEHR"},
            {"word": "de postre", "translation": "for dessert", "pronunciation": "deh POHS-treh"},
        ],
        "grammar": {
            "topic": "Polite requests with 'quisiera'",
            "explanation": "'Quisiera' (I would like) is more polite than 'quiero' (I want) and is commonly used when ordering food.",
        },
        "example_sentences": [
            {"target_language": "Quisiera la sopa, por favor.", "english": "I would like the soup, please."},
            {"target_language": "¿Puede traer la cuenta?", "english": "Can you bring the bill?"},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'For dessert, I would like ice cream.'", "answer": "De postre, quisiera helado."},
            {"type": "fill_in_blank", "prompt": "¿Puedo ver el ___ (menu)?", "answer": "menú"},
        ],
    },
    {
        "lesson_number": 22,
        "title": "Weather Expressions",
        "vocabulary": [
            {"word": "Hace calor", "translation": "It's hot", "pronunciation": "AH-seh kah-LOHR"},
            {"word": "Hace frío", "translation": "It's cold", "pronunciation": "AH-seh FREE-oh"},
            {"word": "Está lloviendo", "translation": "It's raining", "pronunciation": "ehs-TAH yoh-vee-EHN-doh"},
            {"word": "Está nublado", "translation": "It's cloudy", "pronunciation": "ehs-TAH noo-BLAH-doh"},
            {"word": "Hace sol", "translation": "It's sunny", "pronunciation": "AH-seh sohl"},
        ],
        "grammar": {
            "topic": "'Hacer' and 'estar' with weather",
            "explanation": "Many weather expressions use 'hacer' (hace calor, hace frío) while ongoing conditions use 'estar' + gerund (está lloviendo).",
        },
        "example_sentences": [
            {"target_language": "Hoy hace mucho calor.", "english": "Today it's very hot."},
            {"target_language": "Está lloviendo, lleva paraguas.", "english": "It's raining, bring an umbrella."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'It's cold and cloudy.'", "answer": "Hace frío y está nublado."},
            {"type": "fill_in_blank", "prompt": "Hace mucho ___ (sun/sunny) hoy.", "answer": "sol"},
        ],
    },
    {
        "lesson_number": 23,
        "title": "Describing People (Physical)",
        "vocabulary": [
            {"word": "delgado/a", "translation": "thin", "pronunciation": "dehl-GAH-doh"},
            {"word": "moreno/a", "translation": "dark-haired/skinned", "pronunciation": "moh-REH-noh"},
            {"word": "rubio/a", "translation": "blonde", "pronunciation": "ROO-bee-oh"},
            {"word": "ojos", "translation": "eyes", "pronunciation": "OH-hohs"},
            {"word": "pelo", "translation": "hair", "pronunciation": "PEH-loh"},
        ],
        "grammar": {
            "topic": "Describing with 'tener' and 'ser'",
            "explanation": "Use 'tener' for physical features you possess (tengo ojos azules) and 'ser' for overall build (soy delgado).",
        },
        "example_sentences": [
            {"target_language": "Tengo el pelo rubio y los ojos verdes.", "english": "I have blonde hair and green eyes."},
            {"target_language": "Mi hermano es alto y delgado.", "english": "My brother is tall and thin."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'She has brown eyes.'", "answer": "Ella tiene los ojos marrones."},
            {"type": "fill_in_blank", "prompt": "Él es ___ (dark-haired/skinned).", "answer": "moreno"},
        ],
    },
    {
        "lesson_number": 24,
        "title": "Describing Personality",
        "vocabulary": [
            {"word": "amable", "translation": "kind", "pronunciation": "ah-MAH-bleh"},
            {"word": "divertido/a", "translation": "fun", "pronunciation": "dee-vehr-TEE-doh"},
            {"word": "tímido/a", "translation": "shy", "pronunciation": "TEE-mee-doh"},
            {"word": "trabajador/a", "translation": "hard-working", "pronunciation": "trah-bah-hah-DOHR"},
            {"word": "perezoso/a", "translation": "lazy", "pronunciation": "peh-reh-SOH-soh"},
        ],
        "grammar": {
            "topic": "Personality adjectives with 'ser'",
            "explanation": "Personality traits use 'ser' because they describe lasting characteristics, not temporary states.",
        },
        "example_sentences": [
            {"target_language": "Mi amiga es muy amable y divertida.", "english": "My friend is very kind and fun."},
            {"target_language": "Él es trabajador pero un poco tímido.", "english": "He is hard-working but a bit shy."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'They are lazy.'", "answer": "Ellos son perezosos."},
            {"type": "fill_in_blank", "prompt": "Ella es muy ___ (kind).", "answer": "amable"},
        ],
    },
    {
        "lesson_number": 25,
        "title": "The Verb 'Gustar'",
        "vocabulary": [
            {"word": "me gusta", "translation": "I like (singular)", "pronunciation": "meh GOOS-tah"},
            {"word": "me gustan", "translation": "I like (plural)", "pronunciation": "meh GOOS-tahn"},
            {"word": "te gusta", "translation": "you like", "pronunciation": "teh GOOS-tah"},
            {"word": "le gusta", "translation": "he/she likes", "pronunciation": "leh GOOS-tah"},
            {"word": "nos gusta", "translation": "we like", "pronunciation": "nohs GOOS-tah"},
        ],
        "grammar": {
            "topic": "Gustar agrees with the thing liked",
            "explanation": "'Gustar' works backwards from English: the thing liked is the subject. Use 'gusta' with singular nouns/infinitives and 'gustan' with plural nouns.",
        },
        "example_sentences": [
            {"target_language": "Me gusta el chocolate.", "english": "I like chocolate."},
            {"target_language": "Nos gustan las películas.", "english": "We like movies."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "A ella le ___ (gustar) los libros.", "answer": "gustan"},
            {"type": "translation", "prompt": "Translate: 'Do you like coffee?'", "answer": "¿Te gusta el café?"},
        ],
    },
    {
        "lesson_number": 26,
        "title": "Common Irregular Verbs: Ir, Tener, Hacer",
        "vocabulary": [
            {"word": "voy", "translation": "I go", "pronunciation": "voy"},
            {"word": "tengo", "translation": "I have", "pronunciation": "TEHN-goh"},
            {"word": "hago", "translation": "I do/make", "pronunciation": "AH-goh"},
            {"word": "vas", "translation": "you go", "pronunciation": "vahs"},
            {"word": "tiene", "translation": "he/she has", "pronunciation": "tee-EH-neh"},
        ],
        "grammar": {
            "topic": "Irregular yo forms",
            "explanation": "'Ir' (voy, vas, va...), 'tener' (tengo, tienes, tiene...) and 'hacer' (hago, haces, hace...) don't follow regular patterns and must be memorized.",
        },
        "example_sentences": [
            {"target_language": "Voy a la escuela y tengo tres clases.", "english": "I go to school and I have three classes."},
            {"target_language": "Ella hace la tarea todos los días.", "english": "She does homework every day."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Yo ___ (tener) dos gatos.", "answer": "tengo"},
            {"type": "translation", "prompt": "Translate: 'We go to the park.'", "answer": "Vamos al parque."},
        ],
    },
    {
        "lesson_number": 27,
        "title": "Talking About Daily Routine",
        "vocabulary": [
            {"word": "despertarse", "translation": "to wake up", "pronunciation": "dehs-pehr-TAHR-seh"},
            {"word": "levantarse", "translation": "to get up", "pronunciation": "leh-vahn-TAHR-seh"},
            {"word": "ducharse", "translation": "to shower", "pronunciation": "doo-CHAR-seh"},
            {"word": "desayunar", "translation": "to have breakfast", "pronunciation": "deh-sah-yoo-NAHR"},
            {"word": "acostarse", "translation": "to go to bed", "pronunciation": "ah-kohs-TAHR-seh"},
        ],
        "grammar": {
            "topic": "Introducing reflexive verbs",
            "explanation": "Many routine verbs are reflexive because the action is done to oneself: me despierto (I wake myself up), te levantas (you get yourself up).",
        },
        "example_sentences": [
            {"target_language": "Me despierto a las siete.", "english": "I wake up at seven."},
            {"target_language": "Nos acostamos a las once.", "english": "We go to bed at eleven."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'She showers in the morning.'", "answer": "Ella se ducha por la mañana."},
            {"type": "fill_in_blank", "prompt": "Yo ___ (desayunar) a las ocho.", "answer": "desayuno"},
        ],
    },
    {
        "lesson_number": 28,
        "title": "Reflexive Verbs (In Depth)",
        "vocabulary": [
            {"word": "me", "translation": "myself", "pronunciation": "meh"},
            {"word": "te", "translation": "yourself", "pronunciation": "teh"},
            {"word": "se", "translation": "himself/herself/yourself formal", "pronunciation": "seh"},
            {"word": "nos", "translation": "ourselves", "pronunciation": "nohs"},
            {"word": "vestirse", "translation": "to get dressed", "pronunciation": "vehs-TEER-seh"},
        ],
        "grammar": {
            "topic": "Placement of reflexive pronouns",
            "explanation": "Reflexive pronouns go before a conjugated verb (me visto) or can attach to an infinitive (voy a vestirme).",
        },
        "example_sentences": [
            {"target_language": "¿A qué hora te vistes?", "english": "What time do you get dressed?"},
            {"target_language": "Voy a ducharme antes de salir.", "english": "I'm going to shower before going out."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Ellos ___ (levantarse) temprano.", "answer": "se levantan"},
            {"type": "translation", "prompt": "Translate: 'I get dressed quickly.'", "answer": "Me visto rápido."},
        ],
    },
    {
        "lesson_number": 29,
        "title": "Places in the City",
        "vocabulary": [
            {"word": "el banco", "translation": "the bank", "pronunciation": "ehl BAHN-koh"},
            {"word": "la farmacia", "translation": "the pharmacy", "pronunciation": "lah far-MAH-see-ah"},
            {"word": "el mercado", "translation": "the market", "pronunciation": "ehl mehr-KAH-doh"},
            {"word": "la iglesia", "translation": "the church", "pronunciation": "lah ee-GLEH-see-ah"},
            {"word": "el parque", "translation": "the park", "pronunciation": "ehl PAR-keh"},
        ],
        "grammar": {
            "topic": "Contraction 'al'",
            "explanation": "'A' + 'el' contracts to 'al': Voy al banco (I go to the bank). This does not happen with la, los, las.",
        },
        "example_sentences": [
            {"target_language": "Voy al mercado a comprar fruta.", "english": "I'm going to the market to buy fruit."},
            {"target_language": "La farmacia está cerca del parque.", "english": "The pharmacy is near the park."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'We are going to the church.'", "answer": "Vamos a la iglesia."},
            {"type": "fill_in_blank", "prompt": "Voy ___ (a + el) banco.", "answer": "al"},
        ],
    },
    {
        "lesson_number": 30,
        "title": "Giving Directions",
        "vocabulary": [
            {"word": "a la derecha", "translation": "to the right", "pronunciation": "ah lah deh-REH-chah"},
            {"word": "a la izquierda", "translation": "to the left", "pronunciation": "ah lah ees-kee-EHR-dah"},
            {"word": "todo recto", "translation": "straight ahead", "pronunciation": "TOH-doh REHK-toh"},
            {"word": "cerca de", "translation": "near", "pronunciation": "SEHR-kah deh"},
            {"word": "lejos de", "translation": "far from", "pronunciation": "LEH-hohs deh"},
        ],
        "grammar": {
            "topic": "Commands for directions",
            "explanation": "Directions often use the imperative: gire (turn), siga (continue), cruce (cross), which will be studied in depth in later lessons.",
        },
        "example_sentences": [
            {"target_language": "Siga todo recto y gire a la derecha.", "english": "Continue straight and turn right."},
            {"target_language": "El museo está cerca de aquí.", "english": "The museum is near here."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'Turn left, it's far from the hotel.'", "answer": "Gire a la izquierda, está lejos del hotel."},
            {"type": "fill_in_blank", "prompt": "El banco está ___ (near) el parque.", "answer": "cerca de"},
        ],
    },
    {
        "lesson_number": 31,
        "title": "Body Parts",
        "vocabulary": [
            {"word": "la cabeza", "translation": "the head", "pronunciation": "lah kah-BEH-sah"},
            {"word": "el brazo", "translation": "the arm", "pronunciation": "ehl BRAH-soh"},
            {"word": "la pierna", "translation": "the leg", "pronunciation": "lah pee-EHR-nah"},
            {"word": "el estómago", "translation": "the stomach", "pronunciation": "ehl ehs-TOH-mah-goh"},
            {"word": "la espalda", "translation": "the back", "pronunciation": "lah ehs-PAHL-dah"},
        ],
        "grammar": {
            "topic": "'Me duele' for pain",
            "explanation": "To say a body part hurts, use 'me duele' (singular) or 'me duelen' (plural) + the body part, with a definite article, not a possessive.",
        },
        "example_sentences": [
            {"target_language": "Me duele la cabeza.", "english": "My head hurts."},
            {"target_language": "Le duelen las piernas.", "english": "His/her legs hurt."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'My stomach hurts.'", "answer": "Me duele el estómago."},
            {"type": "fill_in_blank", "prompt": "Me duele la ___ (back).", "answer": "espalda"},
        ],
    },
    {
        "lesson_number": 32,
        "title": "Clothing Vocabulary",
        "vocabulary": [
            {"word": "la camisa", "translation": "the shirt", "pronunciation": "lah kah-MEE-sah"},
            {"word": "los pantalones", "translation": "the pants", "pronunciation": "lohs pahn-tah-LOH-nehs"},
            {"word": "los zapatos", "translation": "the shoes", "pronunciation": "lohs sah-PAH-tohs"},
            {"word": "la chaqueta", "translation": "the jacket", "pronunciation": "lah chah-KEH-tah"},
            {"word": "el vestido", "translation": "the dress", "pronunciation": "ehl vehs-TEE-doh"},
        ],
        "grammar": {
            "topic": "'Llevar' and 'ponerse'",
            "explanation": "'Llevar' means to wear (Llevo una camisa azul), while 'ponerse' means to put on, often reflexive (Me pongo la chaqueta).",
        },
        "example_sentences": [
            {"target_language": "Llevo pantalones negros y zapatos blancos.", "english": "I'm wearing black pants and white shoes."},
            {"target_language": "Me pongo la chaqueta porque hace frío.", "english": "I put on my jacket because it's cold."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'She is wearing a red dress.'", "answer": "Ella lleva un vestido rojo."},
            {"type": "fill_in_blank", "prompt": "Necesito comprar ___ (shoes) nuevos.", "answer": "zapatos"},
        ],
    },
    {
        "lesson_number": 33,
        "title": "Shopping Expressions",
        "vocabulary": [
            {"word": "¿Cuánto cuesta?", "translation": "How much does it cost?", "pronunciation": "KWAHN-toh KWEHS-tah"},
            {"word": "barato/a", "translation": "cheap", "pronunciation": "bah-RAH-toh"},
            {"word": "caro/a", "translation": "expensive", "pronunciation": "KAH-roh"},
            {"word": "probarse", "translation": "to try on", "pronunciation": "proh-BAHR-seh"},
            {"word": "la talla", "translation": "the size", "pronunciation": "lah TAH-yah"},
        ],
        "grammar": {
            "topic": "Asking price and size",
            "explanation": "'¿Cuánto cuesta?' asks about price for one item; use '¿Cuánto cuestan?' for multiple items. 'Probarse' is reflexive: me pruebo la camisa.",
        },
        "example_sentences": [
            {"target_language": "¿Cuánto cuestan estos zapatos?", "english": "How much do these shoes cost?"},
            {"target_language": "Quiero probarme esta talla.", "english": "I want to try on this size."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'This jacket is expensive.'", "answer": "Esta chaqueta es cara."},
            {"type": "fill_in_blank", "prompt": "¿Tiene una talla más ___ (cheap)?", "answer": "barata"},
        ],
    },
    {
        "lesson_number": 34,
        "title": "Possessive Adjectives (In Depth)",
        "vocabulary": [
            {"word": "nuestro/a", "translation": "our", "pronunciation": "noo-EHS-troh"},
            {"word": "vuestro/a", "translation": "your (plural, Spain)", "pronunciation": "voo-EHS-troh"},
            {"word": "su", "translation": "his/her/their/your formal", "pronunciation": "soo"},
            {"word": "mis", "translation": "my (plural)", "pronunciation": "mees"},
            {"word": "sus", "translation": "his/her/their (plural)", "pronunciation": "soos"},
        ],
        "grammar": {
            "topic": "Agreement of possessives",
            "explanation": "'Nuestro' and 'vuestro' agree in both gender and number (nuestra casa, nuestros libros); the others only change for number.",
        },
        "example_sentences": [
            {"target_language": "Nuestra casa es grande.", "english": "Our house is big."},
            {"target_language": "Sus hijos estudian mucho.", "english": "Their children study a lot."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'Our friends are here.'", "answer": "Nuestros amigos están aquí."},
            {"type": "fill_in_blank", "prompt": "___ (my, plural) libros están en la mesa.", "answer": "Mis"},
        ],
    },
    {
        "lesson_number": 35,
        "title": "Demonstrative Adjectives",
        "vocabulary": [
            {"word": "este/esta", "translation": "this", "pronunciation": "EHS-teh/tah"},
            {"word": "ese/esa", "translation": "that", "pronunciation": "EH-seh/sah"},
            {"word": "aquel/aquella", "translation": "that (over there)", "pronunciation": "ah-KEHL"},
            {"word": "estos/estas", "translation": "these", "pronunciation": "EHS-tohs"},
            {"word": "esos/esas", "translation": "those", "pronunciation": "EH-sohs"},
        ],
        "grammar": {
            "topic": "Three degrees of distance",
            "explanation": "Spanish has three distance levels: este (near speaker), ese (near listener), aquel (far from both). All agree in gender and number.",
        },
        "example_sentences": [
            {"target_language": "Este libro es mío, ese es tuyo.", "english": "This book is mine, that one is yours."},
            {"target_language": "Aquella casa allá es de mis abuelos.", "english": "That house over there is my grandparents'."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'These shoes are new.'", "answer": "Estos zapatos son nuevos."},
            {"type": "fill_in_blank", "prompt": "___ (that, far) montaña es muy alta.", "answer": "Aquella"},
        ],
    },
    {
        "lesson_number": 36,
        "title": "Comparatives and Superlatives",
        "vocabulary": [
            {"word": "más que", "translation": "more than", "pronunciation": "mahs keh"},
            {"word": "menos que", "translation": "less than", "pronunciation": "MEH-nohs keh"},
            {"word": "tan...como", "translation": "as...as", "pronunciation": "tahn KOH-moh"},
            {"word": "el/la más", "translation": "the most", "pronunciation": "ehl mahs"},
            {"word": "mejor", "translation": "better/best (irregular)", "pronunciation": "meh-HOHR"},
        ],
        "grammar": {
            "topic": "Forming comparisons",
            "explanation": "Use 'más/menos + adjective + que' to compare, and 'el/la más + adjective' for superlatives. 'Bueno' and 'malo' have irregular comparatives: mejor, peor.",
        },
        "example_sentences": [
            {"target_language": "Mi hermano es más alto que yo.", "english": "My brother is taller than me."},
            {"target_language": "Este es el mejor restaurante de la ciudad.", "english": "This is the best restaurant in the city."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'She is as tall as her mother.'", "answer": "Ella es tan alta como su madre."},
            {"type": "fill_in_blank", "prompt": "Este coche es ___ (more) caro que ese.", "answer": "más"},
        ],
    },
    {
        "lesson_number": 37,
        "title": "The Near Future (Ir + a + Infinitive)",
        "vocabulary": [
            {"word": "voy a", "translation": "I am going to", "pronunciation": "voy ah"},
            {"word": "vas a", "translation": "you are going to", "pronunciation": "vahs ah"},
            {"word": "va a", "translation": "he/she is going to", "pronunciation": "vah ah"},
            {"word": "vamos a", "translation": "we are going to", "pronunciation": "VAH-mohs ah"},
            {"word": "mañana", "translation": "tomorrow", "pronunciation": "mah-NYAH-nah"},
        ],
        "grammar": {
            "topic": "Expressing future plans",
            "explanation": "The construction 'ir + a + infinitive' is the most common way to talk about near-future plans, similar to 'going to' in English.",
        },
        "example_sentences": [
            {"target_language": "Mañana voy a visitar a mis abuelos.", "english": "Tomorrow I'm going to visit my grandparents."},
            {"target_language": "Vamos a estudiar esta noche.", "english": "We are going to study tonight."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'They are going to travel to Chile.'", "answer": "Ellos van a viajar a Chile."},
            {"type": "fill_in_blank", "prompt": "Yo ___ (ir a) cocinar esta tarde.", "answer": "voy a"},
        ],
    },
    {
        "lesson_number": 38,
        "title": "Talking About the Past: Preterite Regular Verbs",
        "vocabulary": [
            {"word": "hablé", "translation": "I spoke", "pronunciation": "ah-BLEH"},
            {"word": "comí", "translation": "I ate", "pronunciation": "koh-MEE"},
            {"word": "viví", "translation": "I lived", "pronunciation": "vee-VEE"},
            {"word": "ayer", "translation": "yesterday", "pronunciation": "ah-YEHR"},
            {"word": "la semana pasada", "translation": "last week", "pronunciation": "lah seh-MAH-nah pah-SAH-dah"},
        ],
        "grammar": {
            "topic": "Preterite endings",
            "explanation": "-AR verbs: -é, -aste, -ó, -amos, -asteis, -aron. -ER/-IR verbs: -í, -iste, -ió, -imos, -isteis, -ieron. The preterite describes completed past actions.",
        },
        "example_sentences": [
            {"target_language": "Ayer hablé con mi madre.", "english": "Yesterday I spoke with my mother."},
            {"target_language": "Comimos en un restaurante nuevo.", "english": "We ate at a new restaurant."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Ella ___ (vivir) en Chile por dos años.", "answer": "vivió"},
            {"type": "translation", "prompt": "Translate: 'I studied last week.'", "answer": "Estudié la semana pasada."},
        ],
    },
    {
        "lesson_number": 39,
        "title": "Preterite Irregular Verbs",
        "vocabulary": [
            {"word": "fui", "translation": "I went / I was", "pronunciation": "fwee"},
            {"word": "hice", "translation": "I did/made", "pronunciation": "EE-seh"},
            {"word": "tuve", "translation": "I had", "pronunciation": "TOO-veh"},
            {"word": "dije", "translation": "I said", "pronunciation": "DEE-heh"},
            {"word": "pude", "translation": "I could/was able to", "pronunciation": "POO-deh"},
        ],
        "grammar": {
            "topic": "Irregular preterite stems",
            "explanation": "Many common verbs have irregular preterite stems that don't use regular endings: ir/ser → fui, hacer → hice, tener → tuve. These must be memorized.",
        },
        "example_sentences": [
            {"target_language": "Fui al cine con mis amigos.", "english": "I went to the movies with my friends."},
            {"target_language": "Tuve mucho trabajo ayer.", "english": "I had a lot of work yesterday."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Yo ___ (hacer) la tarea anoche.", "answer": "hice"},
            {"type": "translation", "prompt": "Translate: 'She said the truth.'", "answer": "Ella dijo la verdad."},
        ],
    },
    {
        "lesson_number": 40,
        "title": "Imperfect Tense Introduction",
        "vocabulary": [
            {"word": "hablaba", "translation": "I used to speak / was speaking", "pronunciation": "ah-BLAH-bah"},
            {"word": "comía", "translation": "I used to eat / was eating", "pronunciation": "koh-MEE-ah"},
            {"word": "vivía", "translation": "I used to live / was living", "pronunciation": "vee-VEE-ah"},
            {"word": "siempre", "translation": "always", "pronunciation": "see-EHM-preh"},
            {"word": "cuando era niño/a", "translation": "when I was a child", "pronunciation": "KWAHN-doh EH-rah NEE-nyoh"},
        ],
        "grammar": {
            "topic": "Imperfect endings",
            "explanation": "-AR verbs: -aba, -abas, -aba, -ábamos, -abais, -aban. -ER/-IR verbs: -ía, -ías, -ía, -íamos, -íais, -ían. Used for ongoing or habitual past actions.",
        },
        "example_sentences": [
            {"target_language": "Cuando era niño, jugaba mucho.", "english": "When I was a child, I used to play a lot."},
            {"target_language": "Vivíamos en una casa pequeña.", "english": "We used to live in a small house."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Ella siempre ___ (comer) fruta.", "answer": "comía"},
            {"type": "translation", "prompt": "Translate: 'I used to speak French.'", "answer": "Yo hablaba francés."},
        ],
    },
    {
        "lesson_number": 41,
        "title": "Preterite vs Imperfect",
        "vocabulary": [
            {"word": "mientras", "translation": "while", "pronunciation": "mee-EHN-trahs"},
            {"word": "de repente", "translation": "suddenly", "pronunciation": "deh reh-PEHN-teh"},
            {"word": "una vez", "translation": "once", "pronunciation": "OO-nah vehs"},
            {"word": "todos los días", "translation": "every day", "pronunciation": "TOH-dohs lohs DEE-ahs"},
            {"word": "interrumpir", "translation": "to interrupt", "pronunciation": "een-teh-rroom-PEER"},
        ],
        "grammar": {
            "topic": "When to use each tense",
            "explanation": "Use the imperfect for background/ongoing actions and the preterite for completed actions or interruptions: Mientras dormía (imperfect), sonó el teléfono (preterite).",
        },
        "example_sentences": [
            {"target_language": "Mientras cocinaba, llamó mi amigo.", "english": "While I was cooking, my friend called."},
            {"target_language": "De repente, empezó a llover.", "english": "Suddenly, it started to rain."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Yo ___ (leer, imperfect) cuando sonó el timbre.", "answer": "leía"},
            {"type": "translation", "prompt": "Translate: 'Once, I traveled to Peru.'", "answer": "Una vez, viajé a Perú."},
        ],
    },
    {
        "lesson_number": 42,
        "title": "Direct Object Pronouns",
        "vocabulary": [
            {"word": "lo", "translation": "it/him (masc.)", "pronunciation": "loh"},
            {"word": "la", "translation": "it/her (fem.)", "pronunciation": "lah"},
            {"word": "los / las", "translation": "them", "pronunciation": "lohs / lahs"},
            {"word": "me", "translation": "me", "pronunciation": "meh"},
            {"word": "te", "translation": "you", "pronunciation": "teh"},
        ],
        "grammar": {
            "topic": "Placement of direct object pronouns",
            "explanation": "Direct object pronouns replace nouns already mentioned and go before the conjugated verb: Compro el libro → Lo compro.",
        },
        "example_sentences": [
            {"target_language": "¿Tienes las llaves? Sí, las tengo.", "english": "Do you have the keys? Yes, I have them."},
            {"target_language": "Te veo mañana.", "english": "I'll see you tomorrow."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'I love it (the movie).' (la película)", "answer": "La amo."},
            {"type": "fill_in_blank", "prompt": "¿Compraste el pan? Sí, ___ compré.", "answer": "lo"},
        ],
    },
    {
        "lesson_number": 43,
        "title": "Indirect Object Pronouns",
        "vocabulary": [
            {"word": "me", "translation": "to me", "pronunciation": "meh"},
            {"word": "te", "translation": "to you", "pronunciation": "teh"},
            {"word": "le", "translation": "to him/her/you formal", "pronunciation": "leh"},
            {"word": "nos", "translation": "to us", "pronunciation": "nohs"},
            {"word": "les", "translation": "to them/you plural", "pronunciation": "lehs"},
        ],
        "grammar": {
            "topic": "Indirect objects answer 'to/for whom'",
            "explanation": "Indirect object pronouns indicate who receives the action: Le doy el regalo (I give him/her the gift). They often appear with verbs like dar, decir, escribir.",
        },
        "example_sentences": [
            {"target_language": "Le escribo una carta a mi abuela.", "english": "I write a letter to my grandmother."},
            {"target_language": "Nos dieron buenas noticias.", "english": "They gave us good news."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'I tell you the truth.' (informal you)", "answer": "Te digo la verdad."},
            {"type": "fill_in_blank", "prompt": "___ doy el libro a Juan. (to him)", "answer": "Le"},
        ],
    },
    {
        "lesson_number": 44,
        "title": "Double Object Pronouns",
        "vocabulary": [
            {"word": "se lo", "translation": "it to him/her/them", "pronunciation": "seh loh"},
            {"word": "me lo", "translation": "it to me", "pronunciation": "meh loh"},
            {"word": "te la", "translation": "it to you (fem. object)", "pronunciation": "teh lah"},
            {"word": "dárselo", "translation": "to give it to him/her", "pronunciation": "dar-SEH-loh"},
            {"word": "explicar", "translation": "to explain", "pronunciation": "ehks-plee-KAHR"},
        ],
        "grammar": {
            "topic": "Order and the le/les → se rule",
            "explanation": "When both pronouns are used, indirect comes before direct (me lo, te la). 'Le' and 'les' change to 'se' before 'lo, la, los, las': Le doy el libro → Se lo doy.",
        },
        "example_sentences": [
            {"target_language": "¿El regalo? Se lo doy a ella.", "english": "The gift? I give it to her."},
            {"target_language": "Me lo explicó ayer.", "english": "He/she explained it to me yesterday."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'I give it (the money) to them.' (el dinero)", "answer": "Se lo doy a ellos."},
            {"type": "fill_in_blank", "prompt": "¿La carta? ___ escribo hoy. (to you, informal)", "answer": "Te la"},
        ],
    },
    {
        "lesson_number": 45,
        "title": "Commands (Imperative) - Informal",
        "vocabulary": [
            {"word": "habla", "translation": "speak! (tú)", "pronunciation": "AH-blah"},
            {"word": "come", "translation": "eat! (tú)", "pronunciation": "KOH-meh"},
            {"word": "escribe", "translation": "write! (tú)", "pronunciation": "ehs-KREE-beh"},
            {"word": "no hables", "translation": "don't speak! (tú)", "pronunciation": "noh AH-blehs"},
            {"word": "ven", "translation": "come! (irregular tú)", "pronunciation": "vehn"},
        ],
        "grammar": {
            "topic": "Affirmative and negative tú commands",
            "explanation": "Affirmative tú commands often match the 'él/ella' present form (habla, come). Negative commands use the opposite-vowel subjunctive-like form (no hables, no comas).",
        },
        "example_sentences": [
            {"target_language": "Habla más despacio, por favor.", "english": "Speak more slowly, please."},
            {"target_language": "No comas tan rápido.", "english": "Don't eat so fast."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'Write your name here.' (command, tú)", "answer": "Escribe tu nombre aquí."},
            {"type": "fill_in_blank", "prompt": "___ (venir, command) aquí ahora.", "answer": "Ven"},
        ],
    },
    {
        "lesson_number": 46,
        "title": "Commands (Imperative) - Formal",
        "vocabulary": [
            {"word": "hable", "translation": "speak! (usted)", "pronunciation": "AH-bleh"},
            {"word": "coma", "translation": "eat! (usted)", "pronunciation": "KOH-mah"},
            {"word": "escriba", "translation": "write! (usted)", "pronunciation": "ehs-KREE-bah"},
            {"word": "siéntese", "translation": "sit down! (usted)", "pronunciation": "see-EHN-teh-seh"},
            {"word": "no se preocupe", "translation": "don't worry! (usted)", "pronunciation": "noh seh preh-oh-KOO-peh"},
        ],
        "grammar": {
            "topic": "Usted/ustedes commands",
            "explanation": "Formal commands use the opposite-vowel ending for both affirmative and negative: -ar verbs → -e/-en, -er/-ir verbs → -a/-an.",
        },
        "example_sentences": [
            {"target_language": "Por favor, siéntese aquí.", "english": "Please, sit down here."},
            {"target_language": "No se preocupe, todo está bien.", "english": "Don't worry, everything is fine."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'Speak clearly, please.' (formal command)", "answer": "Hable claramente, por favor."},
            {"type": "fill_in_blank", "prompt": "___ (comer, formal command) despacio.", "answer": "Coma"},
        ],
    },
    {
        "lesson_number": 47,
        "title": "Prepositions of Place",
        "vocabulary": [
            {"word": "encima de", "translation": "on top of", "pronunciation": "ehn-SEE-mah deh"},
            {"word": "debajo de", "translation": "underneath", "pronunciation": "deh-BAH-hoh deh"},
            {"word": "entre", "translation": "between", "pronunciation": "EHN-treh"},
            {"word": "al lado de", "translation": "next to", "pronunciation": "ahl LAH-doh deh"},
            {"word": "detrás de", "translation": "behind", "pronunciation": "deh-TRAHS deh"},
        ],
        "grammar": {
            "topic": "Prepositional phrases with 'de'",
            "explanation": "Most place prepositions end in 'de' and contract with 'el' to 'del': al lado del banco (next to the bank).",
        },
        "example_sentences": [
            {"target_language": "El gato está debajo de la mesa.", "english": "The cat is underneath the table."},
            {"target_language": "La farmacia está entre el banco y el parque.", "english": "The pharmacy is between the bank and the park."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'The book is on top of the shelf.'", "answer": "El libro está encima del estante."},
            {"type": "fill_in_blank", "prompt": "Mi casa está ___ (next to) la iglesia.", "answer": "al lado de"},
        ],
    },
    {
        "lesson_number": 48,
        "title": "Talking About Hobbies",
        "vocabulary": [
            {"word": "el pasatiempo", "translation": "hobby", "pronunciation": "ehl pah-sah-tee-EHM-poh"},
            {"word": "pintar", "translation": "to paint", "pronunciation": "peen-TAHR"},
            {"word": "tocar un instrumento", "translation": "to play an instrument", "pronunciation": "toh-KAHR"},
            {"word": "hacer ejercicio", "translation": "to exercise", "pronunciation": "AH-sehr eh-hehr-SEE-see-oh"},
            {"word": "coleccionar", "translation": "to collect", "pronunciation": "koh-lehk-see-oh-NAHR"},
        ],
        "grammar": {
            "topic": "Talking about frequency",
            "explanation": "Combine hobby verbs with frequency words like 'a veces' (sometimes), 'a menudo' (often), and 'nunca' (never) to describe habits.",
        },
        "example_sentences": [
            {"target_language": "A menudo toco la guitarra los fines de semana.", "english": "I often play guitar on weekends."},
            {"target_language": "Mi pasatiempo favorito es pintar.", "english": "My favorite hobby is painting."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'I collect stamps.'", "answer": "Colecciono sellos."},
            {"type": "fill_in_blank", "prompt": "Ella ___ (hacer ejercicio) todos los días.", "answer": "hace ejercicio"},
        ],
    },
    {
        "lesson_number": 49,
        "title": "Making Plans / Invitations",
        "vocabulary": [
            {"word": "¿Quieres...?", "translation": "Do you want to...?", "pronunciation": "kee-EH-rehs"},
            {"word": "¿Te gustaría...?", "translation": "Would you like to...?", "pronunciation": "teh goos-tah-REE-ah"},
            {"word": "quedar", "translation": "to meet up", "pronunciation": "keh-DAHR"},
            {"word": "estar libre", "translation": "to be free/available", "pronunciation": "ehs-TAHR LEE-breh"},
            {"word": "tener planes", "translation": "to have plans", "pronunciation": "teh-NEHR PLAH-nehs"},
        ],
        "grammar": {
            "topic": "Making polite invitations",
            "explanation": "'¿Te gustaría?' is more polite/tentative than '¿Quieres?'. Both are followed by an infinitive: ¿Te gustaría ir al cine?",
        },
        "example_sentences": [
            {"target_language": "¿Quieres quedar el sábado?", "english": "Do you want to meet up on Saturday?"},
            {"target_language": "¿Estás libre esta tarde?", "english": "Are you free this afternoon?"},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'Would you like to have dinner with me?'", "answer": "¿Te gustaría cenar conmigo?"},
            {"type": "fill_in_blank", "prompt": "No puedo, ya ___ (tener planes).", "answer": "tengo planes"},
        ],
    },
    {
        "lesson_number": 50,
        "title": "Review and Self-Assessment",
        "vocabulary": [
            {"word": "repasar", "translation": "to review", "pronunciation": "reh-pah-SAHR"},
            {"word": "el progreso", "translation": "progress", "pronunciation": "ehl proh-GREH-soh"},
            {"word": "la meta", "translation": "the goal", "pronunciation": "lah MEH-tah"},
            {"word": "seguir practicando", "translation": "to keep practicing", "pronunciation": "seh-GEER prahk-tee-KAHN-doh"},
            {"word": "¡Lo lograste!", "translation": "You made it!", "pronunciation": "loh loh-GRAHS-teh"},
        ],
        "grammar": {
            "topic": "Cumulative review",
            "explanation": "This lesson reviews key structures from Lessons 1-49: ser/estar, present/preterite/imperfect tenses, object pronouns, and commands. Use it to identify weak spots before moving to Intermediate.",
        },
        "example_sentences": [
            {"target_language": "He aprendido mucho en este curso.", "english": "I have learned a lot in this course."},
            {"target_language": "Voy a seguir practicando cada día.", "english": "I am going to keep practicing every day."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Write 3 sentences about yourself using ser, estar, and gustar.", "answer": "Answers vary — check for correct verb agreement and article/pronoun use."},
            {"type": "fill_in_blank", "prompt": "¡Felicidades! ___ (you made it) el nivel principiante.", "answer": "Lo lograste en"},
        ],
    },
]
