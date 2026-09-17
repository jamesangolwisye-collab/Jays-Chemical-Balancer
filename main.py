from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from chempy import balance_stoichiometry

# Set window background color
Window.clearcolor = get_color_from_hex("#F5F5F5")


def make_subscript(text):
    subscript_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return text.translate(subscript_map)


class ChemicalBalancer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)

        # ===== LOGO / TITLE =====
        self.add_widget(Label(
            text="⚛",
            font_size='48sp',
            color=get_color_from_hex("#1976D2"),
            size_hint_y=None,
            height=70
        ))

        self.add_widget(Label(
            text="JAY'S CHEMICAL BALANCER",
            font_size='22sp',
            bold=True,
            color=get_color_from_hex("#1A237E"),
            size_hint_y=None,
            height=40
        ))

        self.add_widget(Label(
            text="Engineered by James Angolwisye",
            font_size='12sp',
            italic=True,
            color=get_color_from_hex("#78909C"),
            size_hint_y=None,
            height=25
        ))

        # ===== INPUT =====
        self.add_widget(Label(
            text="Enter Equation (e.g. C3H8 + O2 -> CO2 + H2O)",
            font_size='13sp',
            color=get_color_from_hex("#546E7A"),
            size_hint_y=None,
            height=30
        ))

        self.entry = TextInput(
            hint_text="Type equation here...",
            font_size='18sp',
            multiline=False,
            size_hint_y=None,
            height=50,
            background_color=get_color_from_hex("#FFFFFF"),
            foreground_color=get_color_from_hex("#000000"),
            padding=[15, 12]
        )
        self.add_widget(self.entry)

        # ===== BUTTONS =====
        btn_layout = BoxLayout(size_hint_y=None, height=55, spacing=15)

        balance_btn = Button(
            text="BALANCE EQUATION",
            background_color=get_color_from_hex("#1976D2"),
            color=get_color_from_hex("#FFFFFF"),
            bold=True,
            font_size='16sp'
        )
        balance_btn.bind(on_press=self.balance_equation)
        btn_layout.add_widget(balance_btn)

        clear_btn = Button(
            text="Clear",
            background_color=get_color_from_hex("#757575"),
            color=get_color_from_hex("#FFFFFF"),
            font_size='15sp',
            size_hint_x=0.35
        )
        clear_btn.bind(on_press=self.clear_all)
        btn_layout.add_widget(clear_btn)

        self.add_widget(btn_layout)

        # ===== RESULT =====
        self.result_label = Label(
            text="Waiting for input...",
            font_size='18sp',
            bold=True,
            color=get_color_from_hex("#757575"),
            size_hint_y=None,
            height=80,
            text_size=(Window.width - 60, None),
            halign='center',
            valign='middle'
        )
        self.add_widget(self.result_label)

        # ===== HISTORY =====
        self.add_widget(Label(
            text="RECENT CALCULATIONS",
            font_size='12sp',
            bold=True,
            color=get_color_from_hex("#9E9E9E"),
            size_hint_y=None,
            height=30
        ))

        self.history_label = Label(
            text="",
            font_size='15sp',
            color=get_color_from_hex("#333333"),
            size_hint_y=None,
            height=150,
            text_size=(Window.width - 60, None),
            halign='left',
            valign='top'
        )
        
        scroll = ScrollView(size_hint=(1, None), height=160)
        scroll.add_widget(self.history_label)
        self.add_widget(scroll)

        self.history = []

    def balance_equation(self, instance):
        self.result_label.color = get_color_from_hex("#000000")
        user_input = self.entry.text.strip()

        if not user_input:
            self.result_label.text = "Please enter an equation!"
            self.result_label.color = get_color_from_hex("#E65100")
            return

        if '->' not in user_input:
            self.result_label.text = "Error: Missing '->' arrow"
            self.result_label.color = get_color_from_hex("#B71C1C")
            return

        try:
            left_side, right_side = user_input.split('->')
            reactants = [m.strip() for m in left_side.split('+') if m.strip()]
            products = [m.strip() for m in right_side.split('+') if m.strip()]

            reac, prod = balance_stoichiometry(set(reactants), set(products))

            reac_str = " + ".join([f"{count if count > 1 else ''}{make_subscript(mol)}" for mol, count in reac.items()])
            prod_str = " + ".join([f"{count if count > 1 else ''}{make_subscript(mol)}" for mol, count in prod.items()])

            final_result = f"{reac_str} → {prod_str}"

            self.result_label.text = final_result
            self.result_label.color = get_color_from_hex("#2E7D32")

            # Add to history
            self.history.insert(0, final_result)
            if len(self.history) > 5:
                self.history = self.history[:5]
            self.history_label.text = "\n".join(self.history)

        except Exception:
            self.result_label.text = "Invalid Equation.\nExample: H2 + O2 -> H2O"
            self.result_label.color = get_color_from_hex("#B71C1C")

    def clear_all(self, instance):
        self.entry.text = ""
        self.result_label.text = "Waiting for input..."
        self.result_label.color = get_color_from_hex("#757575")


class ChemicalBalancerApp(App):
    def build(self):
        self.title = "Jay's Chemical Balancer"
        return ChemicalBalancer()


if __name__ == '__main__':
    ChemicalBalancerApp().run()