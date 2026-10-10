"""
Spanish - Intermediate level
50-lesson curriculum. Lessons 1-10 are fully written (vocab, grammar,
examples, exercises). Lessons 11-50 have real, sequenced titles as the
confirmed roadmap; fill in their content in the next pass using the
same schema as generate_scaffold.py / beginner.py.
"""

lessons = [
    {
        "lesson_number": 1,
        "title": "Subjunctive Mood: Introduction",
        "vocabulary": [
            {"word": "el subjuntivo", "translation": "the subjunctive mood", "pronunciation": "ehl soob-hoon-TEE-voh"},
            {"word": "el indicativo", "translation": "the indicative mood", "pronunciation": "ehl een-dee-kah-TEE-voh"},
            {"word": "espero que", "translation": "I hope that", "pronunciation": "ehs-PEH-roh keh"},
            {"word": "es importante que", "translation": "it's important that", "pronunciation": "ehs eem-por-TAHN-teh keh"},
            {"word": "dudar", "translation": "to doubt", "pronunciation": "doo-DAHR"},
        ],
        "grammar": {
            "topic": "Indicative vs subjunctive",
            "explanation": "The indicative states facts; the subjunctive expresses wishes, doubts, emotions, or hypotheticals, and almost always appears in a clause after 'que' triggered by a verb or expression in the main clause.",
        },
        "example_sentences": [
            {"target_language": "Espero que tengas un buen día.", "english": "I hope you have a good day."},
            {"target_language": "Es importante que estudies para el examen.", "english": "It's important that you study for the exam."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'I doubt that he knows the answer.'", "answer": "Dudo que él sepa la respuesta."},
            {"type": "fill_in_blank", "prompt": "Espero que ___ (tú, estar) bien.", "answer": "estés"},
        ],
    },
    {
        "lesson_number": 2,
        "title": "Present Subjunctive: Regular Verbs",
        "vocabulary": [
            {"word": "hable, hables, hable...", "translation": "-AR subjunctive endings", "pronunciation": "AH-bleh"},
            {"word": "coma, comas, coma...", "translation": "-ER subjunctive endings", "pronunciation": "KOH-mah"},
            {"word": "viva, vivas, viva...", "translation": "-IR subjunctive endings", "pronunciation": "VEE-vah"},
            {"word": "quiero que", "translation": "I want ... to", "pronunciation": "kee-EH-roh keh"},
            {"word": "recomendar", "translation": "to recommend", "pronunciation": "reh-koh-mehn-DAHR"},
        ],
        "grammar": {
            "topic": "Forming the present subjunctive",
            "explanation": "Take the yo form of the present indicative, drop the -o, and add the 'opposite vowel' endings: -ar verbs use e-endings, -er/-ir verbs use a-endings.",
        },
        "example_sentences": [
            {"target_language": "Quiero que hables con ella.", "english": "I want you to talk to her."},
            {"target_language": "Te recomiendo que comas más verduras.", "english": "I recommend that you eat more vegetables."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Es necesario que nosotros ___ (vivir) juntos.", "answer": "vivamos"},
            {"type": "translation", "prompt": "Translate: 'I want them to write the report.'", "answer": "Quiero que ellos escriban el informe."},
        ],
    },
    {
        "lesson_number": 3,
        "title": "Present Subjunctive: Irregular Verbs",
        "vocabulary": [
            {"word": "sea", "translation": "(that) he/she/it be (ser)", "pronunciation": "SEH-ah"},
            {"word": "esté", "translation": "(that) he/she/it be (estar)", "pronunciation": "ehs-TEH"},
            {"word": "vaya", "translation": "(that) he/she/it go (ir)", "pronunciation": "VAH-yah"},
            {"word": "sepa", "translation": "(that) he/she/it know (saber)", "pronunciation": "SEH-pah"},
            {"word": "haya", "translation": "(that) there be / have (haber)", "pronunciation": "AH-yah"},
        ],
        "grammar": {
            "topic": "Memorizing key irregulars",
            "explanation": "Six verbs are fully irregular in the subjunctive: ser (sea), estar (esté), ir (vaya), saber (sepa), haber (haya), and dar (dé). These must be memorized outright.",
        },
        "example_sentences": [
            {"target_language": "Ojalá que todo esté bien.", "english": "I hope everything is okay."},
            {"target_language": "No creo que él sepa la verdad.", "english": "I don't think he knows the truth."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Espero que ___ (ir, ellos) a la fiesta.", "answer": "vayan"},
            {"type": "translation", "prompt": "Translate: 'I hope there is enough food.'", "answer": "Ojalá que haya suficiente comida."},
        ],
    },
    {
        "lesson_number": 4,
        "title": "Subjunctive with Wishes and Hopes",
        "vocabulary": [
            {"word": "ojalá (que)", "translation": "I hope / if only", "pronunciation": "oh-hah-LAH"},
            {"word": "desear", "translation": "to wish/desire", "pronunciation": "deh-seh-AHR"},
            {"word": "esperar", "translation": "to hope", "pronunciation": "ehs-peh-RAHR"},
            {"word": "querer que", "translation": "to want ... to", "pronunciation": "keh-REHR keh"},
            {"word": "preferir que", "translation": "to prefer that", "pronunciation": "preh-feh-REER keh"},
        ],
        "grammar": {
            "topic": "'Ojalá' doesn't need 'que'",
            "explanation": "'Ojalá' can be used with or without 'que' before the subjunctive: Ojalá (que) llueva mañana. It comes from Arabic and expresses a heartfelt wish.",
        },
        "example_sentences": [
            {"target_language": "Ojalá gane el equipo local.", "english": "I hope the home team wins."},
            {"target_language": "Prefiero que vengas temprano.", "english": "I prefer that you come early."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'I hope you (informal) pass the exam.'", "answer": "Ojalá que apruebes el examen."},
            {"type": "fill_in_blank", "prompt": "Deseo que ___ (tú, ser) feliz.", "answer": "seas"},
        ],
    },
    {
        "lesson_number": 5,
        "title": "Subjunctive with Doubt and Denial",
        "vocabulary": [
            {"word": "no creo que", "translation": "I don't think that", "pronunciation": "noh KREH-oh keh"},
            {"word": "dudar que", "translation": "to doubt that", "pronunciation": "doo-DAHR keh"},
            {"word": "negar que", "translation": "to deny that", "pronunciation": "neh-GAHR keh"},
            {"word": "no es cierto que", "translation": "it's not true that", "pronunciation": "noh ehs see-EHR-toh keh"},
            {"word": "es posible que", "translation": "it's possible that", "pronunciation": "ehs poh-SEE-bleh keh"},
        ],
        "grammar": {
            "topic": "Doubt/denial trigger subjunctive; certainty does not",
            "explanation": "Expressions of doubt or denial trigger the subjunctive (no creo que, dudo que), but their affirmative counterparts of certainty use the indicative (creo que + indicative).",
        },
        "example_sentences": [
            {"target_language": "No creo que sea tan difícil.", "english": "I don't think it's that difficult."},
            {"target_language": "Es posible que llueva esta tarde.", "english": "It's possible that it will rain this afternoon."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Dudo que ellos ___ (llegar) a tiempo.", "answer": "lleguen"},
            {"type": "translation", "prompt": "Translate: 'He denies that he did it.'", "answer": "Él niega que lo haya hecho."},
        ],
    },
    {
        "lesson_number": 6,
        "title": "Subjunctive with Emotion",
        "vocabulary": [
            {"word": "me alegra que", "translation": "it makes me happy that", "pronunciation": "meh ah-LEH-grah keh"},
            {"word": "me sorprende que", "translation": "it surprises me that", "pronunciation": "meh sohr-PREHN-deh keh"},
            {"word": "temo que", "translation": "I fear that", "pronunciation": "TEH-moh keh"},
            {"word": "es una pena que", "translation": "it's a shame that", "pronunciation": "ehs OO-nah PEH-nah keh"},
            {"word": "siento que", "translation": "I'm sorry that", "pronunciation": "see-EHN-toh keh"},
        ],
        "grammar": {
            "topic": "Emotion verbs trigger subjunctive",
            "explanation": "Verbs and expressions of emotion (alegrarse, sorprender, temer, sentir) are always followed by the subjunctive in the dependent clause, regardless of certainty.",
        },
        "example_sentences": [
            {"target_language": "Me alegra que estés aquí.", "english": "I'm happy that you're here."},
            {"target_language": "Es una pena que no puedas venir.", "english": "It's a shame that you can't come."},
        ],
        "exercises": [
            {"type": "translation", "prompt": "Translate: 'I fear that we will lose.'", "answer": "Temo que perdamos."},
            {"type": "fill_in_blank", "prompt": "Me sorprende que ella no ___ (saber) nadar.", "answer": "sepa"},
        ],
    },
    {
        "lesson_number": 7,
        "title": "Impersonal Expressions + Subjunctive",
        "vocabulary": [
            {"word": "es necesario que", "translation": "it's necessary that", "pronunciation": "ehs neh-seh-SAH-ree-oh keh"},
            {"word": "es mejor que", "translation": "it's better that", "pronunciation": "ehs meh-HOHR keh"},
            {"word": "es raro que", "translation": "it's strange that", "pronunciation": "ehs RAH-roh keh"},
            {"word": "conviene que", "translation": "it's advisable that", "pronunciation": "kohn-vee-EH-neh keh"},
            {"word": "basta que", "translation": "it's enough that", "pronunciation": "BAHS-tah keh"},
        ],
        "grammar": {
            "topic": "Impersonal 'es + adjective + que'",
            "explanation": "Most impersonal expressions with 'es + adjective + que' require the subjunctive, except those expressing certainty (es verdad que, es obvio que) which take the indicative.",
        },
        "example_sentences": [
            {"target_language": "Es necesario que llegues temprano.", "english": "It's necessary that you arrive early."},
            {"target_language": "Es raro que no haya llamado.", "english": "It's strange that he/she hasn't called."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Es mejor que nosotros ___ (salir) ahora.", "answer": "salgamos"},
            {"type": "translation", "prompt": "Translate: 'It's advisable that you rest.'", "answer": "Conviene que descanses."},
        ],
    },
    {
        "lesson_number": 8,
        "title": "Future Tense (Simple Future)",
        "vocabulary": [
            {"word": "hablaré", "translation": "I will speak", "pronunciation": "ah-blah-REH"},
            {"word": "comeré", "translation": "I will eat", "pronunciation": "koh-meh-REH"},
            {"word": "viviré", "translation": "I will live", "pronunciation": "vee-vee-REH"},
            {"word": "tendré", "translation": "I will have (irregular)", "pronunciation": "tehn-DREH"},
            {"word": "haré", "translation": "I will do/make (irregular)", "pronunciation": "ah-REH"},
        ],
        "grammar": {
            "topic": "Forming the simple future",
            "explanation": "Add -é, -ás, -á, -emos, -éis, -án to the full infinitive for all three verb types. A dozen common verbs have irregular stems (tendré, haré, podré, diré) but keep the same endings.",
        },
        "example_sentences": [
            {"target_language": "Mañana hablaré con el jefe.", "english": "Tomorrow I will speak with the boss."},
            {"target_language": "El próximo año tendremos más tiempo.", "english": "Next year we will have more time."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Ellos ___ (venir) a la boda.", "answer": "vendrán"},
            {"type": "translation", "prompt": "Translate: 'I will call you tomorrow.'", "answer": "Te llamaré mañana."},
        ],
    },
    {
        "lesson_number": 9,
        "title": "Conditional Tense",
        "vocabulary": [
            {"word": "hablaría", "translation": "I would speak", "pronunciation": "ah-blah-REE-ah"},
            {"word": "comería", "translation": "I would eat", "pronunciation": "koh-meh-REE-ah"},
            {"word": "podría", "translation": "I would be able to (irregular)", "pronunciation": "poh-DREE-ah"},
            {"word": "me gustaría", "translation": "I would like", "pronunciation": "meh goos-tah-REE-ah"},
            {"word": "debería", "translation": "I should", "pronunciation": "deh-beh-REE-ah"},
        ],
        "grammar": {
            "topic": "Forming the conditional",
            "explanation": "The conditional uses the same stems as the future (regular = full infinitive, irregular = same irregular stems) with -ía, -ías, -ía, -íamos, -íais, -ían endings.",
        },
        "example_sentences": [
            {"target_language": "Me gustaría viajar a Japón.", "english": "I would like to travel to Japan."},
            {"target_language": "Deberías descansar más.", "english": "You should rest more."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "Yo ___ (poder) ayudarte mañana.", "answer": "podría"},
            {"type": "translation", "prompt": "Translate: 'We would travel by train.'", "answer": "Viajaríamos en tren."},
        ],
    },
    {
        "lesson_number": 10,
        "title": "Present Perfect (Pretérito Perfecto)",
        "vocabulary": [
            {"word": "he hablado", "translation": "I have spoken", "pronunciation": "eh ah-BLAH-doh"},
            {"word": "has comido", "translation": "you have eaten", "pronunciation": "ahs koh-MEE-doh"},
            {"word": "ha vivido", "translation": "he/she has lived", "pronunciation": "ah vee-VEE-doh"},
            {"word": "hemos hecho", "translation": "we have done (irregular participle)", "pronunciation": "EH-mohs EH-choh"},
            {"word": "todavía no", "translation": "not yet", "pronunciation": "toh-dah-VEE-ah noh"},
        ],
        "grammar": {
            "topic": "Haber + past participle",
            "explanation": "The present perfect is formed with the present of 'haber' + past participle (-ado for -ar verbs, -ido for -er/-ir verbs). Some participles are irregular: hecho, dicho, visto, puesto, escrito.",
        },
        "example_sentences": [
            {"target_language": "He terminado mi tarea.", "english": "I have finished my homework."},
            {"target_language": "Todavía no hemos comido.", "english": "We haven't eaten yet."},
        ],
        "exercises": [
            {"type": "fill_in_blank", "prompt": "¿___ (tú, ver) esa película?", "answer": "Has visto"},
            {"type": "translation", "prompt": "Translate: 'She has already written the email.'", "answer": "Ella ya ha escrito el correo."},
        ],
    },
    # --- Confirmed roadmap for Lessons 11-50 (titles only — content pending) ---
    {"lesson_number": 11, "title": "Past Perfect (Pluscuamperfecto)"},
    {"lesson_number": 12, "title": "Future Perfect"},
    {"lesson_number": 13, "title": "Conditional Perfect"},
    {"lesson_number": 14, "title": "Passive Voice with Ser"},
    {"lesson_number": 15, "title": "Passive 'Se' Constructions"},
    {"lesson_number": 16, "title": "Relative Pronouns (que, quien, cuyo)"},
    {"lesson_number": 17, "title": "Por vs Para"},
    {"lesson_number": 18, "title": "Prepositional Pronouns"},
    {"lesson_number": 19, "title": "Nosotros Commands"},
    {"lesson_number": 20, "title": "Indirect Speech (Reported Speech)"},
    {"lesson_number": 21, "title": "Si Clauses: Real Conditions"},
    {"lesson_number": 22, "title": "Si Clauses: Hypothetical Conditions"},
    {"lesson_number": 23, "title": "Idiomatic Expressions with Tener"},
    {"lesson_number": 24, "title": "Idiomatic Expressions with Hacer"},
    {"lesson_number": 25, "title": "Common False Friends"},
    {"lesson_number": 26, "title": "Business Spanish: Meetings"},
    {"lesson_number": 27, "title": "Business Spanish: Emails"},
    {"lesson_number": 28, "title": "Travel Spanish: At the Airport"},
    {"lesson_number": 29, "title": "Travel Spanish: At the Hotel"},
    {"lesson_number": 30, "title": "Talking About Health and Symptoms"},
    {"lesson_number": 31, "title": "At the Doctor's Office"},
    {"lesson_number": 32, "title": "Environmental Vocabulary"},
    {"lesson_number": 33, "title": "Talking About Technology"},
    {"lesson_number": 34, "title": "Expressing Opinions"},
    {"lesson_number": 35, "title": "Agreeing and Disagreeing"},
    {"lesson_number": 36, "title": "Debate Vocabulary and Structures"},
    {"lesson_number": 37, "title": "Narrating a Story in the Past"},
    {"lesson_number": 38, "title": "Describing a Process (Sequencing Words)"},
    {"lesson_number": 39, "title": "Making Complaints and Apologizing"},
    {"lesson_number": 40, "title": "Giving Advice (debería, te recomiendo)"},
    {"lesson_number": 41, "title": "Job Interview Vocabulary"},
    {"lesson_number": 42, "title": "Writing a Formal Letter"},
    {"lesson_number": 43, "title": "Understanding News Headlines"},
    {"lesson_number": 44, "title": "Regional Variations in Spanish"},
    {"lesson_number": 45, "title": "Common Idioms and Sayings"},
    {"lesson_number": 46, "title": "Advanced Ser/Estar Nuances"},
    {"lesson_number": 47, "title": "Gerunds and Progressive Tenses"},
    {"lesson_number": 48, "title": "Reported Commands"},
    {"lesson_number": 49, "title": "Expressing Cause and Effect"},
    {"lesson_number": 50, "title": "Intermediate Review and Assessment"},
]
