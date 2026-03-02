import pandas as pd
from typing import Dict, List, Any, Optional

class AnalyticsService:
    """Service for advanced statistics and data auditing"""

    @staticmethod
    def get_research_grades(df: pd.DataFrame) -> Dict[str, int]:
        """Distribution of CSI, CSII, etc."""
        # Find column containing CSI/CSII
        col = AnalyticsService._find_col(df, ['grad', 'functie', 'position'])
        if not col:
            return {}
        mask = df[col].astype(str).str.contains('CS', case=False, na=False)
        return df[mask][col].value_counts().to_dict()

    @staticmethod
    def get_student_types(df: pd.DataFrame) -> Dict[str, int]:
        """Student, Masterand, Doctorand counts"""
        col = AnalyticsService._find_col(df, ['statut', 'tip', 'categorie', 'studii'])
        if not col:
            # Broad search
            for c in df.columns:
                if df[c].astype(str).str.contains('Student|Masterand|Doctorand', case=False, na=False).any():
                    col = c
                    break
        if not col: return {}
        return df[col].value_counts().to_dict()

    @staticmethod
    def get_integrity_audit(df: pd.DataFrame) -> Dict[str, Any]:
        """Identify missing values and help requests"""
        empty_rows = df[df.isna().any(axis=1) | (df == '').any(axis=1)]

        help_col = AnalyticsService._find_col(df, ['ajutor', 'asistenta', 'help'])
        help_requests = []
        if help_col:
            help_requests = df[df[help_col].astype(str).lower().str.contains('da|yes|true', na=False)].index.tolist()

        return {
            'empty_row_count': len(empty_rows),
            'empty_row_indices': empty_rows.index.tolist(),
            'help_request_count': len(help_requests),
            'help_request_indices': help_requests
        }

    @staticmethod
    def _find_col(df: pd.DataFrame, keywords: List[str]) -> Optional[str]:
        for k in keywords:
            for col in df.columns:
                if k.lower() in str(col).lower():
                    return col
        return None
