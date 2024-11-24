"use client";

import React, { useState, useEffect } from "react";
import SendButton from "./components/send_button";
import TextBox from "./components/text_box";
import ChatBubble from "./components/chat_bubble";
import ChatHeader from "./components/chat_header";
import { FaHandPaper } from "react-icons/fa";
import { FaComputer } from "react-icons/fa6";
import { FaBong } from "react-icons/fa6";
import { PiEyesFill } from "react-icons/pi";

import { useGlobalContext } from "@/context/GlobalContext";

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export default function ChatPage() {
  const { chats, setChats, debaterLeft, debaterRight, billSummary } = useGlobalContext();
  const [currText, setCurrText] = useState("");
  const [evalRes, setEvalRes] = useState("");
  const [closestBills, setClosestBills] = useState([]);


  useEffect(() => {
    const sendChatRequest = async (data = {}) => {
      try {
        const curr_data = {
          persona_name_left: debaterLeft,
          persona_name_right: debaterRight,
          topic: billSummary
        }
        console.log("currdata", curr_data);
        console.log("left person", debaterLeft);
        // Replace with your API endpoint
        const response = await fetch('http://localhost:8000/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(curr_data),
        });

        // const bill_res = await fetch('http://localhost:8000/get_similar_bills', {
        //   method: 'POST',
        //   headers: {
        //     'Content-Type': 'application/json',
        //   },
        //   body: billSummary,
        // });


        if (!response.ok) {
          throw new Error('Failed to fetch');
        }

        const result = await response.json();
        // const result_bill = await bill_res.json();
        // console.log("billl", result_bill);
        // setClosestBills(result_bill);
        setChats(result.chat_history);
        setEvalRes(result.evaluation);
      } catch (error) {
        console.error('Error:', error);
      }
    };
    sendChatRequest();
  }, []);

  
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
            <div className="mx-16 my-4 bg-white rounded-xl p-10 shadow-lg shadow-sky-300">
              <div className="text-xl flex"><FaComputer className="mr-2" size={25}/> Summary</div>
              {`${billSummary}`}
            </div>
            <div className="mx-16 my-4 bg-white rounded-xl p-10 shadow-lg">
              <div className="text-xl flex"><PiEyesFill className="mr-2" size={25}/>Similar Bills</div>
              <li>Bill 203</li>
              <li>Bill 340</li>
              {/* {
                closestBills.map((bill) => (
                  <div>{bill[0]}</div>
                ))
              } */}
            </div>
            <div className="mx-16 my-4 bg-white rounded-xl p-10 shadow-lg shadow-sky-300 overflow-y-scroll">
              <div className="text-xl flex"><FaBong className="mr-2" size={25}/> Evaluation</div>
              {`${evalRes}`}
            </div>
        </div>
    </div>
  );
}
