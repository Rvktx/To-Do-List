from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from task import Base, Task
import config


class Database:
    engine = create_engine(config.DB)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    @staticmethod
    def read_all(missed=False, completed=False):
        if missed:
            tasks = Database.session.query(Task).filter(Task.deadline < datetime.today()).all()
        elif completed:
            tasks = Database.session.query(Task).filter(Task.completed == True).all()
        else:
            tasks = Database.session.query(Task).all()

        if len(tasks) < 1:
            print("There is no tasks")
        else:
            for i, task in enumerate(tasks, 1):
                print('{}. {}'.format(i, task.task))

    @staticmethod
    def read_day(day=datetime.today()):
        date = day.strftime('%A %d %b')
        print(date)

        tasks = Database.session.query(Task).filter(Task.deadline == day.date(),
                                                    Task.completed == False).all()
        if len(tasks) < 1:
            print("There is no tasks this day")
        else:
            for i, task in enumerate(tasks, 1):
                print('{}. {}'.format(i, task.task))

    @staticmethod
    def read_week():
        for dt in range(7):
            day = datetime.today() + timedelta(days=dt)
            Database.read_day(day)

    @staticmethod
    def add():
        task_in = input('Enter task name or "0" if you want to go back:\n')
        if task_in == '0':
            return
        elif task_in == '':
            task_in = 'Unnamed task'
        try:
            deadline_in = input("Enter deadline in YYYY-MM-DD format or leave blank for today's date:\n")
            if deadline_in == '':
                deadline_db = datetime.today()
            else:
                deadline_db = datetime.strptime(deadline_in, '%Y-%m-%d')
            new_task = Task(task=task_in, deadline=deadline_db.date())

            Database.session.add(new_task)
            Database.session.commit()
            print('The task has been added!')
        except ValueError:
            print('Enter correct deadline')
            Database.add()

    @staticmethod
    def mark_completed():
        tasks = Database.session.query(Task).filter(Task.completed == False).all()
        ids = {}

        if len(tasks) < 1:
            print("There is no uncompleted tasks")
        else:
            try:
                print('Chose the number of the task you want to mark as completed or "0" if you want to go back:')
                for i, task in enumerate(tasks, 1):
                    print('{}. {}. {}'.format(i, task.task, task.deadline.strftime('%d, %b')))
                    ids[i] = task.id

                choice = int(input())
                if choice == 0:
                    return
                task = Database.session.query(Task).get(ids[choice])
                task.completed = True
                Database.session.commit()
                print("The task has been marked as completed")
            except KeyError:
                print("Enter correct number!")
                Database.mark_completed()

    @staticmethod
    def remove():
        tasks = Database.session.query(Task).all()
        ids = {}

        if len(tasks) < 1:
            print("Nothing to remove")
        else:
            try:
                print('Chose the number of the task you want to delete or "0" if you want to go back:')
                for i, task in enumerate(tasks, 1):
                    print('{}. {}. {}'.format(i, task.task, task.deadline.strftime('%d, %b')))
                    ids[i] = task.id

                choice = int(input())
                if choice == 0:
                    return
                Database.session.query(Task).filter(Task.id == ids[choice]).delete()
                Database.session.commit()
                print("The task has been removed from database")
            except KeyError:
                print("Enter correct number!")
                Database.mark_completed()
                Database.remove()
