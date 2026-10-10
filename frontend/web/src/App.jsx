// frontend/web/src/App.jsx
import { Routes, Route, Navigate } from "react-router-dom";
import Welcome from "./Pages/Welcome";
import Home from "./Pages/Home";
import Library from "./Pages/Library";
import Study from "./Pages/Study";
import Lesson from "./Pages/Lesson";
import Profile from "./Pages/Profile";
import Scan from "./Pages/Scan";
import StudyMode from "./Pages/StudyMode";
import KeyFactors from "./Pages/KeyFactors";
import Summary from "./Pages/Summary";
import SleepMode from "./Pages/SleepMode";
import BookExam from "./Pages/BookExam";
import Flashcards from "./Pages/FlashCards";

function ProtectedRoute({ children }) {
  const user = localStorage.getItem("lingua_profile");
  return user ? children : <Navigate to="/" replace />;
}

const guard = (element) => <ProtectedRoute>{element}</ProtectedRoute>;

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Welcome />} />
      <Route path="/home" element={guard(<Home />)} />
      <Route path="/library" element={guard(<Library />)} />
      <Route path="/study" element={guard(<Study />)} />
      <Route path="/lesson" element={guard(<Lesson />)} />
      <Route path="/profile" element={guard(<Profile />)} />
      <Route path="/scan" element={guard(<Scan />)} />
      <Route path="/study-mode" element={guard(<StudyMode />)} />
      <Route path="/key-factors" element={guard(<KeyFactors />)} />
      <Route path="/summary" element={guard(<Summary />)} />
      <Route path="/sleep-mode" element={guard(<SleepMode />)} />
      <Route path="/book-exam" element={guard(<BookExam />)} />
      <Route path="/flashcards" element={guard(<Flashcards />)} />
      {/* Unknown address: back to the start instead of a blank page */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
