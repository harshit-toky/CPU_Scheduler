import { useState, useRef } from "react";
import Popup from "./Popup";
import AlgoCharts from "./AlgoCharts";

export default function ProcessTable() {
  const [processes, setProcesses] = useState([]);
  const [ganttData, setGanttData] = useState([]);
  const [sjfGanttData, setSjfGanttData] = useState([]);
  const [priorityGanttData, setPriorityGanttData] = useState([]);
  const [showPopup, setShowPopup] = useState(false);
  const [roundRobinGanttData, setRoundRobinGanttData] = useState([]);
  // const [responseType, setResponseType] = useState('');
  const [aiAlgo, setAiAlgo] = useState(null); // FCFS, SJF, etc.
  const [remainingAlgos, setRemainingAlgos] = useState([]);
  const [showSoftMetrics, setShowSoftMetrics] = useState(false);
  const [showAiWhy, setShowAiWhy] = useState(false);
  const whyRef = useRef(null);
  const metricsRef = useRef(null);
  const [aiData, setAiData] = useState(null);


  const scrollToWhy = () => {
    setShowAiWhy(true);
    setTimeout(() => {
      whyRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100); // delay for rendering
  };
  
  const scrollToMetrics = () => {
    setShowSoftMetrics(true);
    setTimeout(() => {
      metricsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);
  };
  


  const addProcess = () => {
    const lastProcess = processes[processes.length - 1];
    const newId = lastProcess ? lastProcess.id + 1 : 1; // If array is empty, start from 1

    setProcesses([
      ...processes,
      { id: newId, arrivalTime: "", burstTime: "", priority: "" }
    ]);
  };

  const removeProcess = (id) => {
    setProcesses(processes.filter((process) => process.id !== id));
  };

  const handleChange = (id, field, value) => {
    setProcesses(
      processes.map((process) =>
        process.id === id ? { ...process, [field]: value } : process
      )
    );
  };
  // const handleResponseType = (type) => {
  //   setResponseType(type); // "AI" or "Simple"
  //   console.log("Type Selected :", type)
  // };

  const handlePopupSubmit = (data) => {
    setGanttData([]);
    setPriorityGanttData([]);
    setRoundRobinGanttData([]);
    setSjfGanttData([]);
    setShowSoftMetrics(false);
    setShowAiWhy(false);
  
    if (data.responseType === "AI") {
      console.log("Parent AI Response Selected");
      get_ai_data();
    }else{
  
      if (!data || !Array.isArray(data.selected)) {
        console.warn("Invalid data or missing selected algorithms");
        return;
      }
    
      console.log("Selected Algorithms:", data.selected);
      console.log("Time Quantum:", data.timeQuantum);
    
      if (data.selected.includes("FCFS")) {
        get_fcfs_scheduling_data();
      }
      if (data.selected.includes("SJF")) {
        get_sjf_scheduling_data();
      }
      if (data.selected.includes("Priority")) {
        get_priority_scheduling_data();
      }
      if (data.selected.includes("Round Robin")) {
        get_round_robin_data(data.timeQuantum);
      }
    }
  };

  const get_ai_data = async () => {
    try{
      const response = await fetch('http://localhost:5000/generate_ai_response');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      setAiData(data)
      console.log("AI DATA :", data); 
      const all = ["FCFS", "SJF", "Priority", "Round Robin"];
      const selected = data.predicted_best_algo;

      const remaining = all.filter(a => a !== selected);
      console.log("Remaining Algos :", remaining);  

      setAiAlgo(selected);
      setRemainingAlgos(remaining);

      if (selected === 'SJF') get_sjf_scheduling_data();
      else if (selected === 'FCFS') get_fcfs_scheduling_data();
      else if (selected === 'RR') get_round_robin_data(data.best_time_quantum_if_rr);
      else if (selected === 'Priority') get_priority_scheduling_data();
      else console.warn("Invalid AI algo");

    }catch (error) {
      console.error("Error fetching AI scheduling data:", error);
    }
  }
  

  const get_fcfs_scheduling_data = async () => {
    try {
      const response = await fetch('http://localhost:5000/fcfs_scheduling');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      console.log("FCFS Scheduling Gantt Log:", data);
      setGanttData(data); 
    } catch (error) {
      console.error("Error fetching FCFS scheduling data:", error);
    }
  };

  const get_sjf_scheduling_data = async () => {
    try {
      const response = await fetch('http://localhost:5000/sjf_scheduling');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      console.log("SJF Scheduling Gantt Log:", data);
      setSjfGanttData(data); 
    } catch (error) {
      console.error("Error fetching FCFS scheduling data:", error);
    }
  };

  const get_priority_scheduling_data = async () => {
    try {
      const response = await fetch('http://localhost:5000/priority_scheduling');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      console.log("Priority Scheduling Gantt Log:", data);
      setPriorityGanttData(data); 
    } catch (error) {
      console.error("Error fetching FCFS scheduling data:", error);
    }
  };
  
  const get_round_robin_data = async (quantum) => {
    try {
      const response = await fetch(`http://localhost:5000/roundRobin_scheduling?timeQuantum=${quantum}`);
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      console.log("Round Robin Gantt Log:", data);
      setRoundRobinGanttData(data); // Make sure this state exists
    } catch (error) {
      console.error("Error fetching Round Robin data:", error);
    }
  };
  
  
  const handleSubmit = async () => {
    if(processes.length  <= 2){
      alert("Please Enter "+ (3-processes.length) +" more processes")
      return;
    }
    const jsonData = JSON.stringify(processes);
    
    try {
      const response = await fetch("http://127.0.0.1:5000/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsonData,
      });
  
      const data = await response.json();
      setShowPopup(true);
      
    } catch (error) {
      console.error("Error sending data:", error);
      alert("Failed to send data to server.");
    }
    // await get_fcfs_scheduling_data();
    // await get_sjf_scheduling_data();
    // await get_priority_scheduling_data();
  };
  

  // Function to generate and download JSON file
  const downloadJSON = () => {
    if(processes.length  <= 2){
      alert("Please Enter "+ (3-processes.length) +" more processes")
      return;
    }
    // return JSON.stringify(processes, null, 2);
    const jsonData = JSON.stringify(processes, null, 2);
    const blob = new Blob([jsonData], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    // Create a temporary <a> element and trigger download
    const a = document.createElement("a");
    a.href = url;
    a.download = "processes.json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };
  const metricNameMap = {
    avg_rt: "Average Response Time",
    avg_tat: "Average Turnaround Time",
    avg_wt: "Average Waiting Time",
    fairness: "Fairness Score",
    priority_violations: "Priority Violations",
    starved: "Starved Processes"
  };

  return (
    <div className="p-4 text-left">
      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-200">
            <th className="border border-gray-300 p-2">Process ID</th>
            <th className="border border-gray-300 p-2">Arrival Time</th>
            <th className="border border-gray-300 p-2">Burst Time</th>
            <th className="border border-gray-300 p-2">Priority</th>
            <th className="border border-gray-300 p-2">Action</th>
          </tr>
        </thead>
        <tbody>
          {processes.length === 0 ? (
            <tr>
              <td colSpan="5" className="text-center p-4 text-gray-500">
                No processes added yet.
              </td>
            </tr>
          ) : (
            processes.map((process) => (
              <tr key={process.id} className="border border-gray-300">
                <td className="border border-gray-300 p-2">{process.id}</td>

                {/* Arrival Time Input */}
                <td className="border border-gray-300 p-2">
                  <input
                    type="number"
                    min={1}
                    value={process.arrivalTime}
                    onChange={(e) => handleChange(process.id, "arrivalTime", e.target.value)}
                    placeholder="Enter Arrival Time"
                    className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  />
                </td>

                {/* Burst Time Input */}
                <td className="border border-gray-300 p-2">
                  <input
                    type="number"
                    value={process.burstTime}
                    onChange={(e) => handleChange(process.id, "burstTime", e.target.value)}
                    placeholder="Enter Burst Time"
                    className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  />
                </td>

                {/* Priority Input */}
                <td className="border border-gray-300 p-2">
                  <input
                    type="number"
                    value={process.priority}
                    onChange={(e) => handleChange(process.id, "priority", e.target.value)}
                    placeholder="Enter Priority"
                    className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  />
                </td>

                {/* Remove Button */}
                <td className="border border-gray-300 p-2">
                  <button 
                    onClick={() => removeProcess(process.id)} 
                    className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                  >
                    Remove
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      <button 
        onClick={addProcess} 
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
        Add Process
      </button>
      
      <div className="w-fit mx-auto mt-4">
        <button 
          onClick={handleSubmit} 
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
          Submit Data
        </button>
      </div>
      {!aiAlgo && (
        <Popup
          isOpen={showPopup}
          onClose={() => setShowPopup(false)}
          onSubmit={handlePopupSubmit}
          // onResponseType={handleResponseType}
        />
      )}
      {/* <div className="w-fit mx-auto m-10">
        {chart && (
            <>
                <img src={chart} alt="Gantt Chart" height={100} />
                {alert("Gantt chart generated Successfully")}
            </>
        )} */}
      {/* </div> */}
      {/* Gantt chart section */}
      <AlgoCharts ganttData = {ganttData} sjfGanttData = {sjfGanttData} priorityGanttData = {priorityGanttData} roundRobinGanttData = {roundRobinGanttData} />
      
      {aiAlgo && (
        <div>
          <div className="text-left mt-6">
            <h2 className="text-xl font-bold mb-2">AI Suggested: {aiAlgo}</h2>
            <div className="flex justify-start gap-4 mt-4">
              <button onClick={scrollToWhy} className="px-4 py-2 bg-purple-500 text-white rounded">
                Why?
              </button>
              <button onClick={scrollToMetrics} className="px-4 py-2 bg-indigo-500 text-white rounded">
                Show Soft Metrics
              </button>
              <button onClick={() => setShowPopup(true)} className="px-4 py-2 bg-yellow-500 text-black rounded">
                Need Other Algos
              </button>
            </div>
          </div>
          {showAiWhy && (
            <div ref = {whyRef} className="mt-4 p-4 border border-gray-300 rounded bg-white shadow-md">
              <h3 className="font-semibold mb-2">Why this algorithm?</h3>
              {/* <p>The AI chose <strong>{aiAlgo}</strong> because it had the best combination of turnaround time, waiting time, fairness, and priority respect based on the process set.</p> */}
              {aiData.explanation}
            </div>
          )}
    
          {showSoftMetrics && (
            <div ref={metricsRef} className="mt-4 p-4 border border-gray-300 rounded bg-white shadow-md">
              <button className="float-right mr-2 px-3 py-1 border border-gray-300 rounded-md text-sm text-gray-700 hover:bg-gray-100 transition"
              onClick={()=>setShowSoftMetrics(false)}>
                  Hide
              </button>
    
              <h3 className="text-xl font-bold mb-2">Soft Metrics</h3>
              {/* Replace this with actual metrics component if needed */}
              <ul>
                {Object.entries(aiData.soft_metrics).map(([algo, metrics]) => (
                  <li key={algo} style={{ marginBottom: "1rem" }}>
                    <span style={{ fontWeight: "700" }}>{algo}</span>
                    <div style={{ marginLeft: "1rem", color: "#666", fontSize: "0.95rem" }}>
                      {Object.entries(metrics).map(([metric, value], index, arr) => (
                        <span key={metric}>
                          <span style={{ fontWeight: 600 }}>{metricNameMap[metric] || metric}:</span> {value}
                          {index < arr.length - 1 ? ", " : "."}
                        </span>
                      ))}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
          <Popup
          isOpen={showPopup}
          onClose={() => setShowPopup(false)}
          onSubmit={handlePopupSubmit}
          // onResponseType={handleResponseType}
          algoList={remainingAlgos}
          aiButton={false}
          />

        </div>
      )}
      
      
    </div>
  );
}
