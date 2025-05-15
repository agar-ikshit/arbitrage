import React, { createContext, useState, useContext } from 'react';

const CoinContext = createContext();

export const CoinProvider = ({ children }) => {
  const [coin, setCoin] = useState("BTC");

  return (
    <CoinContext.Provider value={{ coin, setCoin }}>
      {children}
    </CoinContext.Provider>
  );
};

// Custom hook for easier usage
export const useCoin = () => useContext(CoinContext);
