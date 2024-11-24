"use client";
import { useState } from "react";
import Dropdown from "./components/dropdown";
import AvatarBig from "./components/avatar_big";
import Button from "./components/button_big";
import { useRouter } from 'next/navigation'
import { useGlobalContext } from "@/context/GlobalContext";
import TextBox from "./components/text_box";

export default function Home() {
  const debaters = {
    debater1: "/miis/image1.png",
    debater2: "/miis/image2.png",
    debater3: "/miis/image3.png",
    debater4: "/miis/image4.png",
  };

  const fetchContent = async () => {
    try {
      const response = await fetch('https://www.ola.org/en/legislative-business/bills/parliament-43/session-1/bill-195');
      const data = await response.text();
      setHtmlContent(data);
    } catch (error) {
      console.error('Error fetching website:', error);
      setHtmlContent('Failed to fetch content.');
    } 
  };

  const defaultImage = "/miis/default.png";
  const { debaterLeft, setDebaterLeft, debaterRight, setDebaterRight } = useGlobalContext();
  const [imageLeft, setImageLeft] = useState(defaultImage);
  const [imageRight, setImageRight] = useState(defaultImage);
  const [transitionLeft, setTransitionLeft] = useState(false);
  const [transitionRight, setTransitionRight] = useState(false);
  const [showBanner, setShowBanner] = useState(false);
  const [animate, setAnimate] = useState(false);
  const [htmlContent, setHtmlContent] = useState('');
  const [billUrl, setBillUrl] = useState('');


  const handleDropdownChange = (event, setImage, setTransition, setDebater) => {
    const selectedDebater = event.target.value;
    if (Object.keys(debaters).includes(selectedDebater)) {
      setDebater(selectedDebater);
      setTransition(true);
      setTimeout(() => {
        setImage(debaters[selectedDebater] || defaultImage);
        setTransition(false);
      }, 400);
    }
  };

  const handleButtonClick = () => {
    setShowBanner(true);
    fetchContent();
    console.log(htmlContent);
    setTimeout(() => {
        setAnimate(true);
    }, 100);
    setTimeout(() => {
        router.push("/chat");
    }, 1500);
};

  return (
    <div className="flex flex-col my-12 bg-zinc-100 mx-96 py-16 px-48 rounded-xl border-2 focus:border-sky-300 shadow-lg">
        {showBanner && (
            <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-75 flex items-center justify-center z-50">
                <div
                    className={`absolute top-1/2 transform translate-y-16 w-80 bg-white h-1 transition-transform duration-1000 ease-linear ${
                        animate ? "translate-x-[96em]" : "translate-x-2"
                    }`}
                />
                <div
                    className={`absolute top-1/2 transform -translate-y-20 w-96 bg-white h-1 transition-transform duration-1000 ease-linear ${
                        animate ? "-translate-x-2" : "-translate-x-96"
                    }`}
                />
                <div
                    className={`absolute top-1/2 transform -translate-y-32 w-96 bg-white h-1 transition-transform duration-1000 ease-linear ${
                        animate ? "-translate-x-[20em]" : "translate-x-[90em]"
                    }`}
                />
                <div className="absolute top-1/2 transform -translate-y-1/2 w-full bg-white h-24 flex items-center justify-center">
                    <h1 className="text-black text-xl font-bold">Battle Starting!</h1>
                </div>
            </div>
        )}
        <div className="m-auto flex items-center justify-center pb-6 pt-2">
            <div className="flex-1 flex flex-col items-center justify-center">
                <AvatarBig
                  image={imageLeft}
                  alt="Debater Left"
                  transition={transitionLeft}
                />
                <br/>
                <Dropdown onChange={(e) => handleDropdownChange(e, setImageLeft, setTransitionLeft, setDebaterLeft)} debaters={debaters} setDebater={setDebaterLeft} />
            </div>

            <div className="flex-1 flex flex-col items-center justify-center">
                <AvatarBig
                  image={imageRight}
                  alt="Debater Right"
                  transition={transitionRight}
                />
                <br />
                <Dropdown onChange={(e) => handleDropdownChange(e, setImageRight, setTransitionRight, setDebaterRight)} debaters={debaters} />
            </div>
        </div>
        <TextBox text={billUrl} setText={setBillUrl} />
        <div className="flex-1 m-auto items-center justify-center">
            <Button onClick={handleButtonClick} label={"Start Battle"}/>
        </div>
    </div>
  );
}
