from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.styles import Style
from address_book import addressbook_main
from note import note_main
from sort import sort_main


class MainMenu:
    def __init__(self, options):
        self.options = options

    def show(self):
        result = 0
        while result is not None:
            result = radiolist_dialog(
                title="Welcome to Exponenta app.",
                text=self._generate_menu_text(),
                values=self.options,
                style=self._get_style(),
            ).run()
            self._handle_selection(result)

    def _generate_menu_text(self):
        return """Here you can:
            1. Sort your folder with random files,
            2. Make your own address book,
            3. Write some notes
            What would you like to do ? """

    def _get_style(self):
        return Style.from_dict(
            {
                "dialog": "bg:#539ce6",
                "checkbox": "#e8612c",
                "dialog.body": "bg:#a9cfd0",
                "frame.label": "#280e6e",
                "dialog.body label": "#613ccf",
            }
        )

    def _handle_selection(self, result):
        print(result)
        if result == "addressbook":
            address_book = AddressBook()
            address_book.run()
        elif result == "notebook":
            note_book = NoteBook()
            note_book.run()
        elif result == "sort":
            file_sorter = FileSorter()
            file_sorter.run()


class AddressBook:
    def run(self):
        addressbook_main()


class NoteBook:
    def run(self):
        note_main()


class FileSorter:
    def run(self):
        sort_main()


def main():
    options = [
        ("sort", "Sort directory"),
        ("addressbook", "Address book"),
        ("notebook", "Notebook"),
    ]

    main_menu = MainMenu(options)
    main_menu.show()


if __name__ == "__main__":
    main()
