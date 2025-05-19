package assignment

import (
	"fmt"
	"sort"
)

// AssignmentServer handles the assignment of tasks to volunteers
type AssignmentServer struct {
	Tasks      map[int]*Task
	Volunteers []*Volunteer
	// Assignments map[int]*Volunteer

	// key is task id
	// val is another dict of volunteer ids
	Assignments map[int]map[int]*Volunteer
}

func NewAssignmentServer(tasks map[int]*Task, volunteers []*Volunteer) *AssignmentServer {
	return &AssignmentServer{
		Tasks:       tasks,
		Volunteers:  volunteers,
		Assignments: make(map[int]map[int]*Volunteer),
	}
}

// GetInterestedVolunteers returns a list of volunteers interested in a specific task
func (as *AssignmentServer) GetInterestedVolunteers(task *Task) []*Volunteer {
	var interestedVolunteers []*Volunteer
	for _, volunteer := range as.Volunteers {
		_, interested := volunteer.IsInterested(task)
		if interested {
			interestedVolunteers = append(interestedVolunteers, volunteer)
		}
	}
	return interestedVolunteers
}

// AssignTasks assigns tasks to volunteers based on their interests
func (as *AssignmentServer) AssignTasks() {
	for _, task := range as.Tasks {
		as.AssignTask(task)
	}
}

// Method to assign an individual task
// Ensure tasks with multi-persons are assigned correctly
func (as *AssignmentServer) AssignTask(task *Task) {
	for task.VolunteersNeeded > 0 {
		interestedVolunteers := as.GetInterestedVolunteers(task)
		assigned := false
		if len(interestedVolunteers) > 0 {
			assigned = as.AssignTaskToVolunteer(task, interestedVolunteers)
		}

		// assign to anyone else
		if !assigned {
			as.AssignTaskToVolunteer(task, as.Volunteers)
		}
	}
}

func (as *AssignmentServer) AssignTaskToVolunteer(task *Task, volunteers []*Volunteer) bool {
	for _, volunteer := range volunteers {
		// Initialize inner set if it doesn't exist
		if _, exists := as.Assignments[task.ID]; !exists {
			as.Assignments[task.ID] = make(map[int]*Volunteer)
		}

		// check if already assigned
		if _, ok := as.Assignments[task.ID][volunteer.ID]; ok {
			continue
		}

		// If there are interested volunteers, assign the task to the first available one
		as.Assignments[task.ID][volunteer.ID] = volunteer

		// calculate the individual score
		volunteer.AssignTaskScore(task.ID)

		// decrement the volunteers needed
		task.VolunteersNeeded--

		// able to assign a volunteer
		return true
	}

	// not successful at assigning a volunteer
	return false
}

// PrintAssignments prints the assignments of tasks to volunteers
func (as *AssignmentServer) PrintAssignments() {
	// Extract and sort task IDs
	taskIDs := make([]int, 0, len(as.Tasks))
	for id := range as.Tasks {
		taskIDs = append(taskIDs, id)
	}
	sort.Ints(taskIDs)

	// Print assignments sorted by task ID
	for _, id := range taskIDs {
		task := as.Tasks[id]
		fmt.Println(task)
		if assignees, ok := as.Assignments[task.ID]; ok {
			for _, assignee := range assignees {
				fmt.Printf("    Assigned to %s\n", assignee)
			}
		} else {
			fmt.Println("    Unassigned")
		}
		fmt.Println()
	}
}

// Method to sum all of the volunteers satisfaction scores
func (as *AssignmentServer) PrintSatisfactionScore(volunteers []*Volunteer) {
	// Get the overall quality of assignments
	overallSatisfactionScore := 0
	for _, volunteer := range volunteers {
		overallSatisfactionScore += volunteer.GetTaskTotalScore()
		// fmt.Printf("Volunteer %s overall satisfaction score %d\n", volunteer.Name, volunteer.GetTaskTotalScore())
	}
	fmt.Printf("Overall satisfaction score %d\n", overallSatisfactionScore)
}
