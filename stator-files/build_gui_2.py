import sys
from advanced_creator import AdvancedStatorCreator
from OCC.Display.SimpleGui import init_display
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QGridLayout, QLineEdit, QPushButton,
                             QVBoxLayout, QFormLayout, QGroupBox,
                             QComboBox, QMessageBox)


class GeomGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        # Main Window Properties
        self.setWindowTitle('Geometry Editor')
        width = 550
        height = 1200
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)

        self.mainLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.mainLayout)

        self.create_display()
        self.create_ui()
        self.set_default_values()

    def create_display(self):
        display_layout = QVBoxLayout()
        self.mainLayout.addLayout(display_layout, 0, 0)

    def create_ui(self):
        inputUILayout = QVBoxLayout()

        statorDimensionsBox = QGroupBox('Stator Dimensions')
        statorDimensionsBoxLayout = QFormLayout()

        draw_button = QPushButton()
        draw_button.setText("Draw")
        draw_button.clicked.connect(self.draw)
        clear_button = QPushButton()
        clear_button.setText("Clear All")
        clear_button.clicked.connect(self.clear_all)

        inputUILayout.addWidget(statorDimensionsBox)
        inputUILayout.addWidget(draw_button)
        inputUILayout.addWidget(clear_button)

        base_parameters = QGroupBox('Base Parameters')
        teeth_parameters = QGroupBox('Teeth Parameters')
        slot_parameters = QGroupBox('Slot Parameters')
        slotFilletBox = QGroupBox('Slot Fillets')
        base_parameters_layout = QFormLayout()
        teeth_parameters_layout = QFormLayout()
        slot_parameters_layout = QFormLayout()
        slotFilletBoxLayout = QFormLayout()

        self.machineTypeComboBox = QComboBox()
        self.machineTypeComboBox.addItems(['Outer', 'Inner'])
        self.slotTypeComboBox = QComboBox()
        self.slotTypeComboBox.addItems(['Curved', 'Flat'])
        self.slotCornerTypeComboBox = QComboBox()
        self.slotCornerTypeComboBox.addItems(["Inner", "Outer", "Both", "No Fillet"])
        self.teeth_feet_type_combobox = QComboBox()
        self.teeth_feet_type_combobox.addItems(["Default", "Custom", "No Feet"])
        self.teeth_width_type_combobox = QComboBox()
        # self.teeth_width_type_combobox.addItems(["Constant", "Expanding", "Manual"])
        self.teeth_width_type_combobox.addItems(["Constant", "Expanding"])

        self.active_length = QLineEdit()
        self.active_length.setAlignment(Qt.AlignCenter)
        self.active_length.setValidator(QIntValidator(0, 2147483647))

        self.stator_inner_radius = QLineEdit()
        self.stator_inner_radius.setAlignment(Qt.AlignCenter)
        self.stator_inner_radius.setValidator(QIntValidator(0, 2147483647))

        self.stator_outer_radius = QLineEdit()
        self.stator_outer_radius.setAlignment(Qt.AlignCenter)
        self.stator_outer_radius.setValidator(QIntValidator(0, 2147483647))

        self.num_of_slots = QLineEdit()
        self.num_of_slots.setAlignment(Qt.AlignCenter)
        self.num_of_slots.setValidator(QIntValidator(2, 2147483647))

        self.teeth_width = QLineEdit()
        self.teeth_width.setAlignment(Qt.AlignCenter)
        self.teeth_width.setValidator(QIntValidator(0, 2147483647))

        self.slot_depth = QLineEdit()
        self.slot_depth.setAlignment(Qt.AlignCenter)
        self.slot_depth.setValidator(QIntValidator(0, 2147483647))

        self.slot_opening_depth = QLineEdit()
        self.slot_opening_depth.setAlignment(Qt.AlignCenter)
        self.slot_opening_depth.setValidator(QIntValidator(0, 2147483647))

        self.slot_opening_depth_1 = QLineEdit()
        self.slot_opening_depth_1.setAlignment(Qt.AlignCenter)
        self.slot_opening_depth_1.setValidator(QIntValidator(0, 2147483647))

        self.slot_opening_width = QLineEdit()
        self.slot_opening_width.setAlignment(Qt.AlignCenter)
        self.slot_opening_width.setValidator(QIntValidator(0, 2147483647))

        self.fillet_radius_inner = QLineEdit()
        self.fillet_radius_inner.setAlignment(Qt.AlignCenter)
        self.fillet_radius_inner.setValidator(QIntValidator(0, 2147483647))

        self.fillet_radius_outer = QLineEdit()
        self.fillet_radius_outer.setAlignment(Qt.AlignCenter)
        self.fillet_radius_outer.setValidator(QIntValidator(0, 2147483647))

        statorDimensionsBoxLayout.addRow("Machine Type:  ", self.machineTypeComboBox)

        base_parameters_layout.addRow("Number of Slots:       ", self.num_of_slots)
        base_parameters_layout.addRow("Active Length:         ", self.active_length)
        base_parameters_layout.addRow("Stator Inner Radius:   ", self.stator_inner_radius)
        base_parameters_layout.addRow("Stator Outer Radius:   ", self.stator_outer_radius)

        teeth_parameters_layout.addRow("Teeth Feet Type:  ", self.teeth_feet_type_combobox)
        teeth_parameters_layout.addRow("Teeth Width Type: ", self.teeth_width_type_combobox)
        teeth_parameters_layout.addRow("Teeth Width:      ", self.teeth_width)

        slot_parameters_layout.addRow("Bottom Type:             ", self.slotTypeComboBox)
        slot_parameters_layout.addRow("Total Depth:             ", self.slot_depth)
        slot_parameters_layout.addRow("Opening Total Depth:     ", self.slot_opening_depth)
        slot_parameters_layout.addRow("Opening Part 1 Depth:    ", self.slot_opening_depth_1)
        slot_parameters_layout.addRow("Opening Width:           ", self.slot_opening_width)

        slotFilletBoxLayout.addRow("Corner Fillet: ",       self.slotCornerTypeComboBox)
        slotFilletBoxLayout.addRow("Fillet Radius Inner: ", self.fillet_radius_inner)
        slotFilletBoxLayout.addRow("Fillet Radius Outer: ", self.fillet_radius_outer)

        statorDimensionsBoxLayout.addRow(base_parameters)
        statorDimensionsBoxLayout.addRow(teeth_parameters)
        statorDimensionsBoxLayout.addRow(slot_parameters)
        statorDimensionsBoxLayout.addRow(slotFilletBox)

        statorDimensionsBox.setLayout(statorDimensionsBoxLayout)
        teeth_parameters.setLayout(teeth_parameters_layout)
        base_parameters.setLayout(base_parameters_layout)
        slot_parameters.setLayout(slot_parameters_layout)
        slotFilletBox.setLayout(slotFilletBoxLayout)

        self.mainLayout.addLayout(inputUILayout, 1, 1)

    def set_default_values(self):
        self.machineTypeComboBox.setCurrentText("Outer")
        self.stator_inner_radius.setText("200")
        self.stator_outer_radius.setText("400")
        self.active_length.setText("200")
        self.num_of_slots.setText("15")
        self.teeth_width.setText("20")
        self.slot_depth.setText("100")
        self.slot_opening_depth.setText("20")
        self.slot_opening_depth_1.setText("10")
        self.slot_opening_width.setText("20")
        self.fillet_radius_inner.setText("20")
        self.fillet_radius_outer.setText("20")

    def input_check(self):
        try:
            if int(self.num_of_slots.text()) < 2:
                self.raise_error("Invalid Input", "Minimum number of slots/teeth is 2.")
                return True
            if int(self.active_length.text()) <= 0:
                self.raise_error("Invalid Input", "Active length cannot be 0.")
                return True
            if int(self.teeth_width.text()) <= 0:
                self.raise_error("Invalid Input", "Teeth width cannot be 0.")
                return True
            if int(self.slot_depth.text()) <= 0:
                self.raise_error("Invalid Input", "Slot depth cannot be 0.")
                return True
            if int(self.slot_opening_depth.text()) <= 0:
                self.raise_error("Invalid Input", "Slot opening depth cannot be 0.")
                return True
            if int(self.slot_opening_depth_1.text()) <= 0:
                self.raise_error("Invalid Input", "Slot opening depth 1 cannot be 0.")
                return True
            elif int(self.slot_opening_depth.text()) <= int(self.slot_opening_depth_1.text()):
                self.raise_error("Invalid Input", "Slot opening depth 1 must be smaller than total opening depth.")
                return True
            if int(self.slot_opening_width.text()) <= 0:
                self.raise_error("Invalid Input", "Slot opening width cannot be 0.")
                return True
            if int(self.stator_inner_radius.text()) <= 0:
                self.raise_error("Invalid Input", "Stator inner radius cannot be 0.")
                return True
            if int(self.stator_outer_radius.text()) <= 0:
                self.raise_error("Invalid Input", "Stator outer radius cannot be 0.")
                return True
        except:
            self.raise_error("Invalid Input", "Input field(s) cannot be empty.")
            return True
        return False

    def clear_all(self):
        self.stator_outer_radius.setText("")
        self.active_length.setText("")
        self.stator_inner_radius.setText("")
        self.num_of_slots.setText("")
        self.teeth_width.setText("")
        self.slot_depth.setText("")
        self.slot_opening_depth_1.setText("")
        self.slot_opening_width.setText("")
        self.slot_opening_depth.setText("")
        self.fillet_radius_inner.setText("")
        self.fillet_radius_outer.setText("")

    def draw(self):
        if self.input_check():
            return

        inputs = {"stator_type":                self.machineTypeComboBox.currentText(),
                  "slot_type":                  self.slotTypeComboBox.currentText(),
                  "teeth_feet_type":            self.teeth_feet_type_combobox.currentText(),
                  "teeth_width_type":           self.teeth_width_type_combobox.currentText(),
                  "active_length":          int(self.active_length.text()),
                  "stator_inner_radius":    int(self.stator_inner_radius.text()),
                  "stator_outer_radius":    int(self.stator_outer_radius.text()),
                  "num_of_slots":           int(self.num_of_slots.text()),
                  "teeth_width":            int(self.teeth_width.text()),
                  "slot_opening_depth":     int(self.slot_opening_depth.text()),
                  "slot_opening_depth_1":   int(self.slot_opening_depth_1.text()),
                  "slot_opening_width":     int(self.slot_opening_width.text()),
                  "slot_depth":             int(self.slot_depth.text()),
                  "fillet_type":                self.slotCornerTypeComboBox.currentText(),
                  "fillet_radius_inner":    int(self.fillet_radius_inner.text()),
                  "fillet_radius_outer":    int(self.fillet_radius_outer.text()),
                  }

        asc = AdvancedStatorCreator(inputs)
        base = asc.base()
        slot = asc.slot()
        if isinstance(slot, str):
            self.raise_error("Build Error", slot)
            return
        display, start_display, add_menu, add_function_to_menu = init_display('wx')
        display.DisplayShape(asc.stator(slot, base), update=True)
        start_display()

    def raise_error(self, window, msg):
        QMessageBox.critical(self, window, msg, QMessageBox.Ok, QMessageBox.Ok)


def main():
    app = QApplication(sys.argv)

    editor = GeomGUI()
    editor.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()