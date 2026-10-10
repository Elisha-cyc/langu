// frontend/web/src/Pages/Study.jsx
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

// Library.jsx is the single place that shows courses (Course tab),
// language books, and My Books. This page used to duplicate that list,
// so it now just sends the person back to Library.
export default function Study() {
  const navigate = useNavigate();

  useEffect(() => {
    navigate("/library", { replace: true });
  }, [navigate]);

  return null;
}
