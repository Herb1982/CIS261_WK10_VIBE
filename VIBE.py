import os
import sys

STORAGE_FILE = "student_grades.txt"

students = []


def calculate_average(test1, test2, test3):
    return round((test1 + test2 + test3) / 3, 2)


def calculate_grade(average):
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def format_score(value):
    return f"{value:.2f}"


def load_students():
    if not os.path.exists(STORAGE_FILE):
        return

    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 7:
                    print(f"Warning: Skipping malformed record on line {line_number}.")
                    continue

                name, student_id, t1, t2, t3, avg, grade = parts
                try:
                    test1 = float(t1)
                    test2 = float(t2)
                    test3 = float(t3)
                    average = float(avg)
                except ValueError:
                    print(f"Warning: Invalid numeric values on line {line_number}. Skipping record.")
                    continue

                students.append({
                    "name": name,
                    "id": student_id,
                    "test1": test1,
                    "test2": test2,
                    "test3": test3,
                    "average": average,
                    "grade": grade,
                })
    except IOError as error:
        print(f"Error reading {STORAGE_FILE}: {error}")


def save_students():
    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as file:
            for student in students:
                file.write(
                    "|".join(
                        [
                            student["name"],
                            student["id"],
                            format_score(student["test1"]),
                            format_score(student["test2"]),
                            format_score(student["test3"]),
                            format_score(student["average"]),
                            student["grade"],
                        ]
                    )
                    + "\n"
                )
    except IOError as error:
        print(f"Error saving to {STORAGE_FILE}: {error}")


def prompt_for_score(prompt_text):
    while True:
        value = input(prompt_text).strip()
        if value.upper() == "ESC":
            return None
        try:
            score = float(value)
            if score < 0 or score > 100:
                print("Please enter a score between 0 and 100.")
                continue
            return score
        except ValueError:
            print("Invalid input. Enter a numeric score or ESC to cancel.")


def add_student():
    print("\nEnter new student information (type ESC at any prompt to cancel).")

    name = input("Student name: ").strip()
    if name.upper() == "ESC":
        return

    student_id = input("Student ID: ").strip()
    if student_id.upper() == "ESC":
        return

    test1 = prompt_for_score("Test 1 score: ")
    if test1 is None:
        return

    test2 = prompt_for_score("Test 2 score: ")
    if test2 is None:
        return

    test3 = prompt_for_score("Test 3 score: ")
    if test3 is None:
        return

    average = calculate_average(test1, test2, test3)
    grade = calculate_grade(average)

    students.append({
        "name": name,
        "id": student_id,
        "test1": test1,
        "test2": test2,
        "test3": test3,
        "average": average,
        "grade": grade,
    })

    print(f"Student '{name}' added with average {format_score(average)} and grade {grade}.")


def display_students():
    if not students:
        print("\nNo student records available.")
        return

    print("\nStudent Records")
    print("=" * 87)
    header = (
        "Name".ljust(20)
        + "ID".ljust(12)
        + "Test 1".rjust(8)
        + "Test 2".rjust(9)
        + "Test 3".rjust(9)
        + "Average".rjust(10)
        + "Grade".rjust(9)
    )
    print(header)
    print("-" * 87)

    for student in students:
        print(
            f"{student['name'][:20].ljust(20)}"
            f"{student['id'][:12].ljust(12)}"
            f"{format_score(student['test1']).rjust(8)}"
            f"{format_score(student['test2']).rjust(9)}"
            f"{format_score(student['test3']).rjust(9)}"
            f"{format_score(student['average']).rjust(10)}"
            f"{student['grade'].rjust(9)}"
        )


def class_statistics():
    if not students:
        print("\nNo student records available to calculate statistics.")
        return

    averages = [student["average"] for student in students]
    highest = max(averages)
    lowest = min(averages)
    overall = round(sum(averages) / len(averages), 2)

    print("\nClass Statistics")
    print("=" * 20)
    print(f"Highest average: {format_score(highest)}")
    print(f"Lowest average:  {format_score(lowest)}")
    print(f"Class average:   {format_score(overall)}")


def search_student():
    if not students:
        print("\nNo student records available.")
        return

    query = input("Enter student name to search: ").strip()
    if query.upper() == "ESC":
        return

    found = [s for s in students if query.lower() in s["name"].lower()]

    if not found:
        print(f"No students found matching '{query}'.")
        return

    print(f"\nFound {len(found)} student(s) matching '{query}':")
    print("-" * 87)
    print(
        "Name".ljust(20)
        + "ID".ljust(12)
        + "Test 1".rjust(8)
        + "Test 2".rjust(9)
        + "Test 3".rjust(9)
        + "Average".rjust(10)
        + "Grade".rjust(9)
    )
    print("-" * 87)
    for student in found:
        print(
            f"{student['name'][:20].ljust(20)}"
            f"{student['id'][:12].ljust(12)}"
            f"{format_score(student['test1']).rjust(8)}"
            f"{format_score(student['test2']).rjust(9)}"
            f"{format_score(student['test3']).rjust(9)}"
            f"{format_score(student['average']).rjust(10)}"
            f"{student['grade'].rjust(9)}"
        )


def print_menu():
    print("\nStudent Grade Calculator")
    print("=" * 24)
    print("1. Add new student record")
    print("2. Display all students")
    print("3. Show class statistics")
    print("4. Search student by name")
    print("5. Save records and exit")
    print("Type ESC at any menu prompt to exit without saving.")


def main():
    print("Loading student records...")
    load_students()
    print(f"Loaded {len(students)} records from {STORAGE_FILE}.\n")

    while True:
        print_menu()
        choice = input("Select an option: ").strip()
        if choice.upper() == "ESC":
            print("Exiting without saving. Goodbye!")
            sys.exit(0)

        if choice == "1":
            add_student()
            continue
        if choice == "2":
            display_students()
            continue
        if choice == "3":
            class_statistics()
            continue
        if choice == "4":
            search_student()
            continue
        if choice == "5":
            save_students()
            print(f"Records saved to {STORAGE_FILE}. Goodbye!")
            sys.exit(0)

        print("Invalid selection. Please choose a number from 1 to 5, or type ESC to exit.")


if __name__ == "__main__":
    main()
