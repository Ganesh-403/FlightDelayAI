import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import PredictionForm from './components/PredictionForm';
import HistoryList from './components/HistoryList';
import { motion, AnimatePresence } from 'framer-motion';
import { X, CheckCircle2 } from 'lucide-react';

export default function App() {
  const [history, setHistory] = useState([]);
  const [user, setUser] = useState(null);
  const [lastPrediction, setLastPrediction] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/v1/predict/history?limit=6');
      setHistory(res.data);
    } catch (err) {
      console.error('History fetch failed', err);
    }
  };

  const handleNewPrediction = (result) => {
    setLastPrediction(result);
    fetchHistory(); // Refresh the list
  };

  return (
    <div className="relative pt-32 pb-20 px-6">
      <Navbar user={user} onLogout={() => setUser(null)} />
      
      <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Side: Form */}
        <div className="lg:col-span-7">
          <header className="mb-12">
            <h1 className="text-5xl font-black mb-4 tracking-tight leading-tight">
              Predict Flight Delays with <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-purple-400">
                AI Precision.
              </span>
            </h1>
            <p className="text-slate-400 text-lg max-w-xl">
              Utilize our advanced neural forecasting engine to analyze congestion, 
              weather patterns, and historical trends in seconds.
            </p>
          </header>
          
          <PredictionForm onNewPrediction={handleNewPrediction} />
        </div>

        {/* Right Side: History */}
        <div className="lg:col-span-5 h-full">
          <HistoryList history={history} />
        </div>
      </main>

      {/* Result Modal */}
      <AnimatePresence>
        {lastPrediction && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-slate-950/80 backdrop-blur-sm">
            <motion.div 
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="glass-card max-w-md w-full p-10 relative overflow-hidden"
            >
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 to-purple-500" />
              <button 
                onClick={() => setLastPrediction(null)}
                className="absolute top-4 right-4 text-slate-500 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>

              <div className="flex flex-col items-center text-center">
                <div className="bg-emerald-500/10 p-3 rounded-full mb-6">
                  <CheckCircle2 className="text-emerald-500 w-10 h-10" />
                </div>
                <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-2">Analysis Complete</h3>
                <h2 className="text-2xl font-black mb-8">Estimated Arrival Delay</h2>
                
                <div className="flex items-baseline gap-2 mb-8">
                  <span className="text-7xl font-black text-white">{lastPrediction.delay_prediction.toFixed(1)}</span>
                  <span className="text-xl font-bold text-indigo-400">min</span>
                </div>

                <div className="grid grid-cols-2 gap-4 w-full">
                  <div className="bg-white/5 p-4 rounded-2xl border border-white/5">
                    <span className="block text-[10px] text-slate-500 uppercase font-bold mb-1">Reliability</span>
                    <span className="text-emerald-400 font-bold">High ({(lastPrediction.confidence * 100).toFixed(0)}%)</span>
                  </div>
                  <div className="bg-white/5 p-4 rounded-2xl border border-white/5">
                    <span className="block text-[10px] text-slate-500 uppercase font-bold mb-1">Weather</span>
                    <span className="text-white font-bold">{lastPrediction.weather.temp}°C</span>
                  </div>
                </div>

                <button 
                  onClick={() => setLastPrediction(null)}
                  className="w-full bg-white text-slate-950 font-bold py-4 rounded-2xl mt-8 hover:bg-slate-200 transition-colors"
                >
                  Confirm & Close
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
