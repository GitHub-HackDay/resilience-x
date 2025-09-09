#!/usr/bin/env python3
"""
Simple test script to validate the demo setup.
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def test_weaviate_connection():
    """Test if Weaviate is accessible."""
    try:
        response = requests.get('http://localhost:8080/v1/.well-known/ready', timeout=5)
        return response.status_code == 200
    except:
        return False

def test_docker_compose():
    """Test if docker-compose.yml is valid."""
    try:
        result = subprocess.run(['docker', 'compose', 'config'], 
                              capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        return result.returncode == 0
    except:
        return False

def test_scripts_executable():
    """Test if scripts are executable."""
    repo_root = Path(__file__).parent.parent
    scripts = ['demo.sh', 'ingest.sh']
    
    for script in scripts:
        script_path = repo_root / 'scripts' / script
        if not script_path.exists():
            return False, f"{script} not found"
        if not script_path.stat().st_mode & 0o111:
            return False, f"{script} not executable"
    
    return True, "All scripts are executable"

def main():
    print("🔍 Validating Resilience-X Demo Setup")
    print("=" * 40)
    
    # Test docker compose config
    print("📋 Testing docker-compose.yml...")
    if test_docker_compose():
        print("✅ Docker Compose configuration is valid")
    else:
        print("❌ Docker Compose configuration error")
        return False
    
    # Test scripts
    print("🔧 Testing script permissions...")
    scripts_ok, scripts_msg = test_scripts_executable()
    if scripts_ok:
        print(f"✅ {scripts_msg}")
    else:
        print(f"❌ {scripts_msg}")
        return False
    
    # Test if Weaviate can start
    print("🐳 Testing Weaviate startup...")
    try:
        subprocess.run(['docker', 'compose', 'up', '-d', 'weaviate'], 
                      check=True, cwd=Path(__file__).parent.parent,
                      capture_output=True)
        print("✅ Weaviate container started")
        
        # Wait for readiness
        print("⏳ Waiting for Weaviate to be ready...")
        for i in range(30):  # 30 second timeout
            if test_weaviate_connection():
                print("✅ Weaviate is ready and responding")
                break
            time.sleep(1)
        else:
            print("❌ Weaviate failed to become ready within 30 seconds")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Weaviate: {e}")
        return False
    
    print("\n🎉 Demo setup validation completed successfully!")
    print("\nNext steps:")
    print("1. Run: bash scripts/demo.sh")
    print("2. Open: http://localhost:8000/docs (API)")
    print("3. Test with sample crisis questions")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)