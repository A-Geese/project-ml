export default function ChatBubble({ message, image, alt, className = "" }) {
    return (
        <div className={`max-w-xs flex ${message.sender==="user" ? "self-end flex-row-reverse" : "self-start"}`}>
            <ChatAvatar image={image} alt={alt} />
            <div
                className={`px-8 py-4 border-4 border-gray-200 rounded-full ${
                message.sender === "user"
                    ? "bg-gradient-to-b from-sky-400 to-sky-500 border-4 text-white self-end"
                    : "bg-gradient-to-b from-white to-[#EBEFED] border-4 text-black self-start"
                }`}
            >
                {message.text}
            </div>
        </div>
    );
  }

function ChatAvatar({image, alt}) {
    return (
        <img
            src={image}
            alt={alt}
            className="w-[70px] h-[70px] m-1"
        />
    )
}