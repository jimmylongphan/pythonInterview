package assignment

import (
	"encoding/csv"
	"os"
	"strconv"
	"strings"
)

// LoadTasks loads tasks from a CSV file
func LoadTasks(filename string) (map[int]*Task, error) {
	tasks := make(map[int]*Task)

	// Open the file for reading
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	// Read all records from the CSV file
	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	for _, record := range records[1:] { // Skip the header line
		id, _ := strconv.Atoi(record[0])
		name := record[1]
		volunteersNeeded, _ := strconv.Atoi(record[2])
		description := record[3]

		// Create a new Task instance and add it to the tasks map
		tasks[id] = &Task{ID: id, Name: name, VolunteersNeeded: volunteersNeeded, Description: description}
	}
	return tasks, nil
}

// LoadVolunteers loads volunteers from a CSV file
func LoadVolunteers(filename string, tasks map[int]*Task) ([]*Volunteer, error) {
	volunteers := make([]*Volunteer, 0)

	// Open the file for reading
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	// Read all records from the CSV file
	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	for _, record := range records[1:] { // Skip the header line
		id, _ := strconv.Atoi(record[0])
		name := record[1]

		// Create the list of preferred task ordering
		//

		// Create a new Volunteer instance
		volunteer := Volunteer{ID: id, Name: name}

		// Add the task to the volunteer's interested tasks
		taskIDs := record[2]
		for _, taskID := range strings.Fields(taskIDs) {
			taskIDInt, _ := strconv.Atoi(taskID)
			if task, ok := tasks[taskIDInt]; ok {
				volunteer.AddInterestedTask(task)
			}
		}
		// Add the volunteer to the volunteers slice
		volunteers = append(volunteers, &volunteer)
	}

	return volunteers, nil
}
