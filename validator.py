# validator.py
import pandas as pd
import re

class DataValidator:
    def __init__(self, df):
        self.df = df
        self.issues = []

    def validate_all(self, email_col=None, cnp_col=None):
        self.issues = []
        self.check_empty_rows()
        if email_col: self.check_emails(email_col)
        if cnp_col: self.check_cnps(cnp_col)
        return self.issues

    def check_empty_rows(self):
        empty_mask = self.df.isna().all(axis=1)
        if empty_mask.any():
            rows = self.df.index[empty_mask].tolist()
            self.issues.append({
                "type": "warning",
                "message": f"Rânduri complet goale detectate: {len(rows)}",
                "details": f"Rânduri (1-based): {[r+2 for r in rows[:10]]}"
            })

    def check_emails(self, col):
        if col not in self.df.columns: return
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        invalid = self.df[self.df[col].apply(lambda x: not re.match(pattern, str(x)) if pd.notna(x) else False)]
        if not invalid.empty:
            self.issues.append({
                "type": "error",
                "message": f"Formate de email invalide în coloana '{col}'",
                "details": f"Rânduri: {[r+2 for r in invalid.index[:10].tolist()]}"
            })

    def check_cnps(self, col):
        if col not in self.df.columns: return
        # Simple length check for CNP
        invalid = self.df[self.df[col].apply(lambda x: len(str(x).strip()) != 13 if pd.notna(x) else False)]
        if not invalid.empty:
            self.issues.append({
                "type": "warning",
                "message": f"CNP-uri cu lungime invalidă în coloana '{col}' (trebuie 13 caractere)",
                "details": f"Rânduri: {[r+2 for r in invalid.index[:10].tolist()]}"
            })
