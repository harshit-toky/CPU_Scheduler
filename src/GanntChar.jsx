// import { Chart } from "react-google-charts";

// export default function GanttChart({ ganttData }) {
//   // Base start time
//   const latestEnd = Math.max(...ganttData.map((entry) => entry.end));

//   const baseTime = new Date(2023, 0, 1, 9, 0, 0); // Jan 1, 2023 09:00:00

//   // Clone and extend ganttData with a hidden padding row
//   const extendedData = [
//     ...ganttData,
//     {
//       id: "zzzz",
//       start: latestEnd+5,
//       end: latestEnd+6, // adjust as needed
//       isPadding: true,
//     },
//   ];
//   let id = 1
//   const chartData = [
//     [
//       { type: "string", label: "Task ID" },
//       { type: "string", label: "Task Name" },
//       { type: "string", label: "Resource" },
//       { type: "date", label: "Start" },
//       { type: "date", label: "End" },
//       { type: "number", label: "Duration" },
//       { type: "number", label: "Percent Complete" },
//       { type: "string", label: "Dependencies" },
//     ],
//     ...extendedData.map((entry) => {
//       const startDate = new Date(baseTime.getTime() + entry.start * 60000);
//       const endDate = new Date(baseTime.getTime() + entry.end * 60000);
//       return [
//         `P${id++}`,
//         entry.isPadding ? "" : `P${entry.id}`,
//         entry.isPadding ? "padding" : "normal", // this maps to the palette
//         startDate,
//         endDate,
//         null,
//         entry.isPadding ? 0 : entry.percent_complete || 100,
//         null,
//       ];
//     }),
    
//   ];

//   const options = {
//     height: 100 + ganttData.length * 40,
//     gantt: {
//       trackHeight: 30,
//       labelStyle: {
//         fontName: "Arial",
//         fontSize: 14,
//         color: "#757575",
//       },
//       criticalPathEnabled: false,
//       barCornerRadius: 4,
//       palette: [
//         {
//           color: "#76A7FA", // Normal task color
//           dark: "#003F5C",
//           light: "#C8D8F8",
//         },
//         {
//           color: "transparent", // Padding row color (fully transparent)
//           dark: "transparent",
//           light: "transparent",
//         },
//       ],
//     },
//   };
  

//   return (
//     <div className="p-4">
//       <Chart
//         chartType="Gantt"
//         width="100%"
//         height={`${options.height}px`}
//         data={chartData}
//         options={options}
//         loader={<div>Loading Chart...</div>}
//       />
//     </div>
//   );
// }
import { Chart } from "react-google-charts";

export default function GanttChart({algoTitle,  ganttData }) {
  // Base start time
  const latestEnd = Math.max(...ganttData.map((entry) => entry.end));
  const baseTime = new Date(2023, 0, 1, 0, 0, 0); // Jan 1, 2023 09:00:00
  // const baseTime = new Date(0)

  // Padding to extend chart visibility
  // const extendedData = [
  //   ...ganttData
  //   // {
  //   //   id: "zzzz",
  //   //   start: latestEnd + 5,
  //   //   end: latestEnd + 6,
  //   //   isPadding: true,
  //   // },
  // ];

  // Timeline-specific chart data
  const chartData = [
    [
      { type: "string", id: "Process" },   // Determines row
      { type: "string", id: "Slice" },     // Label shown in the bar
      { type: "date", id: "Start" },
      { type: "date", id: "End" },
    ],
    ...ganttData.map((entry, index) => {
      const startDate = new Date(baseTime.getTime() + entry.start * 1000);
      const endDate = new Date(baseTime.getTime() + entry.end * 1000);
      // const startDate = new Date(0, 0, 0, 0, 0, entry.start);
      // const endDate = new Date(0, 0, 0, 0, 0, entry.end);
      return [
        `P${entry.id}`,                                     // Same id = same row
        `P${entry.id} (${entry.percent_complete || 100}%)`,
        startDate,
        endDate,
      ];
    }),
  ];

  const options = {
    title : algoTitle,
    timeline: {
      showRowLabels: true,
      colorByRowLabel: true,
      rowLabelStyle: {
        fontName: "Arial",
        fontSize: 14,
        color: "#757575",
      },
    },
    // hAxis: {
    //   minValue: new Date(0, 0, 0, 0, 0, 0), // Start at 0 seconds
    //   maxValue: new Date(0, 0, 0, 0, 0, latestEnd), // End at totalTime seconds
    //   format: 's', // Display in seconds (can also use 'm:ss')
    // },
    avoidOverlappingGridLines: false,
    height: 100 + ganttData.length * 40,
  };

  return (
    <div className="p-4">
      <h2 className="text-2xl font-semibold text-center text-gray-700 mb-4">
        {algoTitle}
      </h2>

      <Chart
        chartType="Timeline"
        width="100%"
        height={`${options.height}px`}
        data={chartData}
        options={options}
        loader={<div>Loading Chart...</div>}
      />
    </div>
  );
}
