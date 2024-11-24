export default function ChatHeader({text}) {
    return (
        <header 
        className="z-10 text-center bg-gradient-to-b from-white to-neutral-300 
                h-24 py-4 px-6 pt-8 text-xl font-bold shadow-lg shadow-sky-300">
            {text}
        </header>
    );
  }
  