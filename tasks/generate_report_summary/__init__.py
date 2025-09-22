#region generated meta
import typing
class Inputs(typing.TypedDict):
    api_key: str
    ticker: str
    years: int
    question_group: str
    question_ids: list[str]
    batch: bool
    use_cache: bool
class Outputs(typing.TypedDict):
    summary_result: dict
    status: str
    message: str
#endregion

from oocana import Context
import requests
import json
import time


def _make_request_with_retry(url: str, headers: dict, json_data: dict = None, max_retries: int = 3) -> requests.Response:
    """Make HTTP POST request with retry logic for transient failures"""
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=json_data, timeout=60)  # Longer timeout for analysis
            return response
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise e


def main(params: Inputs, _context: Context) -> Outputs:
    """
    Generate Report Summary - Create customized financial analysis summaries
    
    Args:
        params: Input parameters including API key, company details, and questions
        _context: OOMOL context object (unused)
        
    Returns:
        Generated summary analysis, status, and messages
    """
    
    api_key = params["api_key"]
    base_url = "https://market-lens.innolabs.cc"
    
    # Prepare headers with API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # POST /api/fundamental/create_report
        url = f"{base_url}/api/fundamental/create_report"
        
        # Prepare request body with correct parameter structure
        request_body = {
            "ticker": params["ticker"],
            "years": params["years"],
            "question_group": params["question_group"],
            "question_ids": params["question_ids"],
            "batch": params["batch"],
            "use_cache": params["use_cache"]
        }
        
        # Validate required parameters for summary generation
        if not request_body.get("ticker"):
            raise ValueError("Ticker symbol is required for analysis.")
        
        response = _make_request_with_retry(url, headers, request_body)
        
        # Handle different HTTP status codes
        if response.status_code == 200:
            try:
                result_data = response.json()
                return {
                    "summary_result": result_data,
                    "status": "success",
                    "message": "Successfully generated report summary"
                }
            except json.JSONDecodeError:
                raise ValueError("Analysis completed but failed to parse JSON response")
                
        elif response.status_code == 400:
            # Bad request - likely invalid parameters
            error_detail = "Invalid request parameters."
            try:
                error_info = response.json()
                if "detail" in error_info:
                    error_detail = error_info["detail"]
            except:
                pass
            raise ValueError(f"Bad request: {error_detail}")
            
        elif response.status_code == 401:
            raise ValueError("Authentication failed. Please check your API key.")
            
        elif response.status_code == 403:
            raise ValueError("Access forbidden. Insufficient permissions for analysis endpoint.")
            
        elif response.status_code == 404:
            raise ValueError("Analysis endpoint not found. Please verify the API base URL.")
            
        elif response.status_code == 422:
            # Validation error - common for analysis requests
            raise ValueError("Validation error. Please check company symbol and report period format.")
            
        elif response.status_code == 429:
            raise ValueError("Rate limit exceeded. Analysis requests are resource-intensive. Please retry after some time.")
            
        elif 500 <= response.status_code < 600:
            raise ValueError(f"Server error {response.status_code}. Analysis service may be temporarily unavailable.")
        else:
            response.raise_for_status()
        
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        raise ValueError("Network connection failed after retries. Analysis requests may take longer. Please check connectivity and try again.")
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request failed: {str(e)}")
        
    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")