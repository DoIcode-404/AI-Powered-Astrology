#!/bin/bash

# Manual API Testing Script Using curl
# Usage: ./MANUAL_CURL_TESTS.sh https://your-railway-url
# Or:     ./MANUAL_CURL_TESTS.sh http://localhost:8005 (for local testing)

set -e

# Configuration
BASE_URL="${1:-http://localhost:8005}"
TIMESTAMP=$(date +%s)
TEST_EMAIL="test.user.${TIMESTAMP}@astrology.test"
TEST_USERNAME="testuser_${TIMESTAMP}"
TEST_PASSWORD="TestPassword123!@"
VERBOSE="${VERBOSE:-true}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Cleanup on exit
trap cleanup EXIT

cleanup() {
    echo -e "\n${BLUE}=== TEST SUMMARY ===${NC}"
    echo "Total Tests: $TESTS_RUN"
    echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
        exit 0
    else
        echo -e "${RED}❌ SOME TESTS FAILED${NC}"
        exit 1
    fi
}

# Helper function to make API calls
api_call() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    local expected_status="$5"
    local token="$6"

    TESTS_RUN=$((TESTS_RUN + 1))

    local url="${BASE_URL}${endpoint}"
    local headers="-H 'Content-Type: application/json'"

    if [ ! -z "$token" ]; then
        headers="$headers -H 'Authorization: Bearer $token'"
    fi

    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $name"
    echo "  Method: $method"
    echo "  URL: $url"

    if [ ! -z "$data" ]; then
        echo "  Data: $data"
    fi

    # Make the request
    local response_file="/tmp/api_response_${TESTS_RUN}.json"
    local http_code_file="/tmp/http_code_${TESTS_RUN}"

    if [ "$method" = "GET" ]; then
        curl -s -o "$response_file" -w "%{http_code}" \
            -X GET "$url" \
            -H "Content-Type: application/json" \
            $([ ! -z "$token" ] && echo "-H 'Authorization: Bearer $token'") \
            > "$http_code_file"
    elif [ "$method" = "POST" ]; then
        curl -s -o "$response_file" -w "%{http_code}" \
            -X POST "$url" \
            -H "Content-Type: application/json" \
            $([ ! -z "$token" ] && echo "-H 'Authorization: Bearer $token'") \
            $([ ! -z "$data" ] && echo "-d '$data'") \
            > "$http_code_file"
    elif [ "$method" = "PUT" ]; then
        curl -s -o "$response_file" -w "%{http_code}" \
            -X PUT "$url" \
            -H "Content-Type: application/json" \
            $([ ! -z "$token" ] && echo "-H 'Authorization: Bearer $token'") \
            $([ ! -z "$data" ] && echo "-d '$data'") \
            > "$http_code_file"
    elif [ "$method" = "DELETE" ]; then
        curl -s -o "$response_file" -w "%{http_code}" \
            -X DELETE "$url" \
            -H "Content-Type: application/json" \
            $([ ! -z "$token" ] && echo "-H 'Authorization: Bearer $token'") \
            > "$http_code_file"
    fi

    local http_code=$(cat "$http_code_file")

    echo "  Expected Status: $expected_status"
    echo "  Actual Status: $http_code"

    if [ "$http_code" = "$expected_status" ]; then
        echo -e "  ${GREEN}✅ PASSED${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "  ${RED}❌ FAILED${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    if [ "$VERBOSE" = "true" ] && [ -f "$response_file" ]; then
        local response=$(cat "$response_file")
        if [ ! -z "$response" ]; then
            echo "  Response: $(echo "$response" | head -c 200)"
        fi
    fi

    # Return the response for variable extraction
    cat "$response_file"
    rm -f "$response_file" "$http_code_file"
}

# ============================================================================
# PHASE 1: CONNECTIVITY TESTS
# ============================================================================

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PHASE 1: CONNECTIVITY & HEALTH CHECKS${NC}"
echo -e "${BLUE}========================================${NC}"

api_call "Health Check" "GET" "/health" "" "200"

# ============================================================================
# PHASE 2: AUTHENTICATION TESTS
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}PHASE 2: AUTHENTICATION TESTS${NC}"
echo -e "${BLUE}========================================${NC}"

# Register new user
REGISTER_DATA="{\"email\":\"$TEST_EMAIL\",\"username\":\"$TEST_USERNAME\",\"password\":\"$TEST_PASSWORD\"}"
REGISTER_RESPONSE=$(api_call "User Registration" "POST" "/auth/register" "$REGISTER_DATA" "200")

# Extract tokens
ACCESS_TOKEN=$(echo "$REGISTER_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4 | head -1)
REFRESH_TOKEN=$(echo "$REGISTER_RESPONSE" | grep -o '"refresh_token":"[^"]*' | cut -d'"' -f4 | head -1)
USER_ID=$(echo "$REGISTER_RESPONSE" | grep -o '"user_id":"[^"]*' | cut -d'"' -f4 | head -1)

echo -e "  ${GREEN}Tokens extracted:${NC}"
echo "    Access Token: ${ACCESS_TOKEN:0:20}..."
echo "    Refresh Token: ${REFRESH_TOKEN:0:20}..."
echo "    User ID: $USER_ID"

# Login with same credentials
LOGIN_DATA="{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}"
LOGIN_RESPONSE=$(api_call "User Login" "POST" "/auth/login" "$LOGIN_DATA" "200")

# Update tokens from login
NEW_ACCESS=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4 | head -1)
if [ ! -z "$NEW_ACCESS" ]; then
    ACCESS_TOKEN="$NEW_ACCESS"
    echo -e "  ${GREEN}Access token updated from login${NC}"
fi

# Refresh token
REFRESH_DATA="{\"refresh_token\":\"$REFRESH_TOKEN\"}"
REFRESH_RESPONSE=$(api_call "Token Refresh" "POST" "/auth/refresh_token" "$REFRESH_DATA" "200")

# Update access token from refresh
NEW_ACCESS=$(echo "$REFRESH_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4 | head -1)
if [ ! -z "$NEW_ACCESS" ]; then
    ACCESS_TOKEN="$NEW_ACCESS"
    echo -e "  ${GREEN}Access token refreshed${NC}"
fi

# Test invalid credentials
INVALID_LOGIN="{\"email\":\"$TEST_EMAIL\",\"password\":\"WrongPassword123!\"}"
api_call "Invalid Credentials (Expected Error)" "POST" "/auth/login" "$INVALID_LOGIN" "401"

# ============================================================================
# PHASE 3: KUNDALI TESTS
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}PHASE 3: KUNDALI TESTS${NC}"
echo -e "${BLUE}========================================${NC}"

# Generate kundali (no save)
KUNDALI_DATA='{
    "birthDate":"1990-05-15",
    "birthTime":"14:30",
    "latitude":28.7041,
    "longitude":77.1025,
    "timezone":"Asia/Kolkata"
}'

api_call "Generate Kundali" "POST" "/kundali/generate_kundali" "$KUNDALI_DATA" "200" "$ACCESS_TOKEN"

# Save kundali
SAVE_KUNDALI_DATA='{
    "name":"Test Kundali - Manual Test",
    "birthDate":"1990-05-15",
    "birthTime":"14:30",
    "latitude":28.7041,
    "longitude":77.1025,
    "timezone":"Asia/Kolkata"
}'

SAVE_RESPONSE=$(api_call "Save Kundali" "POST" "/kundali/save_kundali" "$SAVE_KUNDALI_DATA" "201" "$ACCESS_TOKEN")

# Extract kundali ID
KUNDALI_ID=$(echo "$SAVE_RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4 | head -1)
echo -e "  ${GREEN}Kundali ID extracted: $KUNDALI_ID${NC}"

# List kundalis
api_call "List Kundalis" "GET" "/kundali/list_kundalis" "" "200" "$ACCESS_TOKEN"

# Get specific kundali
if [ ! -z "$KUNDALI_ID" ]; then
    api_call "Get Kundali Details" "GET" "/kundali/get_kundali/$KUNDALI_ID" "" "200" "$ACCESS_TOKEN"

    # Update kundali
    UPDATE_DATA='{"name":"Updated Test Kundali - Modified"}'
    api_call "Update Kundali" "PUT" "/kundali/update_kundali/$KUNDALI_ID" "$UPDATE_DATA" "200" "$ACCESS_TOKEN"
else
    echo -e "${YELLOW}⚠️  Skipping get/update/delete (no kundali ID)${NC}"
fi

# ============================================================================
# PHASE 4: PREDICTION TESTS
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}PHASE 4: PREDICTION TESTS${NC}"
echo -e "${BLUE}========================================${NC}"

if [ ! -z "$KUNDALI_ID" ]; then
    # Create prediction
    PREDICTION_DATA="{
        \"kundali_id\":\"$KUNDALI_ID\",
        \"prediction_type\":\"career\",
        \"timeframe\":\"next_year\"
    }"

    PREDICTION_RESPONSE=$(api_call "Create Prediction" "POST" "/predictions/create" "$PREDICTION_DATA" "201" "$ACCESS_TOKEN")

    # Extract prediction ID
    PREDICTION_ID=$(echo "$PREDICTION_RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4 | head -1)
    echo -e "  ${GREEN}Prediction ID extracted: $PREDICTION_ID${NC}"

    # List predictions
    api_call "List Predictions" "GET" "/predictions/list" "" "200" "$ACCESS_TOKEN"
else
    echo -e "${YELLOW}⚠️  Skipping prediction tests (no kundali)${NC}"
fi

# ============================================================================
# PHASE 5: ERROR HANDLING TESTS
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}PHASE 5: ERROR HANDLING TESTS${NC}"
echo -e "${BLUE}========================================${NC}"

# Invalid endpoint
api_call "Invalid Endpoint (Expected 404)" "GET" "/nonexistent/endpoint" "" "404"

# Missing required fields
INVALID_KUNDALI_DATA='{"birthDate":"1990-05-15"}'
api_call "Missing Required Fields (Expected 422)" "POST" "/kundali/generate_kundali" "$INVALID_KUNDALI_DATA" "422" "$ACCESS_TOKEN"

# Invalid date format
INVALID_DATE_DATA='{
    "birthDate":"invalid-date",
    "birthTime":"14:30",
    "latitude":28.7041,
    "longitude":77.1025,
    "timezone":"Asia/Kolkata"
}'
api_call "Invalid Date Format (Expected 422)" "POST" "/kundali/generate_kundali" "$INVALID_DATE_DATA" "422" "$ACCESS_TOKEN"

# Unauthorized access (no token)
api_call "Unauthorized Access (Expected 401)" "GET" "/kundali/list_kundalis" "" "401"

# ============================================================================
# CLEANUP & FINAL DELETE
# ============================================================================

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}CLEANUP${NC}"
echo -e "${BLUE}========================================${NC}"

if [ ! -z "$KUNDALI_ID" ]; then
    api_call "Delete Kundali" "DELETE" "/kundali/delete_kundali/$KUNDALI_ID" "" "200" "$ACCESS_TOKEN"
fi