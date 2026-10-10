// mobile/src/ui.js
import React from "react";
import { Text, TouchableOpacity, StyleSheet } from "react-native";
export const C = { bg: "#0f172a", card: "#1e293b", accent: "#6366f1", text: "#f1f5f9", mute: "#94a3b8" };
export const s = StyleSheet.create({
  screen: { flex: 1, backgroundColor: C.bg, padding: 16, paddingTop: 48 },
  h1: { color: C.text, fontSize: 26, fontWeight: "700" },
  p: { color: C.mute, marginVertical: 4 },
  body: { color: C.text, fontSize: 16, lineHeight: 25 },
  card: { backgroundColor: C.card, borderRadius: 14, padding: 14, marginVertical: 6 },
  input: { backgroundColor: C.card, color: C.text, borderRadius: 10, padding: 12, marginVertical: 6 },
  row: { flexDirection: "row", flexWrap: "wrap" },
});
export const Btn = ({ t, onPress, alt, disabled }) => (
  <TouchableOpacity disabled={disabled} onPress={onPress}
    style={{ backgroundColor: alt ? C.card : C.accent, padding: 12, borderRadius: 10, margin: 3, opacity: disabled ? 0.5 : 1, flexGrow: 1 }}>
    <Text style={{ color: C.text, textAlign: "center", fontWeight: "600" }}>{t}</Text>
  </TouchableOpacity>
);
