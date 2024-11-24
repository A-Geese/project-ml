"use client";
import { useState, useEffect } from "react";
import Dropdown from "./components/dropdown";
import AvatarBig from "./components/avatar_big";
import Button from "./components/button_big";
import { useRouter } from 'next/navigation';
import { useGlobalContext } from "@/context/GlobalContext";
import TextBox from "./components/text_box";

export default function Home() {
  const { debaterLeft, setDebaterLeft, setChats, debaterRight, setDebaterRight, name2PartyImage, setName2PartyImage, billSummary, setBillSummary } = useGlobalContext();
  const router = useRouter();
  const [allMpps, setAllMpps] = useState([]);
  const [imageLeft, setImageLeft] = useState("/miis/default.png");
  const [imageRight, setImageRight] = useState("/miis/default.png");
  const [transitionLeft, setTransitionLeft] = useState(false);
  const [transitionRight, setTransitionRight] = useState(false);
  const [showBanner, setShowBanner] = useState(false);
  const [animate, setAnimate] = useState(false);
  const [debaterNames, setDebaterNames] = useState([]);
  const [billUrl, setBillUrl] = useState("");

  // Fetch data on mount
  useEffect(() => {
    async function fetchMpps() {
      try {
        const res = await fetch("http://localhost:8000/all_mpps");
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json();
        setAllMpps(data);

        // Generate name-to-image mapping
        const party2Image = {
          "New Democratic Party of Ontario": "/miis/ndp.png",
          "Progressive Conservative Party of Ontario": "/miis/conservative.png",
          "Ontario Liberal Party": "/miis/liberal.png",
          "Green Party of Ontario": "/miis/green.png",
        };

        const nameImageMap = data.reduce((acc, item) => {
          const partyImage = party2Image[item.party];
          if (partyImage) acc[item.name] = partyImage;
          return acc;
        }, {});
        setName2PartyImage(nameImageMap);
      } catch (error) {
        console.error("Failed to fetch MPPs:", error);
      }
    }
    fetchMpps();
  }, [setName2PartyImage]);


  const handleDropdownChange = (event, setImage, setTransition, setDebater) => {
    const selectedDebater = event.target.value;
    if (allMpps.map(a => a.name).includes(selectedDebater)) {
      setDebater(selectedDebater);
      setTransition(true);
      setTimeout(() => {
        setImage(name2PartyImage[selectedDebater] || "/miis/default.png");
        setTransition(false);
      }, 400);
    }
  };

  const handleButtonClick = async () => {
    setShowBanner(true);
    setTimeout(() => setAnimate(true), 100);

    try {
      const response = await fetch("http://localhost:8000/summarize_policy", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: billUrl }),
      });

      if (response.ok) {
        const data = await response.json();
        setBillSummary(data);
        console.log("sum", data);
        setTimeout(() => router.push("/chat"), 1500);
      } else {
        console.error("Failed to summarize policy");
      }
    } catch (error) {
      console.error("Error:", error);
    }    
  };

  return (
    <div className="flex flex-col my-12 bg-zinc-100 mx-80 py-16 px-48 rounded-xl border-2 focus:border-sky-300 shadow-lg">
      {showBanner && (
        <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-75 flex items-center justify-center z-50">
          <div
            className={`absolute top-1/2 transform translate-y-16 w-80 bg-white h-1 transition-transform duration-1000 ease-linear ${
              animate ? "translate-x-[96em]" : "translate-x-2"
            }`}
          />
          <div
            className={`absolute top-1/2 transform -translate-y-20 w-96 bg-white h-1 transition-transform duration-1000 ease-linear ${
              animate ? "-translate-x-[96em]" : "-translate-x-96"
            }`}
          />
          <div
            className={`absolute top-1/2 transform -translate-y-32 w-96 bg-white h-1 transition-transform duration-1000 ease-linear ${
              animate ? "-translate-x-[80em]" : "translate-x-[90em]"
            }`}
          />
          <div className="absolute top-1/2 transform -translate-y-1/2 w-full bg-white h-24 flex items-center justify-center">
            <h1 className="text-black text-xl font-bold">Battle Starting!</h1>
          </div>
        </div>
      )}
      <div className="m-auto flex items-center justify-center pb-6 pt-2">
        <div className="flex-1 flex flex-col items-center justify-center">
          <AvatarBig image={imageLeft} alt="Debater Left" transition={transitionLeft} />
          <Dropdown
            onChange={(e) => handleDropdownChange(e, setImageLeft, setTransitionLeft, setDebaterLeft)}
            debaters={allMpps.map(a => a.name)}
          />
        </div>

        <div className="flex-1 flex flex-col items-center justify-center">
          <AvatarBig image={imageRight} alt="Debater Right" transition={transitionRight} />
          <Dropdown
            onChange={(e) => handleDropdownChange(e, setImageRight, setTransitionRight, setDebaterRight)}
            debaters={allMpps.map(a => a.name)}
          />
        </div>
      </div>
      <TextBox text={billUrl} setText={setBillUrl} />
      <div className="flex-1 m-auto items-center justify-center">
        <Button onClick={handleButtonClick} label="Start Battle" />
      </div>
    </div>
  );
}
