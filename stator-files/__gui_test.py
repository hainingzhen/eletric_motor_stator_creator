from __advanced_creator_test import AdvancedStatorCreator
from OCC.Display.SimpleGui import init_display


class Gui:

    def __init__(self):
        self.asc = AdvancedStatorCreator()
        self.run()

    def run(self):
        base = self.asc.base()
        slot = self.asc.slot()
        if isinstance(slot, str):
            self.error(slot)
            return
        display, start_display, add_menu, add_function_to_menu = init_display('wx')
        display.DisplayShape(self.asc.stator(slot, base), update=True)
        start_display()

    def error(self, err):
        print("Error Msg: ", err)


if __name__ == '__main__':
    Gui()