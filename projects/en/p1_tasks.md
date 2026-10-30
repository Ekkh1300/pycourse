# Project 1 — Task Manager

A simple task management application where users can:
- Add tasks
- List all tasks
- Mark tasks as complete
- Remove tasks
- View task details

## Requirements:
1. Store tasks in a JSON file (tasks.json)
2. Each task has: id, title, done (boolean)
3. Use command-line arguments to control the application
4. Handle invalid inputs gracefully

## Commands:
- `python tasks.py add "Task title"` - Add a new task
- `python tasks.py list` - List all tasks
- `python tasks.py done <id>` - Mark task <id> as complete
- `python tasks.py remove <id>` - Remove task <id>
- `python tasks.py list` - List all tasks

## Example:
```bash
python tasks.py add "Buy groceries"
python tasks.py list
# Output:
# 1: [ ] Buy groceries
# 2: [x] Read documentation

python tasks.py done 1
python tasks.py list
# Output:
# 1: [x] Buy groceries
# 2: [x] Read documentation