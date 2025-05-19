package main

import (
	"./assignment"
)

func main() {
	// Load tasks from the CSV file
	tasks, err := assignment.LoadTasks("tasks.csv")
	if err != nil {
		panic(err)
	}

	// Load volunteers from the CSV file
	volunteers, err := assignment.LoadVolunteers("volunteers.csv", tasks)
	if err != nil {
		panic(err)
	}

	server := assignment.NewAssignmentServer(tasks, volunteers)

	// Assign tasks to volunteers
	server.AssignTasks()
	// Print the assignments of tasks to volunteers
	server.PrintAssignments()

	// Print the overal satisfaction score
	server.PrintSatisfactionScore(volunteers)

}
