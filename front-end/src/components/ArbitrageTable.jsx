import React, { useEffect, useState } from 'react';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper,
  Select, MenuItem, FormControl, InputLabel, Typography, CircularProgress, Box 
} from '@mui/material';
import { getArbitrageData } from '../services/api';
import { useCoin } from '../../context/Coincontext';

const coinOptions = ["BTC", "ETH", "XRP", "LTC", "DOGE"]; 

const ArbitrageTable = () => {
  const { coin, setCoin } = useCoin();
  const [arbitrageData, setArbitrageData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await getArbitrageData(coin);
        setArbitrageData(data);
      } catch (err) {
        setError("Failed to fetch data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [coin]);

  const handleCoinChange = (event) => {
    setCoin(event.target.value);
  };

  const best = arbitrageData?.best_arbitrage_opportunity;
  const all = arbitrageData?.all_arbitrage_opportunities || [];

  return (
    <Box sx={{ mt: 4 }}>
      <FormControl sx={{ mb: 2, minWidth: 200 }}>
        <InputLabel>Coin</InputLabel>
        <Select value={coin} label="Coin" onChange={handleCoinChange}>
          {coinOptions.map(c => (
            <MenuItem key={c} value={c}>{c}</MenuItem>
          ))}
        </Select>
      </FormControl>

      {loading ? (
        <Box display="flex" justifyContent="center" mt={4}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Typography color="error" align="center" mt={4}>
          {error}
        </Typography>
      ) : (
        <TableContainer component={Paper}>
          <Typography variant="h6" align="center" sx={{ py: 2 }}>
            Arbitrage Opportunities for {coin}
          </Typography>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Coin</TableCell>
                <TableCell>Buy From</TableCell>
                <TableCell>Buy Price (Original)</TableCell>
                <TableCell>Buy Price (INR)</TableCell>
                <TableCell>Sell To</TableCell>
                
               
                <TableCell>Sell Price (Original)</TableCell>
                <TableCell>Sell Price (INR)</TableCell>
                <TableCell>Profit (INR)</TableCell>
                <TableCell>Profit (%)</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {all.map((op, i) => (
                <TableRow
                  key={i}
                  sx={{
                    backgroundColor:
                      best &&
                      op.coin === best.coin &&
                      op.buy_from === best.buy_from &&
                      op.sell_to === best.sell_to
                        ? "rgba(76, 175, 80, 0.15)"
                        : "inherit",
                  }}
                >
                  <TableCell>{op.coin}</TableCell>
                  <TableCell>{op.buy_from}</TableCell>
                  <TableCell>{`${op.buy_price_original.toFixed(7)} ${op.buy_original_currency}`}</TableCell>
                   <TableCell>{op.buy_price_in_inr.toFixed(2)}</TableCell>
                  <TableCell>{op.sell_to}</TableCell>
                  
                 
                  <TableCell>{`${op.sell_price_original.toFixed(7)} ${op.sell_original_currency}`}</TableCell>
                  <TableCell>{op.sell_price_in_inr.toFixed(2)}</TableCell>
                  <TableCell>{op.profit_in_inr.toFixed(2)}</TableCell>
                  <TableCell>{op.profit_percentage.toFixed(2)}%</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

export default ArbitrageTable;
