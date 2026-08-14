import tkinter as tk
from tkinter import ttk, filedialog

from gpio import GPIO
from operation_logger import OperationLogger
from state_manager import StateManager


class MCUSimulatorGUI:
    """Scrollable GUI for the MCU Register Simulator."""

    def __init__(self, root):
        # =====================================================
        # MAIN WINDOW
        # =====================================================

        self.root = root
        self.root.title("MCU Register Simulator")
        self.root.geometry("1100x750")
        self.root.minsize(700, 500)

        # =====================================================
        # BACKEND
        # =====================================================

        self.gpio = GPIO()
        self.gpio.configure_output()

        self.logger = OperationLogger()
        self.state_manager = StateManager()

        # =====================================================
        # REGISTER DEFINITIONS
        # =====================================================

        self.registers = {
            "GPIO_CTRL": {
                "address": GPIO.GPIO_CTRL,
                "access": "RW"
            },
            "GPIO_DATA": {
                "address": GPIO.GPIO_DATA,
                "access": "RW"
            },
            "GPIO_STATUS": {
                "address": GPIO.GPIO_STATUS,
                "access": "RO"
            },
            "GPIO_CONFIG": {
                "address": 0x4000000C,
                "access": "RW"
            },
            "GPIO_COMMAND": {
                "address": 0x40000010,
                "access": "WO"
            }
        }

        # =====================================================
        # BUILD GUI
        # =====================================================

        self._build_interface()

    # =========================================================
    # SCROLLABLE INTERFACE
    # =========================================================

    def _build_interface(self):
        title = ttk.Label(
            self.root,
            text="MCU REGISTER SIMULATOR",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)

        outer_frame = ttk.Frame(self.root)
        outer_frame.pack(
            fill="both",
            expand=True
        )

        self.canvas = tk.Canvas(
            outer_frame,
            highlightthickness=0
        )
        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            outer_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.main_frame = ttk.Frame(
            self.canvas,
            padding=15
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.main_frame,
            anchor="nw"
        )

        self.main_frame.bind(
            "<Configure>",
            self._update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self._resize_scrollable_frame
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self._mouse_wheel
        )

        self.canvas.bind_all(
            "<Button-4>",
            self._mouse_wheel_linux
        )

        self.canvas.bind_all(
            "<Button-5>",
            self._mouse_wheel_linux
        )

        self._build_content()

    # =========================================================
    # BUILD CONTENT
    # =========================================================

    def _build_content(self):
        main_frame = self.main_frame

        # =====================================================
        # REGISTER SELECTOR
        # =====================================================

        selector_frame = ttk.LabelFrame(
            main_frame,
            text="Select Register",
            padding=10
        )
        selector_frame.pack(
            fill="x",
            pady=5
        )

        self.register_var = tk.StringVar(
            value="GPIO_CTRL"
        )

        self.register_selector = ttk.Combobox(
            selector_frame,
            textvariable=self.register_var,
            values=list(self.registers.keys()),
            state="readonly",
            width=30
        )
        self.register_selector.pack(
            padx=10,
            pady=5
        )

        self.register_selector.bind(
            "<<ComboboxSelected>>",
            self.on_register_selected
        )

        # =====================================================
        # REGISTER INFORMATION
        # =====================================================

        register_frame = ttk.LabelFrame(
            main_frame,
            text="Register Information",
            padding=10
        )
        register_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            register_frame,
            text="Register:"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.register_name_label = ttk.Label(
            register_frame,
            text="GPIO_CTRL"
        )
        self.register_name_label.grid(
            row=0,
            column=1,
            sticky="w",
            padx=10
        )

        ttk.Label(
            register_frame,
            text="Address:"
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        self.address_label = ttk.Label(
            register_frame,
            text="0x40000000"
        )
        self.address_label.grid(
            row=1,
            column=1,
            sticky="w",
            padx=10
        )

        ttk.Label(
            register_frame,
            text="Access:"
        ).grid(
            row=2,
            column=0,
            sticky="w"
        )

        self.access_label = ttk.Label(
            register_frame,
            text="RW"
        )
        self.access_label.grid(
            row=2,
            column=1,
            sticky="w",
            padx=10
        )

        # =====================================================
        # SIMULATOR INFORMATION
        # =====================================================

        info_frame = ttk.LabelFrame(
            main_frame,
            text="Simulator Information",
            padding=10
        )
        info_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            info_frame,
            text="MCU Model: Generic 32-bit MCU"
        ).pack(anchor="w")

        ttk.Label(
            info_frame,
            text="Peripheral: GPIO"
        ).pack(anchor="w")

        ttk.Label(
            info_frame,
            text="Register Width: 32-bit"
        ).pack(anchor="w")

        ttk.Label(
            info_frame,
            text="GPIO Pins: 8"
        ).pack(anchor="w")

        # =====================================================
        # REGISTER VALUE
        # =====================================================

        value_frame = ttk.LabelFrame(
            main_frame,
            text="Register Value",
            padding=10
        )
        value_frame.pack(
            fill="x",
            pady=5
        )

        self.value_label = ttk.Label(
            value_frame,
            text="0x00000000",
            font=("Consolas", 18, "bold")
        )
        self.value_label.pack(
            pady=8
        )

        # =====================================================
        # BINARY REPRESENTATION
        # =====================================================

        binary_frame = ttk.LabelFrame(
            main_frame,
            text="32-bit Binary Representation",
            padding=10
        )
        binary_frame.pack(
            fill="x",
            pady=5
        )

        self.binary_label = ttk.Label(
            binary_frame,
            text="00000000000000000000000000000000",
            font=("Consolas", 13)
        )
        self.binary_label.pack(
            pady=8
        )

        # =====================================================
        # REGISTER BITS
        # =====================================================

        bit_frame = ttk.LabelFrame(
            main_frame,
            text="Register Bits",
            padding=10
        )
        bit_frame.pack(
            fill="x",
            pady=5
        )

        self.bit_buttons = []

        for bit in range(31, -1, -1):
            button = tk.Button(
                bit_frame,
                text="0",
                width=3,
                command=lambda b=bit: self.toggle_register_bit(b)
            )

            button.grid(
                row=0,
                column=31 - bit,
                padx=1,
                pady=2
            )

            ttk.Label(
                bit_frame,
                text=str(bit),
                font=("Arial", 8)
            ).grid(
                row=1,
                column=31 - bit
            )

            self.bit_buttons.append(button)

        ttk.Label(
            bit_frame,
            text="MSB (31)"
        ).grid(
            row=2,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(5, 0)
        )

        ttk.Label(
            bit_frame,
            text="LSB (0)"
        ).grid(
            row=2,
            column=28,
            columnspan=4,
            sticky="e",
            pady=(5, 0)
        )

        # =====================================================
        # REGISTER FIELDS
        # =====================================================

        self.field_frame = ttk.LabelFrame(
            main_frame,
            text="Register Fields",
            padding=10
        )
        self.field_frame.pack(
            fill="x",
            pady=5
        )

        # =====================================================
        # WRITE REGISTER
        # =====================================================

        write_frame = ttk.LabelFrame(
            main_frame,
            text="Write Register",
            padding=10
        )
        write_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            write_frame,
            text="Hex Value:"
        ).pack(side="left")

        self.write_entry = ttk.Entry(
            write_frame,
            width=20
        )
        self.write_entry.pack(
            side="left",
            padx=10
        )

        self.write_entry.bind(
            "<Return>",
            lambda event: self.write_register()
        )

        ttk.Button(
            write_frame,
            text="CLEAR",
            command=self.clear_input
        ).pack(
            side="left",
            padx=5
        )

        # =====================================================
        # REGISTER BUTTONS
        # =====================================================

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(
            pady=8
        )

        ttk.Button(
            button_frame,
            text="READ",
            command=self.read_register
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="WRITE",
            command=self.write_register
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="RESET REGISTER",
            command=self.reset_register
        ).pack(
            side="left",
            padx=5
        )

        # =====================================================
        # STATE MANAGEMENT
        # =====================================================

        state_frame = ttk.LabelFrame(
            main_frame,
            text="Simulator State",
            padding=10
        )
        state_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Button(
            state_frame,
            text="SAVE STATE",
            command=self.save_state
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            state_frame,
            text="LOAD STATE",
            command=self.load_state
        ).pack(
            side="left",
            padx=5
        )

        # =====================================================
        # GPIO PIN DISPLAY
        # =====================================================

        gpio_frame = ttk.LabelFrame(
            main_frame,
            text="GPIO Pins",
            padding=10
        )
        gpio_frame.pack(
            fill="x",
            pady=5
        )

        self.pin_labels = []

        for pin in range(8):
            label = ttk.Label(
                gpio_frame,
                text=f"GPIO{pin}: LOW",
                width=14
            )

            label.grid(
                row=0,
                column=pin,
                padx=4,
                pady=4
            )

            self.pin_labels.append(label)

        # =====================================================
        # GPIO CONTROLS
        # =====================================================

        gpio_control_frame = ttk.LabelFrame(
            main_frame,
            text="GPIO Peripheral Controls",
            padding=10
        )
        gpio_control_frame.pack(
            fill="x",
            pady=5
        )

        # -----------------------------------------------------
        # ENABLE / DISABLE
        # -----------------------------------------------------

        enable_frame = ttk.Frame(
            gpio_control_frame
        )
        enable_frame.pack(
            fill="x",
            pady=3
        )

        ttk.Label(
            enable_frame,
            text="Peripheral:"
        ).pack(side="left")

        ttk.Button(
            enable_frame,
            text="ENABLE",
            command=self.enable_gpio
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            enable_frame,
            text="DISABLE",
            command=self.disable_gpio
        ).pack(
            side="left",
            padx=5
        )

        # -----------------------------------------------------
        # MODE
        # -----------------------------------------------------

        mode_frame = ttk.Frame(
            gpio_control_frame
        )
        mode_frame.pack(
            fill="x",
            pady=3
        )

        ttk.Label(
            mode_frame,
            text="Mode:"
        ).pack(side="left")

        self.gpio_mode_var = tk.StringVar(
            value="OUTPUT"
        )

        self.gpio_mode_selector = ttk.Combobox(
            mode_frame,
            textvariable=self.gpio_mode_var,
            values=["INPUT", "OUTPUT"],
            state="readonly",
            width=12
        )
        self.gpio_mode_selector.pack(
            side="left",
            padx=10
        )

        self.gpio_mode_selector.bind(
            "<<ComboboxSelected>>",
            self.on_gpio_mode_changed
        )

        # -----------------------------------------------------
        # GPIO STATUS
        # -----------------------------------------------------

        status_frame = ttk.Frame(
            gpio_control_frame
        )
        status_frame.pack(
            fill="x",
            pady=3
        )

        ttk.Label(
            status_frame,
            text="Ready:"
        ).pack(side="left")

        self.gpio_ready_label = ttk.Label(
            status_frame,
            text="READY"
        )
        self.gpio_ready_label.pack(
            side="left",
            padx=5
        )

        ttk.Label(
            status_frame,
            text="Error:"
        ).pack(
            side="left",
            padx=(20, 0)
        )

        self.gpio_error_label = ttk.Label(
            status_frame,
            text="OK"
        )
        self.gpio_error_label.pack(
            side="left",
            padx=5
        )

        ttk.Button(
            status_frame,
            text="CLEAR ERROR",
            command=self.clear_gpio_error
        ).pack(
            side="left",
            padx=10
        )

        ttk.Button(
            status_frame,
            text="RESET GPIO",
            command=self.reset_gpio
        ).pack(
            side="left",
            padx=5
        )

        # -----------------------------------------------------
        # INDIVIDUAL GPIO CONTROLS
        # -----------------------------------------------------

        pin_control_frame = ttk.Frame(
            gpio_control_frame
        )
        pin_control_frame.pack(
            fill="x",
            pady=5
        )

        self.gpio_control_buttons = []

        for pin in range(8):
            pin_frame = ttk.LabelFrame(
                pin_control_frame,
                text=f"GPIO{pin}",
                padding=4
            )
            pin_frame.grid(
                row=0,
                column=pin,
                padx=2
            )

            set_button = ttk.Button(
                pin_frame,
                text="SET",
                width=7,
                command=lambda p=pin: self.set_gpio_pin(p)
            )
            set_button.pack(pady=2)

            clear_button = ttk.Button(
                pin_frame,
                text="CLEAR",
                width=7,
                command=lambda p=pin: self.clear_gpio_pin(p)
            )
            clear_button.pack(pady=2)

            toggle_button = ttk.Button(
                pin_frame,
                text="TOGGLE",
                width=7,
                command=lambda p=pin: self.toggle_gpio_pin(p)
            )
            toggle_button.pack(pady=2)

            self.gpio_control_buttons.append(
                (
                    set_button,
                    clear_button,
                    toggle_button
                )
            )

        # =====================================================
        # OPERATION HISTORY
        # =====================================================

        history_frame = ttk.LabelFrame(
            main_frame,
            text="Operation History",
            padding=10
        )
        history_frame.pack(
            fill="both",
            expand=True,
            pady=5
        )

        history_list_frame = ttk.Frame(
            history_frame
        )
        history_list_frame.pack(
            fill="both",
            expand=True
        )

        self.history_list = tk.Listbox(
            history_list_frame,
            height=10,
            font=("Consolas", 10)
        )
        self.history_list.pack(
            side="left",
            fill="both",
            expand=True
        )

        history_scrollbar = ttk.Scrollbar(
            history_list_frame,
            orient="vertical",
            command=self.history_list.yview
        )
        history_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.history_list.configure(
            yscrollcommand=history_scrollbar.set
        )

        ttk.Button(
            history_frame,
            text="CLEAR HISTORY",
            command=self.clear_history
        ).pack(
            pady=5
        )

        # =====================================================
        # SIMULATOR STATUS
        # =====================================================

        simulator_status_frame = ttk.LabelFrame(
            main_frame,
            text="Simulator Status",
            padding=8
        )
        simulator_status_frame.pack(
            fill="x",
            pady=5
        )

        self.status_label = ttk.Label(
            simulator_status_frame,
            text="Ready."
        )
        self.status_label.pack(
            anchor="w"
        )

        # =====================================================
        # INITIAL UPDATE
        # =====================================================

        self.update_register_display()
        self.update_field_display()
        self.update_gpio_display()
        self.update_gpio_status_display()
        self.update_history_display()

    # =========================================================
    # SCROLLING
    # =========================================================

    def _update_scroll_region(self, event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def _resize_scrollable_frame(self, event):
        self.canvas.itemconfigure(
            self.canvas_window,
            width=event.width
        )

    def _mouse_wheel(self, event):
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def _mouse_wheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(
                -3,
                "units"
            )
        elif event.num == 5:
            self.canvas.yview_scroll(
                3,
                "units"
            )

    # =========================================================
    # STATUS MESSAGE
    # =========================================================

    def set_status(self, message):
        self.status_label.config(
            text=message
        )

    # =========================================================
    # INPUT
    # =========================================================

    def clear_input(self):
        self.write_entry.delete(
            0,
            tk.END
        )

        self.set_status(
            "Input cleared."
        )

    # =========================================================
    # OPERATION LOGGING
    # =========================================================

    def log_operation(
        self,
        operation,
        target,
        value=None
    ):
        self.logger.log(
            operation,
            target,
            value
        )

        self.update_history_display()

    def update_history_display(self):
        self.history_list.delete(
            0,
            tk.END
        )

        for entry in self.logger.get_history():
            line = (
                f"{entry['time']}  "
                f"{entry['operation']:<8} "
                f"{entry['target']:<20}"
            )

            if entry["value"] is not None:
                line += f" {entry['value']}"

            self.history_list.insert(
                tk.END,
                line
            )

        self.history_list.yview_moveto(1.0)

    def clear_history(self):
        self.logger.clear()

        self.update_history_display()

        self.set_status(
            "Operation history cleared."
        )

    # =========================================================
    # REGISTER SELECTION
    # =========================================================

    def get_selected_register(self):
        name = self.register_var.get()

        if name not in self.registers:
            raise ValueError(
                f"Unknown register: {name}"
            )

        return self.registers[name]

    def on_register_selected(self, event=None):
        register_name = self.register_var.get()
        register_info = self.get_selected_register()

        self.register_name_label.config(
            text=register_name
        )

        self.address_label.config(
            text=f"0x{register_info['address']:08X}"
        )

        self.access_label.config(
            text=register_info["access"]
        )

        self.update_register_display()
        self.update_field_display()

        self.set_status(
            f"Selected register: {register_name}"
        )

    # =========================================================
    # REGISTER DISPLAY
    # =========================================================

    def update_register_display(self):
        register_name = self.register_var.get()
        register_info = self.get_selected_register()

        address = register_info["address"]
        access = register_info["access"]

        self.register_name_label.config(
            text=register_name
        )

        self.address_label.config(
            text=f"0x{address:08X}"
        )

        self.access_label.config(
            text=access
        )

        if access == "WO":
            self.value_label.config(
                text="WRITE-ONLY"
            )

            self.binary_label.config(
                text="READ NOT AVAILABLE"
            )

            self.update_bit_display()
            return

        try:
            value = (
                self.gpio
                .get_register_map()
                .read(address)
            )

            self.value_label.config(
                text=f"0x{value:08X}"
            )

            self.binary_label.config(
                text=f"{value:032b}"
            )

        except PermissionError:
            self.value_label.config(
                text="READ NOT AVAILABLE"
            )

            self.binary_label.config(
                text="READ NOT AVAILABLE"
            )

        self.update_bit_display()

    # =========================================================
    # BIT DISPLAY
    # =========================================================

    def update_bit_display(self):
        register_info = self.get_selected_register()

        address = register_info["address"]
        access = register_info["access"]

        if access == "WO":
            for button in self.bit_buttons:
                button.config(
                    text="-",
                    state="disabled"
                )
            return

        try:
            value = (
                self.gpio
                .get_register_map()
                .read(address)
            )

        except PermissionError:
            for button in self.bit_buttons:
                button.config(
                    text="-",
                    state="disabled"
                )
            return

        for index, bit in enumerate(
            range(31, -1, -1)
        ):
            bit_value = (
                value >> bit
            ) & 1

            self.bit_buttons[index].config(
                text=str(bit_value)
            )

            if access == "RO":
                self.bit_buttons[index].config(
                    state="disabled"
                )
            else:
                self.bit_buttons[index].config(
                    state="normal"
                )

    # =========================================================
    # TOGGLE REGISTER BIT
    # =========================================================

    def toggle_register_bit(self, bit):
        register_info = self.get_selected_register()

        address = register_info["address"]
        access = register_info["access"]

        if access != "RW":
            self.set_status(
                "ERROR: This register cannot be modified."
            )
            return

        try:
            register = (
                self.gpio
                .get_register_map()
                .registers[address]
            )

            register.toggle_bit(bit)

            self.update_register_display()
            self.update_field_display()
            self.update_gpio_display()

            self.log_operation(
                "BIT",
                f"{self.register_var.get()}.bit{bit}"
            )

            self.set_status(
                f"Bit {bit} toggled."
            )

        except PermissionError:
            self.set_status(
                "ERROR: Write operation not allowed."
            )

    # =========================================================
    # REGISTER FIELDS
    # =========================================================

    def update_field_display(self):
        for widget in self.field_frame.winfo_children():
            widget.destroy()

        register_info = self.get_selected_register()

        address = register_info["address"]
        access = register_info["access"]

        register = (
            self.gpio
            .get_register_map()
            .registers[address]
        )

        if not register.fields:
            ttk.Label(
                self.field_frame,
                text="This register has no named fields."
            ).pack(
                anchor="w"
            )
            return

        ttk.Label(
            self.field_frame,
            text="FIELD",
            width=15
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5
        )

        ttk.Label(
            self.field_frame,
            text="BITS",
            width=10
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=5
        )

        ttk.Label(
            self.field_frame,
            text="VALUE",
            width=12
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=5
        )

        ttk.Label(
            self.field_frame,
            text="ACTION",
            width=12
        ).grid(
            row=0,
            column=3,
            sticky="w",
            padx=5
        )

        for row, (field_name, field) in enumerate(
            register.fields.items(),
            start=1
        ):
            bit_msb = field.lsb + field.width - 1
            bit_lsb = field.lsb

            ttk.Label(
                self.field_frame,
                text=field_name,
                width=15
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=5,
                pady=3
            )

            ttk.Label(
                self.field_frame,
                text=f"{bit_msb}:{bit_lsb}",
                width=10
            ).grid(
                row=row,
                column=1,
                sticky="w",
                padx=5
            )

            try:
                current_value = register.read_field(
                    field_name
                )
            except PermissionError:
                current_value = "N/A"

            value_var = tk.StringVar(
                value=str(current_value)
            )

            value_entry = ttk.Entry(
                self.field_frame,
                textvariable=value_var,
                width=12
            )
            value_entry.grid(
                row=row,
                column=2,
                sticky="w",
                padx=5
            )

            value_entry.bind(
                "<Return>",
                lambda event,
                name=field_name,
                var=value_var:
                self.write_field_value(
                    name,
                    var
                )
            )

            write_button = ttk.Button(
                self.field_frame,
                text="WRITE",
                command=lambda
                name=field_name,
                var=value_var:
                self.write_field_value(
                    name,
                    var
                )
            )

            write_button.grid(
                row=row,
                column=3,
                sticky="w",
                padx=5
            )

            if access != "RW":
                value_entry.config(
                    state="disabled"
                )

                write_button.config(
                    state="disabled"
                )

    def write_field_value(
        self,
        field_name,
        value_var
    ):
        register_info = self.get_selected_register()

        address = register_info["address"]

        try:
            value_text = value_var.get().strip()

            if not value_text:
                self.set_status(
                    f"ERROR: Enter a value for {field_name}."
                )
                return

            value = int(
                value_text,
                10
            )

            register = (
                self.gpio
                .get_register_map()
                .registers[address]
            )

            register.write_field(
                field_name,
                value
            )

            self.update_register_display()
            self.update_field_display()
            self.update_gpio_display()
            self.update_gpio_status_display()

            self.log_operation(
                "FIELD",
                f"{self.register_var.get()}.{field_name}",
                str(value)
            )

            self.set_status(
                f"{field_name} updated to {value}."
            )

        except ValueError as error:
            self.set_status(
                f"ERROR: {error}"
            )

        except TypeError as error:
            self.set_status(
                f"ERROR: {error}"
            )

        except PermissionError:
            self.set_status(
                "ERROR: This register cannot be modified."
            )

    # =========================================================
    # READ
    # =========================================================

    def read_register(self):
        try:
            register_info = self.get_selected_register()

            register_name = self.register_var.get()
            address = register_info["address"]

            value = (
                self.gpio
                .get_register_map()
                .read(address)
            )

            self.update_register_display()
            self.update_field_display()
            self.update_gpio_display()
            self.update_gpio_status_display()

            self.log_operation(
                "READ",
                register_name,
                f"0x{value:08X}"
            )

            self.set_status(
                "Register read successful."
            )

        except Exception as error:
            self.set_status(
                f"ERROR: {error}"
            )

    # =========================================================
    # WRITE
    # =========================================================

    def write_register(self):
        text = self.write_entry.get().strip()

        if not text:
            self.set_status(
                "ERROR: Enter a hexadecimal value."
            )
            return

        try:
            value = int(
                text,
                16
            )

            if value < 0 or value > 0xFFFFFFFF:
                self.set_status(
                    "ERROR: Value must be between "
                    "0x00000000 and 0xFFFFFFFF."
                )
                return

            register_info = self.get_selected_register()

            register_name = self.register_var.get()
            address = register_info["address"]

            self.gpio.get_register_map().write(
                address,
                value
            )

            self.update_register_display()
            self.update_field_display()
            self.update_gpio_display()
            self.update_gpio_status_display()

            self.log_operation(
                "WRITE",
                register_name,
                f"0x{value:08X}"
            )

            self.set_status(
                f"Write successful: 0x{value:08X}"
            )

        except PermissionError:
            self.set_status(
                "ERROR: This register is read-only."
            )

        except ValueError:
            self.set_status(
                "ERROR: Enter a valid hexadecimal value."
            )

    # =========================================================
    # RESET REGISTER
    # =========================================================

    def reset_register(self):
        register_info = self.get_selected_register()

        register_name = self.register_var.get()
        address = register_info["address"]

        try:
            self.gpio.get_register_map().reset(
                address
            )

            self.update_register_display()
            self.update_field_display()
            self.update_gpio_display()
            self.update_gpio_status_display()

            self.log_operation(
                "RESET",
                register_name
            )

            self.set_status(
                "Register reset successfully."
            )

        except Exception as error:
            self.set_status(
                f"ERROR: {error}"
            )

    # =========================================================
    # SAVE STATE
    # =========================================================

    def save_state(self):
        filename = filedialog.asksaveasfilename(
            title="Save Simulator State",
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )

        if not filename:
            return

        try:
            self.state_manager.save_state(
                self.gpio,
                filename
            )

            self.log_operation(
                "SAVE",
                filename
            )

            self.set_status(
                f"State saved: {filename}"
            )

        except OSError as error:
            self.set_status(
                f"ERROR saving state: {error}"
            )

    # =========================================================
    # LOAD STATE
    # =========================================================

    def load_state(self):
        filename = filedialog.askopenfilename(
            title="Load Simulator State",
            filetypes=[
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )

        if not filename:
            return

        try:
            self.state_manager.load_state(
                self.gpio,
                filename
            )

            self.update_register_display()
            self.update_field_display()
            self.update_gpio_display()
            self.update_gpio_status_display()

            self.log_operation(
                "LOAD",
                filename
            )

            self.set_status(
                f"State loaded: {filename}"
            )

        except (
            OSError,
            ValueError,
            KeyError
        ) as error:
            self.set_status(
                f"ERROR loading state: {error}"
            )

    # =========================================================
    # GPIO DISPLAY
    # =========================================================

    def update_gpio_display(self):
        try:
            enabled = (
                self.gpio
                .get_register_map()
                .read_field(
                    GPIO.GPIO_CTRL,
                    GPIO.ENABLE_FIELD
                )
                == 1
            )

        except PermissionError:
            enabled = False

        if not enabled:
            for pin in range(8):
                self.pin_labels[pin].config(
                    text=f"GPIO{pin}: DISABLED"
                )
            return

        for pin in range(8):
            try:
                state = self.gpio.read_pin(pin)

                if state:
                    text = f"GPIO{pin}: HIGH"
                else:
                    text = f"GPIO{pin}: LOW"

            except RuntimeError:
                text = f"GPIO{pin}: ERROR"

            self.pin_labels[pin].config(
                text=text
            )

    # =========================================================
    # GPIO STATUS
    # =========================================================

    def update_gpio_status_display(self):
        try:
            ready = self.gpio.is_ready()
            error = self.gpio.has_error()

            self.gpio_ready_label.config(
                text="READY"
                if ready
                else "DISABLED"
            )

            self.gpio_error_label.config(
                text="ERROR"
                if error
                else "OK"
            )

            for buttons in self.gpio_control_buttons:
                for button in buttons:
                    button.config(
                        state="normal"
                        if ready
                        else "disabled"
                    )

        except Exception:
            self.gpio_ready_label.config(
                text="UNKNOWN"
            )

            self.gpio_error_label.config(
                text="UNKNOWN"
            )

    # =========================================================
    # ENABLE GPIO
    # =========================================================

    def enable_gpio(self):
        try:
            self.gpio.enable()

            self.update_register_display()
            self.update_field_display()
            self.update_gpio_display()
            self.update_gpio_status_display()

            self.log_operation(
                "ENABLE",
                "GPIO"
            )

            self.set_status(
                "GPIO peripheral enabled."
            )

        except Exception as error:
            self.set_status(
                f"GPIO ERROR: {error}"
            )

    # =========================================================
    # DISABLE GPIO
    # =========================================================

    def disable_gpio(self):
        try:
            self.gpio.disable()

            self.update_register_display()
            self.update_field_display()
            self.update_gpio_display()
            self.update_gpio_status_display()

            self.log_operation(
                "DISABLE",
                "GPIO"
            )

            self.set_status(
                "GPIO peripheral disabled."
            )

        except Exception as error:
            self.set_status(
                f"GPIO ERROR: {error}"
            )

    # =========================================================
    # GPIO MODE
    # =========================================================

    def on_gpio_mode_changed(self, event=None):
        mode = self.gpio_mode_var.get()

        try:
            if mode == "OUTPUT":
                self.gpio.configure_output()

            elif mode == "INPUT":
                self.gpio.configure_input()

            self.update_register_display()
            self.update_field_display()
            self.update_gpio_display()
            self.update_gpio_status_display()

            self.set_status(
                f"GPIO mode changed to {mode}."
            )

        except Exception as error:
            self.set_status(
                f"GPIO ERROR: {error}"
            )

    # =========================================================
    # SET GPIO PIN
    # =========================================================

    def set_gpio_pin(self, pin):
        try:
            self.gpio.set_pin(pin)

            self.update_register_display()
            self.update_field_display()
            self.update_gpio_display()
            self.update_gpio_status_display()

            self.log_operation(
                "SET",
                f"GPIO{pin}"
            )

            self.set_status(
                f"GPIO{pin} set HIGH."
            )

        except (
            RuntimeError,
            ValueError,
            TypeError
        ) as error:
            self.update_gpio_status_display()

            self.set_status(
                f"GPIO ERROR: {error}"
            )

    # =========================================================
    # CLEAR GPIO PIN
    # =========================================================

    def clear_gpio_pin(self, pin):
        try:
            self.gpio.clear_pin(pin)

            self.update_register_display()
            self.update_field_display()
            self.update_gpio_display()
            self.update_gpio_status_display()

            self.log_operation(
                "CLEAR",
                f"GPIO{pin}"
            )

            self.set_status(
                f"GPIO{pin} set LOW."
            )

        except (
            RuntimeError,
            ValueError,
            TypeError
        ) as error:
            self.update_gpio_status_display()

            self.set_status(
                f"GPIO ERROR: {error}"
            )

    # =========================================================
    # TOGGLE GPIO PIN
    # =========================================================

    def toggle_gpio_pin(self, pin):
        try:
            self.gpio.toggle_pin(pin)

            self.update_register_display()
            self.update_field_display()
            self.update_gpio_display()
            self.update_gpio_status_display()

            self.log_operation(
                "TOGGLE",
                f"GPIO{pin}"
            )

            self.set_status(
                f"GPIO{pin} toggled."
            )

        except (
            RuntimeError,
            ValueError,
            TypeError
        ) as error:
            self.update_gpio_status_display()

            self.set_status(
                f"GPIO ERROR: {error}"
            )

    # =========================================================
    # CLEAR GPIO ERROR
    # =========================================================

    def clear_gpio_error(self):
        self.gpio.clear_error()

        self.update_register_display()
        self.update_field_display()
        self.update_gpio_display()
        self.update_gpio_status_display()

        self.set_status(
            "GPIO error cleared."
        )

    # =========================================================
    # RESET GPIO
    # =========================================================

    def reset_gpio(self):
        self.gpio = GPIO()
        self.gpio.configure_output()

        self.update_register_display()
        self.update_field_display()
        self.update_gpio_display()
        self.update_gpio_status_display()

        self.log_operation(
            "RESET",
            "GPIO"
        )

        self.set_status(
            "GPIO peripheral reset."
        )


# =============================================================
# PROGRAM ENTRY POINT
# =============================================================

def main():
    root = tk.Tk()

    MCUSimulatorGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()