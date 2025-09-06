#region generated meta
import typing
class Inputs(typing.TypedDict):
    api_key: str
    analysis_type: typing.Literal["report_summary", "predefined_questions", "cached_periods", "cached_report"]
    company_symbol: str | None
    report_period: str | None
    questions: str | None
    base_url: str
class Outputs(typing.TypedDict):
    result: dict
    status: str
    message: str
#endregion

from oocana import Context
import requests
import json


def main(params: Inputs, _context: Context) -> Outputs:
    """
    Financial Report Analyzer - Call various financial analysis API endpoints
    
    Args:
        params: Input parameters including API key, analysis type, and other options
        _context: OOMOL context object (unused)
        
    Returns:
        Analysis results, status, and messages
    """
    
    api_key = params["api_key"]
    analysis_type = params["analysis_type"]
    base_url = params["base_url"].rstrip("/")
    
    # Prepare headers with API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        if analysis_type == "predefined_questions":
            # GET /api/fundamental/predefined_report_questions
            url = f"{base_url}/api/fundamental/predefined_report_questions"
            response = requests.get(url, headers=headers)
            
        elif analysis_type == "cached_periods":
            # GET /api/fundamental/cached_report_periods  
            url = f"{base_url}/api/fundamental/cached_report_periods"
            response = requests.get(url, headers=headers)
            
        elif analysis_type == "cached_report":
            # GET /api/fundamental/cached_report
            url = f"{base_url}/api/fundamental/cached_report"
            query_params = {}
            if params.get("company_symbol"):
                query_params["symbol"] = params["company_symbol"]
            if params.get("report_period"):
                query_params["period"] = params["report_period"]
            
            response = requests.get(url, headers=headers, params=query_params)
            
        elif analysis_type == "report_summary":
            # POST /api/fundamental/report_summary
            url = f"{base_url}/api/fundamental/report_summary"
            
            # Prepare request body
            request_body = {}
            if params.get("company_symbol"):
                request_body["company_symbol"] = params["company_symbol"]
            if params.get("report_period"):
                request_body["report_period"] = params["report_period"]
            if params.get("questions"):
                try:
                    # Try to parse questions as JSON array
                    request_body["questions"] = json.loads(params["questions"])
                except json.JSONDecodeError:
                    # If not JSON, treat as single question
                    request_body["questions"] = [params["questions"]]
            
            response = requests.post(url, headers=headers, json=request_body)
            
        else:
            raise ValueError(f"Unsupported analysis type: {analysis_type}")
        
        # Handle different HTTP status codes
        if response.status_code == 200:
            # Success case - continue to parse response
            pass
        elif response.status_code == 400:
            raise ValueError("Bad request - invalid request parameters")
        elif response.status_code == 401:
            raise ValueError("Authentication failed. Please check your API key.")
        elif response.status_code == 403:
            raise ValueError("Access forbidden. Insufficient permissions for this endpoint.")
        elif response.status_code == 404:
            raise ValueError("Endpoint not found. Please verify the API base URL.")
        elif response.status_code == 422:
            raise ValueError("Validation error. Please check request parameters.")
        elif response.status_code == 429:
            raise ValueError("Rate limit exceeded. Please retry after some time.")
        elif 500 <= response.status_code < 600:
            raise ValueError(f"Server error {response.status_code}. Service may be temporarily unavailable.")
        else:
            response.raise_for_status()
        
        # Parse response
        try:
            result_data = response.json()
        except json.JSONDecodeError:
            result_data = {"raw_response": response.text}
        
        return {
            "result": result_data,
            "status": "success",
            "message": f"Successfully completed {analysis_type} analysis"
        }
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP error {e.response.status_code}"
        try:
            error_detail = e.response.json()
            if "detail" in error_detail:
                error_msg += f": {error_detail['detail']}"
        except:
            error_msg += f": {e.response.text}"
            
        raise ValueError(error_msg)
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request failed: {str(e)}")
        
    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")