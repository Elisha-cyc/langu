"""
Spanish - Advanced level
50-lesson curriculum. Lessons 1-10 are fully written (vocab, grammar,
examples, exercises). Lessons 11-50 have real, sequenced titles as the
confirmed roadmap; fill in their content in the next pass using the
same schema as generate_scaffold.py / beginner.py.
"""

lessons = [
    {
        "lesson_number": 1,
        "title": "Imperfect Subjunctive",
        "vocabulary": [
            {"word": "hablara / hablase", "translation": "I spoke/were to speak (two valid forms)", "pronunciation": "ah-BLAH-rah"},
            {"word": "tuviera / tuviese", "translation": "I had/were to have", "pronunciation": "too-vee-EH-rah"},
            {"word": "si yo fuera", "translation": "if I were", "pronunciation": "see yoh FWEH-rah"},
            {"word": "como si", "translation": "as if", "pronunciation": "KOH-moh see"},
            {"word": "quisiera", "translation": "I would like (polite, from querer)", "pronunciation": "kee-see-EH-rah"},
        ],
        "grammar": {
            "topic": "Forming the imperfect subjunctive",
            "explanation": "Take the 'ellos' form of the preterite, drop '-ron', and add -ra (or -se) endings: hablaron → hablara/hablase. Both forms are interchangeable in most contexts, though -ra is more common in speech.",
        },
        "example_sentences": [
            {"target_language": "Si yo fuera rico, viajaría por el mundo.", "english": "If I were rich, I would travel the world."},
            {"target_language": "Me habló como si lo supiera todo.", "english": "He spoke to me as if he knew everything."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Ojalá ___ (tener, yo) más tiempo ayer.", "answer": "tuviera"},
            {"type": "translation", "prompt": "Translate: 'If she called me, I would answer.'", "answer": "Si ella me llamara, contestaría."},
        ],
    },
    {
        "lesson_number": 2,
        "title": "Pluperfect Subjunctive",
        "vocabulary": [
            {"word": "hubiera hablado", "translation": "I had spoken (subjunctive)", "pronunciation": "oo-bee-EH-rah ah-BLAH-doh"},
            {"word": "hubiera sido", "translation": "I had been (subjunctive)", "pronunciation": "oo-bee-EH-rah SEE-doh"},
            {"word": "si hubiera sabido", "translation": "if I had known", "pronunciation": "see oo-bee-EH-rah sah-BEE-doh"},
            {"word": "arrepentirse", "translation": "to regret", "pronunciation": "ah-rreh-pehn-TEER-seh"},
            {"word": "de haber sabido", "translation": "had I known", "pronunciation": "deh ah-BEHR sah-BEE-doh"},
        ],
        "grammar": {
            "topic": "Hubiera + past participle",
            "explanation": "Used for hypothetical past situations that didn't happen: 'hubiera' (imperfect subjunctive of haber) + past participle expresses regret or contrary-to-fact past conditions.",
        },
        "example_sentences": [
            {"target_language": "Si hubiera sabido, te habría llamado.", "english": "If I had known, I would have called you."},
            {"target_language": "Me arrepiento de no haber estudiado más.", "english": "I regret not having studied more."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'If they had arrived earlier, they would have seen the show.'", "answer": "Si hubieran llegado antes, habrían visto el espectáculo."},
            {"type": "fill_in_blank", "prompt": "Ojalá ___ (venir, tú) a la fiesta anoche.", "answer": "hubieras venido"},
        ],
    },
    {
        "lesson_number": 3,
        "title": "Sequence of Tenses with Subjunctive",
        "vocabulary": [
            {"word": "concordancia de tiempos", "translation": "sequence/agreement of tenses", "pronunciation": "kohn-kohr-DAHN-see-ah"},
            {"word": "cláusula principal", "translation": "main clause", "pronunciation": "KLOW-soo-lah preen-see-PAHL"},
            {"word": "cláusula subordinada", "translation": "subordinate clause", "pronunciation": "soo-bohr-dee-NAH-dah"},
            {"word": "anterioridad", "translation": "anteriority (happening before)", "pronunciation": "ahn-teh-ree-oh-ree-DAHD"},
            {"word": "simultaneidad", "translation": "simultaneity", "pronunciation": "see-mool-tah-neh-ee-DAHD"},
        ],
        "grammar": {
            "topic": "Matching tenses correctly",
            "explanation": "A present/future main clause pairs with present or present-perfect subjunctive; a past/conditional main clause pairs with imperfect or pluperfect subjunctive: Espero que venga (present) vs Esperaba que viniera (past).",
        },
        "example_sentences": [
            {"target_language": "Esperaba que hubieras terminado el proyecto.", "english": "I hoped you had finished the project."},
            {"target_language": "Dudo que haya mentido.", "english": "I doubt he has lied."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Quería que ___ (tú, quedarse).", "answer": "te quedaras"},
            {"type": "translation", "prompt": "Translate: 'I was afraid that it had already started.'", "answer": "Temía que ya hubiera empezado."},
        ],
    },
    {
        "lesson_number": 4,
        "title": "Complex Si Clauses Review",
        "vocabulary": [
            {"word": "de no ser por", "translation": "if it weren't for", "pronunciation": "deh noh sehr pohr"},
            {"word": "a menos que", "translation": "unless", "pronunciation": "ah MEH-nohs keh"},
            {"word": "con tal de que", "translation": "provided that", "pronunciation": "kohn tahl deh keh"},
            {"word": "en caso de que", "translation": "in case", "pronunciation": "ehn KAH-soh deh keh"},
            {"word": "siempre que", "translation": "as long as", "pronunciation": "see-EHM-preh keh"},
        ],
        "grammar": {
            "topic": "Conditional connectors beyond 'si'",
            "explanation": "Several connectors besides 'si' introduce conditions and require the subjunctive: a menos que, con tal de que, en caso de que, siempre que.",
        },
        "example_sentences": [
            {"target_language": "No iré a menos que me invites.", "english": "I won't go unless you invite me."},
            {"target_language": "Te ayudaré con tal de que me escuches.", "english": "I'll help you provided that you listen to me."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'In case it rains, bring an umbrella.'", "answer": "En caso de que llueva, trae un paraguas."},
            {"type": "fill_in_blank", "prompt": "Iremos siempre que ___ (haber) tiempo.", "answer": "haya"},
        ],
    },
    {
        "lesson_number": 5,
        "title": "Nuanced Uses of Por and Para",
        "vocabulary": [
            {"word": "por lo tanto", "translation": "therefore", "pronunciation": "pohr loh TAHN-toh"},
            {"word": "para colmo", "translation": "to top it off", "pronunciation": "PAH-rah KOHL-moh"},
            {"word": "por si acaso", "translation": "just in case", "pronunciation": "pohr see ah-KAH-soh"},
            {"word": "para siempre", "translation": "forever", "pronunciation": "PAH-rah see-EHM-preh"},
            {"word": "por más que", "translation": "no matter how much", "pronunciation": "pohr mahs keh"},
        ],
        "grammar": {
            "topic": "Idiomatic and fixed expressions",
            "explanation": "Beyond the basic rules (por = cause/means, para = purpose/destination), both prepositions appear in many fixed idiomatic phrases that must be learned individually.",
        },
        "example_sentences": [
            {"target_language": "Por más que lo intento, no lo entiendo.", "english": "No matter how much I try, I don't understand it."},
            {"target_language": "Llevaré paraguas por si acaso.", "english": "I'll bring an umbrella just in case."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'And to top it off, it started to rain.'", "answer": "Y para colmo, empezó a llover."},
            {"type": "fill_in_blank", "prompt": "Te querré ___ (forever).", "answer": "para siempre"},
        ],
    },
    {
        "lesson_number": 6,
        "title": "Advanced Idiomatic Expressions",
        "vocabulary": [
            {"word": "estar en las nubes", "translation": "to have one's head in the clouds", "pronunciation": "ehs-TAHR ehn lahs NOO-behs"},
            {"word": "no tener pelos en la lengua", "translation": "to not mince words", "pronunciation": "noh teh-NEHR PEH-lohs ehn lah LEHN-gwah"},
            {"word": "costar un ojo de la cara", "translation": "to cost an arm and a leg", "pronunciation": "kohs-TAHR oon OH-hoh"},
            {"word": "tirar la toalla", "translation": "to throw in the towel", "pronunciation": "tee-RAHR lah toh-AH-yah"},
            {"word": "meter la pata", "translation": "to put one's foot in it (make a mistake)", "pronunciation": "meh-TEHR lah PAH-tah"},
        ],
        "grammar": {
            "topic": "Idioms resist literal translation",
            "explanation": "Idiomatic expressions can't be translated word-for-word; they must be learned as fixed units tied to their figurative meaning, often varying by region.",
        },
        "example_sentences": [
            {"target_language": "Ese coche debe de costar un ojo de la cara.", "english": "That car must cost an arm and a leg."},
            {"target_language": "Metí la pata al mencionar su ex.", "english": "I put my foot in it by mentioning her ex."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'Don't throw in the towel now.'", "answer": "No tires la toalla ahora."},
            {"type": "fill_in_blank", "prompt": "Siempre dice lo que piensa, no tiene ___ en la lengua.", "answer": "pelos"},
        ],
    },
    {
        "lesson_number": 7,
        "title": "Literary Spanish: Reading Short Stories",
        "vocabulary": [
            {"word": "el narrador", "translation": "the narrator", "pronunciation": "ehl nah-rrah-DOHR"},
            {"word": "el desenlace", "translation": "the ending/denouement", "pronunciation": "ehl deh-sehn-LAH-seh"},
            {"word": "el trasfondo", "translation": "the background/backdrop", "pronunciation": "ehl trahs-FOHN-doh"},
            {"word": "la trama", "translation": "the plot", "pronunciation": "lah TRAH-mah"},
            {"word": "el simbolismo", "translation": "symbolism", "pronunciation": "ehl seem-boh-LEES-moh"},
        ],
        "grammar": {
            "topic": "Literary past tenses",
            "explanation": "Literary Spanish leans heavily on the preterite for narration and the imperfect for description, plus the occasional literary preterite of 'ser/ir' (fuera) as a stylistic alternative to the pluperfect.",
        },
        "example_sentences": [
            {"target_language": "El narrador describe el trasfondo antes de revelar la trama.", "english": "The narrator describes the backdrop before revealing the plot."},
            {"target_language": "El desenlace sorprendió a todos los lectores.", "english": "The ending surprised all the readers."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'The symbolism in this story is very strong.'", "answer": "El simbolismo en este cuento es muy fuerte."},
            {"type": "fill_in_blank", "prompt": "¿Quién es el ___ (narrator) de la historia?", "answer": "narrador"},
        ],
    },
    {
        "lesson_number": 8,
        "title": "Formal Academic Writing",
        "vocabulary": [
            {"word": "en primer lugar", "translation": "in the first place", "pronunciation": "ehn pree-MEHR loo-GAHR"},
            {"word": "cabe destacar que", "translation": "it's worth noting that", "pronunciation": "KAH-beh dehs-tah-KAHR"},
            {"word": "por consiguiente", "translation": "consequently", "pronunciation": "pohr kohn-see-gee-EHN-teh"},
            {"word": "en conclusión", "translation": "in conclusion", "pronunciation": "ehn kohn-kloo-see-OHN"},
            {"word": "sin embargo", "translation": "however", "pronunciation": "seen ehm-BAR-goh"},
        ],
        "grammar": {
            "topic": "Discourse markers in essays",
            "explanation": "Academic Spanish relies on discourse connectors to structure arguments logically; these phrases signal contrast, consequence, and conclusion in formal writing.",
        },
        "example_sentences": [
            {"target_language": "Cabe destacar que los resultados fueron significativos.", "english": "It's worth noting that the results were significant."},
            {"target_language": "Sin embargo, hace falta más investigación.", "english": "However, more research is needed."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'In conclusion, the study confirms the hypothesis.'", "answer": "En conclusión, el estudio confirma la hipótesis."},
            {"type": "fill_in_blank", "prompt": "___ (consequently), decidimos cambiar el método.", "answer": "Por consiguiente"},
        ],
    },
    {
        "lesson_number": 9,
        "title": "Persuasive Writing and Rhetoric",
        "vocabulary": [
            {"word": "el argumento", "translation": "the argument", "pronunciation": "ehl ar-goo-MEHN-toh"},
            {"word": "la retórica", "translation": "rhetoric", "pronunciation": "lah reh-TOH-ree-kah"},
            {"word": "convencer", "translation": "to convince", "pronunciation": "kohn-vehn-SEHR"},
            {"word": "refutar", "translation": "to refute", "pronunciation": "reh-foo-TAHR"},
            {"word": "el llamado a la acción", "translation": "call to action", "pronunciation": "yah-MAH-doh ah lah ahk-see-OHN"},
        ],
        "grammar": {
            "topic": "Rhetorical questions and emphasis",
            "explanation": "Persuasive Spanish often uses rhetorical questions (¿Acaso no merecemos algo mejor?) and emphatic structures ('lo que + verb + es que') to strengthen an argument.",
        },
        "example_sentences": [
            {"target_language": "Lo que realmente necesitamos es un cambio.", "english": "What we really need is change."},
            {"target_language": "¿Acaso no merecemos algo mejor?", "english": "Don't we deserve something better?"},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'Her argument managed to convince the jury.'", "answer": "Su argumento logró convencer al jurado."},
            {"type": "fill_in_blank", "prompt": "El abogado intentó ___ (refute) el testimonio.", "answer": "refutar"},
        ],
    },
    {
        "lesson_number": 10,
        "title": "Legal and Bureaucratic Spanish",
        "vocabulary": [
            {"word": "el contrato", "translation": "the contract", "pronunciation": "ehl kohn-TRAH-toh"},
            {"word": "la cláusula", "translation": "the clause", "pronunciation": "lah KLOW-soo-lah"},
            {"word": "el/la demandante", "translation": "the plaintiff", "pronunciation": "deh-mahn-DAHN-teh"},
            {"word": "por medio de la presente", "translation": "by means of this document", "pronunciation": "pohr MEH-dee-oh deh lah preh-SEHN-teh"},
            {"word": "el trámite", "translation": "the bureaucratic procedure", "pronunciation": "ehl TRAH-mee-teh"},
        ],
        "grammar": {
            "topic": "Fixed formal legal phrasing",
            "explanation": "Legal Spanish uses highly formulaic, archaic-sounding set phrases ('por medio de la presente', 'en fe de lo cual') and heavy nominalization, distinct from everyday register.",
        },
        "example_sentences": [
            {"target_language": "Por medio de la presente, se notifica el cambio de dirección.", "english": "By means of this document, the change of address is notified."},
            {"target_language": "Este trámite puede tardar varias semanas.", "english": "This procedure can take several weeks."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'The contract includes a confidentiality clause.'", "answer": "El contrato incluye una cláusula de confidencialidad."},
            {"type": "fill_in_blank", "prompt": "El ___ (plaintiff) presentó una demanda.", "answer": "demandante"},
        ],
    },
    # --- Confirmed roadmap for Lessons 11-50 (titles only — content pending) ---
    {"lesson_number": 11, "title": "Medical Spanish Vocabulary"},
    {"lesson_number": 12, "title": "Advanced Business Negotiation Language"},
    {"lesson_number": 13, "title": "Debating Complex Topics"},
    {"lesson_number": 14, "title": "Understanding Poetry and Figurative Language"},
    {"lesson_number": 15, "title": "Regional Dialects: Caribbean Spanish"},
    {"lesson_number": 16, "title": "Regional Dialects: Andean Spanish"},
    {"lesson_number": 17, "title": "Regional Dialects: Rioplatense Spanish (Voseo)"},
    {"lesson_number": 18, "title": "History of the Spanish Language"},
    {"lesson_number": 19, "title": "Advanced Connectors and Discourse Markers"},
    {"lesson_number": 20, "title": "Nominalization and Complex Sentence Structure"},
    {"lesson_number": 21, "title": "Subjunctive in Adverbial Clauses"},
    {"lesson_number": 22, "title": "Advanced Relative Clauses"},
    {"lesson_number": 23, "title": "Passive and Impersonal Constructions Review"},
    {"lesson_number": 24, "title": "Advanced Vocabulary: Politics"},
    {"lesson_number": 25, "title": "Advanced Vocabulary: Economics"},
    {"lesson_number": 26, "title": "Advanced Vocabulary: Science and Technology"},
    {"lesson_number": 27, "title": "Understanding Song Lyrics and Cultural References"},
    {"lesson_number": 28, "title": "Analyzing News Editorials"},
    {"lesson_number": 29, "title": "Formal Presentations and Public Speaking"},
    {"lesson_number": 30, "title": "Advanced Listening: Podcasts and Interviews"},
    {"lesson_number": 31, "title": "Writing a Persuasive Essay"},
    {"lesson_number": 32, "title": "Understanding Legal Contracts"},
    {"lesson_number": 33, "title": "Idioms Related to Emotions"},
    {"lesson_number": 34, "title": "Advanced Verb + Preposition Combinations"},
    {"lesson_number": 35, "title": "Nuances of Ser, Estar, and Haber"},
    {"lesson_number": 36, "title": "Advanced Time Expressions"},
    {"lesson_number": 37, "title": "Understanding Humor and Wordplay"},
    {"lesson_number": 38, "title": "Formal vs Informal Register Shifts"},
    {"lesson_number": 39, "title": "Advanced Narrative Techniques"},
    {"lesson_number": 40, "title": "Translating Complex Texts"},
    {"lesson_number": 41, "title": "Understanding Regional Slang"},
    {"lesson_number": 42, "title": "Advanced Correspondence (Diplomatic/Formal)"},
    {"lesson_number": 43, "title": "Analyzing Literature: Magical Realism"},
    {"lesson_number": 44, "title": "Advanced Debate and Argumentation"},
    {"lesson_number": 45, "title": "Understanding Bureaucracy and Government Forms"},
    {"lesson_number": 46, "title": "Advanced Cultural Idioms Across Latin America"},
    {"lesson_number": 47, "title": "Mastering Nuanced Word Choice (Synonyms)"},
    {"lesson_number": 48, "title": "Advanced Listening Comprehension: Fast Native Speech"},
    {"lesson_number": 49, "title": "Capstone Project: Extended Conversation Practice"},
    {"lesson_number": 50, "title": "Advanced Review and Fluency Assessment"},
]
