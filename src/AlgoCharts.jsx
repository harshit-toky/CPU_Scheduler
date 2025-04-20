import React from 'react'
import GanttChart from './GanntChar'

export default function AlgoCharts({ganttData, sjfGanttData, priorityGanttData, roundRobinGanttData}) {
  return (
    <div>
    {ganttData?.gantt_log?.length > 0 && (
        <div className="mt-4">
          <GanttChart algoTitle={"FCFS Scheduling Algorithm"} Data={ganttData} />
        </div>
      )}
    
      {sjfGanttData?.gantt_log?.length > 0 && (
        <div className="">
          <GanttChart algoTitle={"SJF Scheduling Algorithm"} Data={sjfGanttData} />
        </div>
      )}
    
      {priorityGanttData?.gantt_log?.length > 0 && (
        <div className="">
          <GanttChart algoTitle={"Priority Scheduling Algorithm"} Data={priorityGanttData} />
        </div>
      )}
    
      {roundRobinGanttData?.gantt_log?.length > 0 && (
        <div className="">
          <GanttChart algoTitle={"Round Robin Scheduling Algorithm"} Data={roundRobinGanttData} />
        </div>
      )}
      </div>
  )
}