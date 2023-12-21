# Import necessary modules
import MAIN_database_things as ez
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout


class DataManager:
    result_data = None
    absent_list = []

    @classmethod
    def set_result_data(cls, data):
        cls.result_data = data

    @classmethod
    def get_result_data(cls):
        return cls.result_data

    @classmethod
    def set_absent_list(cls, absent_list):
        cls.absent_list = absent_list

    @classmethod
    def get_absent_list(cls):
        return cls.absent_list


class MyScreenManager(ScreenManager):
    pass


class DisplayDataPage(Screen):
    checked_items = []

    def init(self, **kwargs):
        super(DisplayDataPage, self).init(**kwargs)
        self.data = None

    def on_pre_enter(self):
        if self.do_layout:
            self.clear_widgets()
        home_page = App.get_running_app().root.get_screen("home_page")
        self.data = home_page.authenticate()

        if not self.data:
            print("All Data Successfully Deleted!")
            # self.manager.current = "home_page"
            # return

        DataManager.set_result_data(self.data)

        larger_data = len(self.data)
        if larger_data < 14:
            larger_data = len(self.data) + 5
        self.layout = GridLayout(
            cols=1,
            spacing=10,
            padding=(0, 100),
            size_hint=(None, None),
            size=(400, larger_data * 40),
        )
        for item in self.data:
            label = Label(
                text=f"ID: {item[0]}, Name: {item[1]}",
                size_hint_x=None,
                width=300,
            )
            self.layout.add_widget(label)

        scrollview = ScrollView()
        scrollview.add_widget(self.layout)

        exit_button = Button(
            text="Exit",
            size_hint=(0.2, None),
            height=40,
            background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        exit_button.bind(on_release=self.on_exit_button)
        back_button = Button(
            text="Back",
            size_hint=(0.2, None),
            height=40,
            background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        back_button.bind(on_release=self.on_back_button)

        button_box_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, None), height=40
        )
        button_box_layout.add_widget(back_button)
        button_box_layout.add_widget(exit_button)

        main_layout = AnchorLayout()
        scroll_box_layout = BoxLayout(orientation="vertical")
        scroll_box_layout.add_widget(scrollview)
        scroll_box_layout.add_widget(button_box_layout)
        main_layout.add_widget(scroll_box_layout)

        self.add_widget(main_layout)

    # Methods for button callbacks

    def on_back_button(self, instance):
        self.manager.current = "all_present_page"

    def on_exit_button(self, instance):
        App.get_running_app().stop()


class LoadingScreen(Screen):
    pass


class HomePage(Screen):
    result = None
    class_id = ""

    def update_class_id(self, new_text):
        self.class_id = new_text

    def update_password(self, new_text):
        self.password = new_text

    def authenticate(self):
        if not self.class_id or not self.password:
            print("Class ID and Password are required.")
        else:
            HomePage.result = ez.obj.authenticate_user(self.class_id, self.password)
            DataManager.set_result_data(HomePage.result)
            self.is_authenticated = True
            return HomePage.result

    @classmethod
    def get_class_id(cls):
        return cls.class_id


class SelectPage(Screen):
    checked_items = []

    def _init_(self, **kwargs):
        super(SelectPage, self)._init_(**kwargs)
        self.layout = None
        # Create buttons during initialization

    def create_buttons(self):
        done_button = Button(
            text="Done",
            size_hint=(0.2, None),
            height=40,
            background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        done_button.bind(on_release=self.on_done_button)

        back_button = Button(
            text="Back",
            size_hint=(0.2, None),
            height=40,
            background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        back_button.bind(on_release=self.on_back_button)

        box_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=40)
        box_layout.add_widget(back_button)
        box_layout.add_widget(done_button)

        self.add_widget(box_layout)

    def build_ui(self):
        if self.do_layout:
            self.clear_widgets()  # Clear existing widgets before building new ones
        home_page = self.manager.get_screen("home_page")
        data = home_page.authenticate()
        larger_data = len(data)
        if larger_data < 14:
            larger_data = len(data) + 5
        self.layout = GridLayout(
            cols=1,
            spacing=10,
            padding=(0, 100),
            size_hint=(None, None),
            size=(400, larger_data * 40),
        )
        scrollview = ScrollView()
        scrollview.add_widget(self.layout)
        self.add_widget(scrollview)

        if not data:
            print("Authentication is required.")
            self.manager.current = "home_page"
            return

        DataManager.set_result_data(data)

        for item in data:
            box = BoxLayout(orientation="horizontal", padding=(10, 0, 0, 0))
            checkbox = CheckBox(active=False)
            checkbox.bind(active=self.on_checkbox_active)
            checkbox.id, checkbox.name = item
            label = Label(
                text=f"ID: {checkbox.id}, Name: {checkbox.name}",
                size_hint_x=None,
                width=300,
            )
            box.add_widget(checkbox)
            box.add_widget(label)
            self.layout.add_widget(box)
        self.create_buttons()

    def on_pre_enter(self):
        self.build_ui()

    def on_done_button(self, instance):
        self.mark_absent()

    def on_back_button(self, instance):
        self.manager.current = "all_present_page"

    def on_checkbox_active(self, instance, value):
        if value:
            self.checked_items.append((instance.id, instance.name))
        else:
            self.checked_items = [
                item
                for item in self.checked_items
                if item != (instance.id, instance.name)
            ]

    def mark_absent(self):
        home_page = self.manager.get_screen("home_page")
        class_name = home_page.class_id
        if self.checked_items:
            count = len(self.checked_items)
            roll_numbers = [item[0] for item in self.checked_items if len(item) >= 2]
            ez.obj.custome_marking(class_name, roll_numbers)
            DataManager.set_absent_list(roll_numbers)
        else:
            print("No students selected to mark absent.")
        self.manager.current = "select_result_page"


class DeletefromDatabase(Screen):
    checked_items = []

    def _init_(self, **kwargs):
        super(DeletefromDatabase, self)._init_(**kwargs)
        self.layout = None

    def create_buttons(self):
        delete_button = Button(
            text="Delete",
            size_hint=(0.2, None),
            height=40,
            background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        delete_button.bind(on_release=self.on_delete_button)
        delete_all_button = Button(
            text="Delete ALL",
            size_hint=(0.2, None),
            height=40,
            background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        delete_all_button.bind(on_release=self.on_delete_all_button)

        back_button = Button(
            text="Back",
            size_hint=(0.2, None),
            height=40,
            background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        back_button.bind(on_release=self.on_back_button)

        box_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=40)
        box_layout.add_widget(back_button)
        box_layout.add_widget(delete_button)
        box_layout.add_widget(delete_all_button)

        self.add_widget(box_layout)

    def build_ui(self):
        if self.do_layout:
            self.clear_widgets()  # Clear existing widgets before building new ones

        home_page = self.manager.get_screen("home_page")
        data = home_page.authenticate()
        larger_data = len(data)
        if larger_data < 14:
            larger_data = len(data) + 5

        self.layout = GridLayout(
            cols=1,
            spacing=10,
            padding=(0, 100),
            size_hint=(None, None),
            size=(400, larger_data * 40),
        )
        scrollview = ScrollView()
        scrollview.add_widget(self.layout)
        self.add_widget(scrollview)

        if not data:
            print("Authentication is required.")
            self.manager.current = "home_page"
            return

        DataManager.set_result_data(data)

        self.checked_items = []
        for item in data:
            box = BoxLayout(orientation="horizontal", padding=(10, 0, 0, 0))
            checkbox = CheckBox(active=False)
            checkbox.bind(active=self.on_checkbox_active)
            checkbox.id, checkbox.name = item
            label = Label(
                text=f"ID: {checkbox.id}, Name: {checkbox.name}",
                size_hint_x=None,
                width=300,
            )
            box.add_widget(checkbox)
            box.add_widget(label)
            self.layout.add_widget(box)
        self.create_buttons()

    def on_pre_enter(self):
        self.build_ui()

    def on_delete_all_button(self, instance):
        self.delete_everything()

    def on_delete_button(self, instance):
        self.delete_from_database()

    def on_back_button(self, instance):
        self.manager.current = "all_present_page"

    def on_checkbox_active(self, instance, value):
        if value:
            self.checked_items.append((instance.id, instance.name))
        else:
            self.checked_items = [
                item
                for item in self.checked_items
                if item != (instance.id, instance.name)
            ]

    def delete_from_database(self):
        home_page = App.get_running_app().root.get_screen("home_page")
        class_name = home_page.class_id
        if self.checked_items:
            roll_numbers = []
            for item in self.checked_items:
                if len(item) >= 2:
                    roll_numbers.append(item[0])
                else:
                    print("Invalid item in checked_items:", item)
            ez.obj.delete_data(class_name, roll_numbers)
            self.manager.current = "delete_result_page"

        else:
            print("No students selected to be deleted.")

    def delete_everything(self):
        home_page = App.get_running_app().root.get_screen("home_page")
        class_name = home_page.class_id
        ez.obj.delete_all(class_name)
        print("Everyont was successfully deleted from the database!")


class AllPresent(Screen):
    name = "all_present_page"

    def mark_all_present(self):
        home_page = App.get_running_app().root.get_screen("home_page")
        class_name = home_page.class_id
        ez.obj.mark_all_present(class_name)  # Call the mark_all_present method


class CreateTables(Screen):
    def create_new_tables(self, class_name):
        ez.obj.create_table_for_class(class_name)
        self.manager.current = "all_present_page"
        self.manager.transition.direction = "left"


class Database(Screen):
    pass


class CheckTable(Screen):
    pass


class AddtoDatabase(Screen):
    def _init_(self, **kwargs):
        super(AddtoDatabase, self)._init_(**kwargs)
        self.build_ui()

    def add_to_data(self, student_name, roll_no):
        if not student_name or not roll_no:
            print("Student Name and Roll Number are required.")
        else:
            home_page = App.get_running_app().root.get_screen("home_page")
            class_id = home_page.class_id
            ez.obj.add_individual_chunks_database(class_id, student_name, roll_no)
            print(f"Added data for {student_name} with roll number {roll_no}")
            self.manager.current = "all_present_page"
            App.get_running_app().root.transition.direction = "left"

    def build_ui(self):
        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            spacing=50,
            padding=50,
            background_color=(0, 0, 1, 1),
        )

        grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter("height"))

        student_name_input = TextInput(
            hint_text="Student Name",
            multiline=False,
            size_hint_y=None,
            height=50,
        )

        roll_no_input = TextInput(
            hint_text="Roll No",
            multiline=False,
            size_hint_y=None,
            height=50,
        )

        spacer = Widget(size_hint_y=None, height=200)

        proceed_button = Button(
            text="Proceed",
            size_hint_y=None,
            height=50,
            background_color=(0.9, 0, 0.9, 1),
            color=(1, 1, 1, 1),
            on_release=lambda instance: self.add_to_data(
                student_name_input.text, roll_no_input.text
            ),
        )

        exit_button = Button(
            text="Back",
            size_hint_y=None,
            height=50,
            background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1),
            on_release=self.on_back_button,
        )

        grid_layout.add_widget(student_name_input)
        grid_layout.add_widget(roll_no_input)
        grid_layout.add_widget(spacer)
        grid_layout.add_widget(proceed_button)

        layout.add_widget(grid_layout)
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def on_back_button(self, instance):
        self.manager.current = "all_present_page"
        App.get_running_app().root.transition.direction = "left"

    def on_pre_enter(self, *args):
        self.build_ui()


class AddFile(Screen):
    file_path = ""

    def add_class_name_input(self, file_name_input, class_name_input):
        if file_name_input and class_name_input:
            default_path = "C:/Users/Admin/Documents/GitHub/Attendance-management-/src/"
            file_path = default_path + file_name_input + ".csv"
            ez.obj.add_data_into_tables(file_path, class_name_input)
            print(f"Data added for class {class_name_input} using file: {file_path}")
            self.manager.current = "all_present_page"
            App.get_running_app().root.transition.direction = "left"

        else:
            print("Please provide both class name and file name.")

    def build_ui(self):
        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            spacing=50,
            padding=50,
            background_color=(0, 0, 1, 1),
        )

        grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter("height"))

        class_id_input = TextInput(
            hint_text="Class Name",
            multiline=False,
            size_hint_y=None,
            height=50,
        )

        file_name_input = TextInput(
            hint_text="File Name",
            multiline=False,
            size_hint_y=None,
            height=50,
        )

        spacer = Widget(size_hint_y=None, height=200)

        proceed_button = Button(
            text="Proceed",
            size_hint_y=None,
            height=60,
            background_color=(0.9, 0, 0.9, 1),
            color=(1, 1, 1, 1),
            on_release=lambda instance: self.add_class_name_input(
                file_name_input.text, class_id_input.text
            ),
        )

        exit_button = Button(
            text="Back",
            size_hint_y=None,
            height=60,
            background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1),
            on_release=self.on_back_button,
        )

        grid_layout.add_widget(file_name_input)
        grid_layout.add_widget(class_id_input)
        grid_layout.add_widget(spacer)
        grid_layout.add_widget(proceed_button)

        layout.add_widget(grid_layout)
        layout.add_widget(exit_button)

        # self.clear_widgets()
        self.add_widget(layout)

    def on_back_button(self, instance):
        self.manager.current = "all_present_page"
        App.get_running_app().root.transition.direction = "left"

    def on_pre_enter(self, *args):
        self.build_ui()


class EditDatbase(Screen):
    def on_pre_enter(self):
        self.clear_widgets()

        main_layout = BoxLayout(orientation="vertical")

        button_layout = BoxLayout(
            orientation="vertical",
            padding=50,
            spacing=20,
            background_color=(0, 0, 1, 1),
        )

        add_button = Button(
            text="Add to Database",
            size_hint_y=(None),
            # size_hint=(0.5, None),
            height=60,
            pos_hint={"center_x": 0.5, "top": 1},
            background_color=(0.9, 0, 0.9, 1),
            color=(1, 1, 1, 1),
            on_release=self.on_add_release,
        )

        delete_button = Button(
            text="Delete from Database",
            size_hint_y=(None),
            # size_hint=(0.5, None),
            height=60,
            pos_hint={"center_x": 0.5, "top": 1},
            background_color=(0.9, 0, 0.9, 1),
            color=(1, 1, 1, 1),
            on_release=self.on_delete_release,
        )
        button_layout_back_button = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20,
            background_color=(0, 0, 1, 1),
        )
        back_button = Button(
            text="Back",
            size_hint_y=(None),
            height=40,
            background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        back_button.bind(on_release=self.on_back_release)
        button_layout.add_widget(add_button)
        button_layout.add_widget(delete_button)
        button_layout_back_button.add_widget(back_button)

        main_layout.add_widget(button_layout)
        main_layout.add_widget(button_layout_back_button)
        self.add_widget(main_layout)

    def on_add_release(self, instance):
        self.manager.current = "addtodatabase"
        App.get_running_app().root.transition.direction = "left"

    def on_delete_release(self, instance):
        self.manager.current = "deletedatabase"
        App.get_running_app().root.transition.direction = "left"

    def on_back_release(self, instance):
        self.manager.current = "all_present_page"
        App.get_running_app().root.transition.direction = "right"


class SelectResultPage(Screen):
    def on_pre_enter(self):
        absent_count = len(self.manager.get_screen("select_page").checked_items)
        self.ids.absent_count_label.text = f"Absentees: {absent_count}"


class DeleteResultPage(Screen):
    def on_pre_enter(self):
        delete_count = len(self.manager.get_screen("deletedatabase").checked_items)
        self.ids.delete_count_label.text = f"Records Deleted: {delete_count}"


class ResultPage(Screen):
    total_absent = "EVERYONE IS SUCCESSFULLY MARKED PRESENT!"

    def build_ui(self):
        self.clear_widgets()

        layout = BoxLayout(orientation="vertical")

        label_heading = Label(
            text="Result Page",
            font_size=54,
            size_hint_y=None,
            height="70dp",
            pos_hint={"center_x": 0.5, "top": 1},
        )

        grid_layout = GridLayout(cols=1)

        label_total_absent = Label(text=self.total_absent, font_size=20)

        buttons_layout = BoxLayout(size_hint_y=None, height="40dp")

        back_button = Button(
            text="Back",
            background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1),
            on_release=lambda x: self.on_back_button(),
        )

        exit_button = Button(
            text="Exit",
            background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1),
            on_release=lambda x: App.get_running_app().stop(),
        )

        buttons_layout.add_widget(back_button)
        buttons_layout.add_widget(exit_button)

        layout.add_widget(label_heading)
        layout.add_widget(grid_layout)
        grid_layout.add_widget(label_total_absent)
        grid_layout.add_widget(buttons_layout)

        self.add_widget(layout)

    def on_back_button(self):
        self.manager.current = "all_present_page"
        App.get_running_app().root.transition.direction = "right"

    def on_pre_enter(self, *args):
        self.build_ui()


class AttendanceApp(App):
    def build(self):
        kv = Builder.load_file("dkwutimdoin.kv")
        return kv


if __name__ == "__main__":
    app = AttendanceApp()
    app.run()  # Run the application
