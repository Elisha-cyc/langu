// mobile/src/Library.jsx
import React, { useEffect, useState, useCallback } from "react";
import {
  View,
  Text,
  ScrollView,
  ActivityIndicator,
  Alert,
  TextInput,
} from "react-native";
import * as DocumentPicker from "expo-document-picker";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { get, post, upload } from "./api";
import { s, Btn, C } from "./ui";

const TOPICS = [
  "Greetings",
  "Introducing Yourself",
  "Numbers 1–10",
  "Numbers 11–100",
  "Days of the Week",
  "Months of the Year",
  "Telling Time",
  "Family Members",
  "Colors",
  "Basic Adjectives",
  "Alphabet and Sounds",
  "Pronunciation Basics",
  "Common Nouns",
  "Pronouns",
  "Yes/No Questions",
  "Question Words",
  "Present Tense Verbs",
  "Past Tense Verbs",
  "Future Tense",
  "Negative Sentences",
  "This and That",
  "Prepositions of Place",
  "Food Vocabulary",
  "Ordering at a Restaurant",
  "Shopping Phrases",
  "Asking for Directions",
  "Transportation",
  "Weather",
  "The Four Seasons",
  "Body Parts",
  "Daily Routine",
  "Hobbies and Free Time",
  "School Vocabulary",
  "Work and Jobs",
  "Animals",
  "Emotions and Feelings",
  "Polite Requests",
  "Counting Objects",
  "Making Comparisons",
  "Making Plans and Invitations",
  "At the Hotel",
  "At the Doctor",
  "At the Airport",
  "Talking on the Phone",
  "Describing People",
  "Describing Places",
  "Giving Opinions",
  "Telling a Story",
  "Common Idioms",
  "Everyday Conversation",
];

export default function Library({ profile, onOpen, onEdit, onScan }) {
  const [tab, setTab] = useState("official");
  const [data, setData] = useState({
    official_books: [],
    my_books: [],
    native_books: [],
  });
  const [busy, setBusy] = useState(true);

  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);
  const [searching, setSearching] = useState(false);
  const [note, setNote] = useState("");
  const [adding, setAdding] = useState(null);
  const [saved, setSaved] = useState([]); // downloaded online books

  const language = profile?.learning_language || "";

  const load = useCallback(async () => {
    try {
      const id = await AsyncStorage.getItem("user_id");
      setData(await get("/library?user_id=" + id));
    } catch (e) {
      if (!e.isCanceled) Alert.alert("Library error", e.message);
    }
    setBusy(false);
  }, []);
  useEffect(() => {
    load();
  }, [load]);

  // Downloaded online books come from the server, so they are still there
  // after you close the app (they used to live only in memory).
  const loadSaved = useCallback(async () => {
    try {
      const r = await get(
        "/library/online/saved?language=" + encodeURIComponent(language),
      );
      setSaved(r.results || []);
    } catch (e) {}
  }, [language]);

  useEffect(() => {
    if (tab === "native") loadSaved();
  }, [tab, loadSaved]);

  const importPdf = async () => {
    const r = await DocumentPicker.getDocumentAsync({
      type: [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      ],
    });
    if (r.canceled) return;
    try {
      setBusy(true);
      const a = r.assets[0];
      const form = new FormData();
      form.append("book", {
        uri: a.uri,
        name: a.name,
        type: a.mimeType || "application/pdf",
      });
      await upload("/library/import", form);
      await load();
      setTab("my");
    } catch (e) {
      if (!e.isCanceled) Alert.alert("Import failed", e.message);
      setBusy(false);
    }
  };

  const searchOnline = async () => {
    setSearching(true);
    setResults(null);
    setNote("");
    try {
      const q = query.trim()
        ? "&query=" + encodeURIComponent(query.trim())
        : "";
      const r = await get(
        "/library/online/search?language=" + encodeURIComponent(language) + q,
      );
      setResults(r.results || []);
      if (r.note) setNote(r.note);
      else if (!r.results?.length)
        setNote("No " + language + " books found. Try a different search.");
    } catch (e) {
      if (!e.isCanceled) Alert.alert("Search failed", e.message);
    }
    setSearching(false);
  };

  const addOnline = async (book) => {
    setAdding(book.gutenberg_id);
    try {
      await post(
        "/library/online/add",
        {
          gutenberg_id: book.gutenberg_id,
          title: book.title,
          author: book.author,
          language,
        },
        120000,
      );
      await loadSaved();
    } catch (e) {
      if (!e.isCanceled) Alert.alert("Couldn't add book", e.message);
    }
    setAdding(null);
  };

  // Downloaded books open by file name like every other book.
  const openSaved = async (b, mode) => {
    try {
      const book = await post(
        "/library/online/add",
        {
          gutenberg_id: b.gutenberg_id,
          title: b.title,
          author: b.author,
          language,
        },
        120000,
      );
      onOpen({ book, kind: "user", mode });
    } catch (e) {
      if (!e.isCanceled) Alert.alert("Couldn't open book", e.message);
    }
  };

  const openNative = async (b, mode) => {
    try {
      const book = await post("/library/native/open", {
        file_name: b.file_name,
        language,
      });
      onOpen({ book, kind: "user", mode });
    } catch (e) {
      if (!e.isCanceled) Alert.alert("Couldn't open book", e.message);
    }
  };

  const course =
    (data.official_books || []).length > 0
      ? data.official_books
      : TOPICS.map((title, i) => ({
          id: i + 1,
          title,
          level: profile?.learner_level,
        }));

  const list = (tab === "official" ? course : data.my_books) || [];
  const kind = tab === "official" ? "official" : "user";

  return (
    <ScrollView style={s.screen}>
      <Text style={s.h1}>Library</Text>
      <Text style={s.p}>
        {profile?.learning_language} • {profile?.learner_level} • explained in{" "}
        {profile?.native_language}
      </Text>
      <Btn t="⚙ Change language / level" alt onPress={onEdit} />
      <View style={s.row}>
        <Btn
          t="Course"
          alt={tab !== "official"}
          onPress={() => setTab("official")}
        />
        <Btn
          t={(language || "Native") + " Books"}
          alt={tab !== "native"}
          onPress={() => setTab("native")}
        />
        <Btn t="My Books" alt={tab !== "my"} onPress={() => setTab("my")} />
      </View>

      {tab === "my" && (
        <View style={s.row}>
          <Btn t="＋ Import PDF / DOCX" onPress={importPdf} />
          <Btn t="📷 Scan a page" onPress={onScan} />
        </View>
      )}

      {tab === "native" && (
        <View>
          {(data.native_books || []).length > 0 && (
            <>
              <Text style={[s.p, { marginTop: 8 }]}>On this server</Text>
              {data.native_books.map((b) => (
                <View key={b.file_name} style={s.card}>
                  <Text style={[s.body, { fontWeight: "700" }]}>{b.title}</Text>
                  <Text style={s.p}>
                    {b.type} • {b.size_kb} KB
                  </Text>
                  <View style={s.row}>
                    <Btn t="Study" onPress={() => openNative(b, "study")} />
                    <Btn
                      t="😴 Sleep"
                      alt
                      onPress={() => openNative(b, "sleep")}
                    />
                  </View>
                </View>
              ))}
            </>
          )}

          {saved.length > 0 && (
            <>
              <Text style={[s.p, { marginTop: 8 }]}>Downloaded</Text>
              {saved.map((b) => (
                <View key={b.gutenberg_id} style={s.card}>
                  <Text style={[s.body, { fontWeight: "700" }]}>{b.title}</Text>
                  <Text style={s.p}>{b.author || b.size_kb + " KB"}</Text>
                  <View style={s.row}>
                    <Btn t="Study" onPress={() => openSaved(b, "study")} />
                    <Btn
                      t="😴 Sleep"
                      alt
                      onPress={() => openSaved(b, "sleep")}
                    />
                  </View>
                </View>
              ))}
            </>
          )}

          <Text style={[s.p, { marginTop: 8 }]}>
            Free public-domain books in {language}, from Project Gutenberg.
          </Text>
          <View style={s.row}>
            <TextInput
              style={[s.input, { flex: 1 }]}
              placeholder="Search by title or author (optional)"
              placeholderTextColor={C.mute}
              value={query}
              onChangeText={setQuery}
              onSubmitEditing={searchOnline}
            />
            <Btn
              t={searching ? "Searching…" : "Search"}
              disabled={searching}
              onPress={searchOnline}
            />
          </View>

          {searching && (
            <ActivityIndicator color={C.accent} style={{ margin: 16 }} />
          )}
          {!!note && <Text style={s.p}>{note}</Text>}

          {(results || []).map((r) => (
            <View key={r.gutenberg_id} style={s.card}>
              <Text style={[s.body, { fontWeight: "700" }]}>{r.title}</Text>
              <Text style={s.p}>{r.author}</Text>
              <Btn
                t={adding === r.gutenberg_id ? "Adding…" : "＋ Download"}
                disabled={adding === r.gutenberg_id}
                onPress={() => addOnline(r)}
              />
            </View>
          ))}
        </View>
      )}

      {tab !== "native" && (
        <>
          {busy && (
            <ActivityIndicator color={C.accent} style={{ margin: 20 }} />
          )}
          {!busy && list.length === 0 && (
            <Text style={s.p}>Nothing here yet.</Text>
          )}
          {list.map((b, i) => (
            <View key={b.file_name || b.id || i} style={s.card}>
              <Text style={[s.body, { fontWeight: "700" }]}>{b.title}</Text>
              <Text style={s.p}>{b.level || b.type || ""}</Text>
              <View style={s.row}>
                <Btn
                  t="Study"
                  onPress={() => onOpen({ book: b, kind, mode: "study" })}
                />
                <Btn
                  t="😴 Sleep"
                  alt
                  onPress={() => onOpen({ book: b, kind, mode: "sleep" })}
                />
              </View>
            </View>
          ))}
        </>
      )}
    </ScrollView>
  );
}
