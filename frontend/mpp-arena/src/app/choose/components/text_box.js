export default function TextBox({ text, setText }) {
    const handleChange = (e) => {
        setText(e.target.value); // Update the state with the input value
    };

    return (
        <input
            type="text"
            value={text} // Bind the state to the input value
            onChange={handleChange} // Update state on change
            placeholder="Bill URL"
            className="text-lg flex-1 p-5 mt-2 mb-6 rounded-xl shadow-md hover:ring-4 bg-gradient-to-b from-white to-[#EBEFED]"
        />
    );
}
