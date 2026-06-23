import { useState } from "react";

import Header from "./components/Header";
import UrlInput from "./components/UrlInput";
import ChatBox from "./components/ChatBox";
import LoadingSpinner from "./components/LoadingSpinner";

import api from "./services/api";

export default function App() {

  const [messages, setMessages] = useState([]);

  const [question, setQuestion] = useState("");

  const [loading, setLoading] = useState(false);
  const [videoReady, setVideoReady] = useState(false);


  const processVideo = async (url) => {

setLoading(true);
setVideoReady(false);

try {

  await api.post("/url", { url });

  const videoId =
    new URL(url).searchParams.get("v");

  setMessages(prev => [
    ...prev,
    {
      role: "assistant",
      text: "⏳ Video processing started. Please wait..."
    }
  ]);

  const interval = setInterval(async () => {

    try {

      const res = await api.get(
        `/status/${videoId}`
      );

      const status = res.data.status;

      console.log("Status:", status);

      if (status === "ready") {

        clearInterval(interval);

        setVideoReady(true);

        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            text: "✅ Video processed successfully. You can now ask questions."
          }
        ]);

        setLoading(false);
      }

      if (
        typeof status === "string" &&
        status.startsWith("error")
      ) {

        clearInterval(interval);

        setLoading(false);

        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            text: status
          }
        ]);
      }

    } catch (err) {

      console.error(err);

      clearInterval(interval);

      setLoading(false);

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          text: "Failed to check processing status."
        }
      ]);
    }

  }, 5000);

} catch (error) {

  setLoading(false);

  setMessages(prev => [
    ...prev,
    {
      role: "assistant",
      text:
        error.response?.data?.error ||
        error.message ||
        "Unable to process video."
    }
  ]);
}

};

  const sendQuestion = async () => {

if (!question) return;

if (!videoReady) {

  setMessages(prev => [
    ...prev,
    {
      role: "assistant",
      text: "⏳ Video is still processing. Please wait."
    }
  ]);

  return;
}

const userMessage = {
  role: "user",
  text: question
};

setMessages(prev => [
  ...prev,
  userMessage
]);

const currentQuestion = question;

setQuestion("");

try {

  const res = await api.post(
    "/chat",
    {
      query: currentQuestion
    }
  );

  setMessages(prev => [
    ...prev,
    {
      role: "assistant",
      text: res.data.response
    }
  ]);

} catch (error) {

  setMessages(prev => [
    ...prev,
    {
      role: "assistant",
      text:
        error.response?.data?.error ||
        "Something went wrong."
    }
  ]);
}

};

  return (



  <div className="max-w-5xl mx-auto px-6 py-10">

    <Header />

    <UrlInput
      onProcess={processVideo}
    />

    <div className="suggestion-row">

      <button
        className="suggestion-chip"
        onClick={() => setQuestion("Summarize this video")}
      >
        📄 Summarize Video
      </button>

      <button
        className="suggestion-chip"
        onClick={() => setQuestion("What are the key takeaways?")}
      >
        🎯 Key Takeaways
      </button>

      <button
        className="suggestion-chip"
        onClick={() => setQuestion("Explain this video in simple terms")}
      >
        🧠 Explain Simply
      </button>

      <button
        className="suggestion-chip"
        onClick={() => setQuestion("Generate interview questions from this video")}
      >
        💼 Interview Questions
      </button>

    </div>

    {loading && <LoadingSpinner />}

    <ChatBox
      messages={messages}
    />

    <div style={{ marginTop: "20px" }}>

      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask anything about the video..."
        className="question-box"
        disabled={!videoReady}
      />

      <button
        onClick={sendQuestion}
        disabled={!videoReady}
        className="action-btn send-btn"
        style={{
          opacity: videoReady ? 1 : 0.5,
          cursor: videoReady ? "pointer" : "not-allowed"
        }}
      >
        {videoReady
          ? "✨ Send Question"
          : "⏳ Processing Video"}
      </button>

    </div>

  </div>

);
}