import io

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def _read_csv_bytes(file_bytes: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(file_bytes), dtype=str, keep_default_na=False, na_values=[""])
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.duplicated()]
    return df


def load_data(uploaded_file) -> pd.DataFrame | None:
    if uploaded_file is None:
        return None
    try:
        return _read_csv_bytes(uploaded_file.getvalue())
    except Exception as e:
        st.error(f"Error loading {uploaded_file.name}: {e}")
        return None


def get_single_file_pairs(df: pd.DataFrame):
    src_cols = [c for c in df.columns if c.startswith("src_")]
    paired = []
    unpaired_src = []

    for s_col in src_cols:
        t_col = s_col.replace("src_", "tgt_", 1)
        if t_col in df.columns:
            paired.append((s_col, t_col))
        else:
            unpaired_src.append(s_col)

    tgt_cols = [c for c in df.columns if c.startswith("tgt_")]
    unpaired_tgt = [c for c in tgt_cols if c.replace("tgt_", "src_", 1) not in df.columns]

    return paired, unpaired_src, unpaired_tgt


def get_common_columns(df_s: pd.DataFrame, df_t: pd.DataFrame) -> list[str]:
    return [c for c in df_s.columns if c in df_t.columns]