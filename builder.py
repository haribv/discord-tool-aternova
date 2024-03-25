import os

class PythonBuilder:
    def __init__(self):
        self.banner = """
        *****************************************
        *                                       *
        *        ATERNOVA BUILDER               *
        *                                       *
        *****************************************
        """

    def show_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')  
            print(self.banner)
            print("[1] Build Aternova In Folder")
            print("[2] Build Out Folder")
            print("[3] Quit")
            choice = input("Please select an option: ")

            if choice == '1':
                self.build('main.py')
            elif choice == '2':
                filename = input("Enter the path of the Python file to build: ")
                self.build(filename)
            elif choice == '3':
                print("Exiting...")
                break
            else:
                input("Invalid option! Press Enter to continue...")

    def build(self, filename):

        os.system(f'pyinstaller --onefile {filename}')

        print("Build completed! Executable file is in the 'dist' directory.")
        input("Press Enter to continue...")

if __name__ == "__main__":
    builder = PythonBuilder()
    builder.show_menu()
