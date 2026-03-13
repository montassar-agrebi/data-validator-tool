import pandas as pd


def normalize_series(
    ser: pd.Series,
    mode: str = "Normalized",
    ignore_case: bool = True,
    trim: bool = True,
) -> pd.Series:
    s = ser.astype(str)
    if trim:
        s = s.str.strip()

    s_upper = s.str.upper()
    nullish = s_upper.isin(["NAN", "NONE", "NULL", ""])
    s = s.mask(nullish, "EMPTY")

    if mode == "Normalized":
        s = s.str.replace(r"\.0$", "", regex=True)
        if ignore_case:
            s = s.str.upper()

    return s


def classify_mismatch(miss_df: pd.DataFrame, s_col: str, t_col: str) -> str:
    if miss_df is None or miss_df.empty:
        return "Perfect match"

    src = miss_df[s_col].astype(str).str.upper()
    tgt = miss_df[t_col].astype(str).str.upper()

    src_empty = src.isin(["EMPTY", "NAN", "NONE", "NULL", ""])
    tgt_empty = tgt.isin(["EMPTY", "NAN", "NONE", "NULL", ""])

    total = len(miss_df)
    src_empty_count = int(src_empty.sum())
    tgt_empty_count = int(tgt_empty.sum())
    wrong_values_count = int((~src_empty & ~tgt_empty).sum())

    if tgt_empty_count == total and src_empty_count < total:
        return "Only NULL/EMPTY values on Target"
    if src_empty_count == total and tgt_empty_count < total:
        return "Only NULL/EMPTY values on Source"
    if total > 0 and max(src_empty_count, tgt_empty_count) / total >= 0.6 and wrong_values_count > 0:
        return "NULL/EMPTY values in the majority + some wrong values"
    if total > 0 and wrong_values_count / total >= 0.8:
        return "Mostly wrong values (non-null mismatches)"

    return "Mixed mismatch patterns (NULLs + value differences)"


def samples_block(miss_df: pd.DataFrame, key_col: str, s_col: str, t_col: str, n: int = 5) -> list[str]:
    if miss_df is None or miss_df.empty:
        return []
    rows = miss_df[[key_col, s_col, t_col]].head(n).values.tolist()
    return [f"{r[0]} | src={r[1]} | tgt={r[2]}" for r in rows]


def norm_key(series: pd.Series) -> pd.Series:
    x = series.astype(str).str.strip()
    x = x.str.replace(r"\.0$", "", regex=True)
    x = x.str.upper()
    x = x.replace(["NAN", "NONE", "NULL", ""], "EMPTY")
    return x