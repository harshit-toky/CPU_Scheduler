import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const algorithms = ["FCFS", "SJF", "Priority", "Round Robin"];

const Popup = ({ isOpen, onClose, onSubmit }) => {
  const [selected, setSelected] = useState([]);
  const [timeQuantum, setTimeQuantum] = useState("");
  const [selectAll, setSelectAll] = useState(false);
  const [error, setError] = useState("");

  const handleCheck = (algo) => {
    setError("");
    if (selected.includes(algo)) {
      setSelected(selected.filter((item) => item !== algo));
      if (algo === "Round Robin") setTimeQuantum("");
    } else {
      setSelected([...selected, algo]);
    }
  };

  const handleSelectAll = () => {
    setError("");
    if (!selectAll) {
      setSelected([...algorithms]);
      setSelectAll(true);
    } else {
      setSelected([]);
      setTimeQuantum("");
      setSelectAll(false);
    }
  };

  const handleSubmit = () => {
    if (selected.length === 0) {
      setError("Please select at least one algorithm.");
      return;
    }
    if (selected.includes("Round Robin") && !timeQuantum) {
      setError("Please enter a time quantum for Round Robin.");
      return;
    }
    setError("");
    onSubmit({ selected, timeQuantum });
    onClose();
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className="bg-white rounded-2xl shadow-xl w-[90%] max-w-md p-6"
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0.8 }}
          >
            <h2 className="text-xl font-semibold mb-4">Select Algorithm</h2>

            <div className="flex items-center space-x-2 mb-3">
              <input
                type="checkbox"
                checked={selectAll}
                onChange={handleSelectAll}
                className="w-4 h-4"
              />
              <label className="text-sm font-medium">Select All</label>
            </div>

            {algorithms.map((algo) => (
              <div key={algo} className="flex items-center space-x-2 mb-2">
                <input
                  type="checkbox"
                  checked={selected.includes(algo)}
                  onChange={() => handleCheck(algo)}
                  className="w-4 h-4"
                />
                <label className="text-sm">{algo}</label>
              </div>
            ))}

            {selected.includes("Round Robin") && (
              <div className="mt-4">
                <label className="block text-sm font-medium mb-1">
                  Time Quantum
                </label>
                <input
                  type="number"
                  value={timeQuantum}
                  onChange={(e) => setTimeQuantum(e.target.value)}
                  className="w-full px-3 py-2 border rounded-md text-sm"
                  placeholder="Enter time quantum"
                />
              </div>
            )}

            {error && (
              <p className="mt-3 text-sm text-red-600 font-medium">{error}</p>
            )}

            <div className="flex justify-end space-x-3 mt-6">
              <button
                className="px-4 py-2 bg-gray-300 text-sm rounded-md hover:bg-gray-400"
                onClick={onClose}
              >
                Close
              </button>
              <button
                className="px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700"
                onClick={handleSubmit}
              >
                OK
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default Popup;
