import { useGlobalContext } from "@/context/GlobalContext";


export default function ChatBubble({ message, alt }) {
    const defaultImage = "/miis/default.png";
    const { debaterLeft, debaterRight, name2PartyImage } = useGlobalContext();

    return (
        <div className={`w-[520px] flex ${message.name===debaterRight ? "self-end flex-row-reverse" : "self-start"}`}>
            <ChatAvatar image={name2PartyImage[message.name] || defaultImage} alt={alt} />
            <div
                className={`px-8 py-4 w-[520px] border-4 border-gray-200 rounded-xl ${
                message.name === debaterRight
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
            className="w-[70px] h-[70px] m-1 animate-tiltWithPause "
        />
    )
}