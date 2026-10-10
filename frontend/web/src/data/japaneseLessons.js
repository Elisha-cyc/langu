// frontend/web/src/data/japaneseLessons.js
// =====================================================================
// Static fallback curriculum: 50 beginner Japanese lessons.
// Only used when the backend returns no official lessons for Japanese.
// =====================================================================
export const JAPANESE_LESSONS = [
  {
    title: "Greetings",
    vocab: [
      ["こんにちは", "konnichiwa", "Hello / good afternoon"],
      ["おはようございます", "ohayou gozaimasu", "Good morning"],
      ["こんばんは", "konbanwa", "Good evening"],
      ["さようなら", "sayounara", "Goodbye"],
      ["ありがとうございます", "arigatou gozaimasu", "Thank you"],
      ["すみません", "sumimasen", "Excuse me / sorry"],
    ],
    examples: [
      [
        "こんにちは、元気ですか。",
        "Konnichiwa, genki desu ka.",
        "Hello, how are you?",
      ],
      [
        "はい、元気です。ありがとうございます。",
        "Hai, genki desu. Arigatou gozaimasu.",
        "Yes, I'm fine. Thank you.",
      ],
    ],
    note: "Japanese greetings change with the time of day. おはよう is used in the morning, こんにちは in the afternoon, and こんばんは in the evening. Adding ございます makes a phrase more polite.",
  },
  {
    title: "Introducing Yourself",
    vocab: [
      ["はじめまして", "hajimemashite", "Nice to meet you"],
      ["わたしは〜です", "watashi wa ~ desu", "I am ~"],
      [
        "よろしくおねがいします",
        "yoroshiku onegaishimasu",
        "Please treat me well / pleased to meet you",
      ],
      ["なまえ", "namae", "name"],
      ["しゅっしん", "shusshin", "hometown / origin"],
      ["がくせい", "gakusei", "student"],
    ],
    examples: [
      [
        "はじめまして、わたしはユキです。",
        "Hajimemashite, watashi wa Yuki desu.",
        "Nice to meet you, I'm Yuki.",
      ],
      [
        "よろしくおねがいします。",
        "Yoroshiku onegaishimasu.",
        "Pleased to meet you.",
      ],
    ],
    note: "わたしは〜です is the core self-introduction pattern: 'As for me, I am ~.' The topic particle は is pronounced 'wa' here, not 'ha'.",
  },
  {
    title: "Numbers 1–10",
    vocab: [
      ["いち (1)", "ichi", "one"],
      ["に (2)", "ni", "two"],
      ["さん (3)", "san", "three"],
      ["よん / し (4)", "yon / shi", "four"],
      ["ご (5)", "go", "five"],
      [
        "ろく〜じゅう (6–10)",
        "roku, nana, hachi, kyuu, juu",
        "six through ten",
      ],
    ],
    examples: [
      [
        "りんごが3こあります。",
        "Ringo ga san-ko arimasu.",
        "There are three apples.",
      ],
      ["いち、に、さん、し。", "Ichi, ni, san, shi.", "One, two, three, four."],
    ],
    note: "4 and 7 have two readings each (よん/し and なな/しち); よん and なな are more common in daily speech to avoid confusion with other words.",
  },
  {
    title: "Numbers 11–100",
    vocab: [
      ["じゅういち (11)", "juuichi", "eleven"],
      ["にじゅう (20)", "nijuu", "twenty"],
      ["さんじゅう (30)", "sanjuu", "thirty"],
      ["ごじゅう (50)", "gojuu", "fifty"],
      ["ひゃく (100)", "hyaku", "one hundred"],
      ["にじゅうさん (23)", "nijuu-san", "twenty-three"],
    ],
    examples: [
      [
        "わたしは にじゅう さいです。",
        "Watashi wa nijuu-sai desu.",
        "I am twenty years old.",
      ],
      ["ひゃくえんです。", "Hyaku-en desu.", "It's 100 yen."],
    ],
    note: "Numbers above 10 are built compositionally: 十 (juu) + digit for 11–19, and digit + 十 for multiples of ten. 23 = に (2) + じゅう (10) + さん (3).",
  },
  {
    title: "Days of the Week",
    vocab: [
      ["げつようび", "getsuyoubi", "Monday"],
      ["かようび", "kayoubi", "Tuesday"],
      ["すいようび", "suiyoubi", "Wednesday"],
      ["もくようび", "mokuyoubi", "Thursday"],
      ["きんようび", "kinyoubi", "Friday"],
      ["どようび / にちようび", "doyoubi / nichiyoubi", "Saturday / Sunday"],
    ],
    examples: [
      [
        "きょうは げつようびです。",
        "Kyou wa getsuyoubi desu.",
        "Today is Monday.",
      ],
      [
        "どようびに あいましょう。",
        "Doyoubi ni aimashou.",
        "Let's meet on Saturday.",
      ],
    ],
    note: "Every day name ends in ようび ('day of the week'). Each is tied to an element: 月 (moon), 火 (fire), 水 (water), 木 (wood), 金 (gold), 土 (earth), 日 (sun).",
  },
  {
    title: "Months of the Year",
    vocab: [
      ["いちがつ", "ichigatsu", "January"],
      ["しがつ", "shigatsu", "April"],
      ["しちがつ", "shichigatsu", "July"],
      ["じゅうにがつ", "juunigatsu", "December"],
      ["なんがつ", "nangatsu", "what month"],
      ["たんじょうび", "tanjoubi", "birthday"],
    ],
    examples: [
      [
        "わたしの たんじょうびは さんがつです。",
        "Watashi no tanjoubi wa sangatsu desu.",
        "My birthday is in March.",
      ],
      [
        "なんがつが すきですか。",
        "Nangatsu ga suki desu ka.",
        "Which month do you like?",
      ],
    ],
    note: "Months are simply the number plus がつ ('month'). No special names to memorize — just count 1 through 12 and add がつ.",
  },
  {
    title: "Telling Time",
    vocab: [
      ["いま なんじですか", "ima nanji desu ka", "What time is it now?"],
      ["〜じ", "~ji", "~ o'clock"],
      ["〜ふん / ぷん", "~fun / pun", "~ minutes"],
      ["ごぜん", "gozen", "AM"],
      ["ごご", "gogo", "PM"],
      ["はん", "han", "half (past)"],
    ],
    examples: [
      ["いま ごご さんじです。", "Ima gogo sanji desu.", "It's 3 PM now."],
      [
        "よじはんに あいましょう。",
        "Yoji-han ni aimashou.",
        "Let's meet at 4:30.",
      ],
    ],
    note: "時 (じ) attaches to hours and 分 (ふん/ぷん) to minutes; the reading of 分 shifts between ふん and ぷん depending on the preceding number.",
  },
  {
    title: "Family Members",
    vocab: [
      ["かぞく", "kazoku", "family"],
      [
        "ちち / おとうさん",
        "chichi / otousan",
        "my father / (someone's) father",
      ],
      ["はは / おかあさん", "haha / okaasan", "my mother / (someone's) mother"],
      ["あに / おにいさん", "ani / oniisan", "older brother"],
      ["いもうと", "imouto", "younger sister"],
      ["こども", "kodomo", "child"],
    ],
    examples: [
      [
        "わたしの かぞくは よにんです。",
        "Watashi no kazoku wa yonin desu.",
        "My family has four people.",
      ],
      [
        "これは わたしの ははです。",
        "Kore wa watashi no haha desu.",
        "This is my mother.",
      ],
    ],
    note: "Japanese uses humble terms (ちち, はは) for your own family and honorific terms (おとうさん, おかあさん) when referring to someone else's family, or addressing your own directly.",
  },
  {
    title: "Colors",
    vocab: [
      ["あか", "aka", "red"],
      ["あお", "ao", "blue"],
      ["きいろ", "kiiro", "yellow"],
      ["みどり", "midori", "green"],
      ["しろ", "shiro", "white"],
      ["くろ", "kuro", "black"],
    ],
    examples: [
      [
        "あかい くるまが すきです。",
        "Akai kuruma ga suki desu.",
        "I like red cars.",
      ],
      ["そらは あおいです。", "Sora wa aoi desu.", "The sky is blue."],
    ],
    note: "Some colors (あか, あお, しろ, くろ) can become い-adjectives by adding い (あかい = 'red'), while others like みどり and きいろ usually attach with の instead.",
  },
  {
    title: "Basic Adjectives",
    vocab: [
      ["おおきい", "ookii", "big"],
      ["ちいさい", "chiisai", "small"],
      ["あたらしい", "atarashii", "new"],
      ["ふるい", "furui", "old (things)"],
      ["たかい", "takai", "expensive / tall"],
      ["やすい", "yasui", "cheap"],
    ],
    examples: [
      [
        "この かばんは たかいです。",
        "Kono kaban wa takai desu.",
        "This bag is expensive.",
      ],
      [
        "ちいさい いぬが すきです。",
        "Chiisai inu ga suki desu.",
        "I like small dogs.",
      ],
    ],
    note: "Words ending in い like these are called い-adjectives; they conjugate on their own without needing です's help for tense, though です is added for politeness.",
  },
  {
    title: "Hiragana: あ-row (Vowels)",
    vocab: [
      ["あ", "a", "a"],
      ["い", "i", "i"],
      ["う", "u", "u"],
      ["え", "e", "e"],
      ["お", "o", "o"],
      ["あい", "ai", "love"],
    ],
    examples: [
      ["あいうえお", "a i u e o", "the five Japanese vowels"],
      ["あい は うつくしい。", "Ai wa utsukushii.", "Love is beautiful."],
    ],
    note: "Every hiragana sound is built from these five vowels. Master あいうえお first — nearly every other character is a consonant blended with one of these.",
  },
  {
    title: "Hiragana: か-row",
    vocab: [
      ["か", "ka", "ka"],
      ["き", "ki", "ki"],
      ["く", "ku", "ku"],
      ["け", "ke", "ke"],
      ["こ", "ko", "ko"],
      ["かき", "kaki", "persimmon"],
    ],
    examples: [
      ["かき が すきです。", "Kaki ga suki desu.", "I like persimmons."],
      ["こ", "ko", "child (also written 子)"],
    ],
    note: "The か-row adds a 'k' sound in front of each vowel: ka, ki, ku, ke, ko. Adding two small marks (゛) turns か into が (ga), voicing the consonant.",
  },
  {
    title: "Hiragana: さ-row",
    vocab: [
      ["さ", "sa", "sa"],
      ["し", "shi", "shi"],
      ["す", "su", "su"],
      ["せ", "se", "se"],
      ["そ", "so", "so"],
      ["すし", "sushi", "sushi"],
    ],
    examples: [
      [
        "すし が たべたいです。",
        "Sushi ga tabetai desu.",
        "I want to eat sushi.",
      ],
    ],
    note: "Note that し is pronounced 'shi', not 'si' — one of a few irregular readings in the hiragana chart worth memorizing early.",
  },
  {
    title: "Hiragana: た-row",
    vocab: [
      ["た", "ta", "ta"],
      ["ち", "chi", "chi"],
      ["つ", "tsu", "tsu"],
      ["て", "te", "te"],
      ["と", "to", "to"],
      ["たこ", "tako", "octopus"],
    ],
    examples: [["たこ が すきです。", "Tako ga suki desu.", "I like octopus."]],
    note: "ち (chi) and つ (tsu) are irregular readings, similar to how し worked in the さ-row. These three exceptions are worth drilling with flashcards.",
  },
  {
    title: "Hiragana: な-row",
    vocab: [
      ["な", "na", "na"],
      ["に", "ni", "ni"],
      ["ぬ", "nu", "nu"],
      ["ね", "ne", "ne"],
      ["の", "no", "no"],
      ["いぬ", "inu", "dog"],
    ],
    examples: [["いぬ が すきです。", "Inu ga suki desu.", "I like dogs."]],
    note: "の doubles as both a hiragana character and the possessive particle meaning 'of' — わたしの ('my/mine') uses this same character.",
  },
  {
    title: "Hiragana: は-row",
    vocab: [
      ["は", "ha", "ha"],
      ["ひ", "hi", "hi"],
      ["ふ", "fu", "fu"],
      ["へ", "he", "he"],
      ["ほ", "ho", "ho"],
      ["はな", "hana", "flower"],
    ],
    examples: [
      ["はな が きれいです。", "Hana ga kirei desu.", "The flower is pretty."],
    ],
    note: "は also functions as the topic particle, pronounced 'wa' in that role — one character with two very different jobs depending on context.",
  },
  {
    title: "Hiragana: ま-row",
    vocab: [
      ["ま", "ma", "ma"],
      ["み", "mi", "mi"],
      ["む", "mu", "mu"],
      ["め", "me", "me"],
      ["も", "mo", "mo"],
      ["やま", "yama", "mountain"],
    ],
    examples: [
      ["やま に のぼります。", "Yama ni noborimasu.", "I climb the mountain."],
    ],
    note: "も also functions as a particle meaning 'too / also', similar to how の and は double as grammar particles.",
  },
  {
    title: "Hiragana: や-row",
    vocab: [
      ["や", "ya", "ya"],
      ["ゆ", "yu", "yu"],
      ["よ", "yo", "yo"],
      ["やさい", "yasai", "vegetable"],
      ["ゆき", "yuki", "snow"],
      ["よる", "yoru", "night"],
    ],
    examples: [
      ["ゆき が ふっています。", "Yuki ga futte imasu.", "Snow is falling."],
    ],
    note: "The や-row only has three sounds (ya, yu, yo) rather than five, since 'yi' and 'ye' don't exist as standard hiragana.",
  },
  {
    title: "Hiragana: ら-row",
    vocab: [
      ["ら", "ra", "ra"],
      ["り", "ri", "ri"],
      ["る", "ru", "ru"],
      ["れ", "re", "re"],
      ["ろ", "ro", "ro"],
      ["さくら", "sakura", "cherry blossom"],
    ],
    examples: [
      [
        "さくら が きれいです。",
        "Sakura ga kirei desu.",
        "The cherry blossoms are beautiful.",
      ],
    ],
    note: "Japanese 'r' sounds sit between an English 'r' and 'l' — made with a quick flick of the tongue tip, closer to a soft 'd' than either English sound.",
  },
  {
    title: "Hiragana: わ & ん",
    vocab: [
      ["わ", "wa", "wa"],
      ["を", "wo", "wo (object particle)"],
      ["ん", "n", "n"],
      ["わたし", "watashi", "I / me"],
      ["ほん", "hon", "book"],
      ["にほん", "nihon", "Japan"],
    ],
    examples: [
      ["ほん を よみます。", "Hon wo yomimasu.", "I read a book."],
      [
        "わたし は にほんじんです。",
        "Watashi wa nihonjin desu.",
        "I am Japanese.",
      ],
    ],
    note: "を is almost always pronounced 'o' and used only as the object-marking particle. ん is the only hiragana that represents a consonant alone, always closing a syllable.",
  },
  {
    title: "Katakana Basics",
    vocab: [
      ["ア", "a", "a"],
      ["コーヒー", "koohii", "coffee"],
      ["テレビ", "terebi", "television"],
      ["カメラ", "kamera", "camera"],
      ["パン", "pan", "bread"],
      ["アメリカ", "amerika", "America"],
    ],
    examples: [
      ["コーヒー を ください。", "Koohii wo kudasai.", "Coffee, please."],
      ["テレビ を みます。", "Terebi wo mimasu.", "I watch television."],
    ],
    note: "Katakana shares the same sounds as hiragana but looks more angular, and is used mainly for foreign loanwords, foreign names, and for emphasis — similar to italics in English.",
  },
  {
    title: "Particles: は & が",
    vocab: [
      ["は (wa)", "wa", "topic marker"],
      ["が", "ga", "subject marker"],
      ["これは〜です", "kore wa ~ desu", "this is ~"],
      ["だれが", "dare ga", "who (as subject)"],
      ["なにが", "nani ga", "what (as subject)"],
      ["すきです", "suki desu", "like"],
    ],
    examples: [
      [
        "わたしは がくせいです。",
        "Watashi wa gakusei desu.",
        "As for me, I am a student.",
      ],
      ["だれが きましたか。", "Dare ga kimashita ka.", "Who came?"],
    ],
    note: "は introduces the topic being discussed, while が marks the grammatical subject, often used to highlight new or specific information — a subtle but important distinction.",
  },
  {
    title: "Particles: を & に",
    vocab: [
      ["を", "wo", "direct object marker"],
      ["に", "ni", "direction / time / location marker"],
      ["がっこうに いきます", "gakkou ni ikimasu", "go to school"],
      ["ごはんを たべます", "gohan wo tabemasu", "eat a meal"],
      ["しちじに", "shichi-ji ni", "at 7 o'clock"],
      ["ともだちに あう", "tomodachi ni au", "meet a friend"],
    ],
    examples: [
      [
        "まいにち がっこうに いきます。",
        "Mainichi gakkou ni ikimasu.",
        "I go to school every day.",
      ],
      ["ごはんを たべました。", "Gohan wo tabemashita.", "I ate a meal."],
    ],
    note: "を marks the thing being acted on, while に marks a destination, a specific point in time, or the target of certain verbs like 会う ('to meet').",
  },
  {
    title: "Particles: で & と",
    vocab: [
      ["で", "de", "location of action / means"],
      ["と", "to", "and / with"],
      ["でんしゃで いきます", "densha de ikimasu", "go by train"],
      [
        "としょかんで べんきょうします",
        "toshokan de benkyou shimasu",
        "study at the library",
      ],
      ["ともだちと", "tomodachi to", "with a friend"],
      ["パンと ぎゅうにゅう", "pan to gyuunyuu", "bread and milk"],
    ],
    examples: [
      [
        "としょかんで べんきょうします。",
        "Toshokan de benkyou shimasu.",
        "I study at the library.",
      ],
      [
        "ともだちと えいがを みます。",
        "Tomodachi to eiga wo mimasu.",
        "I watch a movie with a friend.",
      ],
    ],
    note: "で marks where an action happens or the tool used to do it, while と links nouns together like 'and', or marks who you're doing something 'with'.",
  },
  {
    title: "This, That, Which (これ/それ/あれ)",
    vocab: [
      ["これ", "kore", "this (near speaker)"],
      ["それ", "sore", "that (near listener)"],
      ["あれ", "are", "that (far from both)"],
      ["どれ", "dore", "which one"],
      ["この〜", "kono ~", "this ~ (+noun)"],
      ["どの〜", "dono ~", "which ~ (+noun)"],
    ],
    examples: [
      [
        "これは わたしの ほんです。",
        "Kore wa watashi no hon desu.",
        "This is my book.",
      ],
      [
        "あれは なんですか。",
        "Are wa nan desu ka.",
        "What is that (over there)?",
      ],
    ],
    note: "これ/それ/あれ/どれ stand alone as pronouns, while この/その/あの/どの must be followed directly by a noun, like 'this book' rather than just 'this'.",
  },
  {
    title: "Asking Yes/No Questions",
    vocab: [
      ["〜ですか", "~desu ka", "is it ~? (polite question)"],
      ["はい", "hai", "yes"],
      ["いいえ", "iie", "no"],
      ["ほんとうですか", "hontou desu ka", "really?"],
      ["わかりますか", "wakarimasu ka", "do you understand?"],
      ["だいじょうぶですか", "daijoubu desu ka", "are you okay?"],
    ],
    examples: [
      ["がくせいですか。", "Gakusei desu ka.", "Are you a student?"],
      ["はい、がくせいです。", "Hai, gakusei desu.", "Yes, I am a student."],
    ],
    note: "Turning a statement into a question in Japanese is simple: just add か to the end of a です or ます sentence — no word order change needed, unlike English.",
  },
  {
    title: "Verbs: Present Tense (~ます)",
    vocab: [
      ["たべます", "tabemasu", "eat"],
      ["のみます", "nomimasu", "drink"],
      ["いきます", "ikimasu", "go"],
      ["みます", "mimasu", "see / watch"],
      ["します", "shimasu", "do"],
      ["きます", "kimasu", "come"],
    ],
    examples: [
      [
        "まいあさ パンを たべます。",
        "Maiasa pan wo tabemasu.",
        "I eat bread every morning.",
      ],
      ["がっこうに いきます。", "Gakkou ni ikimasu.", "I go to school."],
    ],
    note: "The polite present tense in ~ます also covers the future in Japanese — たべます means both 'eats' and 'will eat', depending on context.",
  },
  {
    title: "Verbs: Past Tense (~ました)",
    vocab: [
      ["たべました", "tabemashita", "ate"],
      ["のみました", "nomimashita", "drank"],
      ["いきました", "ikimashita", "went"],
      ["みました", "mimashita", "saw / watched"],
      ["しました", "shimashita", "did"],
      ["きました", "kimashita", "came"],
    ],
    examples: [
      [
        "きのう えいがを みました。",
        "Kinou eiga wo mimashita.",
        "I watched a movie yesterday.",
      ],
      [
        "レストランで たべました。",
        "Resutoran de tabemashita.",
        "I ate at a restaurant.",
      ],
    ],
    note: "To form the polite past tense, simply swap ~ます for ~ました. This pattern works consistently across all polite-form verbs.",
  },
  {
    title: "Verbs: Negative Form (~ません)",
    vocab: [
      ["たべません", "tabemasen", "don't/won't eat"],
      ["いきません", "ikimasen", "don't/won't go"],
      ["わかりません", "wakarimasen", "don't understand"],
      ["ありません", "arimasen", "there isn't (things)"],
      ["いません", "imasen", "there isn't (people/animals)"],
      ["すみません", "sumimasen", "excuse me (lit. 'it does not end')"],
    ],
    examples: [
      ["にくを たべません。", "Niku wo tabemasen.", "I don't eat meat."],
      ["わかりません。", "Wakarimasen.", "I don't understand."],
    ],
    note: "Swap ~ます for ~ません to negate a polite verb. For past negative, ~ませんでした is used, e.g. たべませんでした ('didn't eat').",
  },
  {
    title: "い-Adjectives",
    vocab: [
      ["いい", "ii", "good"],
      ["わるい", "warui", "bad"],
      ["あつい", "atsui", "hot"],
      ["さむい", "samui", "cold"],
      ["おいしい", "oishii", "delicious"],
      ["むずかしい", "muzukashii", "difficult"],
    ],
    examples: [
      ["きょうは あついです。", "Kyou wa atsui desu.", "Today is hot."],
      [
        "この りょうりは おいしいです。",
        "Kono ryouri wa oishii desu.",
        "This dish is delicious.",
      ],
    ],
    note: "To negate an い-adjective, drop the final い and add くない: あつい → あつくない ('not hot'). This is a self-contained conjugation, unlike な-adjectives.",
  },
  {
    title: "な-Adjectives",
    vocab: [
      ["きれい(な)", "kirei (na)", "pretty / clean"],
      ["げんき(な)", "genki (na)", "energetic / well"],
      ["しずか(な)", "shizuka (na)", "quiet"],
      ["ゆうめい(な)", "yuumei (na)", "famous"],
      ["べんり(な)", "benri (na)", "convenient"],
      ["すき(な)", "suki (na)", "likeable / favorite"],
    ],
    examples: [
      [
        "ここは しずかな こうえんです。",
        "Koko wa shizukana kouen desu.",
        "This is a quiet park.",
      ],
      ["げんきですか。", "Genki desu ka.", "Are you doing well?"],
    ],
    note: "な-adjectives need な before a noun (しずかな こうえん = 'quiet park') but drop it before です — the opposite pattern from い-adjectives, which never need な.",
  },
  {
    title: "Food Vocabulary",
    vocab: [
      ["ごはん", "gohan", "rice / meal"],
      ["みず", "mizu", "water"],
      ["にく", "niku", "meat"],
      ["やさい", "yasai", "vegetables"],
      ["くだもの", "kudamono", "fruit"],
      ["たまご", "tamago", "egg"],
    ],
    examples: [
      [
        "やさいを たくさん たべます。",
        "Yasai wo takusan tabemasu.",
        "I eat a lot of vegetables.",
      ],
      ["みずを ください。", "Mizu wo kudasai.", "Water, please."],
    ],
    note: "ごはん literally means 'cooked rice' but is also used generally to mean 'meal' — asking ごはんを たべましたか can simply mean 'have you eaten?'",
  },
  {
    title: "Ordering at a Restaurant",
    vocab: [
      ["メニュー", "menyuu", "menu"],
      ["ちゅうもん", "chuumon", "order"],
      ["〜を おねがいします", "~ wo onegaishimasu", "~, please"],
      [
        "おすすめは なんですか",
        "osusume wa nan desu ka",
        "what do you recommend?",
      ],
      ["おかいけい", "okaikei", "the bill"],
      ["ごちそうさまでした", "gochisousama deshita", "thank you for the meal"],
    ],
    examples: [
      ["すしを おねがいします。", "Sushi wo onegaishimasu.", "Sushi, please."],
      [
        "おかいけいを おねがいします。",
        "Okaikei wo onegaishimasu.",
        "The bill, please.",
      ],
    ],
    note: "〜をおねがいします is a versatile polite phrase for requesting almost anything, from food to services — more common in shops and restaurants than 〜をください。",
  },
  {
    title: "Shopping Phrases",
    vocab: [
      ["いくらですか", "ikura desu ka", "how much is it?"],
      ["たかい", "takai", "expensive"],
      ["やすい", "yasui", "cheap"],
      ["これを ください", "kore wo kudasai", "I'll take this"],
      ["カードで", "kaado de", "by card"],
      ["げんきんで", "genkin de", "by cash"],
    ],
    examples: [
      ["これは いくらですか。", "Kore wa ikura desu ka.", "How much is this?"],
      [
        "カードで おねがいします。",
        "Kaado de onegaishimasu.",
        "By card, please.",
      ],
    ],
    note: "で here marks the means of payment, the same particle used for 'by train' or 'with a pen' — one particle covering many kinds of 'method'.",
  },
  {
    title: "Asking for Directions",
    vocab: [
      ["えきは どこですか", "eki wa doko desu ka", "where is the station?"],
      ["まっすぐ", "massugu", "straight ahead"],
      ["みぎ", "migi", "right"],
      ["ひだり", "hidari", "left"],
      ["ちかい", "chikai", "near"],
      ["とおい", "tooi", "far"],
    ],
    examples: [
      ["えきは どこですか。", "Eki wa doko desu ka.", "Where is the station?"],
      [
        "まっすぐ いって ください。",
        "Massugu itte kudasai.",
        "Please go straight ahead.",
      ],
    ],
    note: "どこ ('where') pairs naturally with です か to form simple location questions — a pattern that extends to だれ ('who'), なに ('what'), and いつ ('when')。",
  },
  {
    title: "Transportation",
    vocab: [
      ["でんしゃ", "densha", "train"],
      ["バス", "basu", "bus"],
      ["ひこうき", "hikouki", "airplane"],
      ["くるま", "kuruma", "car"],
      ["じてんしゃ", "jitensha", "bicycle"],
      ["えき", "eki", "station"],
    ],
    examples: [
      [
        "でんしゃで がっこうに いきます。",
        "Densha de gakkou ni ikimasu.",
        "I go to school by train.",
      ],
      ["じてんしゃが すきです。", "Jitensha ga suki desu.", "I like bicycles."],
    ],
    note: "で marks the method of transportation, so 'by train/bus/car' is always mode + で in Japanese, following the same pattern used for tools and payment methods.",
  },
  {
    title: "Weather",
    vocab: [
      ["てんき", "tenki", "weather"],
      ["はれ", "hare", "sunny"],
      ["あめ", "ame", "rain"],
      ["くもり", "kumori", "cloudy"],
      ["ゆき", "yuki", "snow"],
      ["かぜ", "kaze", "wind"],
    ],
    examples: [
      [
        "きょうは いい てんきですね。",
        "Kyou wa ii tenki desu ne.",
        "The weather is nice today, isn't it?",
      ],
      ["あしたは あめです。", "Ashita wa ame desu.", "It will rain tomorrow."],
    ],
    note: "ね at the end of a sentence invites agreement, similar to 'isn't it?' in English — commonly used when commenting on the weather.",
  },
  {
    title: "The Four Seasons",
    vocab: [
      ["はる", "haru", "spring"],
      ["なつ", "natsu", "summer"],
      ["あき", "aki", "autumn"],
      ["ふゆ", "fuyu", "winter"],
      ["きせつ", "kisetsu", "season"],
      ["いちばん すきな きせつ", "ichiban sukina kisetsu", "favorite season"],
    ],
    examples: [
      [
        "はるが いちばん すきです。",
        "Haru ga ichiban suki desu.",
        "I like spring the best.",
      ],
      ["ふゆは さむいです。", "Fuyu wa samui desu.", "Winter is cold."],
    ],
    note: "いちばん means 'number one / most' and combines with adjectives to express superlatives, as in いちばん すき ('like the best')。",
  },
  {
    title: "Body Parts",
    vocab: [
      ["あたま", "atama", "head"],
      ["め", "me", "eye"],
      ["みみ", "mimi", "ear"],
      ["て", "te", "hand"],
      ["あし", "ashi", "foot / leg"],
      ["おなか", "onaka", "stomach"],
    ],
    examples: [
      ["あたまが いたいです。", "Atama ga itai desu.", "My head hurts."],
      ["てを あらいます。", "Te wo araimasu.", "I wash my hands."],
    ],
    note: "To describe pain or discomfort, use 〜が いたいです ('~ hurts'), placing the body part before が rather than using a separate verb like 'hurt'.",
  },
  {
    title: "Daily Routine",
    vocab: [
      ["おきます", "okimasu", "wake up"],
      ["ねます", "nemasu", "sleep / go to bed"],
      ["シャワーを あびます", "shawaa wo abimasu", "take a shower"],
      ["はを みがきます", "ha wo migakimasu", "brush teeth"],
      ["でかけます", "dekakemasu", "go out"],
      ["かえります", "kaerimasu", "return home"],
    ],
    examples: [
      [
        "まいあさ しちじに おきます。",
        "Maiasa shichi-ji ni okimasu.",
        "I wake up at 7 every morning.",
      ],
      [
        "よる じゅういちじに ねます。",
        "Yoru juuichi-ji ni nemasu.",
        "I go to bed at 11 at night.",
      ],
    ],
    note: "に after a specific clock time marks 'at' that time, but is dropped after relative time words like きょう ('today') or まいあさ ('every morning')。",
  },
  {
    title: "Hobbies & Free Time",
    vocab: [
      ["しゅみ", "shumi", "hobby"],
      ["おんがくを ききます", "ongaku wo kikimasu", "listen to music"],
      ["ほんを よみます", "hon wo yomimasu", "read books"],
      ["えいがを みます", "eiga wo mimasu", "watch movies"],
      ["スポーツを します", "supootsu wo shimasu", "play sports"],
      ["りょこうします", "ryokou shimasu", "travel"],
    ],
    examples: [
      [
        "わたしの しゅみは どくしょです。",
        "Watashi no shumi wa dokusho desu.",
        "My hobby is reading.",
      ],
      [
        "しゅうまつに えいがを みます。",
        "Shuumatsu ni eiga wo mimasu.",
        "I watch movies on weekends.",
      ],
    ],
    note: "します ('to do') is one of the most flexible verbs in Japanese, pairing with countless nouns like スポーツ, べんきょう, and りょこう to form new verb phrases.",
  },
  {
    title: "School Vocabulary",
    vocab: [
      ["がっこう", "gakkou", "school"],
      ["せんせい", "sensei", "teacher"],
      ["きょうしつ", "kyoushitsu", "classroom"],
      ["しゅくだい", "shukudai", "homework"],
      ["テスト", "tesuto", "test"],
      ["じゅぎょう", "jugyou", "class / lesson"],
    ],
    examples: [
      ["しゅくだいを します。", "Shukudai wo shimasu.", "I do homework."],
      [
        "せんせいは やさしいです。",
        "Sensei wa yasashii desu.",
        "The teacher is kind.",
      ],
    ],
    note: "せんせい is used both as a job title and a respectful term of address — never attach さん to it, since せんせい already carries built-in respect。",
  },
  {
    title: "Work & Jobs",
    vocab: [
      ["しごと", "shigoto", "job / work"],
      ["かいしゃ", "kaisha", "company"],
      ["かいしゃいん", "kaishain", "company employee"],
      ["いしゃ", "isha", "doctor"],
      ["エンジニア", "enjinia", "engineer"],
      ["やすみ", "yasumi", "day off"],
    ],
    examples: [
      [
        "わたしの しごとは エンジニアです。",
        "Watashi no shigoto wa enjinia desu.",
        "My job is engineer.",
      ],
      ["きょうは やすみです。", "Kyou wa yasumi desu.", "Today is a day off."],
    ],
    note: "Job titles typically follow the pattern わたしの しごとは 〜です, mirroring the same self-introduction structure used for names and hobbies。",
  },
  {
    title: "Animals",
    vocab: [
      ["いぬ", "inu", "dog"],
      ["ねこ", "neko", "cat"],
      ["とり", "tori", "bird"],
      ["さかな", "sakana", "fish"],
      ["うさぎ", "usagi", "rabbit"],
      ["ぞう", "zou", "elephant"],
    ],
    examples: [
      ["ねこが すきです。", "Neko ga suki desu.", "I like cats."],
      ["とりが とんでいます。", "Tori ga tonde imasu.", "A bird is flying."],
    ],
    note: "For animals and people, いる (not ある) is used to describe existence: ねこが います ('there is a cat') — the いる/ある distinction marks animate vs inanimate things。",
  },
  {
    title: "Emotions & Feelings",
    vocab: [
      ["うれしい", "ureshii", "happy"],
      ["かなしい", "kanashii", "sad"],
      ["たのしい", "tanoshii", "fun / enjoyable"],
      ["こわい", "kowai", "scary"],
      ["しんぱい", "shinpai", "worried"],
      ["びっくりしました", "bikkuri shimashita", "was surprised"],
    ],
    examples: [
      [
        "きょうは とても たのしかったです。",
        "Kyou wa totemo tanoshikatta desu.",
        "Today was very fun.",
      ],
      [
        "しんぱいしないで ください。",
        "Shinpai shinaide kudasai.",
        "Please don't worry.",
      ],
    ],
    note: "い-adjectives conjugate into the past by dropping い and adding かった: たのしい → たのしかった ('was fun'), following the same pattern for negation and past tense。",
  },
  {
    title: "Polite Requests (~てください)",
    vocab: [
      ["まってください", "matte kudasai", "please wait"],
      ["みてください", "mite kudasai", "please look"],
      ["いってください", "itte kudasai", "please go / say"],
      ["たすけてください", "tasukete kudasai", "please help"],
      ["きいてください", "kiite kudasai", "please listen / ask"],
      ["みせてください", "misete kudasai", "please show me"],
    ],
    examples: [
      [
        "ちょっと まってください。",
        "Chotto matte kudasai.",
        "Please wait a moment.",
      ],
      [
        "これを みせてください。",
        "Kore wo misete kudasai.",
        "Please show me this.",
      ],
    ],
    note: "The て-form of a verb plus ください forms a polite request. It's one of the most useful patterns in beginner Japanese — the て-form itself unlocks many other grammar points too。",
  },
  {
    title: "Counting Objects (Counters)",
    vocab: [
      ["〜こ", "~ko", "general counter (small objects)"],
      ["〜まい", "~mai", "flat objects (paper, tickets)"],
      ["〜ひき", "~hiki", "small animals"],
      ["〜にん", "~nin", "people"],
      ["〜さつ", "~satsu", "bound objects (books)"],
      ["〜ほん", "~hon", "long thin objects"],
    ],
    examples: [
      [
        "りんごを ふたつ ください。",
        "Ringo wo futatsu kudasai.",
        "Two apples, please.",
      ],
      [
        "ほんを さんさつ かいました。",
        "Hon wo san-satsu kaimashita.",
        "I bought three books.",
      ],
    ],
    note: "Japanese requires a different counter word depending on the shape or category of what's being counted — one of the trickier features for beginners, best learned a few counters at a time。",
  },
  {
    title: "Making Comparisons",
    vocab: [
      ["〜より", "~yori", "than ~"],
      ["〜のほうが", "~ no hou ga", "~ is more"],
      ["いちばん", "ichiban", "the most"],
      ["おなじ", "onaji", "the same"],
      ["〜ほど〜ない", "~ hodo ~nai", "not as ~ as"],
      [
        "どちらが すきですか",
        "dochira ga suki desu ka",
        "which do you like better?",
      ],
    ],
    examples: [
      [
        "いぬのほうが ねこより すきです。",
        "Inu no hou ga neko yori suki desu.",
        "I like dogs more than cats.",
      ],
      [
        "これが いちばん おいしいです。",
        "Kore ga ichiban oishii desu.",
        "This is the most delicious.",
      ],
    ],
    note: "Comparisons use 〜より ('than') alongside 〜のほうが ('~ is more'), placed on the item being favored — the sentence structure differs noticeably from the English 'more ~ than'。",
  },
  {
    title: "Making Plans & Invitations",
    vocab: [
      ["いっしょに", "issho ni", "together"],
      ["〜ませんか", "~masen ka", "won't you ~? (invitation)"],
      ["〜ましょう", "~mashou", "let's ~"],
      ["よてい", "yotei", "plan / schedule"],
      ["ひま", "hima", "free time"],
      ["やくそく", "yakusoku", "promise / appointment"],
    ],
    examples: [
      [
        "いっしょに えいがを みませんか。",
        "Issho ni eiga wo mimasen ka.",
        "Won't you watch a movie together with me?",
      ],
      ["こんど あいましょう。", "Kondo aimashou.", "Let's meet next time."],
    ],
    note: "〜ませんか is a soft, polite way to invite someone by asking a negative question ('won't you ~?'), which feels less pushy in Japanese than a direct suggestion。",
  },
  {
    title: "Basic Kanji: Numbers & Days",
    vocab: [
      ["一", "ichi", "one"],
      ["二", "ni", "two"],
      ["三", "san", "three"],
      ["日", "hi / nichi", "day / sun"],
      ["月", "tsuki / getsu", "moon / month"],
      ["人", "hito / jin", "person"],
    ],
    examples: [
      ["一月一日", "ichigatsu tsuitachi", "January 1st"],
      [
        "三人の ひとが きました。",
        "San-nin no hito ga kimashita.",
        "Three people came.",
      ],
    ],
    note: "These six kanji appear constantly across dates, counting, and everyday words — a solid foundation before moving on to more complex characters。",
  },
].map((lesson, index) => ({
  id: index + 1,
  title: lesson.title,
  level: "Beginner",
  vocab: lesson.vocab,
  examples: lesson.examples,
  note: lesson.note,
}));
