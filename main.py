import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput


class BhattaMobileApp(App):

  def build(self):
    self.init_db()
    root = TabbedPanel()
    root.do_default_tab = False

    # --- Tab 1: Labor & Advance ---
    tab_labor = TabbedPanelItem(text="مزدور کھاتہ")
    labor_layout = BoxLayout(
        orientation="vertical", padding=15, spacing=10
    )

    self.lab_name = TextInput(
        hint_text="مزدور کا نام", font_size=18, multiline=False, halign="right"
    )
    self.lab_cat = Spinner(
        text="شعبہ منتخب کریں",
        values=("پتھائی", "بھرائی", "جلائی", "نکاسی"),
        font_size=18,
    )
    self.lab_adv = TextInput(
        hint_text="پیشگی رقم (Rs)",
        font_size=18,
        input_filter="float",
        multiline=False,
        halign="right",
    )

    btn_save_lab = Button(
        text="مزدور محفوظ کریں",
        font_size=18,
        background_color=(0.1, 0.6, 0.3, 1),
    )
    btn_save_lab.bind(on_press=self.save_labor)

    self.lab_status = Label(text="", font_size=16, color=(0, 1, 0, 1))

    labor_layout.add_widget(self.lab_name)
    labor_layout.add_widget(self.lab_cat)
    labor_layout.add_widget(self.lab_adv)
    labor_layout.add_widget(btn_save_lab)
    labor_layout.add_widget(self.lab_status)
    tab_labor.add_widget(labor_layout)

    # --- Tab 2: Sales ---
    tab_sales = TabbedPanelItem(text="فروخت اور بل")
    sales_layout = BoxLayout(
        orientation="vertical", padding=15, spacing=10
    )

    self.cust_name = TextInput(
        hint_text="خریدار کا نام", font_size=18, multiline=False, halign="right"
    )
    self.bricks_qty = TextInput(
        hint_text="اینٹوں کی تعداد",
        font_size=18,
        input_filter="int",
        multiline=False,
        halign="right",
    )
    self.rate_per_k = TextInput(
        hint_text="فی ہزار ریٹ (Rate)",
        font_size=18,
        input_filter="float",
        multiline=False,
        halign="right",
    )

    btn_save_sale = Button(
        text="بل بنائیں اور محفوظ کریں",
        font_size=18,
        background_color=(0.1, 0.4, 0.7, 1),
    )
    btn_save_sale.bind(on_press=self.save_sale)

    self.sale_result = Label(text="", font_size=16, color=(1, 1, 1, 1))

    sales_layout.add_widget(self.cust_name)
    sales_layout.add_widget(self.bricks_qty)
    sales_layout.add_widget(self.rate_per_k)
    sales_layout.add_widget(btn_save_sale)
    sales_layout.add_widget(self.sale_result)
    tab_sales.add_widget(sales_layout)

    # --- Tab 3: Daily Expenses ---
    tab_cash = TabbedPanelItem(text="روزنامچہ اخراجات")
    cash_layout = BoxLayout(
        orientation="vertical", padding=15, spacing=10
    )

    self.exp_desc = TextInput(
        hint_text="تفصیل خرچ (ڈیزل / چائے)",
        font_size=18,
        multiline=False,
        halign="right",
    )
    self.exp_amount = TextInput(
        hint_text="رقم (Rs)",
        font_size=18,
        input_filter="float",
        multiline=False,
        halign="right",
    )

    btn_save_exp = Button(
        text="خرچ محفوظ کریں",
        font_size=18,
        background_color=(0.8, 0.2, 0.2, 1),
    )
    btn_save_exp.bind(on_press=self.save_expense)

    self.exp_status = Label(text="", font_size=16, color=(1, 1, 0, 1))

    cash_layout.add_widget(self.exp_desc)
    cash_layout.add_widget(self.exp_amount)
    cash_layout.add_widget(btn_save_exp)
    cash_layout.add_widget(self.exp_status)
    tab_cash.add_widget(cash_layout)

    root.add_widget(tab_labor)
    root.add_widget(tab_sales)
    root.add_widget(tab_cash)

    return root

  def init_db(self):
    conn = sqlite3.connect("bhatta_mobile.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS labor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, category TEXT, advance REAL
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT, qty INTEGER, rate REAL, total REAL
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT, amount REAL
        )
    """
    )
    conn.commit()
    conn.close()

  def save_labor(self, instance):
    name = self.lab_name.text
    cat = self.lab_cat.text
    adv = self.lab_adv.text
    if not name or cat == "شعبہ منتخب کریں":
      self.lab_status.text = "نام اور شعبہ درج کریں!"
      return
    conn = sqlite3.connect("bhatta_mobile.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO labor (name, category, advance) VALUES (?, ?, ?)",
        (name, cat, float(adv) if adv else 0.0),
    )
    conn.commit()
    conn.close()
    self.lab_status.text = "مزدور محفوظ ہو گیا!"
    self.lab_name.text = ""
    self.lab_adv.text = ""

  def save_sale(self, instance):
    cust = self.cust_name.text
    try:
      qty = int(self.bricks_qty.text)
      rate = float(self.rate_per_k.text)
    except ValueError:
      self.sale_result.text = "مقدار اور ریٹ درست لکھیں!"
      return
    total = (qty / 1000) * rate
    conn = sqlite3.connect("bhatta_mobile.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sales (customer, qty, rate, total) VALUES (?, ?, ?, ?)",
        (cust, qty, rate, total),
    )
    conn.commit()
    conn.close()
    self.sale_result.text = f"کل بل: Rs {total:.2f}"
    self.cust_name.text = ""
    self.bricks_qty.text = ""
    self.rate_per_k.text = ""

  def save_expense(self, instance):
    desc = self.exp_desc.text
    try:
      amount = float(self.exp_amount.text)
    except ValueError:
      self.exp_status.text = "رقم درست لکھیں!"
      return
    if not desc:
      self.exp_status.text = "خرچ کی تفصیل لکھیں!"
      return
    conn = sqlite3.connect("bhatta_mobile.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (description, amount) VALUES (?, ?)",
        (desc, amount),
    )
    conn.commit()
    conn.close()
    self.exp_status.text = "خرچ محفوظ ہو گیا!"
    self.exp_desc.text = ""
    self.exp_amount.text = ""


if __name__ == "__main__":
  BhattaMobileApp().run()
