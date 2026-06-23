import { useState } from "react";

export default function UrlInput({ onProcess }) {

  const [url,setUrl] = useState("");

  return (
    <div>

      <input
        value={url}
        onChange={(e)=>setUrl(e.target.value)}
        placeholder="Paste YouTube URL..."
        className="url-box"
      />

      <button
        onClick={()=>onProcess(url)}
        className="action-btn process-btn"
      >
        🚀 Process Video
      </button>

    </div>
  );
}