# ui_constants.py
import customtkinter as ctk

# Theme Colors (Modern Blue & Slate)
PRIMARY_COLOR = "#3b82f6"
PRIMARY_HOVER = "#2563eb"
BG_DARK = "#0f172a"
BG_LIGHT = "#f1f5f9"
TEXT_COLOR = "#f8fafc"

class ThemeManager:
    @staticmethod
    def apply_initial_theme(theme_mode="dark"):
        ctk.set_appearance_mode(theme_mode)
        ctk.set_default_color_theme("blue")

    @staticmethod
    def get_tab_font():
        return ("Inter", 13, "bold")

    @staticmethod
    def get_header_font():
        return ("Inter", 24, "bold")

    @staticmethod
    def toggle_theme():
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        return new_mode
