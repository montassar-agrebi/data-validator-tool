import io

import numpy as np
import pandas as pd
import streamlit as st

from src.comparison import normalize_series
from src.profiling import load_data
from src.validator import (
    build_dual_file_results,
    global_score,
)

# =========================
# PAGE CONFIG (MUST BE FIRST)
# =========================
st.set_page_config(page_title="Data Validation Tool", page_icon="📊", layout="wide")

# =========================
# SIMPLE HEADER (STABLE)
# =========================
st.title("📊 Data Validation Tool")
st.caption("Developed by Montassar Agrebi")


def kpi_block(rows_compared: int, cols_compared: int, mismatched_cells: int, rows_with_mismatch: int):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows Compared", f"{rows_compared:,}")
    c2.metric("Columns Compared", f"{cols_compared:,}")
    c3.metric("Mismatched Cells", f"{mismatched_cells:,}")
    c4.metric("Rows w/ ≥1 Mismatch", f"{rows_with_mismatch:,}")


# =========================
# DUAL FILE COMPARISON
# =========================
st.markdown("### 📂 Dual File Comparison (Source vs Target)")
st.caption("Assumes a UNIQUE primary key on both sides. If not, the tool will stop.")

ca, cb = st.columns(2)

with ca:
    fs = st.file_uploader("Source CSV", type=["csv"], key="us")

with cb:
    ft = st.file_uploader("Target CSV", type=["csv"], key="ut")

df_s = load_data(fs)
df_t = load_data(ft)

if df_s is None or df_t is None:
    st.info("💡 Upload both Source and Target CSVs to compare.")
    st.stop()

common_cols = [c for c in df_s.columns if c in df_t.columns]
if not common_cols:
    st.error("No common columns found between Source and Target.")
    st.stop()

left, right = st.columns([2, 2])

with left:
    key_col = st.selectbox("Select Primary Key (UNIQUE):", options=common_cols, key="kid")

with right:
    compare_mode2 = st.radio("Comparison Mode:", options=["Normalized", "Strict"], horizontal=True, key="mode2")

results_tab2 = build_dual_file_results(
    df_s=df_s,
    df_t=df_t,
    key_col=key_col,
    compare_mode=compare_mode2,
)

if results_tab2["has_duplicates"]:
    st.error(
        "❌ Selected key is NOT unique (after normalization).\n\n"
        f"- Source duplicates: {results_tab2['dup_s']}\n"
        f"- Target duplicates: {results_tab2['dup_t']}\n\n"
        "Choose another key or fix extracts."
    )
    st.stop()

common_keys = results_tab2["common_keys"]
only_in_s = results_tab2["only_in_s"]
only_in_t = results_tab2["only_in_t"]
s_common = results_tab2["s_common"]
t_common = results_tab2["t_common"]
summary2 = results_tab2["summary"]
total_mismatched_cells = results_tab2["total_mismatched_cells"]
rows_with_any_mismatch = results_tab2["rows_with_any_mismatch"]

k1, k2, k3 = st.columns(3)
k1.metric("Common keys compared", f"{len(common_keys):,}")
k2.metric("Only in Source", f"{len(only_in_s):,}")
k3.metric("Only in Target", f"{len(only_in_t):,}")

if len(common_keys) == 0:
    st.error("No overlapping keys found. Check extract scope or key selection.")
    st.stop()

cols_compared = len(summary2)
rows_compared = len(common_keys)
rows_with_mismatch_count = int(rows_with_any_mismatch.sum())
avg_acc = float(np.mean([v["Accuracy"] for v in summary2.values()])) if summary2 else 1.0

st.divider()
kpi_block(rows_compared, cols_compared, total_mismatched_cells, rows_with_mismatch_count)

cA, cB = st.columns([1, 2])

with cA:
    st.metric("Global Accuracy", f"{avg_acc:.2%}")
    st.write(global_score(avg_acc))
    st.metric("Data Loss (Rows)", f"{len(only_in_s):,}", delta=-len(only_in_s), delta_color="inverse")

with cB:
    top = (
        pd.DataFrame([{"Attribute": k, "Mismatches": v["MismatchCount"]} for k, v in summary2.items()])
        .sort_values("Mismatches", ascending=False)
        .head(10)
        .set_index("Attribute")
    )
    st.caption("Top 10 columns by mismatch count")
    st.bar_chart(top)

st.subheader("🧾 Overview")

ov2 = pd.DataFrame(
    [{
        "Attribute": k,
        "Accuracy": v["Accuracy"],
        "Status": v["Status"],
        "Mismatches": v["MismatchCount"],
        "Insight": v["Insight"],
    } for k, v in summary2.items()]
).sort_values(["Mismatches", "Accuracy"], ascending=[False, True])

st.dataframe(
    ov2.style.format({"Accuracy": "{:.2%}"}).background_gradient(cmap="RdYlGn", subset=["Accuracy"]),
    use_container_width=True)

st.subheader("🔍 Error Inspector & 📋 Tracker Copy")
sel2 = st.selectbox("Select Column to Inspect:", options=list(summary2.keys()), key="s2")
d2 = summary2[sel2]

if d2["MismatchCount"] > 0:
    samples_md = "\n".join([f"- {x}" for x in d2["Samples"]]) if d2["Samples"] else "- (no samples)"
    snippet2 = (
        f"**{sel2}** | {d2['Status']} ({d2['Accuracy']:.0%}) | {d2['Insight']}\n"
        f"Key: {key_col}\n"
        f"Samples:\n{samples_md}"
    )
else:
    snippet2 = f"**{sel2}** | ✅ Perfect Match (100%)"

colL, colR = st.columns([1, 1])

with colL:
    st.text_area("Tracker Snippet (copy/paste):", value=snippet2, height=160)

    st.download_button(
        "⬇️ Download summary (CSV)",
        data=ov2.to_csv(index=False).encode("utf-8"),
        file_name="summary_dual_file.csv",
        mime="text/csv"
    )

    if d2["MismatchCount"] > 0:
        s_ser = s_common[sel2]
        t_ser = t_common[sel2]
        mask = normalize_series(s_ser, mode=compare_mode2) != normalize_series(t_ser, mode=compare_mode2)

        full_miss = pd.concat([s_ser[mask], t_ser[mask]], axis=1, keys=["src", "tgt"]).reset_index()
        full_miss.columns = ["_key_norm", "src", "tgt"]
        full_miss[key_col] = full_miss["_key_norm"]
        full_miss = full_miss[[key_col, "src", "tgt"]]

        st.download_button(
            "⬇️ Download selected column mismatches (CSV)",
            data=full_miss.to_csv(index=False).encode("utf-8"),
            file_name=f"mismatches_{sel2}.csv",
            mime="text/csv"
        )

with colR:
    if d2["Preview"] is not None and not d2["Preview"].empty:
        st.write(f"Preview (first 100) for **{sel2}**")
        st.dataframe(d2["Preview"], use_container_width=True)
    else:
        st.success(f"No mismatches found in {sel2}!")
