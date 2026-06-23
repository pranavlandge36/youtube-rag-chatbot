export default function Message({ text, role }) {

  if (role === "user") {
    return (
      <div className="user-message">
        <div className="user-bubble">
          {text}
        </div>
      </div>
    );
  }

  return (
    <div className="bot-message">
      <div className="bot-bubble">
        {text}
      </div>
    </div>
  );
}