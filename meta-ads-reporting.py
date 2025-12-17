import marimo

__generated_with = "0.18.4"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt

    import datetime

    from utils.api_schema import API_CONFIG
    from utils.data_processing import (
        build_url,
        fetch_data,
        process_data,
        enforce_dataframe_types,
    )
    return (
        API_CONFIG,
        build_url,
        datetime,
        enforce_dataframe_types,
        fetch_data,
        mo,
        pd,
        process_data,
    )


@app.cell
def _(mo):
    mo.md("""
    # 🚀 Meta Ads Performance Dashboard

    Generate valid Graph API URLs and show performance data as interactive table and chart
    """)
    return


@app.cell
def _(mo):
    # --- AUTHENTICATION ---

    # 2. Try to get Account ID from URL parameters
    query_params = mo.query_params()
    print(query_params)
    # meta ads urls contain ?act= so it's easy to find and reuse
    initial_account_id = (query_params.get("act") or "")
    print(type(initial_account_id))

    account_id = mo.ui.text(value=initial_account_id, label="Account ID:")
    return (account_id,)


@app.cell
def _(mo):
    access_token = mo.ui.text(value="", label="Access Token", kind="password")
    return (access_token,)


@app.cell
def _(datetime, mo):
    today = datetime.date.today()
    start_date = mo.ui.date(
        value=today - datetime.timedelta(days=7), label="Start Date"
    )
    end_date = mo.ui.date(value=today, label="End Date")
    return end_date, start_date


@app.cell
def _(access_token, account_id, mo):
    auth_tab = mo.vstack(
        [
            mo.hstack([access_token, account_id],
                      justify="start", align="center"),
        ]
    )
    return (auth_tab,)


@app.cell
def _(API_CONFIG, mo):
    # --- PARAMETERS ---
    level = mo.ui.dropdown(
        options=API_CONFIG["levels"], value="campaign", label="Level"
    )

    date_preset = mo.ui.dropdown(
        options=["custom"] + API_CONFIG["date_presets"],
        value="last_30d",
        label="Date Preset",
    )

    time_increment = mo.ui.dropdown(
        options=API_CONFIG["time_increments"],
        value="all_days",
        label="Time Increment",
    )

    breakdowns = mo.ui.multiselect(
        options=API_CONFIG["breakdowns"], label="Breakdowns (optional)"
    )

    default_fields = [
        "campaign_name",
        "impressions",
        "spend",
        "clicks",
        "ctr",
        "cpc",
    ]
    fields = mo.ui.multiselect(
        options=API_CONFIG["fields"], value=default_fields, label="Values: "
    )

    conversion_goal = mo.ui.dropdown(
        options=API_CONFIG["conversion_goals"],
        value="purchase",
        label="Conversion Goal",
    )
    return (
        breakdowns,
        conversion_goal,
        date_preset,
        fields,
        level,
        time_increment,
    )


@app.cell
def _(date_preset, end_date, mo, start_date, time_increment):
    date_section = [date_preset, time_increment]
    if date_preset.value == "custom":
        date_section.append(mo.hstack([start_date, end_date], justify="start"))
    return (date_section,)


@app.cell
def _(meta_ads_insights, mo):
    run_api = mo.ui.run_button(
        on_change=meta_ads_insights,
        label="Call API",
        kind="success",
        tooltip="Choose values first",
    )
    return (run_api,)


@app.cell
def _(
    breakdowns,
    conversion_goal,
    date_section,
    fields,
    level,
    mo,
    run_api,
    url_preview,
):
    mo.md(f"""## ⚙️ Configuration""")
    config_tab = mo.vstack(
        [
            mo.hstack([level, breakdowns], justify="start"),
            mo.hstack(date_section, justify="start"),
            mo.hstack([fields, conversion_goal], justify="start"),
            url_preview,
            run_api,
        ]
    )
    return (config_tab,)


@app.cell
def _(auth_tab, config_tab, mo):
    tabs = mo.ui.tabs(
        {"🔐 Authentication": auth_tab, "⚙️ Config": config_tab}, lazy=True
    )
    tabs
    return


@app.cell
def _(
    access_token,
    account_id,
    breakdowns,
    build_url,
    date_preset,
    end_date,
    fields,
    level,
    start_date,
    time_increment,
):
    generated_url = build_url(
        account_id.value,
        access_token.value,
        level.value,
        date_preset.value,
        time_increment.value,
        breakdowns.value,
        fields.value,
        start_date.value,
        end_date.value,
    )
    return (generated_url,)


@app.cell
def _(generated_url, mo):
    url_preview = mo.accordion(
        {
            "↪ Generated Meta Ads Insights Graph URL": mo.ui.text(
                generated_url, kind="url", full_width=True
            )
        }
    )
    return (url_preview,)


@app.cell
def _(mo):
    mo.md(f"""
    ## 📊 Meta Ads Performance Data
    """)
    return


@app.cell
def _(
    conversion_goal,
    enforce_dataframe_types,
    fetch_data,
    generated_url,
    pd,
    process_data,
):
    def meta_ads_insights(url):
        result = fetch_data(generated_url)
        cleaned_rows = process_data(result, conversion_goal.value)
        df = pd.DataFrame(cleaned_rows)
        df = enforce_dataframe_types(df)
        return df
    return (meta_ads_insights,)


@app.cell
def _(generated_url, meta_ads_insights, run_api):
    if run_api.value:
        df = meta_ads_insights(generated_url)
    return (df,)


@app.cell
def _(df, mo):
    # Warning if the api limit of 5000 rows is reached
    number_of_returned_rows = df.shape[0]

    if number_of_returned_rows == 5000:
        mo.callout(
            "API Result was limited. Did not return all rows", kind="danger"
        )
    return


@app.cell
def _(df, mo):
    selected = mo.ui.dataframe(df)
    return (selected,)


@app.cell
def _(mo, selected):
    chart = mo.ui.data_explorer(selected.value)
    return (chart,)


@app.cell
def _(chart, df, mo, selected):
    mo.ui.tabs({"Table": df, "Interactive Table": selected, "📈 Chart": chart})
    return


if __name__ == "__main__":
    app.run()
