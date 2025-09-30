import React, { useState, useEffect } from "react";
import "./PATCHPuzzle.css";

function PATCHPuzzle({ userId, weekNumber }) {
  const [puzzle, setPuzzle] = useState(null);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("/generate-message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, week_number: weekNumber }),
    })
      .then(res => res.json())
      .then(data => setPuzzle(data));
  }, [userId, weekNumber]);

  const submitAnswer = () => {
    setLoading(true);
    fetch("/submit-answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        week_number: weekNumber,
        puzzle_index: puzzle.puzzle_index,
        answer,
      }),
    })
      .then(res => res.json())
      .then(data => {
        setFeedback(data.result === "correct" ? "✅ Correct!" : "❌ Incorrect. PATCH is watching...");
        setLoading(false);
      });
  };

  if (!puzzle) return <div className="glitch">Loading PATCH...</div>;

  return (
    <div className="patch-puzzle glitch">
      <div className="patch-voice">{puzzle.message}</div>
      <input
        type="text"
        value={answer}
        onChange={e => setAnswer(e.target.value)}
        placeholder="Enter your answer"
        className="glitch-input"
      />
      <button onClick={submitAnswer} disabled={loading} className="glitch-btn">
        Submit
      </button>
      {feedback && <div className="patch-feedback glitch">{feedback}</div>}
    </div>
  );
}

export default PATCHPuzzle;
