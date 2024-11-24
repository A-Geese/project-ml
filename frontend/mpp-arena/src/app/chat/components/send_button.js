export default function SendButton({ onClick, type = "button", className = "" }) {
    return (
        <button 
            type={type}
            onClick={onClick}
            className={`hover:scale-150 transition-transform duration-300 text-black text-xs bg-gradient-to-b from-white to-[#EBEFED] py-6 px-4 rounded-full animate-pulseGlow transform scale-[1.4] relative -top-4 right-5 ${className}`}
        >
            Send
        </button>
    );
}
