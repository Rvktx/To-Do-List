from database import Database


def main():
    print('Welcome, enter a number to choose a function')
    while True:
        print('')
        print("1. Today's tasks")
        print("2. Week's task")
        print("3. All task")
        print("4. Missed tasks")
        print("5. Completed tasks")
        print("6. Add task")
        print("7. Complete task")
        print("8. Delete task")
        print("0. Exit")

        choice = input('\n')
        if choice == '0':
            print("Exiting now")
            break
        elif choice == '1':
            Database.read_day()
        elif choice == '2':
            Database.read_week()
        elif choice == '3':
            Database.read_all()
        elif choice == '4':
            Database.read_all(missed=True)
        elif choice == '5':
            Database.read_all(completed=True)
        elif choice == '6':
            Database.add()
        elif choice == '7':
            Database.mark_completed()
        elif choice == '8':
            Database.remove()
        else:
            print('Enter valid function')


if __name__ == '__main__':
    main()
