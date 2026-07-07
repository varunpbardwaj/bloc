import { useState } from "react";

type Task = {
    id: string;
    label: string;
    done: boolean;
};

export function TaskList({ title }: { title: string }) {
    const [tasks, setTasks] = useState<Task[]>([
        { id: "1", label: "Fix nav layout", done: true },
        { id: "2", label: "Add unit tests", done: false },
    ]);

    const toggleTask = (id: string) => {
        setTasks((prev) =>
            prev.map((task) =>
                task.id === id ? { ...task, done: !task.done } : task,
            ),
        );
    };

    return (
        <section className="task-list">
            <h2>{title}</h2>
            <ul>
                {tasks.map((task) => (
                    <li key={task.id}>
                        <input
                            type="checkbox"
                            checked={task.done}
                            onChange={() => toggleTask(task.id)}
                        />
                        <span>{task.label}</span>
                    </li>
                ))}
            </ul>
        </section>
    );
}
