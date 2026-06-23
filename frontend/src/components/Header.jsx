export default function Header() {
  return (
    <div className="youtube-header">

      <div className="logo-circle">
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png"
          alt="YouTube"
          style={{
            width: "50px",
            height: "35px",
            objectFit: "contain"
          }}
        />
      </div>

      <h1>YouTube Chatbot</h1>

      <p>
        Chat with any YouTube video using AI
      </p>

    </div>
  );
}