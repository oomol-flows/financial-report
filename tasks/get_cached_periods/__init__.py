#region generated meta
import typing
Inputs = typing.Dict[str, typing.Any]
class Outputs(typing.TypedDict):
    periods_list: typing.NotRequired[dict]
    status: typing.NotRequired[str]
    message: typing.NotRequired[str]
#endregion

from oocana import Context, context
import requests
import json
import time


def _make_request_with_retry(url: str, headers: dict, max_retries: int = 3) -> requests.Response:
    """Make HTTP request with retry logic for transient failures"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            return response
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise e
    raise Exception("Failed to fetch data after multiple attempts")


async def main(params: Inputs, _context: Context) -> Outputs:
    base_url = "https://llm.oomol.com"
    
    try:
        # Prepare headers with API key
        headers = {
            "Authorization": await _context.oomol_token(),
            "Content-Type": "application/json"
        }

        url = f"{base_url}/api/tasks/custom/financial-report/fundamental/cached_report_periods"
        response = _make_request_with_retry(url, headers)
        
        # Handle different HTTP status codes
        if response.status_code == 200:
            try:
                result_data = response.json()
                return {
                    "periods_list": result_data,
                    "status": "success",
                    "message": "Successfully retrieved cached report periods"
                }
            except json.JSONDecodeError:
                raise ValueError("Retrieved data but failed to parse JSON response")
                
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
            # 打印出response body
            print(response.text)

            raise ValueError(f"Server error {response.status_code}. Service may be temporarily unavailable.")
        else:
            response.raise_for_status()
        
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        raise ValueError("Network connection failed after retries. Please check connectivity and try again.")
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request failed: {str(e)}")
        
    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")
    
    raise ValueError("No cached periods found")