export default function Dropdown({ onChange, debaters }) {
  return (
    <select
      className="bg-gradient-to-b from-white to-[#EBEFED] p-5 rounded-md border-2 border-transparent 
                 shadow-md focus:shadow-lg hover:shadow-lg focus:ring-4 focus:ring-sky-300 focus:ring-opacity-50 
                 hover:ring-4 hover:ring-sky-300 hover:ring-opacity-50 transition duration-300 ease-in-out"
      onChange={onChange}
    >
      <option value="">Select a debater</option>
      {Object.keys(debaters).map((key) => (
        <option key={key} value={key}>
          {key}
        </option>
      ))}
    </select>
  );
}
