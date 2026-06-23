import Message from "./Message";

export default function ChatBox({ messages }) {
  return (
    <div className="chat-box">
      {messages.map((msg,index)=>(
        <Message
          key={index}
          text={msg.text}
          role={msg.role}
        />
      ))}
    </div>
  );
}