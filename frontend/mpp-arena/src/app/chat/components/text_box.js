export default function TextBox({ onClick, type = "button", className = "" }) {
    return (
        <input
            type="text"
            placeholder="Type a message..."
            className="text-lg flex-1 p-5 border-4 border-gray-400 rounded-xl mr-14 bg-gradient-to-b from-white to-[#EBEFED]"
        />
    );
  }
  