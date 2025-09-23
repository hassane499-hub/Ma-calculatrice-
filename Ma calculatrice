# calculatrice.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.metrics import dp
import math
import ast

# Fond noir
Window.clearcolor = (0, 0, 0, 1)

# ---------- SafeEval (sécurisé, prend en charge fonctions utiles) ----------
class SafeEval:
    ALLOWED_NODES = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Load,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd,
        ast.Mod, ast.FloorDiv, ast.Constant, ast.Call, ast.Name, ast.Tuple
    )

    SAFE_FUNCTIONS = {
        "sqrt": math.sqrt,
        "ln": math.log,
        "log10": math.log10,
        "log": math.log10,   # log -> log10 (pour usage commun)
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tan": lambda x: math.tan(math.radians(x)),
        "asin": lambda x: math.degrees(math.asin(x)),
        "acos": lambda x: math.degrees(math.acos(x)),
        "atan": lambda x: math.degrees(math.atan(x)),
        "abs": abs,
        "pow": pow,
        "pi": math.pi,
        "e": math.e,
    }

    @classmethod
    def eval(cls, expression: str):
        try:
            # Normalisations usuelles
            expression = expression.replace('π', 'pi').replace('^', '**').replace('×', '*').replace('÷', '/').replace(',', '.')
            node = ast.parse(expression, mode="eval")
            for subnode in ast.walk(node):
                if not isinstance(subnode, cls.ALLOWED_NODES):
                    raise ValueError("Expression non autorisée")
                if isinstance(subnode, ast.Attribute):
                    raise ValueError("Expression non autorisée")
            return eval(compile(node, "<string>", "eval"), {"__builtins__": {}}, cls.SAFE_FUNCTIONS)
        except ZeroDivisionError:
            raise
        except Exception:
            return "Erreur"

# ---------- Style ----------
BTN_BG = (0.03, 0.16, 0.16, 1)    # foncé
BTN_TEXT = (0.04, 0.85, 0.85, 1)  # turquoise clair
BTN_RED = (0.85, 0.08, 0.08, 1)
BTN_WHITE = (1, 1, 1, 1)

# ---------- Utilitaires UI ----------
def styled_button(label, callback, font_sp=dp(32), bg=None, fg=None):
    if bg is None:
        bg = BTN_BG
    if fg is None:
        fg = BTN_TEXT
    b = Button(text=label, font_size=font_sp, bold=True,
               background_normal='', background_color=bg, color=fg)
    b.bind(on_press=callback)
    return b

# ---------- État partagé ----------
class CalcState:
    expr = ""


# ---------- Écran de base ----------
class BasicScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=10, spacing=8)

        # affichage (50% haut)
        self.display = Label(text="", markup=True, halign='right', valign='middle')
        self.display.font_size = dp(64)   # très gros
        self.display.size_hint_y = 0.5
        self.display.bind(size=self._update_textsize)
        root.add_widget(self.display)

        # keypad (50% bas)
        keypad = BoxLayout(orientation='vertical', size_hint_y=0.5, spacing=6)

        grid = GridLayout(cols=4, spacing=6)
        rows = [
            ["C", "DEL", "(", ")"],
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "-"],
            ["+/-", "0", ".", "+"],
        ]
        for row in rows:
            for label in row:
                if label in ("C", "DEL"):
                    b = styled_button(label, self.on_button, bg=BTN_RED, fg=BTN_WHITE)
                elif label == "=":
                    b = styled_button(label, self.on_eq, bg=BTN_WHITE, fg=(0,0,0,1))
                else:
                    b = styled_button(label, self.on_button)
                grid.add_widget(b)

        keypad.add_widget(grid)

        # bottom row: = and switch
        bottom = BoxLayout(size_hint_y=None, height=dp(72), spacing=6)
        eq_btn = styled_button("=", self.on_eq, bg=BTN_WHITE, fg=(0,0,0,1), font_sp=dp(36))
        switch_btn = styled_button("Fonctions avancées", self.switch_to_adv, font_sp=dp(28))
        bottom.add_widget(eq_btn)
        bottom.add_widget(switch_btn)
        keypad.add_widget(bottom)

        root.add_widget(keypad)
        self.add_widget(root)

        # sync display at start
        self.on_pre_enter = self.sync_display

    def _update_textsize(self, *_):
        self.display.text_size = (self.display.width - dp(20), None)

    def sync_display(self, *a):
        self.display.text = f"[b]{CalcState.expr}[/b]" if CalcState.expr else ""

    def on_button(self, instance):
        lbl = instance.text
        if lbl == "C":
            CalcState.expr = ""
        elif lbl == "DEL":
            CalcState.expr = CalcState.expr[:-1]
        elif lbl == "+/-":
            expr = CalcState.expr
            if not expr: return
            i = len(expr)-1
            while i>=0 and (expr[i].isdigit() or expr[i]=='.'):
                i -= 1
            last = expr[i+1:]
            if not last: return
            if last.startswith('-'):
                new = last[1:]
            else:
                new = '-' + last
            CalcState.expr = expr[:i+1] + new
        else:
            CalcState.expr += lbl
        self.sync_display()

    def on_eq(self, instance):
        if not CalcState.expr:
            return
        try:
            res = SafeEval.eval(CalcState.expr)
            if res == "Erreur":
                self.display.text = "Erreur"
                CalcState.expr = ""
            else:
                CalcState.expr = str(res)
                self.sync_display()
        except ZeroDivisionError:
            self.display.text = "Erreur : Division par zéro"
            CalcState.expr = ""
        except Exception:
            self.display.text = "Erreur"
            CalcState.expr = ""

    def switch_to_adv(self, instance):
        # ensure advanced screen gets current expr
        adv = self.manager.get_screen('advanced')
        adv.sync_from_state()
        self.manager.transition = SlideTransition(direction='left', duration=0.18)
        self.manager.current = 'advanced'


# ---------- Écran avancé ----------
class AdvancedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=10, spacing=8)

        # affichage (partagé)
        self.display = Label(text="", markup=True, halign='right', valign='middle')
        self.display.font_size = dp(64)
        self.display.size_hint_y = 0.5
        self.display.bind(size=self._update_textsize)
        root.add_widget(self.display)

        # keypad (bas 50%)
        keypad = BoxLayout(orientation='vertical', size_hint_y=0.5, spacing=6)

        grid = GridLayout(cols=4, spacing=6)
        # Disposition : C / DEL on top-left ; sin/cos under them (as requested)
        rows = [
            ["C", "DEL", "(", ")"],
            ["sin", "cos", "tan", "%"],
            ["asin", "acos", "atan", "√"],
            ["ln", "log10", "x²", "^"],
            ["π", "e", "1/x", "abs"],
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "-"],
            ["+/-", "0", ".", "+"],
        ]
        for row in rows:
            for label in row:
                if label in ("C", "DEL"):
                    b = styled_button(label, self.on_button, bg=BTN_RED, fg=BTN_WHITE)
                elif label == "=":
                    b = styled_button(label, self.on_eq, bg=BTN_WHITE, fg=(0,0,0,1))
                else:
                    b = styled_button(label, self.on_button)
                grid.add_widget(b)

        keypad.add_widget(grid)

        # bottom row: = and retour
        bottom = BoxLayout(size_hint_y=None, height=dp(72), spacing=6)
        eq_btn = styled_button("=", self.on_eq, bg=BTN_WHITE, fg=(0,0,0,1), font_sp=dp(36))
        back_btn = styled_button("Retour", self.switch_to_basic, font_sp=dp(28))
        bottom.add_widget(eq_btn)
        bottom.add_widget(back_btn)
        keypad.add_widget(bottom)

        root.add_widget(keypad)
        self.add_widget(root)

        # sync on enter
        self.on_pre_enter = self.sync_from_state

    def _update_textsize(self, *_):
        self.display.text_size = (self.display.width - dp(20), None)

    def sync_from_state(self, *a):
        self.display.text = f"[b]{CalcState.expr}[/b]" if CalcState.expr else ""

    def on_button(self, instance):
        lbl = instance.text
        # handle special functions/operators
        if lbl == "C":
            CalcState.expr = ""
        elif lbl == "DEL":
            CalcState.expr = CalcState.expr[:-1]
        elif lbl == "π":
            CalcState.expr += "pi"
        elif lbl == "e":
            CalcState.expr += "e"
        elif lbl == "x²":
            # apply square to current value if exists, otherwise append **
            if CalcState.expr:
                try:
                    val = SafeEval.eval(CalcState.expr)
                    CalcState.expr = str(float(val) ** 2)
                except:
                    CalcState.expr = ""
                    self.display.text = "Erreur"
                    return
            else:
                CalcState.expr += "**2"
        elif lbl == "^":
            CalcState.expr += "^"   # will be normalized to ** by SafeEval
        elif lbl in ("sin","cos","tan","asin","acos","atan","ln","log10","√","abs"):
            # if expression present, apply function immediately
            if CalcState.expr:
                try:
                    val = SafeEval.eval(CalcState.expr)
                    if val == "Erreur":
                        raise ValueError()
                    # mapping
                    if lbl == "sin":
                        out = math.sin(math.radians(float(val)))
                    elif lbl == "cos":
                        out = math.cos(math.radians(float(val)))
                    elif lbl == "tan":
                        out = math.tan(math.radians(float(val)))
                    elif lbl == "asin":
                        out = math.degrees(math.asin(float(val)))
                    elif lbl == "acos":
                        out = math.degrees(math.acos(float(val)))
                    elif lbl == "atan":
                        out = math.degrees(math.atan(float(val)))
                    elif lbl == "ln":
                        out = math.log(float(val))
                    elif lbl == "log10":
                        out = math.log10(float(val))
                    elif lbl == "√":
                        out = math.sqrt(float(val))
                    elif lbl == "abs":
                        out = abs(float(val))
                    else:
                        out = "Erreur"
                    CalcState.expr = str(round(out, 10)).rstrip('0').rstrip('.') if isinstance(out, float) else str(out)
                except ZeroDivisionError:
                    CalcState.expr = ""
                    self.display.text = "Erreur : Division par zéro"
                    return
                except Exception:
                    CalcState.expr = ""
                    self.display.text = "Erreur"
                    return
            else:
                # insert function token for manual input
                if lbl == "√":
                    CalcState.expr += "sqrt("
                elif lbl in ("ln","log10"):
                    CalcState.expr += lbl + "("
                else:
                    CalcState.expr += lbl + "("
        elif lbl == "%":
            # percent of current value
            if CalcState.expr:
                try:
                    val = SafeEval.eval(CalcState.expr)
                    CalcState.expr = str(float(val) / 100.0)
                except:
                    CalcState.expr = ""
                    self.display.text = "Erreur"
                    return
        elif lbl == "1/x":
            if CalcState.expr:
                try:
                    val = SafeEval.eval(CalcState.expr)
                    CalcState.expr = str(1.0 / float(val))
                except ZeroDivisionError:
                    CalcState.expr = ""
                    self.display.text = "Erreur : Division par zéro"
                    return
                except:
                    CalcState.expr = ""
                    self.display.text = "Erreur"
                    return
            else:
                CalcState.expr += "1/"
        elif lbl == "+/-":
            expr = CalcState.expr
            if not expr: return
            i = len(expr)-1
            while i>=0 and (expr[i].isdigit() or expr[i]=='.'):
                i -= 1
            last = expr[i+1:]
            if not last: return
            if last.startswith('-'):
                new = last[1:]
            else:
                new = '-' + last
            CalcState.expr = expr[:i+1] + new
        else:
            # digits, operators, parentheses, dot, etc.
            CalcState.expr += lbl
        self.sync_from_state()

    def on_eq(self, instance):
        if not CalcState.expr:
            return
        try:
            res = SafeEval.eval(CalcState.expr)
            if res == "Erreur":
                self.display.text = "Erreur"
                CalcState.expr = ""
            else:
                CalcState.expr = str(res)
                self.sync_from_state()
        except ZeroDivisionError:
            self.display.text = "Erreur : Division par zéro"
            CalcState.expr = ""
        except Exception:
            self.display.text = "Erreur"
            CalcState.expr = ""

    def switch_to_basic(self, instance):
        basic = self.manager.get_screen('basic')
        basic.sync_display()
        self.manager.transition = SlideTransition(direction='right', duration=0.18)
        self.manager.current = 'basic'


# ---------- App ----------
class CalculatriceApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(BasicScreen(name='basic'))
        sm.add_widget(AdvancedScreen(name='advanced'))
        return sm

if __name__ == '__main__':
    CalculatriceApp().run()
