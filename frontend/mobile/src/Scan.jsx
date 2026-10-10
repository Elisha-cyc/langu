// mobile/src/Scan.jsx
import React, { useRef, useState, useEffect } from "react";
import {
  View,
  Text,
  Image,
  ScrollView,
  ActivityIndicator,
  Alert,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import { createAudioPlayer, setAudioModeAsync } from "expo-audio";
import { post, upload, audioUrl, flatten } from "./api";
import { s, Btn, C } from "./ui";

export default function Scan({ profile, onBack }) {
  const [busy, setBusy] = useState(false);
  const [image, setImage] = useState(null); // picked but not yet scanned
  const [scan, setScan] = useState(null); // { text, audio, lesson }
  const [extra, setExtra] = useState("");
  const player = useRef(null);

  const stop = () => {
    try {
      player.current?.remove();
    } catch (e) {}
    player.current = null;
  };
  useEffect(() => stop, []);

  const play = async (a) => {
    const u = audioUrl(a);
    if (!u) return;
    stop();
    await setAudioModeAsync({ playsInSilentMode: true });
    const p = createAudioPlayer({ uri: u });
    player.current = p;
    p.play();
  };

  // Camera / Gallery: just pick the image and show a preview — matches
  // the web page's "Open Camera" and "Upload Image" buttons, which
  // don't scan yet either.
  const pick = async (camera) => {
    const perm = camera
      ? await ImagePicker.requestCameraPermissionsAsync()
      : await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!perm.granted)
      return Alert.alert(
        "Permission needed",
        "Please allow access in your phone settings.",
      );
    const r = camera
      ? await ImagePicker.launchCameraAsync({ quality: 0.8 })
      : await ImagePicker.launchImageLibraryAsync({ quality: 0.8 });
    if (r.canceled) return;
    setScan(null);
    setExtra("");
    stop();
    setImage(r.assets[0]);
  };

  // Generate: the third, separate action — uploads the picked image and
  // runs the AI teacher on it. Matches the web page's
  // "✨ Scan & Start AI Teacher" button.
  const generateLesson = async () => {
    if (!image) return Alert.alert("Please choose or capture an image first.");
    setBusy(true);
    try {
      const form = new FormData();
      form.append("image", {
        uri: image.uri,
        name: "page.jpg",
        type: "image/jpeg",
      });
      form.append("language", profile.learning_language);
      form.append("target_language", profile.native_language);
      form.append("learner_level", profile.learner_level);
      const res = await upload("/scan", form);
      setScan({
        text: res.page_text || "",
        audio: res.audio,
        lesson: res.lesson,
      });
      play(res.audio); // the passage is read aloud as soon as scanning finishes
    } catch (e) {
      if (!e.isCanceled) Alert.alert("Scan failed", e.message);
    }
    setBusy(false);
  };

  const ask = async (mode) => {
    setBusy(true);
    try {
      const r = await post("/text/summarize", {
        text: scan.text,
        mode,
        language: profile.learning_language,
        target_language: profile.native_language,
        learner_level: profile.learner_level,
      });
      setExtra(r.result);
    } catch (e) {
      if (!e.isCanceled) Alert.alert("Couldn't get " + mode, e.message);
    }
    setBusy(false);
  };

  return (
    <View style={s.screen}>
      <Btn
        t="← Back"
        alt
        onPress={() => {
          stop();
          onBack();
        }}
      />
      <Text style={s.h1}>Scan a page</Text>

      {image && !scan && (
        <Image
          source={{ uri: image.uri }}
          style={{
            width: "100%",
            height: 220,
            borderRadius: 12,
            marginBottom: 12,
          }}
          resizeMode="cover"
        />
      )}

      <View style={s.row}>
        <Btn t="📷 Camera" disabled={busy} onPress={() => pick(true)} />
        <Btn t="🖼 Gallery" alt disabled={busy} onPress={() => pick(false)} />
      </View>

      <Btn
        t={busy ? "🤖 Scanning & Reading Page…" : "✨ Scan & Start AI Teacher"}
        disabled={!image || busy}
        onPress={generateLesson}
      />

      {busy && <ActivityIndicator color={C.accent} style={{ margin: 12 }} />}
      {scan && (
        <>
          <View style={s.row}>
            <Btn t="🔊 Read again" alt onPress={() => play(scan.audio)} />
            <Btn
              t="Summary"
              alt
              disabled={busy}
              onPress={() => ask("summary")}
            />
            <Btn
              t="Key points"
              alt
              disabled={busy}
              onPress={() => ask("key_points")}
            />
            <Btn
              t="Lesson"
              alt
              onPress={() => setExtra(flatten(scan.lesson))}
            />
          </View>
          <ScrollView style={s.card}>
            <Text style={[s.body, { fontWeight: "700" }]}>Passage</Text>
            <Text style={s.body}>{scan.text}</Text>
            {!!extra && (
              <Text style={[s.body, { marginTop: 16 }]}>{extra}</Text>
            )}
          </ScrollView>
        </>
      )}
    </View>
  );
}
