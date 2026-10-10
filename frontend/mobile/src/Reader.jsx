// mobile/src/Reader.jsx
import React, { useEffect, useRef, useState } from "react";
import { View, Text, ScrollView, ActivityIndicator, Alert } from "react-native";
import { createAudioPlayer, setAudioModeAsync } from "expo-audio";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { post, audioUrl } from "./api";
import { s, Btn, C } from "./ui";

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

const normalize = (c) => {
  if (Array.isArray(c?.steps) && c.steps.length)
    return c.steps.map((x) => ({
      sentence: x.sentence || x.text || "",
      teaching: x.teaching || {},
    }));
  return ((c?.passage || "").match(/[^。.!?！？]+[。.!?！？]?/g) || [])
    .filter((t) => t.trim())
    .map((t) => ({ sentence: t, teaching: c?.teaching || {} }));
};

const buildLines = (st) => {
  if (!st) return [];
  const L = [{ id: "sentence", label: "Phrase", text: st.sentence }];
  const t = st.teaching || {};
  if (t.translation)
    L.push({ id: "translation", label: "Translation", text: t.translation });
  (Array.isArray(t.vocabulary) ? t.vocabulary : []).forEach((w, i) =>
    L.push({
      id: "vocab-" + i,
      label: i ? "" : "Vocabulary",
      text: w.word,
      sub: w.meaning,
    }),
  );
  if (t.grammar) L.push({ id: "grammar", label: "Grammar", text: t.grammar });
  (Array.isArray(t.examples) ? t.examples : []).forEach((e, i) =>
    L.push({
      id: "example-" + i,
      label: i ? "" : "Examples",
      text: e.sentence,
      sub: e.translation,
    }),
  );
  return L;
};

// A step is read as a list of small pieces.
const buildSegments = (st, nat, lang) => {
  const t = st.teaching || {};
  const S = [{ id: "sentence", text: st.sentence, lang, after: 500 }];

  if (t.translation)
    S.push({ id: "translation", text: t.translation, lang: nat, after: 1200 });

  (Array.isArray(t.vocabulary) ? t.vocabulary : []).forEach((w, i) =>
    S.push({
      id: "vocab-" + i,
      text: w.word + ". " + w.meaning,
      lang: nat,
      after: 900,
    }),
  );

  if (t.grammar)
    S.push({ id: "grammar", text: t.grammar, lang: nat, after: 1200 });

  (Array.isArray(t.examples) ? t.examples : []).forEach((e, i) => {
    S.push({ id: "example-" + i, text: e.sentence, lang, after: 400 });
    S.push({ id: "example-" + i, text: e.translation, lang: nat, after: 800 });
  });

  return S;
};

export default function Reader({ book, kind, profile, onBack }) {
  const key = "page:" + (book.file_name || book.id);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(1);
  const [steps, setSteps] = useState([]);
  const [idx, setIdx] = useState(0);
  const [activeId, setActiveId] = useState(null);
  const [busy, setBusy] = useState(true);
  const [running, setRunning] = useState(false);
  const [paused, setPaused] = useState(false);
  const [auto, setAuto] = useState(false);
  const [reveal, setReveal] = useState(false);
  const [notice, setNotice] = useState("");

  // Every full start gets a new number. A full stop bumps it, so any older
  // loop knows it is out of date and quits without touching the new one.
  const token = useRef(0);
  // True while the learner has paused: the audio is paused and the loop waits.
  const pausedRef = useRef(false);
  const autoRef = useRef(false);
  const player = useRef(null);
  const resolver = useRef(null);
  // The language the explanations are really written in (English when the
  // learner's native language is Twi, which the AI cannot write).
  const explain = useRef(profile.native_language);

  // Cuts the current audio for good and invalidates any running loop.
  const halt = () => {
    token.current += 1;
    pausedRef.current = false;
    const finish = resolver.current;
    resolver.current = null;
    try {
      player.current?.pause();
    } catch (e) {}
    if (finish) finish();
    try {
      player.current?.remove();
    } catch (e) {}
    player.current = null;
  };

  // Full stop: nothing is kept.
  const stop = () => {
    halt();
    setRunning(false);
    setPaused(false);
    setActiveId(null);
  };

  // Pause: the audio stops right now, even in the middle of a sentence,
  // and Resume continues from exactly that point.
  const pause = () => {
    pausedRef.current = true;
    try {
      player.current?.pause();
    } catch (e) {}
    setRunning(false);
    setPaused(true);
  };

  const resume = () => {
    pausedRef.current = false;
    try {
      player.current?.play();
    } catch (e) {}
    setPaused(false);
    setRunning(true);
  };

  const fetchPage = async (p) => {
    const common = {
      page: p,
      user_id: profile.user_id ?? profile.id ?? 1,
      language: profile.learning_language,
      target_language: profile.native_language,
      learner_level: profile.learner_level,
    };

    const r =
      kind === "official"
        ? await post(
            "/lesson/curriculum",
            { lesson_id: book.id, title: book.title, ...common },
            180000,
          )
        : await post(
            "/teach/page",
            { book: book.file_name, ...common },
            180000,
          );

    explain.current = r.explained_in || profile.native_language;
    setNotice(r.notice || "");
    return { steps: normalize(r.content), total: r.total_pages || 1 };
  };

  const loadPage = async (p) => {
    stop();
    setBusy(true);
    try {
      const d = await fetchPage(p);
      setSteps(d.steps);
      setTotal(d.total);
      setPage(p);
      setIdx(0);
      setActiveId(null);
      setReveal(false);
      await AsyncStorage.setItem(key, String(p));
    } catch (e) {
      Alert.alert("Couldn't load page", e.message);
    }
    setBusy(false);
  };

  useEffect(() => {
    (async () => {
      const v = await AsyncStorage.getItem(key);
      loadPage(v ? parseInt(v, 10) : 1);
    })();
    return () => halt();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Holds the loop here while the learner has paused.
  const holdWhilePaused = async (tok) => {
    while (pausedRef.current && tok === token.current) await wait(150);
  };

  // Plays one piece. Returns when it finishes, or on a full stop.
  const speak = async (text, lang, id, tok) => {
    if (!text || tok !== token.current) return;
    try {
      const a = await post("/audio/read", {
        text: String(text).split(" — ")[0],
        language: lang,
      });
      const u = audioUrl(a.audio);
      if (!u || tok !== token.current) return;

      // If Stop was pressed while the audio was downloading, wait here.
      await holdWhilePaused(tok);
      if (tok !== token.current) return;

      if (id) setActiveId(id);

      await new Promise((res) => {
        let done = false;
        let sub = null;
        let timer = null;
        const p = createAudioPlayer({ uri: u });

        const finish = () => {
          if (done) return;
          done = true;
          clearTimeout(timer);
          try {
            sub?.remove();
          } catch (e) {}
          try {
            p.remove();
          } catch (e) {}
          if (resolver.current === finish) resolver.current = null;
          if (player.current === p) player.current = null;
          res();
        };

        const armTimer = () => {
          // Safety net only: never fires while paused.
          timer = setTimeout(() => {
            if (pausedRef.current) armTimer();
            else finish();
          }, 90000);
        };

        player.current = p;
        resolver.current = finish;
        sub = p.addListener("playbackStatusUpdate", (st) => {
          if (st.didJustFinish) finish();
        });
        armTimer();
        p.play();
      });
    } catch (e) {
      /* skip this piece, keep reading */
    }
  };

  const readFrom = async (startIdx) => {
    halt(); // make sure nothing old is still running
    const tok = token.current;
    setPaused(false);
    setRunning(true);

    try {
      await setAudioModeAsync({
        playsInSilentMode: true,
        shouldPlayInBackground: true,
      });
    } catch (e) {}

    if (tok !== token.current) return;

    const nat = explain.current;
    const lang = profile.learning_language;

    try {
      for (let i = startIdx; i < steps.length; i++) {
        if (tok !== token.current) return;

        setIdx(i);
        setReveal(false);

        const segs = buildSegments(steps[i], nat, lang);

        for (let j = 0; j < segs.length; j++) {
          await holdWhilePaused(tok);
          if (tok !== token.current) return;
          await speak(segs[j].text, segs[j].lang, segs[j].id, tok);
          if (tok !== token.current) return;
          await wait(segs[j].after);
        }

        if (tok !== token.current) return;
        if (!autoRef.current) break;
      }
    } catch (e) {}

    // Only the loop that is still current may reset the buttons.
    if (tok === token.current) {
      setRunning(false);
      setPaused(false);
      setActiveId(null);
    }
  };

  const goToStep = (n) => {
    stop();
    setIdx(n);
    setReveal(false);
  };

  const toggleAuto = () => {
    autoRef.current = !auto;
    setAuto(!auto);
  };

  const step = steps[idx];
  const lines = buildLines(step);
  const activeIndex = lines.findIndex((l) => l.id === activeId);
  const pr = String(step?.teaching?.practice || "");
  const m = pr.match(/^([\s\S]*)\(Answer:\s*([\s\S]+?)\)\s*$/);
  const lastStep = idx >= steps.length - 1;
  const playing = running || paused;

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
      <Text style={s.h1}>{book.title}</Text>
      <Text style={s.p}>
        Lesson • Page {page}/{total} • Step {steps.length ? idx + 1 : 0}/
        {steps.length}
      </Text>
      {!!notice && <Text style={[s.p, { color: C.accent }]}>ℹ️ {notice}</Text>}
      {busy && <ActivityIndicator color={C.accent} style={{ margin: 12 }} />}

      <ScrollView style={s.card}>
        {lines.map((l, i) => {
          const active = i === activeIndex;
          const done = activeIndex !== -1 && i < activeIndex;
          const dim = playing && !active;
          return (
            <View
              key={page + "-" + idx + "-" + l.id}
              style={{
                marginBottom: 14,
                opacity: dim ? (done ? 0.55 : 0.35) : 1,
              }}
            >
              {!!l.label && (
                <Text style={{ color: C.accent, fontSize: 12 }}>{l.label}</Text>
              )}
              <Text
                style={[
                  s.body,
                  {
                    fontWeight: l.id === "sentence" || active ? "700" : "400",
                    fontSize: active ? 19 : 16,
                  },
                ]}
              >
                {l.text}
              </Text>
              {!!l.sub && <Text style={s.p}>{l.sub}</Text>}
            </View>
          );
        })}
        {!!pr && (
          <View style={{ marginTop: 8 }}>
            <Text style={{ color: C.accent, fontSize: 12 }}>Practice</Text>
            <Text style={s.body}>{m ? m[1].trim() : pr}</Text>
            {m &&
              (reveal ? (
                <Text style={[s.body, { fontWeight: "700" }]}>
                  ✅ {m[2].trim()}
                </Text>
              ) : (
                <Btn t="Reveal answer" alt onPress={() => setReveal(true)} />
              ))}
          </View>
        )}
      </ScrollView>

      <View>
        <View style={s.row}>
          <Btn
            t="← Step"
            alt
            disabled={idx === 0 || busy}
            onPress={() => goToStep(idx - 1)}
          />
          {running ? (
            <Btn t="■ Stop" onPress={pause} />
          ) : paused ? (
            <Btn t="▶ Resume" onPress={resume} />
          ) : (
            <Btn
              t="▶ Read"
              disabled={busy || !step}
              onPress={() => readFrom(idx)}
            />
          )}
          <Btn
            t="Step →"
            alt
            disabled={lastStep || busy}
            onPress={() => goToStep(idx + 1)}
          />
        </View>
        <View style={s.row}>
          <Btn
            t={auto ? "🤖 Auto ON" : "🤖 Auto OFF"}
            alt={!auto}
            onPress={toggleAuto}
          />
          {lastStep && (
            <Btn
              t="← Page"
              alt
              disabled={page <= 1 || busy}
              onPress={() => loadPage(page - 1)}
            />
          )}
          {lastStep && (
            <Btn
              t="Page →"
              disabled={page >= total || busy}
              onPress={() => loadPage(page + 1)}
            />
          )}
        </View>
      </View>
    </View>
  );
}
