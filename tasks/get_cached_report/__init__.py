#region generated meta
import typing
class Inputs(typing.TypedDict):
    api_key: str
    ticker: str
    year: int | None
    quarter: int | None
class Outputs(typing.TypedDict):
    report_data: dict
    status: str
    message: str
#endregion

from oocana import Context
import requests
import json
import time


def _make_request_with_retry(url: str, headers: dict, params: dict = None, max_retries: int = 3) -> requests.Response:
    """Make HTTP request with retry logic for transient failures"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            return response
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise e


def main(params: Inputs, _context: Context) -> Outputs:
    """
    Get Cached Report - Retrieve cached financial report data from API
    
    Args:
        params: Input parameters including API key, ticker, and optional year/quarter
        _context: OOMOL context object (unused)
        
    Returns:
        Cached report data, status, and messages
    """
    
    api_key = params["api_key"]
    base_url = "https://market-lens.innolabs.cc"
    ticker = params["ticker"]
    
    # Prepare headers with API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # GET /api/fundamental/cached_report
        url = f"{base_url}/api/fundamental/cached_report"
        query_params = {"ticker": ticker}
        
        if params.get("year"):
            query_params["year"] = params["year"]
        if params.get("quarter"):
            query_params["quarter"] = params["quarter"]
        
        response = _make_request_with_retry(url, headers, query_params)
        
        # Handle different HTTP status codes
        if response.status_code == 200:
            try:
                result_data = response.json()
                return {
                    "report_data": result_data,
                    "status": "success",
                    "message": "Successfully retrieved cached report data"
                }
            except json.JSONDecodeError:
                raise ValueError("Retrieved data but failed to parse JSON response")
                
        elif response.status_code == 401:
            raise ValueError("Authentication failed. Please check your API key.")
            
        elif response.status_code == 403:
            raise ValueError("Access forbidden. Insufficient permissions for this endpoint.")
            
        elif response.status_code == 404:
            # For cached reports, 404 might mean no cached data available
            raise ValueError("No cached report data found for the specified parameters. Try different company symbol or period.")
            
        elif response.status_code == 422:
            raise ValueError("Validation error. Please check company symbol and report period format.")
            
        elif response.status_code == 429:
            raise ValueError("Rate limit exceeded. Please retry after some time.")
            
        elif 500 <= response.status_code < 600:
            raise ValueError(f"Server error {response.status_code}. Service may be temporarily unavailable.")
        else:
            response.raise_for_status()
        
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        raise ValueError("Network connection failed after retries. Please check connectivity and try again.")
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request failed: {str(e)}")
        
    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")