#!/bin/bash
# Development setup script for Resilience-X testing
# Installs all dependencies and sets up the development environment

set -e

echo "🚀 Setting up Resilience-X Development Environment"
echo "================================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

echo ""
echo "📦 Installing Backend Dependencies (Python)"
echo "==========================================="
cd services/api

# Check if uv is available (preferred), otherwise use pip
if command -v uv &> /dev/null; then
    print_status "Using uv for Python dependency management"
    uv sync || {
        print_info "uv sync failed, falling back to pip"
        python3 -m pip install -e ".[test,dev]"
    }
else
    print_status "Using pip for Python dependency management"
    python3 -m pip install -e ".[test,dev]"
fi

cd ../..

echo ""
echo "📦 Installing Frontend Dependencies (Node.js)"
echo "=============================================="
cd apps/web

# Install Node.js dependencies
print_status "Installing Node.js packages"
npm ci

# Install Playwright browsers
print_status "Installing Playwright browsers"
npx playwright install

cd ../..

echo ""
echo "🔧 Setting up Environment Configuration"
echo "======================================="

# Copy environment template if .env doesn't exist
if [ ! -f "services/api/.env" ]; then
    if [ -f "services/api/.env.example" ]; then
        cp services/api/.env.example services/api/.env
        print_status "Created .env file from template"
    fi
fi

# Create .env for web if needed
if [ ! -f "apps/web/.env.local" ]; then
    cat > apps/web/.env.local << EOF
# Frontend environment variables
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
    print_status "Created .env.local for web app"
fi

echo ""
echo "✅ Development Environment Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Start the API: cd services/api && uv run uvicorn main:app --reload --port 8000"
echo "2. Start the web app: cd apps/web && npm run dev"
echo "3. Run tests: ./scripts/test.sh"
echo ""
echo "Available commands:"
echo "  ./scripts/test.sh           - Run all tests"
echo "  ./scripts/test.sh --api-only - Run only API tests"
echo "  ./scripts/test.sh --web-only - Run only web tests"
echo ""
print_status "Ready for development! 🎉"