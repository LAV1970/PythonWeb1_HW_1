from collections import UserList
from pathlib import Path
import pickle

# TODO: add help string

save_file = Path("notes.bin")


class Note:
    def __init__(self, text):
        self.text = text
        self.tags = self.extract_tags(text)

    def extract_tags(self, text):
        return [word[1:] for word in text.split() if word.startswith("#")]


class NoteBook(UserList):
    def __init__(self):
        super().__init__()
        self.load_notes()

    def load_notes(self):
        try:
            with open(save_file, "rb") as file:
                self.data = pickle.load(file)
                print("Notebook successfully loaded")
        except FileNotFoundError:
            print("Notes file not found. A new notepad has been created.")
        except Exception as e:
            print(f"Error loading notes: {e}")

    def save_notes(self):
        with open(save_file, "wb") as file:
            pickle.dump(self.data, file)
            print("Notes saved successfully")

    def add_note(self, text):
        note = Note(text)
        self.data.append({"text": note.text, "tags": note.tags})
        print("The note is added to the notepad")

    def display_all_notes(self):
        print("\n===== All notes from notebook =====")
        for index, note in enumerate(self.data):
            print(f"Note: {index}, Text: {note['text']}, Tags: {note['tags']}")
        print("==============================\n")

    def extract_tags(self, text):
        return [word[1:] for word in text.split() if word.startswith("#")]

    def search_notes(self, search_text):
        matching_notes = []
        for index, note in enumerate(self.data):
            if search_text.lower() in note["text"].lower():
                matching_notes.append((index, note))

        if matching_notes:
            print("Found records:")
            for index, note in matching_notes:
                print(f"Note: {index}, Text: {note['text']}, Tags: {note['tags']}")
        else:
            print("There are no records matching your search query")

    def sort_notes_by_tags(self):
        self.data.sort(key=lambda note: len(note["tags"]))

    def change_note(self, note_index, new_text):
        if 0 <= note_index < len(self.data):
            note = Note(new_text)
            self.data[note_index] = {"text": note.text, "tags": note.tags}
            print(f"Record with index {note_index} changed in notebook")
        else:
            print("The specified entry index does not exist")

    def delete_note(self, note_index):
        if 0 <= note_index < len(self.data):
            del self.data[note_index]
            print(f"Record with index {note_index} deleted in notebook")
        else:
            print("The specified entry index does not exist")


notebook = NoteBook()


class AddCommand:
    def execute(self, args):
        notebook.add_note(" ".join(args))


class ShowCommand:
    def execute(self, args):
        notebook.display_all_notes()


class SortCommand:
    def execute(self, args):
        notebook.sort_notes_by_tags()
        print("Records sorted")


class FindCommand:
    def execute(self, args):
        notebook.search_notes(" ".join(args))


class ChangeCommand:
    def execute(self, args):
        notebook.change_note(int(args[0]), " ".join(args[1:]))


class DeleteCommand:
    def execute(self, args):
        notebook.delete_note(int(args[0]))


class HelpCommand:
    def execute(self, args):
        help()


COMMAND_HANDLERS = {
    "add": AddCommand(),
    "show": ShowCommand(),
    "sort": SortCommand(),
    "find": FindCommand(),
    "change": ChangeCommand(),
    "delete": DeleteCommand(),
    "help": HelpCommand(),
}


class CommandParser:
    def parse(self, text):
        args = text.strip().split()
        if args[0] in COMMAND_HANDLERS:
            COMMAND_HANDLERS[args[0]].execute(args[1:])
        else:
            print("Wrong command. Please try again.")


def note_main():
    help()
    while True:
        choice = input("Enter your command >>> ")
        if choice.lower().startswith(("exit", "close", "quit")):
            notebook.save_notes()
            break
        CommandParser().parse(choice)


if __name__ == "__main__":
    note_main()
