import re
from dataclasses import dataclass


@dataclass
class ActionItem:
    note_id: str = ""
    note_title: str = ""
    note_path: str = ""
    project: str = ""
    Owner: str = ""
    Date: str = ""
    Description: str = ""
    Completed: bool = False
    noteRow: int = 0
    taskString: str = ""
    Comment: str = ""

    def LoadFromString(
        self,
        note_id: str,
        note_title: str,
        note_path: str,
        project: str,
        taskString: str,
        noteRow: int = 0,
        comment: str = "",
    ):
        """
        Loads an action item from the string found in the note.

        """
        # [ ] vs [x] is used to determine if the action item is completed or not.
        # if the first 8 characters after the [ ] are a date in the format YYYY-MM-DD, then we can extract the date and description from the string.
        # any characters before the colon are assumed to be the owner, if there are no characters assume the owner is the default vault owner.

        self.note_id = note_id
        self.note_title = note_title
        self.note_path = note_path
        self.project = project
        self.taskString = taskString
        self.noteRow = noteRow
        self.Completed = "[x]" in taskString.lower()
        date_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", taskString)
        if date_match:
            self.Date = date_match.group(1)
        else:
            self.Date = ""

        # drop the - [ ], -[ ], - [x], etc from the beginning of the string, as well as the date if it exists, and then split on the first colon to separate the owner from the description.
        taskString = re.sub(r"^-?\s*\[.\]\s*", "", taskString)
        taskString = (
            taskString.replace(f"{self.Date}", "", 1).strip()
            if self.Date
            else taskString.strip()
        )

        if ":" in taskString:
            owner_part, description_part = taskString.split(":", 1)
            self.Owner = (
                owner_part.replace(self.Date, "").strip()
                if self.Date
                else owner_part.strip()
            )
            self.Description = description_part.strip()
        else:
            self.Owner = ""
            self.Description = taskString.strip()

        self.Comment = comment

    def Complete(self):
        try:
            from . import Notes as myNotes

            self.Completed = True
            selectedNoteBody = myNotes.read_Note_from_path(self.note_path)
            selectedNoteBody = selectedNoteBody.replace(
                self.taskString, self.taskString.replace("[ ]", "[x]"), 1
            )
            myNotes.write_Note_to_path(self.note_path, selectedNoteBody)
        except Exception as e:
            print(f"Error marking action item as complete: {e}")

    def __str__(self):
        response = ""
        # if self.Completed:
        #     response += "Completed Action Item "
        # else:
        #     response += "Action Item "

        if self.Owner != "":
            response += f"{self.Owner} "
        else:
            response += ""

        response += f" {self.Description}"

        if self.Date != "":
            response += f" on {self.Date}"

        if self.Completed:
            response += " (COMPLETED)"

        return response

    def to_json(self):
        return {
            "id": self.note_id,
            "note_title": self.note_title,
            "note_path": self.note_path,
            "project": self.project,
            "Owner": self.Owner,
            "Date": self.Date,
            "Description": self.Description,
            "Completed": self.Completed,
            "noteRow": self.noteRow,
            "taskString": self.taskString,
            "Comment": self.Comment,
        }


def __test__():

    testStrings = [
        "- [x] 2024-01-01 John Doe: This is a test action item.",
        "- [ ] 2024-01-01 John Doe: This is a test action item.",
        "- [x] John Doe: This is a test action item.",
        "- [x] 2024-01-01: This is a test action item.",
    ]
    for testString in testStrings:
        actionItem = ActionItem()
        actionItem.LoadFromString(
            "test_note_id",
            "test_note_title",
            "test_note_path",
            "test_project",
            testString,
        )
        print("Original String: ", testString)
        print("Result          : ", actionItem)
        print("\tDate: ", actionItem.Date)
        print("\tOwner: ", actionItem.Owner)
        print("\tDescription: ", actionItem.Description)
        print("\tCompleted: ", actionItem.Completed)
        print("\tComment: ", actionItem.Comment)
        print("")


if __name__ == "__main__":
    import os
    import sys

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    # Now re-import as package members
    from _library import Notes as myNotes
    from _library import Tools as myTools

    __test__()
