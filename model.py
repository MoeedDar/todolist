from pydantic import BaseModel
from database import Database

class Task(BaseModel):
    id: int
    description: str
    completed: bool

    @staticmethod
    def create_table(db: Database):
        query = '''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE
            )
        '''
        db.execute(query)

    @staticmethod
    def get_tasks(db: Database):
        query = "SELECT * FROM tasks"
        result = db.execute_fetchall(query)
        return map(lambda row: Task(id=row[0], description=row[1], completed=row[2]), result)

    @staticmethod
    def create_task(db: Database, description: str):
        query = "INSERT INTO tasks (description) VALUES (?)"
        db.execute(query, (description,))

    @staticmethod
    def update_task(db: Database, id: int):
        query = "UPDATE tasks SET completed = NOT completed WHERE id = ?"
        db.execute(query, (id,))

    @staticmethod
    def remove_task(db: Database, id: int):
        query = "DELETE FROM tasks WHERE id = ?"
        db.execute(query, (id,))
