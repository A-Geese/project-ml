"use client";

import React from "react";
import SendButton from "./components/send_button";
import TextBox from "./components/text_box";
import ChatBubble from "./components/chat_bubble";
import ChatHeader from "./components/chat_header";
import { FaHandPaper } from "react-icons/fa";

export default function ChatPage() {
  const messages = [
    { id: 1, text: "Hi there!", sender: "user" },
    { id: 2, text: "Hello! How can I help you?", sender: "bot" },
    { id: 3, text: "What is Next.js?", sender: "user" },
    { id: 4, text: "Next.js is a React framework.", sender: "bot" },
    { id: 5, text: "Can you elaborate?", sender: "user" },
    { id: 6, text: "Sure! It allows server-side rendering and static site generation.", sender: "bot" },
    { id: 7, text: "Cool! Does it work with Tailwind CSS?", sender: "user" },
    { id: 8, text: "Yes, it integrates seamlessly with Tailwind CSS.", sender: "bot" },
    { id: 9, text: "Thanks for explaining!", sender: "user" },
    { id: 10, text: "You're welcome! Anything else?", sender: "bot" },
    { id: 11, text: "No, that's all for now.", sender: "user" },
    { id: 12, text: "Alright, have a great day!", sender: "bot" },
  ];

  return (
    <div className="flex">
        <div className="w-1/2 flex flex-col h-screen bg-gray-100">
            <ChatHeader />
            <div className="flex-1 overflow-y-auto p-4 space-y-4 flex flex-col">
                {messages.map((message) => (
                    <ChatBubble image={"/miis/image1.png"} message={message} key={message.id}/>
                ))}
            </div>
            <footer className="p-4 bg-white flex items-center border-t bg-gradient-to-t from-neutral-200 to-neutral-300">
                <button>
                    <FaHandPaper size={60} className="ml-1 mr-3 text-white p-3 bg-gradient-to-b from-sky-400 to-sky-500 rounded-full hover:shadow-lg hover:scale-105 transition-transform duration-300"/>
                </button>
                <TextBox />
                <SendButton />
            </footer>
        </div>
        <div className="w-1/2 flex flex-col h-screen bg-blue-200">
            <div className="">

            </div>
        </div>
    </div>
  );
}
