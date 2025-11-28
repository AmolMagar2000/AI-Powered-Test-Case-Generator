# 🤖 QE Test Automation Suite

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Gemini](https://img.shields.io/badge/Powered%20by-Gemini%202.0%20Flash-4285F4.svg)](https://deepmind.google/technologies/gemini/)

**AI-Powered Test Case Generator and Selenium Automation Code Generator**

Streamline your QA workflow with intelligent test case generation and automated code creation for Selenium WebDriver using Java and TestNG.

---

## 📸 Screenshots

### Test Case Generator - AI Generation
![Test Case Generator](https://raw.githubusercontent.com/YOUR_USERNAME/qa-test-automation-suite/main/screenshots/test-case-generator.png)
*Generate comprehensive test cases from user stories and requirements using AI*

### Test Automation Code Generator
![Test Automation](https://raw.githubusercontent.com/YOUR_USERNAME/qa-test-automation-suite/main/screenshots/test-automation.png)
*Automatically generate production-ready Selenium automation code in Java*

---

## ✨ Features

### 🧪 Test Case Management
- **Manual Test Case Creation** - Create detailed test cases with all necessary fields
- **AI-Powered Generation** - Generate test cases from requirements using Gemini 2.0 Flash
- **Context-Aware Generation** - Generate additional test cases based on existing context
- **Bulk Operations** - Select, edit, and delete multiple test cases at once
- **Excel Export** - Export all test cases to Excel format for documentation

### 🤖 Automation Code Generation
- **Java Selenium Code** - Generate TestNG-based automation code
- **Page Object Model** - Uses industry-standard POM design pattern
- **Combined Test Suites** - Generate single test class with multiple test methods
- **Separate Test Classes** - Generate individual test files for each test case
- **Download as ZIP** - Package all generated files for easy integration

### 📊 Additional Features
- **Priority Management** - Categorize test cases by High, Medium, Low priority
- **File Attachments** - Support for screenshots, PDFs, DOCX, and Excel files
- **Clean UI** - Modern, intuitive interface with smooth navigation
- **Statistics Dashboard** - Track total and selected test cases
- **Toast Notifications** - User-friendly feedback for all actions

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))
- Git (optional, for version control)

### Installation

#### Option 1: Automated Setup (Windows)

1. **Download/Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/qa-test-automation-suite.git
   cd qa-test-automation-suite
   ```

2. **Run setup script**
   ```bash
   setup.bat
   ```

3. **Configure API Key**
   - Edit `.env` file
   - Replace `your_api_key_here` with your actual Gemini API key

4. **Launch the application**
   ```bash
   streamlit run app.py
   ```

#### Option 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/qa-test-automation-suite.git
   cd qa-test-automation-suite
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**
   ```bash
   # Create .env file in root directory with:
   GEMINI_API_KEY=your_actual_api_key_here
   APP_ENV=development
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   - Navigate to `http://localhost:8501`

---

## 📁 Project Structure

```
qa-test-automation-suite/
│
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── setup.bat                  # Windows setup script
├── setup.sh                   # Linux/Mac setup script
│
├── assets/
│   └── style.css              # Custom CSS styles
│
├── pages/
│   ├── __init__.py
│   ├── test_case_gen.py       # Test case generator page
│   └── test_automation.py     # Automation code generator page
│
├── utils/
│   ├── __init__.py
│   ├── ai_utils.py            # Gemini AI integration
│   ├── code_utils.py          # Code parsing utilities
│   ├── file_utils.py          # File handling (PDF, DOCX, Excel)
│   └── ui_utils.py            # UI helper functions
│
└── screenshots/               # UI screenshots for documentation
    ├── test-case-generator.png
    └── test-automation.png
```

---

## 📖 Usage Guide

### Creating Test Cases Manually

1. Navigate to **Test Case Generator**
2. Select **Manual Creation** tab
3. Fill in the form:
   - **Area**: Category (e.g., UI/UX, API, Database)
   - **Module**: Main module name (e.g., Authentication)
   - **Sub-Module**: Specific feature (e.g., Login)
   - **Test Scenario**: Brief description (required)
   - **Priority**: High, Medium, or Low
   - **Preconditions**: Setup requirements
   - **Test Data**: Input data needed
   - **Test Steps**: Detailed steps (required)
   - **Expected Results**: What should happen (required)
4. Click **Save Test Case**

### Generating Test Cases with AI

1. Navigate to **Test Case Generator**
2. Select **AI Generation** tab
3. Enter your requirements or user story in the text area:
   ```
   Example:
   As a user, I want to login so that I can access my account.
   
   Acceptance Criteria:
   • Valid credentials allow login
   • Invalid credentials show error message
   • Forgot password link is available
   ```
4. Set number of test cases to generate (1-50)
5. Select default priority
6. Click **Generate Test Cases**
7. AI will create comprehensive test cases automatically

### Generating Automation Code

1. In **Test Case Library**, select test cases using checkboxes
2. Click **Automate (N)** button where N is the number selected
3. Choose generation mode:
   - **Combined Test Suite**: Single test class with all tests
   - **Separate Test Classes**: Individual files for each test case
4. Click **Generate Automation Code**
5. Review generated Java code with TestNG annotations
6. Click **Download** to get ZIP file with all code files

### Exporting Test Cases

1. In **Test Case Library**, click **Export Excel**
2. Excel file will download with all test case details:
   - ID, Area, Module, Sub-Module
   - Title, Priority
   - Preconditions, Test Data
   - Test Steps, Expected Results
   - Attachments list

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Streamlit** | Web application framework |
| **Google Gemini 2.0 Flash** | AI model for test case and code generation |
| **Pandas** | Data manipulation and Excel export |
| **PyPDF2** | PDF file processing |
| **python-docx** | Microsoft Word file processing |
| **OpenPyXL** | Excel file handling |
| **python-dotenv** | Environment variable management |

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_actual_api_key_here

# Application Configuration
APP_ENV=development
```

### Supported File Types

**For Attachments:**
- Images: PNG, JPG, JPEG
- Documents: PDF, DOCX, TXT
- Spreadsheets: XLSX, XLS, CSV

---

## 🎨 UI Features

- **Modern Design**: Clean, professional interface with gradient headers
- **Responsive Layout**: Adapts to different screen sizes
- **Priority Indicators**: Color-coded icons (🔴 High, 🟡 Medium, 🟢 Low)
- **Toast Notifications**: Real-time feedback for user actions
- **Smooth Animations**: Enhanced user experience with transitions
- **Sidebar Navigation**: Easy switching between pages
- **Statistics Dashboard**: Quick overview of test case metrics

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'docx'`
```bash
# Solution
pip install python-docx
```

**Issue**: `GEMINI_API_KEY not configured`
```bash
# Solution
# 1. Check if .env file exists in root directory
# 2. Verify GEMINI_API_KEY is set correctly
# 3. Restart the application
```

**Issue**: Port 8501 already in use
```bash
# Solution
streamlit run app.py --server.port 8502
```

**Issue**: Changes not reflecting
```bash
# Solution
# Hard refresh browser: Ctrl + Shift + R (Windows/Linux) or Cmd + Shift + R (Mac)
```

**Issue**: Git push rejected
```bash
# Solution
git pull origin main --rebase
git push origin main
```

---

## 📊 Roadmap

- [ ] Support for additional programming languages (Python, JavaScript)
- [ ] Integration with test management tools (Jira, TestRail)
- [ ] Import test cases from Excel
- [ ] Test case templates library
- [ ] Test execution reports
- [ ] API testing code generation
- [ ] Database validation code generation
- [ ] Mobile automation support (Appium)
- [ ] CI/CD integration examples

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting PR

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Amol Magar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

**Amol Magar**

- GitHub: [@YOUR_GITHUB_USERNAME](https://github.com/YOUR_GITHUB_USERNAME)
- LinkedIn: [Your LinkedIn Profile](https://linkedin.com/in/your-profile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Amazing framework for building data apps
- [Google Gemini](https://deepmind.google/technologies/gemini/) - Powerful AI model
- [TestNG](https://testng.org/) - Testing framework inspiration
- [Selenium WebDriver](https://www.selenium.dev/) - Browser automation standard

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [Issues](https://github.com/YOUR_USERNAME/qa-test-automation-suite/issues)
3. Create a new issue with detailed description
4. Contact the author

---

## ⭐ Show Your Support

If you find this project helpful, please give it a ⭐ on GitHub!

---

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/qa-test-automation-suite?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/qa-test-automation-suite?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/YOUR_USERNAME/qa-test-automation-suite?style=social)

---

**Built with ❤️ by Amol Magar**

*Empowering QA engineers with AI-powered automation*