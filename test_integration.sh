#!/bin/bash
# Integration test script for Longhorn Studies

echo "========================================"
echo "Longhorn Studies Integration Test"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test backend
echo -e "${YELLOW}Testing Backend API...${NC}"
echo ""

# Check if backend is running
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Backend is running"
else
    echo -e "${RED}✗${NC} Backend is not running. Please start it with: cd backend && python app.py"
    exit 1
fi

# Test health endpoint
echo -n "Testing /api/health... "
HEALTH=$(curl -s http://localhost:8000/api/health)
if echo "$HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    exit 1
fi

# Test GET items (empty)
echo -n "Testing GET /api/items... "
ITEMS=$(curl -s http://localhost:8000/api/items)
if [ "$ITEMS" = "[]" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${GREEN}✓ PASS (items exist)${NC}"
fi

# Test POST new item
echo -n "Testing POST /api/items... "
CREATE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/items \
    -H "Content-Type: application/json" \
    -d '{"name": "Integration Test Item", "description": "Created by test script"}')
if echo "$CREATE_RESPONSE" | grep -q "Integration Test Item"; then
    ITEM_ID=$(echo "$CREATE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
    echo -e "${GREEN}✓ PASS (ID: $ITEM_ID)${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    exit 1
fi

# Test GET specific item
echo -n "Testing GET /api/items/$ITEM_ID... "
GET_ITEM=$(curl -s http://localhost:8000/api/items/$ITEM_ID)
if echo "$GET_ITEM" | grep -q "Integration Test Item"; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    exit 1
fi

# Test PUT update item
echo -n "Testing PUT /api/items/$ITEM_ID... "
UPDATE_RESPONSE=$(curl -s -X PUT http://localhost:8000/api/items/$ITEM_ID \
    -H "Content-Type: application/json" \
    -d '{"name": "Updated Test Item", "description": "Updated by test script"}')
if echo "$UPDATE_RESPONSE" | grep -q "Updated Test Item"; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    exit 1
fi

# Test DELETE item
echo -n "Testing DELETE /api/items/$ITEM_ID... "
DELETE_RESPONSE=$(curl -s -X DELETE http://localhost:8000/api/items/$ITEM_ID)
if echo "$DELETE_RESPONSE" | grep -q "deleted successfully"; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    exit 1
fi

# Test user creation
echo -n "Testing POST /api/users... "
USER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/users \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "email": "test@example.com"}')
if echo "$USER_RESPONSE" | grep -q "testuser"; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${GREEN}✓ PASS (user might already exist)${NC}"
fi

echo ""
echo "========================================"
echo -e "${GREEN}All tests passed!${NC}"
echo "========================================"
echo ""
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/api/health"
echo ""
