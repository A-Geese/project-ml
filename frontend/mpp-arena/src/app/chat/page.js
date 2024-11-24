"use client";

import React, { useState, useEffect } from "react";
import SendButton from "./components/send_button";
import TextBox from "./components/text_box";
import ChatBubble from "./components/chat_bubble";
import ChatHeader from "./components/chat_header";
import { FaHandPaper } from "react-icons/fa";
import { useGlobalContext } from "@/context/GlobalContext";

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export default function ChatPage() {
  const { chats, setChats, debaterLeft, debaterRight, billSummary } = useGlobalContext();
  const [currText, setCurrText] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    const sendChatRequest = async (data = {}) => {
      try {
        // Replace with your API endpoint
        const response = await fetch('http://localhost:8000/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          throw new Error('Failed to fetch');
        }

        const result = await response.json();
        setResponses((prev) => [...prev, result]);

        // Send the next request with the previous response
        if (result.next) {
          await sendChatRequest({ previousData: result });
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

    // Initial request when page loads
    sendChatRequest();
  }, []);

  // useEffect(() => {
  //   const getChatResponse = async () => {
  //       try {
  //         const curr_input = {
  //           persona_name: chats && chats.length && chats[0].name === debaterRight ? debaterLeft : debaterRight, 
  //           chat_history: chats ? chats : [],
  //           topic: billSummary
  //         }
  //         console.log("curr_input", curr_input);

  //         const response = await fetch("http://localhost:8000/generate", {
  //           method: "POST",
  //           headers: {
  //             "Content-Type": "application/json",
  //           },
  //           body: JSON.stringify(curr_input),
  //         });

  //         const data = await response.json();
  //         setChats(data.message);

  //         if (data.message !== "END") {
  //           setTimeout(() => getChatResponse(), 1000);
  //         }
  //       } catch (error) {
  //         console.error("API call failed:", error);
  //       }
  //     };
  //     getChatResponse();
  //   }, [])

  
  const handleButtonClick = () => {
    setChats((prevChats) => [...prevChats, {name: "user", id: prevChats.length + 1, text: currText}]);
    setCurrText("");
  }

  return (
    <div className="flex">
        <div className="w-1/2 flex flex-col h-screen bg-gray-100">
            <ChatHeader />
            <div className="flex-1 overflow-y-auto p-4 space-y-4 flex flex-col">
                {chats && chats.length > 1 ? chats.slice(1).map((message, i) => (
                    <ChatBubble key={`${i}`} image={"/miis/image1.png"} message={message} key={message.id}/>
                )) : null}
            </div>
            <footer className="p-4 bg-white flex items-center border-t bg-gradient-to-t from-neutral-200 to-neutral-300">
                <button>
                    <FaHandPaper size={60} className="ml-1 mr-3 text-white p-3 bg-gradient-to-b from-sky-400 to-sky-500 rounded-full hover:shadow-lg hover:scale-105 transition-transform duration-300"/>
                </button>
                <TextBox text={currText} setText={setCurrText}/>
                <SendButton onClick={handleButtonClick} />
            </footer>
        </div>
        <div className="w-1/2 flex flex-col h-screen bg-blue-200">
            <div className="">Relevant Bills</div>

        </div>
    </div>
  );
}
