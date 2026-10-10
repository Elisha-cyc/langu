// frontend/mobile/App.js
import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  TextInput,
  ScrollView,
  ActivityIndicator,
  Alert,
} from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { setBase, post, put } from "./src/api";
import { s, Btn, C } from "./src/ui";
import Library from "./src/Library";
import Reader from "./src/Reader";
import Scan from "./src/Scan";
import Picker from "./src/picker";
import Sleep from "./src/Sleep";

const LEARN = [
  "Arabic",
  "Chinese",
  "Dutch",
  "French",
  "German",
  "Greek",
  "Hebrew",
  "Hindi",
  "Italian",
  "Japanese",
  "Korean",
  "Polish",
  "Portuguese",
  "Russian",
  "Spanish",
  "Swedish",
  "Thai",
  "Turkish",
  "Twi",
  "Vietnamese",
];
const NATIVE = ["English", ...LEARN];
const LEVELS = ["Beginner", "Intermediate", "Advanced"];

export default function App() {
  const [screen, setScreen] = useState("boot");
  const [profile, setProfile] = useState(null);
  const [open, setOpen] = useState(null);
  const [busy, setBusy] = useState(false);
  const [f, setF] = useState({
    server: "http://172.20.10.3:5000",
    name: "",
    native_language: "English",
    learning_language: "Japanese",
    learner_level: "Beginner",
  });

  useEffect(() => {
    (async () => {
      try {
        const server = await AsyncStorage.getItem("server");
        const saved = await AsyncStorage.getItem("profile");
        if (server && saved) {
          const p = JSON.parse(saved);
          setBase(server);
          setProfile(p);
          setF({
            server,
            name: p.name,
            native_language: p.native_language,
            learning_language: p.learning_language,
            learner_level: p.learner_level,
          });
          setScreen("library");
          return;
        }
      } catch (e) {}
      setScreen("setup");
    })();
  }, []);

  // First setup creates the user. Changing language / level later UPDATES the
  // same user (it used to create a brand new one and lose all progress).
  const save = async () => {
    if (!f.name.trim()) return Alert.alert("Please enter your name");
    if (f.native_language === f.learning_language)
      return Alert.alert("Choose two different languages");
    setBusy(true);
    try {
      setBase(f.server);
      const body = {
        name: f.name.trim(),
        native_language: f.native_language,
        learning_language: f.learning_language,
        learner_level: f.learner_level,
      };

      let id;
      if (profile?.id != null) {
        await put("/profile/" + profile.id, body);
        id = profile.id;
      } else {
        const p = await post("/profile", body);
        id = p.id ?? p.user_id ?? p.profile?.id;
        if (id == null)
          throw new Error("Unexpected server reply: " + JSON.stringify(p));
      }

      const prof = { ...body, id };
      await AsyncStorage.setItem("server", f.server.trim());
      await AsyncStorage.setItem("user_id", String(id));
      await AsyncStorage.setItem("profile", JSON.stringify(prof));
      setProfile(prof);
      setScreen("library");
    } catch (e) {
      Alert.alert("Couldn't save", e.message);
    }
    setBusy(false);
  };

  const openBook = ({ book, kind, mode }) => setOpen({ book, kind, mode });

  if (screen === "boot")
    return (
      <View style={s.screen}>
        <ActivityIndicator color={C.accent} />
      </View>
    );

  if (screen === "setup")
    return (
      <ScrollView style={s.screen}>
        <Text style={s.h1}>
          {profile ? "Change language / level" : "Welcome to Lingua AI"}
        </Text>
        <Text style={s.p}>
          Server address (your computer's IP, same network)
        </Text>
        <TextInput
          style={s.input}
          value={f.server}
          autoCapitalize="none"
          autoCorrect={false}
          keyboardType="url"
          onChangeText={(v) => setF({ ...f, server: v })}
        />
        <TextInput
          style={s.input}
          placeholder="Your name"
          placeholderTextColor={C.mute}
          value={f.name}
          onChangeText={(v) => setF({ ...f, name: v })}
        />
        <Picker
          label="Your native language"
          value={f.native_language}
          options={NATIVE}
          onChange={(v) => setF({ ...f, native_language: v })}
        />
        <Picker
          label="Language you want to learn"
          value={f.learning_language}
          options={LEARN}
          onChange={(v) => setF({ ...f, learning_language: v })}
        />
        <Picker
          label="Level"
          value={f.learner_level}
          options={LEVELS}
          onChange={(v) => setF({ ...f, learner_level: v })}
        />
        {(f.native_language === "Twi" || f.learning_language === "Twi") && (
          <Text style={[s.p, { color: C.accent }]}>
            ℹ️ The AI cannot teach or explain in Twi yet. Twi lessons use the
            built-in curriculum and explanations are given in English.
          </Text>
        )}
        <View style={{ height: 8 }} />
        <Btn
          t={busy ? "Saving…" : profile ? "Save" : "Start learning"}
          disabled={busy}
          onPress={save}
        />
        {profile && <Btn t="Cancel" alt onPress={() => setScreen("library")} />}
      </ScrollView>
    );

  if (screen === "scan")
    return <Scan profile={profile} onBack={() => setScreen("library")} />;

  if (open)
    return open.mode === "sleep" ? (
      <Sleep {...open} profile={profile} onBack={() => setOpen(null)} />
    ) : (
      <Reader {...open} profile={profile} onBack={() => setOpen(null)} />
    );

  return (
    <Library
      key={profile?.id}
      profile={profile}
      onOpen={openBook}
      onEdit={() => setScreen("setup")}
      onScan={() => setScreen("scan")}
    />
  );
}
