import axios from 'axios';

const API_URL = 'http://localhost:8000/arbitrage';  

export const getArbitrageData = async (coin = "XRP") => {
  try {
    const response = await axios.get(`${API_URL}?coin=${coin}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching arbitrage data', error);
    return { best_arbitrage_opportunity: null, all_arbitrage_opportunities: [] };
  }
};
