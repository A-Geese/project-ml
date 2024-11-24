'use client'; // Necessary for context usage in the app directory

import React, { createContext, useContext, useState } from 'react';

const GlobalContext = createContext();

export const GlobalProvider = ({ children }) => {
    const [billSummary, setBillSummary] = useState('');
    const [debaterLeft, setDebaterLeft] = useState('');
    const [debaterRight, setDebaterRight] = useState('');
    const [chats, setChats] = useState([]);
    const [name2PartyImage, setName2PartyImage] = useState({});

    return (
        <GlobalContext.Provider value={{ 
            debaterLeft, setDebaterLeft, debaterRight, setDebaterRight, billSummary, setBillSummary,
            chats, setChats, name2PartyImage, setName2PartyImage
        }}>
            {children}
        </GlobalContext.Provider>
    );
};

export const useGlobalContext = () => useContext(GlobalContext);
