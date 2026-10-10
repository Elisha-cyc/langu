# backend/services/audio_service.py
import asyncio
import io
import os
import re
import uuid
from pathlib import Path

from gtts import gTTS
from pydub import AudioSegment


class VoiceUnavailable(ValueError):
    """Raised when there is no voice for the requested language.

    The message is short on purpose: the mobile app shows it in the status line.
    """


class AudioService:

    def __init__(self):
        self.output_folder = Path(__file__).resolve().parent.parent.parent / "data" / "audio"
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # ------------------------------------------------------------------
        # Native-speaker neural voices (Microsoft Edge, free, no API key).
        # Each voice is a person from that country, so the accent is natural.
        # To change a voice, swap the name. Male examples: ja-JP-KeitaNeural,
        # fr-FR-HenriNeural, es-ES-AlvaroNeural, de-DE-ConradNeural,
        # en-GB-RyanNeural, ko-KR-InJoonNeural, zh-CN-YunxiNeural.
        # ------------------------------------------------------------------
        self.edge_voices = {
            "english": "en-US-AriaNeural",
            "japanese": "ja-JP-NanamiNeural",
            "chinese": "zh-CN-XiaoxiaoNeural",
            "mandarin": "zh-CN-XiaoxiaoNeural",
            "korean": "ko-KR-SunHiNeural",
            "arabic": "ar-SA-ZariyahNeural",
            "spanish": "es-ES-ElviraNeural",
            "french": "fr-FR-DeniseNeural",
            "german": "de-DE-KatjaNeural",
            "portuguese": "pt-BR-FranciscaNeural",
            "italian": "it-IT-ElsaNeural",
            "russian": "ru-RU-SvetlanaNeural",
            "hindi": "hi-IN-SwaraNeural",
            "hebrew": "he-IL-HilaNeural",
            "turkish": "tr-TR-EmelNeural",
            "dutch": "nl-NL-ColetteNeural",
            "polish": "pl-PL-ZofiaNeural",
            "swedish": "sv-SE-SofieNeural",
            "greek": "el-GR-AthinaNeural",
            "thai": "th-TH-PremwadeeNeural",
            "vietnamese": "vi-VN-HoaiMyNeural",
            "indonesian": "id-ID-GadisNeural",
            "swahili": "sw-KE-ZuriNeural",
            "bengali": "bn-BD-NabanitaNeural",
            "tamil": "ta-IN-PallaviNeural",
            "urdu": "ur-PK-UzmaNeural",
            "ukrainian": "uk-UA-PolinaNeural",
            "czech": "cs-CZ-VlastaNeural",
            "romanian": "ro-RO-AlinaNeural",
            "hungarian": "hu-HU-NoemiNeural",
            "filipino": "fil-PH-BlessicaNeural",
            "tagalog": "fil-PH-BlessicaNeural",
            "amharic": "am-ET-MekdesNeural",
        }

        # Sleep Teacher: slower and a little lower, which sounds calmer.
        self.EDGE_CALM_RATE = "-15%"
        self.EDGE_CALM_PITCH = "-6Hz"

        # ------------------------------------------------------------------
        # Fallback: gTTS voices. Keys are lowercase; lookups ignore case and
        # anything in brackets, so "Japanese (日本語)" and "japanese" both work.
        # (pip install -U gTTS for Hebrew "iw".)
        # ------------------------------------------------------------------
        self.language_map = {
            "english": "en",
            "japanese": "ja",
            "chinese": "zh-CN",
            "mandarin": "zh-CN",
            "korean": "ko",
            "arabic": "ar",
            "spanish": "es",
            "french": "fr",
            "german": "de",
            "portuguese": "pt",
            "italian": "it",
            "russian": "ru",
            "hindi": "hi",
            "hebrew": "iw",
            "turkish": "tr",
            "dutch": "nl",
            "polish": "pl",
            "swedish": "sv",
            "greek": "el",
            "thai": "th",
            "vietnamese": "vi",
            "indonesian": "id",
            "swahili": "sw",
            "bengali": "bn",
            "tamil": "ta",
            "urdu": "ur",
            "ukrainian": "uk",
            "czech": "cs",
            "romanian": "ro",
            "hungarian": "hu",
            "filipino": "tl",
            "tagalog": "tl",
            "hausa": "ha",
            "amharic": "am",
        }

        # gTTS regional accents (only used if the Edge voice is unavailable).
        self.gtts_accent = {
            "english": "co.uk",
            "french": "fr",
            "spanish": "es",
            "portuguese": "com.br",
        }

        # Also pick up anything else gTTS itself supports, by its own names.
        try:
            from gtts.lang import tts_langs
            for code, name in tts_langs().items():
                self.language_map.setdefault(name.split("(")[0].strip().lower(), code)
        except Exception as e:
            print(f"[audio] could not read gTTS language list: {e}")

        # Languages neither Edge nor gTTS can speak but Khaya (GhanaNLP) can.
        # Needs: pip install khaya  and the KHAYA_API_KEY environment variable.
        self.khaya_map = {
            "twi": "twi",
            "asante twi": "twi",
            "akan": "twi",
            "akuapem twi": "atw",
            "adangme": "ada",
            "dagbani": "dag",
        }

        # Old gTTS "calm" processing (slow + low-pass). Only used for the
        # gTTS and Khaya paths; Edge voices use their own rate and pitch.
        self.SLEEP_SPEED = 0.88
        self.SLEEP_LOWPASS_HZ = 3800
        self.SLEEP_VOLUME_DB = -2

    # ------------------------------------------------------------------
    @staticmethod
    def _key(language):
        raw = (language or "").strip()
        return raw, re.split(r"[(\-–,/]", raw)[0].strip().lower()

    def _resolve(self, language):
        """Return (engine, code, key). Engine is "edge", "gtts" or "khaya".

        Raises VoiceUnavailable when no engine can speak the language.
        """
        raw, key = self._key(language)

        if key in self.khaya_map:
            return "khaya", self.khaya_map[key], key
        if key in self.edge_voices:
            return "edge", self.edge_voices[key], key
        if key in self.language_map:
            return "gtts", self.language_map[key], key

        # Raw gTTS codes such as "ja" or "zh-cn".
        codes = {c.lower(): c for c in self.language_map.values()}
        if raw.lower() in codes:
            return "gtts", codes[raw.lower()], key

        print(f"[audio] no voice for language {language!r}")
        raise VoiceUnavailable(f"No voice available for {raw or 'this language'}")

    def _soften(self, sound):
        slowed = sound._spawn(
            sound.raw_data,
            overrides={"frame_rate": int(sound.frame_rate * self.SLEEP_SPEED)}
        ).set_frame_rate(sound.frame_rate)

        softened = slowed.low_pass_filter(self.SLEEP_LOWPASS_HZ)
        return softened + self.SLEEP_VOLUME_DB

    # ------------------------------------------------------------------
    # Edge neural voices
    # ------------------------------------------------------------------
    def _edge_save(self, text, voice, calm, output):
        import edge_tts

        rate = self.EDGE_CALM_RATE if calm else "+0%"
        pitch = self.EDGE_CALM_PITCH if calm else "+0Hz"

        async def run():
            communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
            await communicate.save(str(output))

        # A fresh event loop works in any Flask thread.
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(run())
        finally:
            loop.close()

        if not output.exists() or output.stat().st_size == 0:
            raise RuntimeError("Edge voice returned no audio")

    # ------------------------------------------------------------------
    # gTTS fallback
    # ------------------------------------------------------------------
    def _gtts_save(self, text, code, key, calm, output, label):
        tld = self.gtts_accent.get(key, "com")

        try:
            tts = gTTS(text=text, lang=code, tld=tld)
        except ValueError:
            print(f"[audio] this gTTS version does not support {code!r}; try: pip install -U gTTS")
            raise VoiceUnavailable(f"No voice available for {label}")

        if not calm:
            tts.save(output)
            return

        raw_path = self.output_folder / f"{uuid.uuid4()}_raw.mp3"
        tts.save(raw_path)
        try:
            sound = AudioSegment.from_file(raw_path, format="mp3")
            self._soften(sound).export(output, format="mp3")
        finally:
            raw_path.unlink(missing_ok=True)

    def _khaya_sound(self, text, code, label):
        key = os.environ.get("KHAYA_API_KEY")
        if not key:
            print(f"[audio] {label} needs a Khaya API key: set KHAYA_API_KEY")
            raise VoiceUnavailable(f"No voice available for {label}")
        try:
            from khaya import KhayaClient
        except ImportError:
            print("[audio] Khaya SDK missing: pip install khaya")
            raise VoiceUnavailable(f"No voice available for {label}")

        # Long text is sent sentence by sentence.
        chunks = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        sound = AudioSegment.empty()
        try:
            with KhayaClient(key) as khaya:
                for chunk in chunks:
                    result = khaya.synthesize(chunk, code)
                    sound += AudioSegment.from_file(io.BytesIO(result.audio), format="wav")
        except Exception as e:
            print(f"[audio] Khaya failed for {label}: {e}")
            raise VoiceUnavailable(f"{label} voice failed")
        return sound

    # ------------------------------------------------------------------
    def generate_audio(self, text, language, calm=False):
        text = (text or "").strip()
        if not text:
            raise ValueError("No text to speak")

        engine, code, key = self._resolve(language)
        label = (language or "").strip()

        # --- Khaya path (e.g. Twi): WAV in, mp3 out when calm, WAV otherwise ---
        if engine == "khaya":
            sound = self._khaya_sound(text, code, label)
            if calm:
                file_name = f"{uuid.uuid4()}.mp3"
                self._soften(sound).export(self.output_folder / file_name, format="mp3")
            else:
                file_name = f"{uuid.uuid4()}.wav"
                sound.export(self.output_folder / file_name, format="wav")
            return f"data/audio/{file_name}"

        file_name = f"{uuid.uuid4()}.mp3"
        output = self.output_folder / file_name

        # --- Native neural voice first ---
        if engine == "edge":
            try:
                self._edge_save(text, code, calm, output)
                return f"data/audio/{file_name}"
            except Exception as e:
                print(f"[audio] Edge voice failed for {label!r}: {e} -> falling back to gTTS")
                output.unlink(missing_ok=True)

                gtts_code = self.language_map.get(key)
                if not gtts_code:
                    raise VoiceUnavailable(f"{label} voice failed")
                code = gtts_code

        # --- gTTS path (fallback, or languages Edge doesn't have) ---
        self._gtts_save(text, code, key, calm, output, label)
        return f"data/audio/{file_name}"


if __name__ == "__main__":

    audio = AudioService()

    for lang, sample in [
        ("Japanese", "こんにちは、私は学生です。"),
        ("French", "Bonjour, je m'appelle Marie."),
        ("Spanish", "Hola, ¿cómo estás?"),
    ]:
        print(lang, audio.generate_audio(text=sample, language=lang, calm=False))