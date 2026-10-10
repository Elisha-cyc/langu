import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { getProfile, getUserId } from "../utils/lesson";

export default function Scan() {
  const navigate = useNavigate();
  const profile = getProfile();

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [cameraOpen, setCameraOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  // Declared BEFORE the effects that use it.
  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setCameraOpen(false);
  };

  useEffect(() => {
    if (!profile) navigate("/");
    return () => {
      stopCamera();
      if (preview) URL.revokeObjectURL(preview);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // The <video> element only exists after cameraOpen is true, so the stream
  // is attached here.
  useEffect(() => {
    if (cameraOpen && videoRef.current && streamRef.current) {
      videoRef.current.srcObject = streamRef.current;
    }
  }, [cameraOpen]);

  const openCamera = async () => {
    try {
      streamRef.current = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" },
      });
      setCameraOpen(true);
    } catch (error) {
      console.error(error);
      alert("Unable to access your camera.");
    }
  };

  const setPicked = (file) => {
    if (preview) URL.revokeObjectURL(preview);
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const capturePhoto = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);

    canvas.toBlob(
      (blob) => {
        setPicked(new File([blob], "camera_scan.jpg", { type: "image/jpeg" }));
        stopCamera();
      },
      "image/jpeg",
      0.95,
    );
  };

  const chooseImage = (event) => {
    const file = event.target.files[0];
    if (file) setPicked(file);
  };

  const generateLesson = async () => {
    if (!image) {
      alert("Please choose or capture an image first.");
      return;
    }

    setLoading(true);

    try {
      const form = new FormData();
      form.append("image", image);
      form.append("language", profile.learning_language);
      form.append("target_language", profile.native_language);
      form.append("learner_level", profile.learner_level);
      form.append("user_id", getUserId());

      const response = await api.post("/scan", form, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 180000,
      });

      localStorage.setItem(
        "generated_lesson",
        JSON.stringify(response.data.lesson),
      );
      localStorage.setItem("scan_text", response.data.page_text);
      // The audio can be missing (no voice for the language): never store "null".
      if (response.data.audio)
        localStorage.setItem("scan_audio", response.data.audio);
      else localStorage.removeItem("scan_audio");
      // Tells Lesson / Summary / Key Factors to use this scan, not an old book.
      localStorage.setItem("study_source", "scan");

      navigate("/study-mode");
    } catch (error) {
      console.error(error);
      alert(error?.response?.data?.error || "Failed to generate AI lesson.");
    } finally {
      setLoading(false);
    }
  };

  if (!profile) return null;

  return (
    <div className="scan-page">
      <div className="scan-header">
        <h1>📷 Scan Book</h1>
        <p>
          Capture a page or upload an image and let your AI teacher read and
          teach it.
        </p>
      </div>

      {!cameraOpen ? (
        <div className="scan-preview">
          {preview ? (
            <img src={preview} alt="Book preview" />
          ) : (
            <div className="scan-placeholder">
              <h2>📖</h2>
              <p>Choose an image or use your camera</p>
            </div>
          )}
        </div>
      ) : (
        <div className="camera-view">
          <video ref={videoRef} autoPlay playsInline muted />
          <button className="capture-btn" onClick={capturePhoto}>
            📸 Capture Photo
          </button>
        </div>
      )}

      <canvas ref={canvasRef} style={{ display: "none" }} />

      <div className="scan-info">
        <div className="info-row">
          <span>Learning Language</span>
          <strong>{profile.learning_language}</strong>
        </div>
        <div className="info-row">
          <span>Native Language</span>
          <strong>{profile.native_language}</strong>
        </div>
        <div className="info-row">
          <span>Current Level</span>
          <strong>{profile.learner_level}</strong>
        </div>
      </div>

      <div className="scan-actions">
        <button
          className="camera-btn"
          onClick={cameraOpen ? stopCamera : openCamera}
        >
          {cameraOpen ? "✖ Close Camera" : "📷 Open Camera"}
        </button>

        <label className="upload-btn">
          🖼 Upload Image
          <input type="file" accept="image/*" hidden onChange={chooseImage} />
        </label>
      </div>

      <button
        className="generate-btn"
        disabled={!image || loading}
        onClick={generateLesson}
      >
        {loading
          ? "🤖 Scanning & Reading Page..."
          : "✨ Scan & Start AI Teacher"}
      </button>
    </div>
  );
}
