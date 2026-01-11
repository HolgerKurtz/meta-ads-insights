# Meta Ads Performance Dashboard

A powerful, interactive dashboard for Social Media Ads Managers to analyze Meta Ads performance data. Built with Python and Marimo, this tool connects directly to the Meta Graph API to fetch, transform, and visualize your ad data.

## Key Features

*   **Direct API Integration**: Fetch real-time insights from your Meta Ad Accounts.
*   **Flexible Granularity**: View data by Campaign, Ad Set, or Ad level.
*   **Custom Metrics**: 
    *   **KUR (Kosten-Umsatz-Relation)**: Automatically calculates the Cost-to-Revenue Ratio (Spend / Value), a critical metric for evaluating efficiency (similar to ROAS but inverse). *Includes intelligent handling of zero-revenue days to ensure accurate averages.*
    *   **ROAS**: Return on Ad Spend.
*   **Dynamic Data Flattening**: Automatically extracts and flattens complex nested JSON fields (like specific conversion actions) into clean columns.
*   **Interactive Visualization**: Filter, sort, and chart your data interactively using Marimo's data explorer.

## Prerequisites

*   **Python 3.12+**
*   **uv**: An extremely fast Python package installer and resolver.
*   **Meta Access Token**: A valid Graph API access token with `ads_read` permissions.
*   **Ad Account ID**: The ID of the ad account you wish to analyze.

## Installation

This project uses `uv` for dependency management.

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd meta-ads-api
    ```

2.  **Install dependencies**:
    ```bash
    uv sync
    ```

## Usage

1.  **Start the Dashboard**:
    Run the Marimo notebook server:
    ```bash
    uv run marimo edit meta-ads-reporting.py
    ```

2.  **Configure Your View**:
    *   **Authentication**: Enter your `Account ID` and `Access Token` in the sidebar or top section.
    *   **Settings**: Choose your Date Range, Level (Campaign/AdSet/Ad), and specific Breakdowns.
    *   **Metrics**: Select the KPIs you want to see. **"KUR"** is available in the "Values" dropdown.
    *   **Run**: Click "Call API" to fetch and process the data.

3.  **Analyze**:
    *   Use the **Interactive Table** to sort by highest Spend or best KUR.
    *   Use the **Chart** tab to visualize trends over time or compare campaigns.

## For Ads Managers

This tool is designed to go beyond standard Ads Manager reporting:
- **Efficiency Analysis**: Quickly spot which campaigns are delivering profitable KUR/ROAS.
- **Custom Timeframes**: Analyze custom date ranges with daily breakdowns to see performance trends.
- **Data Export**: The processed data can be easily exported or viewed as a dataframe for further analysis in Python.

## Project Structure

*   `meta-ads-reporting.py`: Main application logic and UI.
*   `utils/api_schema.py`: Configuration for API fields, parameters, and type definitions.
*   `utils/data_processing.py`: Core logic for API requests, data transformation, and custom metric extraction.
