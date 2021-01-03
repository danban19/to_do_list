from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import random
import sys

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

    def greetings(self):  # prints greetings and options to choose
        mode = input('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit\n''')
        if mode == '1':
            self.today_tasks()
        elif mode == '2':
            self.week_task()
        elif mode == '3':
            self.all_tasks()
        elif mode == '4':
            self.missed_tasks()
        elif mode == '5':
            self.add_task()
        elif mode == '6':
            self.delete_tasks()
        elif mode == '0':
            print('Bye!')
            sys.exit()
        else:
            self.greetings()

    def today_tasks(self):  # prints today's tasks
        today = datetime.today()
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if not rows:
            print('Nothing to do!\n')
        else:
            print(f'Today {datetime.today().date()}')
            for i in range(len(rows)):
                print(f'{i+1}. {rows[i].task}')
        self.greetings()

    def week_task(self):  # prints current week's tasks
        today = datetime.today().date()
        week_days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        for i in range(7):
            i_day = today + timedelta(days=i)
            rows = session.query(Table).filter(Table.deadline == i_day).all()
            print(f"{week_days.get(i_day.weekday())} {i_day.day} {i_day.strftime('%b')}:")
            if not rows:
                print('Nothing to do!\n')
            else:
                for j in range(len(rows)):
                    print(f'{j + 1}. {rows[j].task}')
                print('\n')
        print('\n')
        self.greetings()

    def all_tasks(self):  # prints all tasks
        rows = session.query(Table).order_by(Table.deadline).all()
        print('All tasks:')
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")
        print('\n')
        self.greetings()

    def missed_tasks(self):  # prints missed tasks (where the date has passed)
        rows = session.query(Table).order_by(Table.deadline).filter(Table.deadline < datetime.today().date()).all()
        if not rows:
            print('''Missed tasks:
Nothing is missed!\n''')
        else:
            print('Missed tasks:')
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")
        print('\n')
        self.greetings()

    def add_task(self):  # adds new tasks to the table
        task = input('Enter task\n')
        deadline = input('Enter deadline\n')
        new_row = Table(id=random.randint(0, 9999), task=task,
                        deadline=datetime.strptime(deadline, '%Y-%m-%d'))
        print('The task has been added!\n')
        session.add(new_row)
        session.commit()
        self.greetings()

    def delete_tasks(self):  # deletes the specific task
        rows = session.query(Table).order_by(Table.deadline).all()
        if not rows:
            print('Nothing to delete')
        else:
            print('Choose the number of the task you want to delete:\n')
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")
            delete_number = int(input())
            session.delete(rows[delete_number-1])
            print('The task has been deleted!\n')
            session.commit()
        self.greetings()


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
todo = Table()
todo.greetings()
