# Web Automation Testing Project

## 📋 Overview
This project contains automated test cases for web application testing using Selenium WebDriver with Python. It includes comprehensive test suites for various functionalities including navigation, language switching, POS (Point of Sale) verification, and more.

## 🔧 Project Structure
```
project/
├── allure-results/         # Allure test reports
├── config/                 # Configuration files
│   └── config.py          # Project configuration
├── data/                  # Test data
├── drivers/               # WebDriver executables
├── logs/                  # Test execution logs
├── pages/                 # Page Object Models
│   ├── base_page.py      # Base page class
│   ├── home_page.py      # Home page objects
│   └── language_page.py  # Language page objects
├── tests/                 # Test cases
├── utils/                 # Utility functions
├── screenshots/           # Test failure screenshots
├── reports/              # Test reports
└── videos/               # Test execution videos
```

## 🔥 Features
- Page Object Model design pattern
- Multi-browser support (Chrome, Firefox)
- Parallel test execution support
- Comprehensive reporting (Allure, HTML)
- Screenshot capture on test failure
- Video recording of test execution
- Database logging of test results
- Multi-language testing support
- Support for different environments (nuxqa4, nuxqa5)

## 🛠 Requirements
```
selenium==4.15.0
pytest==7.4.3
pytest-xdist==3.5.0
allure-pytest==2.13.2
pytest-html==4.1.1
webdriver-manager==4.0.1
python-dotenv==1.0.0
```

## 🚀 Setup
1. Install Python 3.x
2. Clone the repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download ChromeDriver and place it in the `drivers/` directory
5. Set up environment variables (optional)

## 💻 Running Tests
### Basic Test Execution
```bash
pytest tests/test_case_4.py -v -s --alluredir=allure-results
```

### With Specific Browser
```bash
pytest --browser chrome tests/test_case_4.py -v
```

### Headless Mode
```bash
pytest --headless tests/test_case_4.py -v
```

### Specific Base URL
```bash
pytest --base-url https://nuxqa4.avtest.ink/ tests/test_case_4.py -v
```

## 📊 Test Reports
### Allure Reports
Generate Allure report:
```bash
C:\\allure\\allure-2.35.1\\bin\\allure.bat serve allure-results
```

## 🧪 Available Test Suites
- Navigation Tests (Navbar)
- Language Change Verification
- POS (Country) Change Tests
- Multi-URL Testing
- Debug Tests

## 🏷 Test Markers
- `@pytest.mark.footer`: Footer-related tests
- `@pytest.mark.redirects`: Redirection tests
- `@pytest.mark.language`: Language-related tests
- `@pytest.mark.debug`: Diagnostic tests
- `@pytest.mark.comprehensive`: Comprehensive test suites
- `@pytest.mark.header`: Header-related tests
- `@pytest.mark.pos`: POS/Country change tests
- `@pytest.mark.booking`: Booking tests
- `@pytest.mark.login`: Login tests

## 🧹 Maintenance
### Clean Test Data
```bash
python clean_test_data.py
```

### Reset Database
```bash
python reset_database.py
```

### Clean Everything
```bash
python clean_everything.py
```

## ⚙️ Configuration
### Default Settings
- Implicit Wait: 10 seconds
- Explicit Wait: 30 seconds
- Default Browser: Chrome
- Default Base URL: https://nuxqa4.avtest.ink/

### Environment Variables
Use `.env` file or system environment variables to configure:
- Database path
- Browser settings
- Test URLs
- Wait times

## 📝 Test Case Organization
Tests are organized by functionality and can be run individually or as part of a suite. Each test case includes:
- Setup and teardown
- Test data management
- Screenshot capture
- Video recording
- Database logging
- Allure reporting

## 🎯 Best Practices
- Use of Page Object Model
- Explicit waits for better reliability
- Screenshot capture on failure
- Detailed logging
- Database result tracking
- Clean code organization
- Modular test structure

## 🔍 Debugging Tools
- `debug_dropdowns.py`: Debug navbar dropdown functionality
- `debug_navbar.py`: Debug navbar interactions
- `debug_pos_verification.py`: Debug POS verification
