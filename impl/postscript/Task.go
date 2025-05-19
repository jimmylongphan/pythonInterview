package assignment

import "fmt"

// Task represents a task with an ID, name, and description.
type Task struct {
	ID               int
	Name             string
	VolunteersNeeded int
	Description      string
}

func (t Task) String() string {
	return fmt.Sprintf("Task #%d: %s", t.ID, t.Name)
}
