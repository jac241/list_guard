import glob
import os.path
from pathlib import Path

from PySide6.QtCore import QFileSystemWatcher

LIST_DIR = "/Users/jamescastiglione/git/jac241/list_guard/test/support/JHN List"


class ListDirectoryWatcher(QFileSystemWatcher):
    def __init__(self, list_manager, parent=None):
        super().__init__(parent)
        self._list_manager = list_manager

        self._setup_signals()

    def _setup_signals(self):
        self.directoryChanged.connect(self._evaluate_changes)

    def _evaluate_changes(self, changed_path):
        for d in self.directories():
            print(d)
            self._list_manager.check_for_newer_list(d)


class ListManager:
    def __init__(self, initial_list_path):
        self.most_recent_list_path = Path(
            self._find_newest_excel_file(initial_list_path)
        )
        print("Initialized with:", self.most_recent_list_path)

    def check_for_newer_list(self, list_dir):
        maybe_newer_list_path = self._find_newest_excel_file(list_dir)
        if self.most_recent_list_path != maybe_newer_list_path:
            print("List set to:", maybe_newer_list_path)
            self.most_recent_list_path = maybe_newer_list_path

    def _find_newest_excel_file(self, list_dir):
        newest_list_path = glob.glob(f"{list_dir}/*.xlsx")[0]
        current_list_update_time = os.path.getmtime(newest_list_path)

        for excel_file_path in glob.glob(f"{list_dir}/*.xlsx"):
            if self._is_newer_list(
                    excel_file_path,
                    newest_list_path,
                    current_list_update_time
            ):
                newest_list_path = excel_file_path

        return Path(newest_list_path)

    def _is_newer_list(self, excel_file_path, current_list_path, current_list_update_time):
        return (excel_file_path != current_list_path and
                not os.path.basename(excel_file_path).startswith(r"~$") and
                os.path.getmtime(excel_file_path) > current_list_update_time )


def initialize(watcher: QFileSystemWatcher, list_dir):
    watcher.addPath(list_dir)