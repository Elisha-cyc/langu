// mobile/src/picker.jsx
import React, { useState } from "react";
import { Modal, View, Text, TouchableOpacity, FlatList } from "react-native";
import { C, s } from "./ui";

export default function Picker({ label, value, options, onChange }) {
  const [open, setOpen] = useState(false);
  return (
    <View>
      <Text style={s.p}>{label}</Text>
      <TouchableOpacity
        style={[
          s.input,
          { flexDirection: "row", justifyContent: "space-between" },
        ]}
        onPress={() => setOpen(true)}
      >
        <Text style={{ color: C.text }}>{value}</Text>
        <Text style={{ color: C.mute }}>▼</Text>
      </TouchableOpacity>
      <Modal
        visible={open}
        transparent
        animationType="slide"
        onRequestClose={() => setOpen(false)}
      >
        <TouchableOpacity
          style={{ flex: 1, backgroundColor: "#000a" }}
          activeOpacity={1}
          onPress={() => setOpen(false)}
        >
          <View
            style={{
              marginTop: "auto",
              backgroundColor: C.card,
              borderTopLeftRadius: 20,
              borderTopRightRadius: 20,
              maxHeight: "60%",
              padding: 12,
            }}
          >
            <FlatList
              data={options}
              keyExtractor={(o) => o}
              renderItem={({ item }) => (
                <TouchableOpacity
                  onPress={() => {
                    onChange(item);
                    setOpen(false);
                  }}
                  style={{ padding: 14 }}
                >
                  <Text
                    style={{
                      color: item === value ? C.accent : C.text,
                      fontSize: 17,
                      fontWeight: item === value ? "700" : "400",
                    }}
                  >
                    {item}
                  </Text>
                </TouchableOpacity>
              )}
            />
          </View>
        </TouchableOpacity>
      </Modal>
    </View>
  );
}
