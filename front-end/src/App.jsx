import React from 'react';
import { CoinProvider } from '../context/Coincontext';
import ArbitrageTable from './components/ArbitrageTable';

function App() {
  return (
    <CoinProvider>
      <ArbitrageTable />
    </CoinProvider>
  );
}

export default App;
