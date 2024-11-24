export default function Button({ onClick, label, type = "button", className = "" }) {
    return (
      <button
        type={type}
        className={`bg-gradient-to-b from-white to-[#EBEFED] text-xl px-6 py-6 rounded-full border-2 border-sky-300 
                    hover:ring-8 hover:ring-sky-300 hover:ring-opacity-50 focus:outline-none focus:ring-4 
                    focus:ring-sky-300 focus:ring-opacity-50 transition duration-300 ease-in-out 
                    animate-pulseGlow ${className}`}
        onClick={onClick}
      >
        {label}
      </button>
    );
  }
  