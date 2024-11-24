"use client";
import { useState } from "react";
import Dropdown from "./components/dropdown";
import AvatarBig from "./components/avatar_big";
import Button from "./components/button_big";
import { useRouter } from 'next/navigation'

export default function Home() {
  const debaters = {
    debater1: "/miis/image1.png",
    debater2: "/miis/image2.png",
    debater3: "/miis/image3.png",
    debater4: "/miis/image4.png",
  };

  const defaultImage = "/miis/default.png";
  const [imageLeft, setImageLeft] = useState(defaultImage);
  const [imageRight, setImageRight] = useState(defaultImage);
  const [transitionLeft, setTransitionLeft] = useState(false);
  const [transitionRight, setTransitionRight] = useState(false);
  const [showBanner, setShowBanner] = useState(false);
  const [animate, setAnimate] = useState(false);
  const router = useRouter();

  const handleDropdownChange = (event, setImage, setTransition) => {
    const selectedDebater = event.target.value;
    setTransition(true);
    setTimeout(() => {
      setImage(debaters[selectedDebater] || defaultImage);
      setTransition(false); // Reset animation
    }, 400); // Matches the transition duration
  };

  const handleButtonClick = () => {
    setShowBanner(true); // Show the banner
    setTimeout(() => {
        setAnimate(true); // Start animation after a small delay
    }, 100);
    setTimeout(() => {
        router.push("/chat");
    }, 1500); // Show the banner for 2 seconds
};

  return (
    <div className="flex flex-col my-20 bg-zinc-100 mx-96 py-16 rounded-xl border-2 focus:border-sky-300 shadow-lg">
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
        <div className="m-auto flex items-center justify-center mx-32 py-6">
            <div className="flex-1 flex flex-col items-center justify-center">
                <AvatarBig
                image={imageLeft}
                alt="Debater Left"
                transition={transitionLeft}
                />
                <br/>
                <Dropdown onChange={(e) => handleDropdownChange(e, setImageLeft, setTransitionLeft)} debaters={debaters} />
            </div>

            <div className="flex-1 flex flex-col items-center justify-center">
                <AvatarBig
                image={imageRight}
                alt="Debater Right"
                transition={transitionRight}
                />
                <br />
                <Dropdown onChange={(e) => handleDropdownChange(e, setImageRight, setTransitionRight)} debaters={debaters} />
            </div>
        </div>
        <div className="flex-1 m-auto items-center justify-center">
            <Button onClick={handleButtonClick} label={"Start Battle"}/>
        </div>
    </div>
  );
}
