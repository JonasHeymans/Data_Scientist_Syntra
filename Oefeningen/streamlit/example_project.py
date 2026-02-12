import io
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dataset Explorer", layout="wide")

st.title("Dataset Explorer Dashboard")
st.caption("Upload een CSV en bouw een mini analytics dashboard met filters, stats en plots.")

# -----------------------------
# Helpers
# -----------------------------
@st.cache_data
def load_csv(file_bytes: bytes, sep: str, decimal: str) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(file_bytes), sep=sep, decimal=decimal)

def get_numeric_cols(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include="number").columns.tolist()

def get_categorical_cols(df: pd.DataFrame) -> list[str]:
    cols = df.select_dtypes(exclude="number").columns.tolist()
    # ook low-cardinality numerics zijn soms categorieën
    low_card = [c for c in get_numeric_cols(df) if df[c].nunique(dropna=True) <= 12]
    return sorted(list(set(cols + low_card)))

# -----------------------------
# Sidebar: data input
# -----------------------------
with st.sidebar:
    st.header("1) Data input")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    sep = st.selectbox("Separator", options=[",", ";", "\t"], index=0)
    decimal = st.selectbox("Decimal", options=[".", ","], index=0)

    st.divider()
    st.header("2) Cleaning")
    drop_na_rows = st.checkbox("Drop rows with NA", value=False)
    fill_na_num = st.checkbox("Fill NA in numeric columns with median", value=True)

    st.divider()
    st.header("3) Filters")
    st.write("Filters verschijnen zodra er data is.")

if uploaded is None:
    st.info("Upload een CSV om te starten.")
    st.stop()

df = load_csv(uploaded.getvalue(), sep=sep, decimal=decimal)

# Cleaning
df_clean = df.copy()
if drop_na_rows:
    df_clean = df_clean.dropna()

if fill_na_num:
    for c in get_numeric_cols(df_clean):
        if df_clean[c].isna().any():
            df_clean[c] = df_clean[c].fillna(df_clean[c].median())

# Basic columns
num_cols = get_numeric_cols(df_clean)
cat_cols = get_categorical_cols(df_clean)

# -----------------------------
# Sidebar filters (dynamic)
# -----------------------------
with st.sidebar:
    if len(cat_cols) > 0:
        cat_filter_col = st.selectbox("Categorical filter column", options=["(none)"] + cat_cols)
    else:
        cat_filter_col = "(none)"

    if cat_filter_col != "(none)":
        options = df_clean[cat_filter_col].dropna().unique().tolist()
        options = sorted(options)[:5000]
        selected = st.multiselect("Keep values", options=options, default=options)
    else:
        selected = None

    if len(num_cols) > 0:
        num_filter_col = st.selectbox("Numeric range column", options=["(none)"] + num_cols)
    else:
        num_filter_col = "(none)"

    if num_filter_col != "(none)":
        vmin = float(df_clean[num_filter_col].min())
        vmax = float(df_clean[num_filter_col].max())
        r = st.slider("Range", min_value=vmin, max_value=vmax, value=(vmin, vmax))
    else:
        r = None

# Apply filters
df_view = df_clean.copy()
if cat_filter_col != "(none)" and selected is not None:
    df_view = df_view[df_view[cat_filter_col].isin(selected)]
if num_filter_col != "(none)" and r is not None:
    df_view = df_view[df_view[num_filter_col].between(r[0], r[1])]

# -----------------------------
# Layout
# -----------------------------
colA, colB, colC, colD = st.columns(4)
colA.metric("Rows", f"{len(df_view):,}")
colB.metric("Columns", f"{df_view.shape[1]:,}")
colC.metric("Numeric cols", f"{len(num_cols):,}")
colD.metric("Categorical cols", f"{len(cat_cols):,}")

tabs = st.tabs(["Data", "Summary", "Plots", "Groupby", "Export"])

# -----------------------------
# Tab: Data
# -----------------------------
with tabs[0]:
    st.subheader("Preview")
    st.dataframe(df_view.head(50), use_container_width=True)

    with st.expander("Column types & missing values"):
        info = pd.DataFrame({
            "dtype": df_view.dtypes.astype(str),
            "missing": df_view.isna().sum(),
            "missing_%": (df_view.isna().mean() * 100).round(2),
            "nunique": df_view.nunique(dropna=True),
        })
        st.dataframe(info, use_container_width=True)

# -----------------------------
# Tab: Summary
# -----------------------------
with tabs[1]:
    st.subheader("Descriptive statistics")
    if len(num_cols) == 0:
        st.warning("No numeric columns found.")
    else:
        st.dataframe(df_view[num_cols].describe().T, use_container_width=True)

    st.subheader("Top categories")
    if len(cat_cols) == 0:
        st.warning("No categorical columns found.")
    else:
        c = st.selectbox("Column", options=cat_cols, key="topcat")
        vc = df_view[c].value_counts(dropna=False).head(20)

        out = vc.reset_index()
        out.columns = [c, "n"]  # altijd uniek

        st.dataframe(out, use_container_width=True)

# -----------------------------
# Tab: Plots
# -----------------------------
with tabs[2]:
    st.subheader("Visualisations (Matplotlib/Seaborn)")
    plot_type = st.selectbox("Plot type", ["Histogram", "Boxplot", "Scatter", "Bar (mean by category)"])

    if plot_type == "Histogram":
        if len(num_cols) == 0:
            st.warning("No numeric columns found.")
        else:
            x = st.selectbox("Numeric column", options=num_cols, key="hist_x")
            bins = st.slider("Bins", 5, 80, 30)

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.hist(df_view[x].dropna().to_numpy(), bins=bins)
            ax.set_title(f"Histogram: {x}")
            ax.set_xlabel(x)
            ax.set_ylabel("count")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

    elif plot_type == "Boxplot":
        if len(num_cols) == 0:
            st.warning("No numeric columns found.")
        else:
            y = st.selectbox("Numeric column", options=num_cols, key="box_y")
            by = st.selectbox("Group by (optional)", options=["(none)"] + cat_cols, key="box_by")

            fig, ax = plt.subplots(figsize=(8, 4))
            if by == "(none)":
                sns.boxplot(y=df_view[y], ax=ax)
                ax.set_xlabel("")
            else:
                sns.boxplot(data=df_view, x=by, y=y, ax=ax)
                ax.tick_params(axis="x", rotation=30)
            ax.set_title("Boxplot")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

    elif plot_type == "Scatter":
        if len(num_cols) < 2:
            st.warning("Need at least 2 numeric columns.")
        else:
            x = st.selectbox("x", options=num_cols, key="sc_x")
            y = st.selectbox("y", options=[c for c in num_cols if c != x], key="sc_y")
            hue = st.selectbox("Color by (optional)", options=["(none)"] + cat_cols, key="sc_hue")

            fig, ax = plt.subplots(figsize=(8, 5))
            if hue == "(none)":
                ax.scatter(df_view[x], df_view[y], alpha=0.7)
            else:
                sns.scatterplot(data=df_view, x=x, y=y, hue=hue, ax=ax, legend=True)
            ax.set_title("Scatter")
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

    else:  # Bar (mean by category)
        if len(num_cols) == 0 or len(cat_cols) == 0:
            st.warning("Need at least 1 numeric and 1 categorical column.")
        else:
            c = st.selectbox("Category", options=cat_cols, key="bar_c")
            y = st.selectbox("Numeric (mean)", options=num_cols, key="bar_y")
            topn = st.slider("Top N categories", 3, 30, 10)

            agg = (df_view.groupby(c, dropna=False)[y]
                   .mean()
                   .sort_values(ascending=False)
                   .head(topn))

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(agg.index.astype(str), agg.values)
            ax.set_title(f"Mean {y} by {c} (Top {topn})")
            ax.set_xlabel(c)
            ax.set_ylabel(f"mean({y})")
            ax.tick_params(axis="x", rotation=30)
            ax.grid(True, axis="y", alpha=0.3)
            st.pyplot(fig)

# -----------------------------
# Tab: Groupby
# -----------------------------
with tabs[3]:
    st.subheader("Custom groupby table")
    if len(cat_cols) == 0 or len(num_cols) == 0:
        st.warning("Need at least 1 categorical and 1 numeric column.")
    else:
        g = st.selectbox("Group column", options=cat_cols, key="gb_g")
        y = st.selectbox("Value column", options=num_cols, key="gb_y")
        metric = st.selectbox("Aggregation", options=["mean", "median", "sum", "min", "max", "count"], key="gb_m")

        if metric == "count":
            out = df_view.groupby(g, dropna=False)[y].count().sort_values(ascending=False)
        else:
            out = getattr(df_view.groupby(g, dropna=False)[y], metric)().sort_values(ascending=False)

        st.dataframe(out.reset_index().rename(columns={y: f"{metric}_{y}"}), use_container_width=True)

# -----------------------------
# Tab: Export
# -----------------------------
with tabs[4]:
    st.subheader("Download filtered data")
    csv_bytes = df_view.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv_bytes, file_name="filtered_data.csv", mime="text/csv")
