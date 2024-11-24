import { useState } from "react";

export default function Dropdown({ onChange, debaters, setDebater }) {
  const [inputValue, setInputValue] = useState("");

  const handleKeyDown = async (event) => {
    if (event.key === "Enter") {
      const query = inputValue.trim();
      if (query) {
        try {
          const response = await fetch(`/get_mpp_from_postal/${encodeURIComponent(query)}`);
          const data = await response.json();
          console.log("Response data:", data); // Handle the response as needed
          setDebater(data.message);
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      }
    }
  };

  return (
    <div>
      <input
        className="bg-gradient-to-b from-white to-[#EBEFED] p-5 rounded-md border-2 border-transparent 
                   shadow-md focus:shadow-lg hover:shadow-lg focus:ring-4 focus:ring-sky-300 focus:ring-opacity-50 
                   hover:ring-4 hover:ring-sky-300 hover:ring-opacity-50 transition duration-300 ease-in-out"
        list="debaters-list"
        placeholder="Select Debater"
        value={inputValue}
        onChange={(e) => {
          setInputValue(e.target.value);
          onChange && onChange(e); // Keep the existing onChange functionality
        }}
        onKeyDown={handleKeyDown}
      />
      <datalist id="debaters-list">
        {Object.keys(debaters).map((key) => (
          <option key={key} value={key}>
            {key}
          </option>
        ))}
      </datalist>
    </div>
  );
}
