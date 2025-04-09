import { useState } from "react";
import GanttChart from "./GanntChar";
import Popup from "./Popup";

export default function ProcessTable() {
  const [processes, setProcesses] = useState([]);
  const [ganttData, setGanttData] = useState([]);
  const [sjfGanttData, setSjfGanttData] = useState([]);
  const [priorityGanttData, setPriorityGanttData] = useState([]);
  const [showPopup, setShowPopup] = useState(false);
  const [roundRobinGanttData, setRoundRobinGanttData] = useState([]);


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

  const handlePopupSubmit = (data) => {
    console.log("Selected Algorithms:", data.selected);
    console.log("Time Quantum:", data.timeQuantum);
    setGanttData([])
    setPriorityGanttData([])
    setRoundRobinGanttData([])
    setSjfGanttData([])
  
    // Example functions for each algorithm
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
      get_round_robin_data(data.timeQuantum); // pass quantum if needed
    }
  };
  

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
      <Popup
        isOpen={showPopup}
        onClose={() => setShowPopup(false)}
        onSubmit={handlePopupSubmit}
      />
      {/* <div className="w-fit mx-auto m-10">
        {chart && (
            <>
                <img src={chart} alt="Gantt Chart" height={100} />
                {alert("Gantt chart generated Successfully")}
            </>
        )} */}
      {/* </div> */}
      {/* Gantt chart section */}
      {ganttData.length > 0 && (
        <div className="mt-4">
          {/* <h2 className="text-xl font-semibold mb-2">Gantt Chart</h2> */}
          <GanttChart algoTitle={"FCFS Scheduling Algorithm"} ganttData={ganttData} />
        </div>
      )}
      {sjfGanttData.length > 0 && (
        <div className="">
          {/* <h2 className="text-xl font-semibold mb-2">Gantt Chart</h2> */}
          <GanttChart algoTitle = {"SJF Scheduling Algorithm"} ganttData={sjfGanttData} />
        </div>
      )}
      {priorityGanttData.length > 0 && (
        <div className="">
          {/* <h2 className="text-xl font-semibold mb-2">Gantt Chart</h2> */}
          <GanttChart algoTitle = {"Priority Scheduling Algorithm"} ganttData={priorityGanttData} />
        </div>
      )}
      {roundRobinGanttData.length > 0 && (
        <div className="">
          {/* <h2 className="text-xl font-semibold mb-2">Gantt Chart</h2> */}
          <GanttChart algoTitle = {"Round Robin Scheduling Algorithm"} ganttData={roundRobinGanttData} />
        </div>
      )}
    </div>
  );
}
