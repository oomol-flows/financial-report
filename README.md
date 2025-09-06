# Financial Report Analysis System

A comprehensive OOMOL workflow system for financial report analysis and data retrieval. This project provides automated tools for analyzing company financial data, generating custom reports, and accessing cached financial information through a structured API interface.

## 🎯 Project Purpose

This system enables users to:
- **Analyze Company Financials**: Retrieve and analyze financial data for publicly traded companies
- **Generate Custom Reports**: Create tailored financial analysis summaries based on specific questions and criteria
- **Access Cached Data**: Efficiently retrieve pre-processed financial reports and periods
- **Automate Workflows**: Build automated financial analysis pipelines using OOMOL's visual workflow system

## 📊 Available Blocks (Tasks)

### 1. Get Cached Report
**Purpose**: Retrieve cached financial report data from the API  
**Icon**: 📊 `:carbon:report:`

**Inputs**:
- `api_key` (secret): Financial Report Analysis API Key
- `ticker` (string): Required stock ticker symbol (e.g., "AAPL", "MSFT")
- `year` (integer, optional): Specific year for the report
- `quarter` (integer, optional): Specific quarter for the report

**Outputs**:
- `report_data`: Cached financial report data object
- `status`: API call status
- `message`: Status message or error details

**Use Case**: Quickly access pre-processed financial data for a specific company and time period.

---

### 2. Get Cached Periods
**Purpose**: Retrieve available cached financial report periods  
**Icon**: 📅 `:carbon:calendar:`

**Inputs**:
- `api_key` (secret): Financial Report Analysis API Key

**Outputs**:
- `periods_list`: List of available cached report periods
- `status`: API call status  
- `message`: Status message or error details

**Use Case**: Check which time periods have cached data available before requesting specific reports.

---

### 3. Get Predefined Questions
**Purpose**: Retrieve predefined financial analysis questions  
**Icon**: ❓ `:carbon:help:`

**Inputs**:
- `api_key` (secret): Financial Report Analysis API Key

**Outputs**:
- `questions_list`: List of predefined analysis questions
- `status`: API call status
- `message`: Status message or error details

**Use Case**: Discover available analysis questions that can be used for generating customized financial reports.

---

### 4. Generate Report Summary
**Purpose**: Generate customized financial analysis summaries  
**Icon**: 📋 `:carbon:document-tasks:`

**Inputs**:
- `api_key` (secret): Financial Report Analysis API Key
- `ticker` (string): Company stock ticker symbol
- `years` (integer): Number of years for analysis (default: 1)
- `question_group` (string): Question group type (e.g., "brief", "detailed")
- `question_ids` (array): Array of specific question IDs
- `batch` (boolean): Whether to process in batch mode (default: false)
- `use_cache` (boolean): Whether to use cached results (default: true)

**Outputs**:
- `summary_result`: Generated financial analysis summary object
- `status`: API call status
- `message`: Status message or error details

**Use Case**: Create comprehensive financial analysis reports based on specific criteria and questions.

## 🔧 Setup and Installation

1. **Install Dependencies**:
   ```bash
   npm install
   poetry install --no-root
   ```

2. **Configure API Keys**:
   - Set up your Financial Report Analysis API key in OOMOL secrets
   - Use the secret key: `${{OO_SECRET:FinancialAPI,Financial Report API,API_KEY}}`

3. **Run Bootstrap**:
   ```bash
   oomol run bootstrap
   ```

## 🚀 Usage Examples

### Basic Financial Analysis Workflow

1. **Check Available Periods**: Use `Get Cached Periods` to see what data is available
2. **Get Report Data**: Use `Get Cached Report` with a specific ticker symbol
3. **Explore Questions**: Use `Get Predefined Questions` to see analysis options
4. **Generate Summary**: Use `Generate Report Summary` to create a custom analysis

### Sample Company Analysis
- Input ticker: `RBLX` (Roblox Corporation)
- Retrieve cached data for recent periods
- Generate analysis summary with predefined questions
- Output comprehensive financial insights

## 🔒 Security Features

- **API Key Management**: Secure storage of API credentials using OOMOL's secret management
- **Error Handling**: Comprehensive error handling with retry logic for network requests
- **Timeout Protection**: Built-in timeout mechanisms to prevent hanging requests

## 🏗️ Architecture

- **OOMOL Framework**: Built on OOMOL's visual workflow system
- **Python Backend**: Core logic implemented in Python with robust error handling
- **API Integration**: RESTful API integration with retry mechanisms
- **Caching System**: Efficient data caching for improved performance

## 📈 Workflow Capabilities

This system supports building complex financial analysis workflows by chaining blocks together:
- Sequential data retrieval and analysis
- Conditional processing based on data availability
- Batch processing for multiple companies
- Custom report generation with flexible question sets

---

*Built with OOMOL - The Visual Workflow Platform*