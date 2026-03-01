import os
import re

filepath = r'c:\Users\Administrator\Downloads\program expert\app.py'
with open(filepath, 'r', encoding='utf-8') as file:
    text = file.read()

# Replace the remaining mojibakes on Genereaza and Ajutor in app.py
text = text.replace('â–¶  ', '')
text = text.replace('â–¶ ', '')
text = text.replace('â “ ', '')
text = text.replace('❓ ', '')
text = text.replace('âœ✨ ', '')

with open(filepath, 'w', encoding='utf-8') as file:
    file.write(text)

print(f"Cleaned {filepath}")
