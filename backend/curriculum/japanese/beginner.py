# backend/curriculum/japanese/beginner.py
#
# Curriculum data for Japanese, Beginner level.
# Loaded dynamically by CurriculumEngine.get_lessons("Japanese", "Beginner")
# via import_module("backend.curriculum.japanese.beginner"), which reads
# the LESSONS list below.
#
# IMPORTANT: "passage" is what /lesson/curriculum uses to generate the
# vocabulary/grammar/examples shown to the learner, so it must actually
# contain the target words for that lesson's title — not just a sentence
# that happens to use one of them in passing. Each passage below leads
# with the actual vocabulary items, then a short sentence using them.

LESSONS = [
    {"id": 1, "title": "Greetings",
     "passage": "こんにちは。おはようございます。こんばんは。さようなら。ありがとうございます。すみません。こんにちは、元気ですか。はい、元気です。"},

    {"id": 2, "title": "Introducing Yourself",
     "passage": "はじめまして。わたしは〜です。よろしくおねがいします。はじめまして、わたしはユキです。よろしくおねがいします。"},

    {"id": 3, "title": "Numbers 1–10",
     "passage": "いち、に、さん、よん、ご、ろく、なな、はち、きゅう、じゅう。りんごが3こあります。"},

    {"id": 4, "title": "Numbers 11–100",
     "passage": "じゅういち、じゅうに、にじゅう、さんじゅう、よんじゅう、ごじゅう、ろくじゅう、ななじゅう、はちじゅう、きゅうじゅう、ひゃく。にじゅうさんです。わたしは にじゅう さいです。"},

    {"id": 5, "title": "Days of the Week",
     "passage": "げつようび、かようび、すいようび、もくようび、きんようび、どようび、にちようび。きょうは げつようびです。どようびに あいましょう。"},

    {"id": 6, "title": "Months of the Year",
     "passage": "いちがつ、にがつ、さんがつ、しがつ、ごがつ、ろくがつ、しちがつ、はちがつ、くがつ、じゅうがつ、じゅういちがつ、じゅうにがつ。わたしの たんじょうびは さんがつです。"},

    {"id": 7, "title": "Telling Time",
     "passage": "いま なんじですか。〜じ。〜ふん。ごぜん。ごご。はん。いま ごご さんじです。よじはんに あいましょう。"},

    {"id": 8, "title": "Family Members",
     "passage": "かぞく。ちち、おとうさん。はは、おかあさん。あに、おにいさん。いもうと。こども。わたしの かぞくは よにんです。これは わたしの ははです。"},

    {"id": 9, "title": "Colors",
     "passage": "あか、あお、きいろ、みどり、しろ、くろ。あかい くるまが すきです。そらは あおいです。"},

    {"id": 10, "title": "Basic Adjectives",
     "passage": "おおきい、ちいさい、あたらしい、ふるい、たかい、やすい。この かばんは たかいです。ちいさい いぬが すきです。"},

    {"id": 11, "title": "Hiragana: あ-row (Vowels)",
     "passage": "あ、い、う、え、お。あいうえお。あい は うつくしい。"},

    {"id": 12, "title": "Hiragana: か-row",
     "passage": "か、き、く、け、こ。かき が すきです。"},

    {"id": 13, "title": "Hiragana: さ-row",
     "passage": "さ、し、す、せ、そ。すし が たべたいです。"},

    {"id": 14, "title": "Hiragana: た-row",
     "passage": "た、ち、つ、て、と。たこ が すきです。"},

    {"id": 15, "title": "Hiragana: な-row",
     "passage": "な、に、ぬ、ね、の。いぬ が すきです。"},

    {"id": 16, "title": "Hiragana: は-row",
     "passage": "は、ひ、ふ、へ、ほ。はな が きれいです。"},

    {"id": 17, "title": "Hiragana: ま-row",
     "passage": "ま、み、む、め、も。やま に のぼります。"},

    {"id": 18, "title": "Hiragana: や-row",
     "passage": "や、ゆ、よ。やさい。ゆき。よる。ゆき が ふっています。"},

    {"id": 19, "title": "Hiragana: ら-row",
     "passage": "ら、り、る、れ、ろ。さくら が きれいです。"},

    {"id": 20, "title": "Hiragana: わ & ん",
     "passage": "わ、を、ん。わたし。ほん。にほん。ほん を よみます。わたし は にほんじんです。"},

    {"id": 21, "title": "Katakana Basics",
     "passage": "ア、コーヒー、テレビ、カメラ、パン、アメリカ。コーヒー を ください。テレビ を みます。"},

    {"id": 22, "title": "Particles: は & が",
     "passage": "は。が。これは〜です。だれが。なにが。すきです。わたしは がくせいです。だれが きましたか。"},

    {"id": 23, "title": "Particles: を & に",
     "passage": "を。に。がっこうに いきます。ごはんを たべます。しちじに。ともだちに あう。まいにち がっこうに いきます。"},

    {"id": 24, "title": "Particles: で & と",
     "passage": "で。と。でんしゃで いきます。としょかんで べんきょうします。ともだちと。パンと ぎゅうにゅう。としょかんで べんきょうします。ともだちと えいがを みます。"},

    {"id": 25, "title": "This, That, Which (これ/それ/あれ)",
     "passage": "これ。それ。あれ。どれ。この〜。どの〜。これは わたしの ほんです。あれは なんですか。"},

    {"id": 26, "title": "Asking Yes/No Questions",
     "passage": "〜ですか。はい。いいえ。ほんとうですか。わかりますか。だいじょうぶですか。がくせいですか。はい、がくせいです。"},

    {"id": 27, "title": "Verbs: Present Tense (~ます)",
     "passage": "たべます。のみます。いきます。みます。します。きます。まいあさ パンを たべます。がっこうに いきます。"},

    {"id": 28, "title": "Verbs: Past Tense (~ました)",
     "passage": "たべました。のみました。いきました。みました。しました。きました。きのう えいがを みました。レストランで たべました。"},

    {"id": 29, "title": "Verbs: Negative Form (~ません)",
     "passage": "たべません。いきません。わかりません。ありません。いません。すみません。にくを たべません。わかりません。"},

    {"id": 30, "title": "い-Adjectives",
     "passage": "いい。わるい。あつい。さむい。おいしい。むずかしい。きょうは あついです。この りょうりは おいしいです。"},

    {"id": 31, "title": "な-Adjectives",
     "passage": "きれい(な)。げんき(な)。しずか(な)。ゆうめい(な)。べんり(な)。すき(な)。ここは しずかな こうえんです。げんきですか。"},

    {"id": 32, "title": "Food Vocabulary",
     "passage": "ごはん。みず。にく。やさい。くだもの。たまご。やさいを たくさん たべます。みずを ください。"},

    {"id": 33, "title": "Ordering at a Restaurant",
     "passage": "メニュー。ちゅうもん。〜を おねがいします。おすすめは なんですか。おかいけい。ごちそうさまでした。すしを おねがいします。おかいけいを おねがいします。"},

    {"id": 34, "title": "Shopping Phrases",
     "passage": "いくらですか。たかい。やすい。これを ください。カードで。げんきんで。これは いくらですか。カードで おねがいします。"},

    {"id": 35, "title": "Asking for Directions",
     "passage": "えきは どこですか。まっすぐ。みぎ。ひだり。ちかい。とおい。まっすぐ いって ください。"},

    {"id": 36, "title": "Transportation",
     "passage": "でんしゃ。バス。ひこうき。くるま。じてんしゃ。えき。でんしゃで がっこうに いきます。じてんしゃが すきです。"},

    {"id": 37, "title": "Weather",
     "passage": "てんき。はれ。あめ。くもり。ゆき。かぜ。きょうは いい てんきですね。あしたは あめです。"},

    {"id": 38, "title": "The Four Seasons",
     "passage": "はる。なつ。あき。ふゆ。きせつ。いちばん すきな きせつ。はるが いちばん すきです。ふゆは さむいです。"},

    {"id": 39, "title": "Body Parts",
     "passage": "あたま。め。みみ。て。あし。おなか。あたまが いたいです。てを あらいます。"},

    {"id": 40, "title": "Daily Routine",
     "passage": "おきます。ねます。シャワーを あびます。はを みがきます。でかけます。かえります。まいあさ しちじに おきます。よる じゅういちじに ねます。"},

    {"id": 41, "title": "Hobbies & Free Time",
     "passage": "しゅみ。おんがくを ききます。ほんを よみます。えいがを みます。スポーツを します。りょこうします。わたしの しゅみは どくしょです。"},

    {"id": 42, "title": "School Vocabulary",
     "passage": "がっこう。せんせい。きょうしつ。しゅくだい。テスト。じゅぎょう。しゅくだいを します。せんせいは やさしいです。"},

    {"id": 43, "title": "Work & Jobs",
     "passage": "しごと。かいしゃ。かいしゃいん。いしゃ。エンジニア。やすみ。わたしの しごとは エンジニアです。きょうは やすみです。"},

    {"id": 44, "title": "Animals",
     "passage": "いぬ。ねこ。とり。さかな。うさぎ。ぞう。ねこが すきです。とりが とんでいます。"},

    {"id": 45, "title": "Emotions & Feelings",
     "passage": "うれしい。かなしい。たのしい。こわい。しんぱい。びっくりしました。きょうは とても たのしかったです。しんぱいしないで ください。"},

    {"id": 46, "title": "Polite Requests (~てください)",
     "passage": "まってください。みてください。いってください。たすけてください。きいてください。みせてください。ちょっと まってください。"},

    {"id": 47, "title": "Counting Objects (Counters)",
     "passage": "〜こ。〜まい。〜ひき。〜にん。〜さつ。〜ほん。りんごを ふたつ ください。ほんを さんさつ かいました。"},

    {"id": 48, "title": "Making Comparisons",
     "passage": "〜より。〜のほうが。いちばん。おなじ。〜ほど〜ない。どちらが すきですか。いぬのほうが ねこより すきです。これが いちばん おいしいです。"},

    {"id": 49, "title": "Making Plans & Invitations",
     "passage": "いっしょに。〜ませんか。〜ましょう。よてい。ひま。やくそく。いっしょに えいがを みませんか。こんど あいましょう。"},

    {"id": 50, "title": "Basic Kanji: Numbers & Days",
     "passage": "一。二。三。日。月。人。一月一日。三人の ひとが きました。"},
]
