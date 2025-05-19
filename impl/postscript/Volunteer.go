package assignment

import "fmt"

// Volunteer represents a volunteer with an ID, name, and a list of interested tasks
type Volunteer struct {
	ID              int
	Name            string
	InterestedTasks []*Task
	// keep a list of scores for every assigned task
	TaskScores      []int
}

// AddInterestedTask adds a task to the volunteer's list of interested tasks
func (v *Volunteer) AddInterestedTask(task *Task) {
	v.InterestedTasks = append(v.InterestedTasks, task)
}

// RemoveInterestedTask removes a task from the volunteer's list of interested tasks
func (v *Volunteer) RemoveInterestedTask(task *Task) {
	for i, t := range v.InterestedTasks {
		if t.ID == task.ID {
			v.InterestedTasks = append(v.InterestedTasks[:i], v.InterestedTasks[i+1:]...)
			return
		}
	}
}

// IsInterested checks if the volunteer is interested in a given task
func (v *Volunteer) IsInterested(task *Task) bool {
	for _, t := range v.InterestedTasks {
		if t.ID == task.ID {
			return true
		}
	}
	return false
}

func (v Volunteer) String() string {
	return fmt.Sprintf("Volunteer #%d: %s", v.ID, v.Name)
}

// Method to assign the score of a task based on its preference
func (v *Volunteer) AssignTaskScore(taskId int) {
	score := -1
	for index, task := range v.InterestedTasks {
		if task.ID == taskId {
			switch index {
			case 0:
				score = 4
			case 1:
				score = 3
			case 2:
				score = 2
			case 3:
				score = 1
			}
			break
		}
	}
	// fmt.Printf("adding score %d to volunteer %s\n", score, v.Name)
	v.TaskScores = append(v.TaskScores, score)
}

// Method to get the total score of all assigned tasks
func (v *Volunteer) GetTaskTotalScore() int {
	totalScore := 0
	for _, score := range v.TaskScores {
		totalScore += score
		// fmt.Printf("Volunteer %s adding score %d, %d\n", v.Name, score, totalScore)
	}
	return totalScore
}
