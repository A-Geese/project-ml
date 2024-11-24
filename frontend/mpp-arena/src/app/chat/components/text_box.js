export default function TextBox({ text, setText }) {
    const handleChange = (e) => {
        setText(e.target.value); // Update the state with the input value
    };

    return (
        <input
            type="text"
            value={text}
            placeholder="Type a message..."
            className="text-lg flex-1 p-5 border-4 border-gray-400 rounded-xl mr-14 bg-gradient-to-b from-white to-[#EBEFED]"
            onChange={handleChange}
        />
    );
  }
  