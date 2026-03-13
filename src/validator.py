import pandas as pd

from src.comparison import (
    classify_mismatch,
    norm_key,
    normalize_series,
    samples_block,
)
from src.profiling import get_single_file_pairs


def global_score(avg_acc: float):
    if avg_acc >= 0.98:
        return "🟢 Healthy"
    if avg_acc >= 0.95:
        return "🟡 Minor Issues"
    return "🔴 Risky Migration"


def build_single_file_results(df1: pd.DataFrame, key_col: str, compare_mode: str) -> dict:
    paired, unpaired_src, unpaired_tgt = get_single_file_pairs(df1)

    summary = {}
    total_mismatched_cells = 0
    rows_with_any_mismatch = pd.Series(False, index=df1.index)

    for s_col, t_col in paired:
        attr = s_col.replace("src_", "", 1)

        s_clean = normalize_series(df1[s_col], mode=compare_mode)
        t_clean = normalize_series(df1[t_col], mode=compare_mode)

        mask = s_clean != t_clean
        miss = df1.loc[mask, [key_col, s_col, t_col]]

        mismatch_count = int(mask.sum())
        total_mismatched_cells += mismatch_count
        rows_with_any_mismatch = rows_with_any_mismatch | mask

        rows_total = len(df1)
        acc = (rows_total - mismatch_count) / rows_total if rows_total else 1.0
        status = "✅ Perfect" if mismatch_count == 0 else f"❌ {mismatch_count} Mismatches"

        insight = classify_mismatch(miss, s_col, t_col) if mismatch_count else "Perfect match"
        samples = samples_block(miss, key_col, s_col, t_col, n=5)

        summary[attr] = {
            "Accuracy": acc,
            "Status": status,
            "MismatchCount": mismatch_count,
            "Insight": insight,
            "Samples": samples,
            "Preview": miss.head(100) if mismatch_count else None,
            "Cols": (s_col, t_col),
        }

    return {
        "paired": paired,
        "unpaired_src": unpaired_src,
        "unpaired_tgt": unpaired_tgt,
        "summary": summary,
        "total_mismatched_cells": total_mismatched_cells,
        "rows_with_any_mismatch": rows_with_any_mismatch,
    }


def build_dual_file_results(df_s: pd.DataFrame, df_t: pd.DataFrame, key_col: str, compare_mode: str) -> dict:
    df_s = df_s.copy()
    df_t = df_t.copy()

    df_s["_key_norm"] = norm_key(df_s[key_col])
    df_t["_key_norm"] = norm_key(df_t[key_col])

    dup_s = int(df_s["_key_norm"].duplicated().sum())
    dup_t = int(df_t["_key_norm"].duplicated().sum())

    if dup_s > 0 or dup_t > 0:
        return {
            "has_duplicates": True,
            "dup_s": dup_s,
            "dup_t": dup_t,
        }

    s_idx = df_s.set_index("_key_norm")
    t_idx = df_t.set_index("_key_norm")

    common_keys = s_idx.index.intersection(t_idx.index)
    only_in_s = s_idx.index.difference(t_idx.index)
    only_in_t = t_idx.index.difference(s_idx.index)

    compare_cols = [c for c in df_s.columns if c in df_t.columns and c != key_col and c != "_key_norm"]
    s_common = s_idx.reindex(common_keys)
    t_common = t_idx.reindex(common_keys)

    summary2 = {}
    total_mismatched_cells = 0
    rows_with_any_mismatch = pd.Series(False, index=common_keys)

    for col in compare_cols:
        s_ser = s_common[col]
        t_ser = t_common[col]

        s_clean = normalize_series(s_ser, mode=compare_mode)
        t_clean = normalize_series(t_ser, mode=compare_mode)

        mask = s_clean != t_clean
        mismatch_count = int(mask.sum())
        total_mismatched_cells += mismatch_count
        rows_with_any_mismatch = rows_with_any_mismatch | pd.Series(mask.values, index=common_keys)

        miss_df = pd.concat([s_ser[mask], t_ser[mask]], axis=1, keys=["src", "tgt"]).reset_index()
        miss_df.columns = ["_key_norm", "src", "tgt"]
        miss_df[key_col] = miss_df["_key_norm"]
        miss_df = miss_df[[key_col, "src", "tgt"]]

        rows_total = len(common_keys)
        acc = (rows_total - mismatch_count) / rows_total if rows_total else 1.0
        status = "✅ Perfect" if mismatch_count == 0 else f"❌ {mismatch_count} Mismatches"
        insight = classify_mismatch(miss_df, "src", "tgt") if mismatch_count else "Perfect match"

        samples = []
        if mismatch_count:
            rows = miss_df[[key_col, "src", "tgt"]].head(5).values.tolist()
            samples = [f"{r[0]} | src={r[1]} | tgt={r[2]}" for r in rows]

        summary2[col] = {
            "Accuracy": acc,
            "Status": status,
            "MismatchCount": mismatch_count,
            "Insight": insight,
            "Samples": samples,
            "Preview": miss_df.head(100) if mismatch_count else None,
        }

    return {
        "has_duplicates": False,
        "dup_s": dup_s,
        "dup_t": dup_t,
        "common_keys": common_keys,
        "only_in_s": only_in_s,
        "only_in_t": only_in_t,
        "s_common": s_common,
        "t_common": t_common,
        "summary": summary2,
        "total_mismatched_cells": total_mismatched_cells,
        "rows_with_any_mismatch": rows_with_any_mismatch,
    }