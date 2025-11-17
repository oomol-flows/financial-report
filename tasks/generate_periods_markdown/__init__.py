#region generated meta
import typing
class Inputs(typing.TypedDict):
    periods_list: dict
class Outputs(typing.TypedDict):
    markdown_output: typing.NotRequired[str]
    periods_count: typing.NotRequired[float]
#endregion

from oocana import Context
from datetime import datetime

def main(params: Inputs, context: Context) -> Outputs:
    """
    Generate markdown output from periods_list data

    Args:
        params: Input parameters containing periods_list
        context: OOMOL context object

    Returns:
        Dictionary with markdown output and periods count
    """
    periods_list = params["periods_list"]

    if not periods_list or "data" not in periods_list:
        raise ValueError("Invalid periods_list: missing 'data' field")

    data = periods_list["data"]
    if not isinstance(data, list):
        raise ValueError("Invalid periods_list: 'data' should be a list")

    # Generate markdown content
    markdown_lines = []
    markdown_lines.append("# Cached Report Periods")
    markdown_lines.append("")
    markdown_lines.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    markdown_lines.append("")
    markdown_lines.append(f"**Total Periods Available: {len(data)}**")
    markdown_lines.append("")

    if len(data) == 0:
        markdown_lines.append("No cached periods available.")
        markdown_output = "\n".join(markdown_lines)
        return {
            "markdown_output": markdown_output,
            "periods_count": 0
        }

    # Group periods by ticker for better organization
    ticker_groups = {}
    for period in data:
        ticker = period.get("ticker", "Unknown")
        if ticker not in ticker_groups:
            ticker_groups[ticker] = []
        ticker_groups[ticker].append(period)

    # Sort tickers for consistent output
    sorted_tickers = sorted(ticker_groups.keys())

    markdown_lines.append("## Available Periods by Ticker")
    markdown_lines.append("")

    for ticker in sorted_tickers:
        periods = ticker_groups[ticker]
        markdown_lines.append(f"### {ticker}")
        markdown_lines.append("")

        # Sort periods by year and quarter
        periods_sorted = sorted(periods, key=lambda x: (x.get("year", 0), x.get("quarter", 0)))

        # Create table
        markdown_lines.append("| Year | Quarter | Period |")
        markdown_lines.append("|------|---------|--------|")

        for period in periods_sorted:
            year = period.get("year", "N/A")
            quarter = period.get("quarter", "N/A")
            period_str = f"Q{quarter} {year}" if quarter != "N/A" and year != "N/A" else f"{year}-{quarter}"
            markdown_lines.append(f"| {year} | {quarter} | {period_str} |")

        markdown_lines.append("")

    markdown_output = "\n".join(markdown_lines)

    return {
        "markdown_output": markdown_output,
        "periods_count": len(data)
    }