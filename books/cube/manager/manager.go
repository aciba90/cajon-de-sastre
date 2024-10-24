package manager

import (
	"bytes"
	"cube/task"
	"cube/worker"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/golang-collections/collections/queue"
	"github.com/google/uuid"
)

type Manager struct {
	Pending       queue.Queue
	TaskDb        map[uuid.UUID]*task.Task
	EventDb       map[uuid.UUID]*task.TaskEvent
	Workers       []string
	WorkerTaskMap map[string][]uuid.UUID
	TaskWorkerMap map[uuid.UUID]string
	LastWorker    int
}

func New(workers []string) *Manager {
	taskDb := make(map[uuid.UUID]*task.Task)
	eventDb := make(map[uuid.UUID]*task.TaskEvent)
	workerTaskMap := make(map[string][]uuid.UUID)
	taskWorkerMap := make(map[uuid.UUID]string)
	for worker := range workers {
		workerTaskMap[workers[worker]] = []uuid.UUID{}
	}

	return &Manager{
		Pending:       *queue.New(),
		Workers:       workers,
		TaskDb:        taskDb,
		EventDb:       eventDb,
		WorkerTaskMap: workerTaskMap,
		TaskWorkerMap: taskWorkerMap,
	}
}

func (m *Manager) SelectWorker() string {
	// round-robin
	m.LastWorker = m.LastWorker + 1%len(m.Workers)
	return m.Workers[m.LastWorker]
}

func (m *Manager) SendWork() {
	if m.Pending.Len() == 0 {
		log.Println("[manager/SendWork] no work in the queue")
		return
	}

	w := m.SelectWorker()

	e := m.Pending.Dequeue()
	te := e.(task.TaskEvent)
	t := te.Task
	log.Printf("[manager/SendWork] pulled %v of pending queue\n", t)

	m.EventDb[te.ID] = &te
	m.WorkerTaskMap[w] = append(m.WorkerTaskMap[w], te.Task.ID)
	m.TaskWorkerMap[t.ID] = w

	t.State = task.Scheduled
	m.TaskDb[t.ID] = &t

	data, err := json.Marshal(te)
	if err != nil {
		log.Printf("[manager/SendWork] unable to marshal task event object: %v\n", te)
	}

	url := fmt.Sprintf("http://%s/tasks", w)
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(data))
	if err != nil {
		log.Printf("[manager/SendWork] error connecting to %v: %v\n", w, err)
		m.Pending.Enqueue(te)
		return
	}
	d := json.NewDecoder(resp.Body)
	if resp.StatusCode != http.StatusCreated {
		e := worker.ErrResponse{}
		err := d.Decode(&e)
		if err != nil {
			fmt.Printf("[manager/SendWork] error decoding response: %s\n", err.Error())
			return
		}
		log.Printf("[manager/SendWork] response error (%d): %s", e.HTTPStatusCode, e.Message)
		return
	}

	t = task.Task{}
	if err = d.Decode(&t); err != nil {
		fmt.Printf("[manager/SendWork] error decoding response: %s\n", err.Error())
		return
	}
	log.Printf("%#v\n", t)
}

func (m *Manager) updateTasks() {
	for _, worker := range m.Workers {
		log.Printf("[manager] Checking worker %v for task updates", worker)
		url := fmt.Sprintf("http://%s/tasks", worker)
		resp, err := http.Get(url)
		if err != nil {
			log.Printf("[manager] Error connecting to %v: %v\n", worker, err)
			return
		}

		if resp.StatusCode != http.StatusOK {
			log.Printf("[manager] Error sending request: %v\n", err)
		}

		d := json.NewDecoder(resp.Body)
		var tasks []*task.Task
		err = d.Decode(&tasks)
		if err != nil {
			log.Printf("[manager] Error unmarshalling tasks: %s\n", err.Error())
		}

		for _, t := range tasks {
			log.Printf("[manager] Attempting to update task %v\n", t.ID)

			_, ok := m.TaskDb[t.ID]
			if !ok {
				log.Printf("[manager] Task with ID %s not found\n", t.ID)
				return
			}

			if m.TaskDb[t.ID].State != t.State {
				m.TaskDb[t.ID].State = t.State
			}

			m.TaskDb[t.ID].StartTime = t.StartTime
			m.TaskDb[t.ID].FinishTime = t.FinishTime
			m.TaskDb[t.ID].ContainerID = t.ContainerID
		}
	}
}

func (m *Manager) UpdateTasks() {
	for {
		log.Println("[manager/UpdateTasks] Checking for task updates from workers")
		m.updateTasks()
		log.Println("[manager/UpdateTasks] Task updates completed")
		log.Println("[manager/UpdateTasks] Sleeping for 15 seconds")
		time.Sleep(15 * time.Second)
	}
}

func (m *Manager) AddTask(te task.TaskEvent) {
	m.Pending.Enqueue(te)
}

func (m *Manager) GetTasks() []*task.Task {
	tasks := []*task.Task{}
	for _, t := range m.TaskDb {
		tasks = append(tasks, t)
	}
	return tasks
}

func (m *Manager) ProcessTasks() {
	for {
		log.Println("[manager/ProcessTasks] Processing any tasks in the queue")
		m.SendWork()
		log.Println("[manager/ProcessTasks] Sleeping for 10 seconds")
		time.Sleep(10 * time.Second)
	}
}
