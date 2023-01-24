import site, os

site.addsitedir("../prmp_qt")

from prmp_qt import *
from qss import QSS
from bulk_file_renamer import *

_LineEdit = LineEdit


class _Base:
    def change(self):
        home: Home = self.window()
        home.updatePreview()


class LineEdit(_LineEdit, _Base):
    def __init__(self, **kwargs):
        _LineEdit.__init__(self, **kwargs)
        self.textEdited.connect(self.change)


class RadioButton(QRadioButton, _Base):
    def __init__(self, *args, **kwargs):
        QRadioButton.__init__(self, *args, **kwargs)
        self.clicked.connect(self.change)


class ComboBox(QComboBox, _Base):
    def __init__(self, **kwargs):
        QComboBox.__init__(self, **kwargs)

    def showEvent(self, e: QShowEvent) -> None:
        self.currentTextChanged.connect(self.change)


class Base(_Base, VFrame):
    def __init__(self, **kwargs) -> None:
        VFrame.__init__(self, **kwargs)

        self.lay = self.layout()
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

    def change(self):
        home: Home = self.window()
        home.updatePreview()


class Option(Base):
    def __init__(self, title: str, description: str) -> None:
        super().__init__()

        top_lay = QHBoxLayout()
        self.lay.addLayout(top_lay)

        top_lay.addWidget(Label(objectName="title", text=title))

        top_lay.addStretch()

        self.switch = Switch(minWidth=50, minHeight=25)
        top_lay.addWidget(self.switch)

        frame = VFrame()
        frame.setDisabled(True)
        self.frame_lay = frame.layout()
        self.lay.addWidget(frame)

        self.switch.toggled.connect(lambda toggle: frame.setEnabled(toggle))
        self.switch.clicked.connect(self.change)

        self.frame_lay.addWidget(Label(objectName="description", text=description))

        self.frame_lay.addWidget(HLine())

    def addWidget(self, widget: QWidget):
        self.frame_lay.addWidget(widget)

    @property
    def enabled(self):
        return self.switch.isChecked()

    def values(self):
        return {}


class DestinationFolder(Option):
    def __init__(self) -> None:
        super().__init__("Change Destination Folder", "Change the destination folder:")

        browse = Button(text="Browse")
        browse.clicked.connect(self.browse)
        self.addWidget(browse)

        self.destination_folder = LineEdit(placeholder="Folder ...")
        self.addWidget(self.destination_folder)

    def browse(self):
        folder = QFileDialog.getExistingDirectory()
        if folder:
            self.destination_folder.setText(folder)
            self.change()

    def values(self):
        return dict(destination_folder=self.destination_folder.text())


class BaseName(Option):
    def __init__(self) -> None:
        super().__init__(
            "Change Base Name",
            "Enable to set a new base name for all files.\nThis will replace the original name:",
        )

        self.new_basename = LineEdit(placeholder="New Base Name ...")
        self.addWidget(self.new_basename)

    def values(self):
        return dict(new_basename=self.new_basename.text())


class ILabel(AlignLabel, _Base):
    def __init__(self, command, **kwargs):
        AlignLabel.__init__(self, **kwargs)
        self.command = command

    def mousePressEvent(self, event: QMouseEvent):
        self.command()
        self.change()


class IntBox(HFrame, _Base):
    validator = QIntValidator()

    def __init__(self, default: int = 0):
        super().__init__()
        lay = self.layout()
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)

        minus = ILabel(self.minus, text="-", objectName="minus")
        lay.addWidget(minus)

        self.number = LineEdit()
        self.number.setAlignment(Qt.AlignCenter)
        self.number.setValidator(self.validator)
        lay.addWidget(self.number)

        plus = ILabel(self.plus, text="+", objectName="plus")
        lay.addWidget(plus)

        self.setValue(default)

    def minus(self):
        if self.value:
            self.setValue(self.value - 1)

    def plus(self):
        self.setValue(self.value + 1)

    @property
    def value(self):
        return int(self.number.text() or 0)

    def setValue(self, value: int):
        self.number.setText(str(value))


class YesNo(QHBoxLayout):
    def __init__(self, yes: str, no: str):
        super().__init__()

        self.yes = RadioButton(yes)
        self.addWidget(self.yes)

        self.no = RadioButton(no)
        self.addWidget(self.no)

    @property
    def value(self):
        return self.yes.isChecked()


class AutoIndexing(Option):
    def __init__(self) -> None:
        super().__init__(
            "Auto Indexing",
            "Add an auto-incremented index before or after base name:",
        )

        form = QFormLayout()
        self.frame_lay.addLayout(form)

        self.separator = LineEdit(placeholder="_")
        form.addRow("Separator:", self.separator)

        self.before_after = YesNo("Before name", "After name")

        form.addRow("Position:", self.before_after)

        self.start_index = IntBox(1)
        form.addRow("Start Index:", self.start_index)

        self.increment = IntBox(1)
        form.addRow("Increment By (step):", self.increment)

        self.zero_padding = IntBox()
        form.addRow("Zero Padding:", self.zero_padding)

    def values(self):
        return dict(
            auto_indexing=self.enabled,
            auto_indexing_start_index=self.start_index.value,
            auto_indexing_step=self.increment.value,
            auto_indexing_separator=self.separator.text(),
            auto_indexing_before=self.before_after.value,
            auto_indexing_zero_padding=self.zero_padding.value,
        )


class Capitalization(Option):
    def __init__(self) -> None:
        super().__init__(
            "Change Base Name",
            "Enable to set a new base name for all files.\nThis will replace the original name:",
        )

        self.lower_case = RadioButton("All Lower Case")
        self.addWidget(self.lower_case)

        self.uper_case = RadioButton("All Upper Case")
        self.addWidget(self.uper_case)

        self.sentence_case = RadioButton("All Sentence Case")
        self.addWidget(self.sentence_case)

    def values(self):
        return dict(
            lower=self.lower_case.isChecked(),
            upper=self.uper_case.isChecked(),
            sentence=self.sentence_case.isChecked(),
        )


class Extension(Option):
    def __init__(self) -> None:
        super().__init__("Change Extension", "Change the extension of the files:")

        self.extension = LineEdit(placeholder="New Extension ...")
        self.addWidget(self.extension)

    def values(self):
        return dict(extension=self.extension.text())


class AddPrefix(Option):
    def __init__(self) -> None:
        super().__init__("Add Prefix", "Add prefix before the base name:")

        self.prefix = LineEdit(placeholder="Prefix ...")
        self.addWidget(self.prefix)

    def values(self):
        return dict(add_prefix=self.prefix.text())


class AddSuffix(Option):
    def __init__(self) -> None:
        super().__init__("Add Suffix", "Add suffix after the base name:")

        self.suffix = LineEdit(placeholder="Suffix ...")
        self.addWidget(self.suffix)

    def values(self):
        return dict(add_suffix=self.suffix.text())


class AddDate(Option):
    def __init__(self) -> None:
        super().__init__("Add Date", "Add last modified date:")

        form = QFormLayout()
        self.frame_lay.addLayout(form)

        self.before_after = YesNo("Before name", "After name")
        form.addRow("Date Position:", self.before_after)

        self.separator = LineEdit(placeholder="-")
        form.addRow("Separator:", self.separator)

        vlay = QVBoxLayout()
        form.addRow("Date format:", vlay)

        self.buttons: list[ComboBox] = []

        ls = ["year", "month", "day"], ["hour", "minute", "second"]

        for l in ls:
            hlay = QHBoxLayout()
            vlay.addLayout(hlay)

            for _ in l:
                button = ComboBox()
                button.addItems([''] + ls[0] + ls[1])
                hlay.addWidget(button)
                self.buttons.append(button)

    def values(self):
        formats = []
        for button in self.buttons:
            format = button.currentText()
            if format:
                formats.append(format)

        return dict(
            add_date=self.enabled,
            add_date_before=self.before_after.value,
            add_date_separator=self.separator.text(),
            add_date_formats=formats,
        )


class AddCharacters(Option):
    def __init__(self) -> None:
        super().__init__(
            "Add characters at position",
            "Add characters at specified position (starts with 0):",
        )

        form = QFormLayout()
        self.frame_lay.addLayout(form)

        self.start_end = YesNo("Start", "End")
        form.addRow("Count from:", self.start_end)

        self.characters = LineEdit(placeholder="-")
        form.addRow("Characters:", self.characters)

        self.position = IntBox()
        form.addRow("Position:", self.position)

    def values(self):
        return dict(
            add_characters=self.characters.text(),
            add_position=self.position.value,
            add_to_start=self.start_end.value,
        )


class RemoveWhitespaces(Option):
    def __init__(self) -> None:
        super().__init__(
            "Remove whitespaces",
            "Remove whitespaces from specified location:",
        )

        self.start_end = RadioButton("All Lower Case")
        self.addWidget(self.start_end)

        self.remove_all = RadioButton("All Upper Case")
        self.addWidget(self.remove_all)

    def values(self):
        return dict(
            remove_whitespaces_start_n_end=self.start_end.isChecked(),
            remove_whitespaces_all=self.remove_all.isChecked(),
        )


class RemoveCharacters(Option):
    def __init__(self) -> None:
        super().__init__(
            "Remove characters", "Remove characters or words from the name:"
        )

        self.characters = LineEdit(placeholder="Characters to be deleted ...")
        self.addWidget(self.characters)

    def values(self):
        return dict(remove_characters=self.characters.text())


class RemoveMultipleCharacters(Option):
    def __init__(self) -> None:
        super().__init__(
            "Remove multiple characters",
            "Remove multiple characters separated by comman (,):",
        )

        self.characters = LineEdit(placeholder="Example: a, 3, |, =")
        self.addWidget(self.characters)

    def values(self):
        return dict(remove_multiple_characters=self.characters.text())


class RemoveCharactersByType(Option):
    def __init__(self) -> None:
        super().__init__(
            "Remove characters by  type",
            "Delete all characters of a chosen type:",
        )

        self.numbers = RadioButton("Remove all numbers")
        self.addWidget(self.numbers)

        self.letters = RadioButton("Remove all letters")
        self.addWidget(self.letters)

        self.non_numbers = RadioButton("Remove all non-numeric characters")
        self.addWidget(self.non_numbers)

        self.non_letters = RadioButton("Remove all non-letters characters")
        self.addWidget(self.non_letters)

    def values(self):
        return dict(
            remove_all_numbers=self.numbers.isChecked(),
            remove_all_letters=self.letters.isChecked(),
            remove_all_non_numerics=self.non_numbers.isChecked(),
            remove_all_non_letters=self.non_letters.isChecked(),
        )


class RemoveCharactersAtPosition(Option):
    def __init__(self) -> None:
        super().__init__(
            "Remove characters at position",
            "Delete a number of characters fromo the start, end or custom range:",
        )

        # first
        hlay = QHBoxLayout()
        self.frame_lay.addLayout(hlay)

        self.first_button = RadioButton("First")
        hlay.addWidget(self.first_button)
        self.first = LineEdit(placeholder="#")
        self.first.setValidator(IntBox.validator)
        hlay.addWidget(self.first)
        hlay.addWidget(Label("characters"))
        self.first_button.toggled.connect(self.first.setEnabled)

        # last
        hlay = QHBoxLayout()
        self.frame_lay.addLayout(hlay)

        self.last_button = RadioButton("Last")
        hlay.addWidget(self.last_button)
        self.last = LineEdit(placeholder="#")
        self.last.setValidator(IntBox.validator)
        hlay.addWidget(self.last)

        self.last_button.toggled.connect(self.last.setEnabled)

        hlay.addWidget(Label("characters"))

        # custom_range
        hlay = QHBoxLayout()
        self.frame_lay.addLayout(hlay)

        self.custom_range = RadioButton("Custom range:")
        hlay.addWidget(self.custom_range)

        self.from_ = LineEdit(placeholder="start")
        self.from_.setValidator(IntBox.validator)
        hlay.addWidget(self.from_)

        hlay.addWidget(Label("to"))

        self.to = LineEdit(placeholder="end")
        self.to.setValidator(IntBox.validator)
        hlay.addWidget(self.to)

        self.custom_range.toggled.connect(self.from_.setEnabled)
        self.custom_range.toggled.connect(self.to.setEnabled)

        for lineEdit in (self.first, self.last, self.from_, self.to):
            lineEdit.setDisabled(True)

    def value(self, lineEdit: LineEdit) -> int:
        return int(lineEdit.text() or 0)

    def values(self):
        vs = dict(
            remove_characters_at_range=self.custom_range.isChecked(),
            remove_characters_at_range_start=self.value(self.from_),
            remove_characters_at_range_end=self.value(self.to),
        )
        if self.first_button.isChecked():
            vs.update(remove_characters_at_first_position=self.value(self.first))

        if self.last_button.isChecked():
            vs.update(remove_characters_at_last_position=self.value(self.last))

        return vs


class ReplaceCharacters(Option):
    def __init__(self) -> None:
        super().__init__(
            "Replace characters",
            "Replace characters or words:",
        )

        hlay = QHBoxLayout()
        self.frame_lay.addLayout(hlay)

        self.old = LineEdit(placeholder="old")
        hlay.addWidget(self.old)

        hlay.addWidget(Label("to"))

        self.new = LineEdit(placeholder="new")
        hlay.addWidget(self.new)

    def values(self):
        return dict(
            replace_characters=self.old.text(), characters_replacement=self.new.text()
        )


class Item(Button):
    def __init__(self, file: str, preview: str):
        super().__init__(checkable=True)

        addShadow(self)

        self.file = file

        lay = QVBoxLayout(self)

        file_label = Label(file)
        lay.addWidget(file_label)

        self.preview_label = Label(preview, objectName="preview")
        lay.addWidget(self.preview_label)

    def setPreview(self, preview: str):
        self.preview_label.setText(preview)


class Preview(Scrollable):
    def __init__(self) -> None:
        super().__init__(widgetClass=VFrame, widgetKwargs=dict(objectName="vframe"))
        self.items: dict[str, Item] = {}
        self.spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

    def preview(self, previews: list[tuple[str]]):
        lay = self.widgetLayout()
        lay.removeItem(self.spacer)

        for file, preview in previews:
            if file not in self.items:
                item = Item(file, preview)
                lay.addWidget(item, 1, Qt.AlignTop)
                self.items[file] = item
            else:
                self.items[file].setPreview(preview)

        lay.addItem(self.spacer)

    def remove_files(self):
        lay = self.widgetLayout()
        files = []
        values = list(self.items.values())
        for item in values:
            if item.isChecked():
                files.append(item.file)
                del self.items[item.file]
                lay.removeWidget(item)
                item.deleteLater()
        self.widget().update()
        self.update()
        return files


class Output(Base):
    def __init__(self, home: "Home", **kwargs) -> None:
        super().__init__(**kwargs)
        self.home = home

        hlay = QHBoxLayout()
        self.lay.addLayout(hlay)

        add_files = Button("Add Files")
        add_files.clicked.connect(self.add_files)
        hlay.addWidget(add_files)

        remove_files = Button("Remove Files", objectName="red")
        remove_files.clicked.connect(self.remove_files)
        hlay.addWidget(remove_files)

        hlay.addStretch()

        self.copy = QRadioButton("Copy")
        self.copy.setChecked(True)
        hlay.addWidget(self.copy)

        move = QRadioButton("Move")
        hlay.addWidget(move)

        save_files = Button("Save Files", objectName="red")
        save_files.clicked.connect(self.save_files)
        hlay.addWidget(save_files)

        self.preview = Preview()
        self.lay.addWidget(self.preview)

    def add_files(self):
        files = QFileDialog.getOpenFileNames(self)[0]
        if files:
            self.home.add_files(files)

    def remove_files(self):
        files = self.preview.remove_files()
        for file in files:
            self.home.files.remove(file)

    def save_files(self):
        self.home.save(copy=self.copy.isChecked())


class Options(Base):
    def __init__(self, options_class: type[Option], **kwargs) -> None:
        super().__init__(**kwargs)
        self.lay.setContentsMargins(0, 0, 0, 5)
        self._options: list[Option] = []
        for option_class in options_class:
            self.add_option(option_class())

    def add_option(self, option: Option):
        self.lay.addWidget(option)
        self._options.append(option)

    def values(self):
        values = {}
        for option in self._options:
            if option.enabled:
                values.update(option.values())
        return values


class Home(HFrame):
    def __init__(self):
        super().__init__()

        self.files: list[str] = []
        self.previews: list[tuple[str, str]] = []

        self.setWindowTitle("Bulk File Renamer")
        lay = self.layout()
        m = 0
        lay.setContentsMargins(m, 5, 5, 5)
        lay.setSpacing(5)

        vframe = VFrame()
        lay.addWidget(vframe)
        vframe.setMinimumWidth(450)
        vframe.setMaximumWidth(450)

        vlay = vframe.layout()
        vlay.setSpacing(0)

        hlay = QHBoxLayout()
        vlay.addLayout(hlay)
        hlay.setSpacing(5)

        self.setMinimumHeight(600)

        scrollable = Scrollable(
            widgetClass=VFrame, widgetKwargs=dict(objectName="vframe")
        )
        vlay.addWidget(scrollable)

        scroll_lay = scrollable.widgetLayout()
        scroll_lay.setContentsMargins(m, m, m, m)
        scroll_lay.setSpacing(0)

        self.change = Options(
            objectName="change",
            options_class=[
                DestinationFolder,
                BaseName,
                AutoIndexing,
                Capitalization,
                Extension,
            ],
        )
        scroll_lay.addWidget(self.change)

        self.add = Options(
            objectName="add",
            options_class=[
                AddPrefix,
                AddSuffix,
                AddDate,
                AddCharacters,
            ],
        )
        scroll_lay.addWidget(self.add)

        self.remove = Options(
            objectName="remove",
            options_class=[
                RemoveWhitespaces,
                RemoveCharacters,
                RemoveMultipleCharacters,
                RemoveCharactersByType,
                RemoveCharactersAtPosition,
                ReplaceCharacters,
            ],
        )
        scroll_lay.addWidget(self.remove)

        hlay.addStretch()

        for name in ("change", "add", "remove"):
            button = QPushButton(name.title())
            button.setCheckable(True)
            button.setObjectName(name)
            hlay.addWidget(button)
            button.toggle()
            button.toggled.connect(getattr(self, f"toggle_{name}"))

        hlay.addStretch()

        self.output = Output(self)
        lay.addWidget(self.output)

    def add_files(self, files: list[str]):
        for file in files:
            if file not in self.files:
                self.files.append(file)

        self.updatePreview(files)

    def toggle_change(self, toggle: bool):
        self.change.setVisible(toggle)

    def toggle_add(self, toggle: bool):
        self.add.setVisible(toggle)

    def toggle_remove(self, toggle: bool):
        self.remove.setVisible(toggle)

    def save(self, copy: bool):
        if self.previews:
            renamer(lists=self.previews, copy=copy)
            QMessageBox.information(self, 'Bulk rename successful.', f'The {len(self.previews)} files have been bulk renamed successfully.')

    @property
    def options(self):
        values = {}
        for op in (self.change, self.add, self.remove):
            values.update(op.values())
        return values

    # def mousePressEvent(self, event: QMouseEvent) -> None:
    #     self.m = QColorDialog(self)
    #     print(self.options)
    #     self.m.show()

    def updatePreview(self, files: list[str] = []):
        files = files or self.files
        self.previews = bulk_file_renamer(files, **self.options)
        self.output.preview.preview(self.previews)

    def showEvent(self, event: QShowEvent) -> None:
        self.move(20, 10)
        files = []
        for l in os.listdir('test'):
            l = os.path.join('test', l)
            if os.path.isfile(l):
                files.append(l)
        self.add_files(files)


class App(QApplication):
    theme_update = Signal()

    def __init__(self):
        super().__init__()

        self.setStyleSheet(QSS)
        self.ui = Home()
        self.ui.destroyed.connect(self.quit)

    def start(self):
        self.ui.show()
        self.exec()


a = App()
a.start()
