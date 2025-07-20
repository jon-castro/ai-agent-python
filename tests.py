from functions.run_python import run_python_file

def run_tests():
    print('run_python_file("calculator", "main.py"):')
    print(run_python_file("calculator", "main.py"))
    print("\n")

    print('run_python_file("calculator", "main.py", ["3 + 5"]):')
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("\n")

    print('run_python_file("calculator", "tests.py"):')
    print(run_python_file("calculator", "tests.py"))
    print("\n")

    print('run_python_file("calculator", "../main.py"):')
    print(run_python_file("calculator", "../main.py"))
    print("\n")

    print('run_python_file("calculator", "nonexistent.py"):')
    print(run_python_file("calculator", "nonexistent.py"))
    print("\n")

if __name__ == "__main__":
    run_tests()
