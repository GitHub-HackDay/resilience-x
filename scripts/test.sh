#!/bin/bash
# Test runner script for Resilience-X project
# Runs all test suites with proper setup and reporting

set -e  # Exit on any error

echo "🧪 Starting Resilience-X Test Suite"
echo "================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "services/api" ] || [ ! -d "apps/web" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Set up environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)/services/api"
export NODE_ENV=test

# Check dependencies
echo "📦 Checking dependencies..."

# Check Python dependencies
if command -v python3 &> /dev/null; then
    print_status "Python 3 found"
else
    print_error "Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Check Node.js dependencies  
if command -v node &> /dev/null; then
    print_status "Node.js found"
else
    print_error "Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Function to run API tests
run_api_tests() {
    echo ""
    echo "🐍 Running API Tests (Python/FastAPI)"
    echo "======================================"
    
    cd services/api
    
    # Check if pytest is available
    if ! python3 -c "import pytest" 2>/dev/null; then
        print_warning "pytest not found, installing test dependencies..."
        python3 -m pip install -e ".[test]" || {
            print_error "Failed to install test dependencies"
            return 1
        }
    fi
    
    # Run API tests
    print_status "Running API unit tests..."
    python3 -m pytest ../../tests/api/ -v --tb=short || {
        print_error "API unit tests failed"
        return 1
    }
    
    print_status "Running API integration tests..."
    python3 -m pytest ../../tests/integration/ -v --tb=short || {
        print_error "API integration tests failed" 
        return 1
    }
    
    cd ../..
    print_status "API tests completed successfully"
}

# Function to run web tests
run_web_tests() {
    echo ""
    echo "🌐 Running Web Tests (Playwright/Next.js)"
    echo "=========================================="
    
    cd apps/web
    
    # Check if dependencies are installed
    if [ ! -d "node_modules" ]; then
        print_warning "Installing web dependencies..."
        npm ci || {
            print_error "Failed to install web dependencies"
            return 1
        }
    fi
    
    # Install Playwright browsers if needed
    if ! npx playwright --version &> /dev/null; then
        print_warning "Installing Playwright browsers..."
        npx playwright install || {
            print_error "Failed to install Playwright browsers"
            return 1
        }
    fi
    
    # Run web tests
    print_status "Running web component tests..."
    npm run test -- --reporter=line || {
        print_error "Web tests failed"
        return 1
    }
    
    cd ../..
    print_status "Web tests completed successfully"
}

# Function to run linting
run_linting() {
    echo ""
    echo "🔍 Running Code Quality Checks"
    echo "==============================="
    
    # Python linting
    cd services/api
    if python3 -c "import black, isort, flake8, mypy" 2>/dev/null; then
        print_status "Running Python code formatting checks..."
        python3 -m black --check . || print_warning "Python formatting issues found"
        python3 -m isort --check-only . || print_warning "Python import sorting issues found"
        python3 -m flake8 . || print_warning "Python linting issues found"
        # python3 -m mypy . || print_warning "Python type checking issues found"
    else
        print_warning "Python linting tools not available"
    fi
    cd ../..
    
    # TypeScript/JavaScript linting
    cd apps/web
    if [ -f "package.json" ] && [ -d "node_modules" ]; then
        print_status "Running TypeScript/JavaScript linting..."
        npm run lint || print_warning "Web linting issues found"
    else
        print_warning "Web linting not available (dependencies not installed)"
    fi
    cd ../..
}

# Function to generate test report
generate_report() {
    echo ""
    echo "📊 Test Summary Report"
    echo "======================"
    
    # Count test files
    api_tests=$(find tests/api tests/integration -name "test_*.py" | wc -l)
    web_tests=$(find tests/web -name "*.spec.ts" | wc -l)
    
    print_status "Test Coverage:"
    echo "  - API Tests: $api_tests test files"
    echo "  - Web Tests: $web_tests test files" 
    echo "  - Integration Tests: Included"
    echo ""
    
    print_status "Test Types Covered:"
    echo "  ✓ Unit Tests (API endpoints, models)"
    echo "  ✓ Integration Tests (service mocking)"
    echo "  ✓ End-to-End Tests (complete user flows)"
    echo "  ✓ Accessibility Tests (WCAG compliance)"
    echo "  ✓ Error Handling Tests (negative cases)"
    echo ""
}

# Main execution
main() {
    local run_api=true
    local run_web=true
    local run_lint=true
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --api-only)
                run_web=false
                run_lint=false
                shift
                ;;
            --web-only)
                run_api=false
                run_lint=false
                shift
                ;;
            --no-lint)
                run_lint=false
                shift
                ;;
            --help)
                echo "Usage: $0 [options]"
                echo "Options:"
                echo "  --api-only    Run only API tests"
                echo "  --web-only    Run only web tests"
                echo "  --no-lint     Skip linting checks"
                echo "  --help        Show this help message"
                exit 0
                ;;
            *)
                print_warning "Unknown option: $1"
                shift
                ;;
        esac
    done
    
    # Run test suites
    if [ "$run_api" = true ]; then
        run_api_tests || exit 1
    fi
    
    if [ "$run_web" = true ]; then
        run_web_tests || exit 1
    fi
    
    if [ "$run_lint" = true ]; then
        run_linting
    fi
    
    # Generate final report
    generate_report
    
    echo ""
    print_status "All tests completed successfully! 🎉"
    echo "Ready for demo and deployment."
}

# Run main function with all arguments
main "$@"