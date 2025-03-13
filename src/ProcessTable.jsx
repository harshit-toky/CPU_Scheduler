import { useState } from "react";

export default function ProcessTable() {
  const [processes, setProcesses] = useState([]);

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
  
      const result = await response.json();
      console.log("Server Response:", result);
      alert(result.message);
    } catch (error) {
      console.error("Error sending data:", error);
      alert("Failed to send data to server.");
    }
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
          onClick={downloadJSON} 
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
          Submit Data
        </button>
      </div>
    </div>
  );
}
