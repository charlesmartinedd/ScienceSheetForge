# 📡 ScienceSheetForge API Documentation

**Version:** 2.0.0
**Base URL:** `http://localhost:3000`
**Content-Type:** `application/json`

---

## Table of Contents

1. [Authentication](#authentication)
2. [Core Endpoints](#core-endpoints)
3. [New API Endpoints](#new-api-endpoints)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Examples](#examples)

---

## Authentication

Currently, the API does not require authentication. For production deployment, consider adding API keys or OAuth2.

---

## Core Endpoints

### GET /

**Description:** Main web interface

**Response:** HTML page

### GET /health

**Description:** Health check endpoint for monitoring

**Response:**
```json
{
  "status": "healthy",
  "service": "ScienceSheetForge",
  "version": "2.0.0",
  "available_formats": ["crossword", "word-search", "matching", "fill-blank", "short-answer", "true-false"],
  "features": {
    "pdf_export": true,
    "batch_generation": true
  }
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

## Worksheet Generation

### POST /generate

**Description:** Generate a single worksheet

**Request Body:**
```json
{
  "grade_level": "K-2 | 3-5 | 6-8",
  "standard_code": "K-LS1-1",
  "worksheet_format": "crossword | word-search | matching | fill-blank | short-answer | true-false"
}
```

**Response:**
```json
{
  "success": true,
  "worksheet": "/view/crossword_K-LS1-1_20251106_123456.png",
  "answer_key": "/view/crossword_K-LS1-1_20251106_123456_ANSWER_KEY.png",
  "timestamp": "20251106_123456",
  "worksheet_format": "crossword",
  "standard": "K-LS1-1"
}
```

**Status Codes:**
- `200 OK` - Worksheet generated successfully
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Standard not found
- `500 Internal Server Error` - Generation failed

**Validation Rules:**
- `grade_level` must be one of: "K-2", "3-5", "6-8"
- `standard_code` must match pattern: `[A-Z0-9\-]+`
- `worksheet_format` must be an available format ID

---

## File Access

### GET /view/:filename

**Description:** View generated worksheet in browser

**Parameters:**
- `filename` (string, required) - PNG filename

**Response:** PNG image

**Status Codes:**
- `200 OK` - File found and returned
- `400 Bad Request` - Invalid filename
- `403 Forbidden` - Path traversal attempt
- `404 Not Found` - File not found

**Security:** Filename must be alphanumeric with underscores/hyphens only, no path separators

---

### GET /download/:filename

**Description:** Download generated worksheet

**Parameters:**
- `filename` (string, required) - PNG filename

**Response:** PNG file download

**Status Codes:**
- `200 OK` - File download started
- `400 Bad Request` - Invalid filename
- `403 Forbidden` - Path traversal attempt
- `404 Not Found` - File not found

---

## New API Endpoints

### GET /api/standards

**Description:** List all available NGSS standards

**Response:**
```json
{
  "success": true,
  "count": 45,
  "standards": [
    {
      "grade_level": "K-2",
      "code": "K-LS1-1",
      "title": "Patterns in the Natural World",
      "description": "Use observations to describe patterns of what plants and animals need to survive"
    },
    ...
  ]
}
```

**Status Codes:**
- `200 OK` - Standards retrieved

---

### GET /api/formats

**Description:** List all available worksheet formats

**Response:**
```json
{
  "success": true,
  "count": 20,
  "formats": [
    {
      "id": "crossword",
      "name": "Crossword Puzzle",
      "category": "Word Activities",
      "icon": "🔤",
      "description": "Science vocabulary crossword puzzle",
      "suitable_grades": ["3-5", "6-8"],
      "features": ["Vocabulary building", "Critical thinking", "Answer key included"],
      "available": true
    },
    ...
  ]
}
```

**Status Codes:**
- `200 OK` - Formats retrieved

---

### GET /api/export-pdf/:filename

**Description:** Convert PNG worksheet to PDF format

**Parameters:**
- `filename` (string, required) - PNG filename to convert

**Response:**
```json
{
  "success": true,
  "pdf_file": "/download/crossword_K-LS1-1_20251106_123456.pdf",
  "message": "PDF exported successfully"
}
```

**Status Codes:**
- `200 OK` - PDF created successfully
- `400 Bad Request` - Invalid filename
- `403 Forbidden` - Access denied
- `404 Not Found` - PNG file not found
- `500 Internal Server Error` - Conversion failed
- `503 Service Unavailable` - PDF export feature not available

**Notes:**
- Original PNG must exist in output folder
- PDF maintains 300 DPI resolution
- RGBA images converted to RGB with white background

---

### POST /api/batch-generate

**Description:** Generate multiple worksheets in parallel

**Request Body:**
```json
{
  "grade_level": "K-2 | 3-5 | 6-8",
  "standard_codes": ["K-LS1-1", "K-PS3-1"],
  "worksheet_formats": ["crossword", "word-search", "matching"],
  "max_workers": 4
}
```

**Parameters:**
- `grade_level` (string, required) - Grade level for all worksheets
- `standard_codes` (array, required) - List of NGSS standard codes
- `worksheet_formats` (array, required) - List of format IDs to generate
- `max_workers` (integer, optional) - Parallel workers (default: 4, max: 8)

**Response:**
```json
{
  "success": true,
  "result": {
    "summary": {
      "total": 6,
      "successful": 6,
      "failed": 0,
      "duration_seconds": 4.523,
      "success_rate": 1.0
    },
    "successful": [
      {
        "format": "crossword",
        "standard": "K-LS1-1",
        "output_file": "/path/to/crossword_K-LS1-1_20251106.png",
        "answer_key": "/path/to/crossword_K-LS1-1_20251106_ANSWER_KEY.png"
      },
      ...
    ],
    "failed": []
  }
}
```

**Status Codes:**
- `200 OK` - Batch generation completed (check result.summary for details)
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - One or more standards not found
- `500 Internal Server Error` - Batch generation failed
- `503 Service Unavailable` - Batch generation feature not available

**Performance Notes:**
- Generation time scales with: `(standards × formats) / workers`
- Recommended max_workers: 4 for CPU-bound tasks
- Each worksheet takes ~1-3 seconds
- Example: 10 standards × 3 formats with 4 workers ≈ 22.5 seconds

---

## Error Handling

### Error Response Format

```json
{
  "success": false,
  "error": "Human-readable error message"
}
```

### Common Error Codes

| Status | Meaning | Common Causes |
|--------|---------|---------------|
| 400 | Bad Request | Invalid parameters, validation failed |
| 403 | Forbidden | Security violation (path traversal) |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Feature not enabled |

### Error Messages

Errors are designed to be user-friendly and not expose internal details:

❌ **Bad:** `Traceback (most recent call last): File "/app/app.py", line 123...`

✅ **Good:** `An error occurred while generating the worksheet. Please try again.`

---

## Rate Limiting

**Current Status:** Not implemented

**Recommendation for Production:**
- Implement rate limiting using Flask-Limiter
- Suggested limits:
  - `/generate`: 60 requests/minute per IP
  - `/api/batch-generate`: 10 requests/minute per IP
  - Other endpoints: 100 requests/minute per IP

---

## Examples

### Example 1: Generate Single Worksheet

```bash
curl -X POST http://localhost:3000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "grade_level": "K-2",
    "standard_code": "K-LS1-1",
    "worksheet_format": "crossword"
  }'
```

**Response:**
```json
{
  "success": true,
  "worksheet": "/view/crossword_K-LS1-1_20251106_104523.png",
  "answer_key": "/view/crossword_K-LS1-1_20251106_104523_ANSWER_KEY.png",
  "timestamp": "20251106_104523",
  "worksheet_format": "crossword",
  "standard": "K-LS1-1"
}
```

---

### Example 2: Batch Generate Worksheets

```bash
curl -X POST http://localhost:3000/api/batch-generate \
  -H "Content-Type: application/json" \
  -d '{
    "grade_level": "3-5",
    "standard_codes": ["3-LS1-1", "3-PS2-1"],
    "worksheet_formats": ["crossword", "word-search", "matching"],
    "max_workers": 4
  }'
```

**Response:**
```json
{
  "success": true,
  "result": {
    "summary": {
      "total": 6,
      "successful": 6,
      "failed": 0,
      "duration_seconds": 8.234,
      "success_rate": 1.0
    },
    "successful": [ /* 6 worksheet objects */ ]
  }
}
```

---

### Example 3: Export to PDF

```bash
# First, generate a worksheet
RESPONSE=$(curl -s -X POST http://localhost:3000/generate \
  -H "Content-Type: application/json" \
  -d '{"grade_level":"K-2","standard_code":"K-LS1-1","worksheet_format":"crossword"}')

# Extract filename
FILENAME=$(echo $RESPONSE | jq -r '.worksheet' | sed 's#/view/##')

# Export to PDF
curl http://localhost:3000/api/export-pdf/$FILENAME

# Download PDF
PDF_FILENAME=$(echo $FILENAME | sed 's/.png/.pdf/')
curl -O http://localhost:3000/download/$PDF_FILENAME
```

---

### Example 4: List Available Standards

```bash
curl http://localhost:3000/api/standards | jq '.count, .standards[0]'
```

**Response:**
```json
45
{
  "grade_level": "K-2",
  "code": "K-LS1-1",
  "title": "Patterns in the Natural World",
  "description": "Use observations to describe patterns of what plants and animals need to survive"
}
```

---

### Example 5: Check Health Status

```bash
curl http://localhost:3000/health | jq
```

**Response:**
```json
{
  "status": "healthy",
  "service": "ScienceSheetForge",
  "version": "2.0.0",
  "available_formats": [
    "crossword",
    "word-search",
    "matching",
    "fill-blank",
    "short-answer",
    "true-false"
  ],
  "features": {
    "pdf_export": true,
    "batch_generation": true
  }
}
```

---

## Security Considerations

### Input Validation

All inputs are validated before processing:
- Grade levels must match allowed list
- Standard codes must match pattern `[A-Z0-9\-]+`
- Worksheet formats must be available
- Filenames must be alphanumeric with underscore/hyphen only

### Path Traversal Protection

File access endpoints (`/view`, `/download`, `/api/export-pdf`) include multiple layers of protection:
1. Filename validation (no `..`, `/`, `\`)
2. `werkzeug.secure_filename()` sanitization
3. `Path.resolve()` canonicalization
4. Relative path validation against output folder

### Security Headers

All responses include:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `X-XSS-Protection: 1; mode=block`
- `Content-Security-Policy`

---

## Client Library Examples

### Python

```python
import requests

class ScienceSheetForgeClient:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url

    def generate_worksheet(self, grade_level, standard_code, worksheet_format):
        response = requests.post(
            f"{self.base_url}/generate",
            json={
                "grade_level": grade_level,
                "standard_code": standard_code,
                "worksheet_format": worksheet_format
            }
        )
        return response.json()

    def batch_generate(self, grade_level, standard_codes, worksheet_formats):
        response = requests.post(
            f"{self.base_url}/api/batch-generate",
            json={
                "grade_level": grade_level,
                "standard_codes": standard_codes,
                "worksheet_formats": worksheet_formats,
                "max_workers": 4
            }
        )
        return response.json()

# Usage
client = ScienceSheetForgeClient()
result = client.generate_worksheet("K-2", "K-LS1-1", "crossword")
print(result)
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

class ScienceSheetForgeClient {
  constructor(baseURL = 'http://localhost:3000') {
    this.client = axios.create({ baseURL });
  }

  async generateWorksheet(gradeLevel, standardCode, worksheetFormat) {
    const response = await this.client.post('/generate', {
      grade_level: gradeLevel,
      standard_code: standardCode,
      worksheet_format: worksheetFormat
    });
    return response.data;
  }

  async batchGenerate(gradeLevel, standardCodes, worksheetFormats) {
    const response = await this.client.post('/api/batch-generate', {
      grade_level: gradeLevel,
      standard_codes: standardCodes,
      worksheet_formats: worksheetFormats,
      max_workers: 4
    });
    return response.data;
  }
}

// Usage
const client = new ScienceSheetForgeClient();
client.generateWorksheet('K-2', 'K-LS1-1', 'crossword')
  .then(result => console.log(result));
```

---

## Changelog

### Version 2.0.0 (November 6, 2025)

**Added:**
- `/health` endpoint with feature flags
- `/api/standards` - List all NGSS standards
- `/api/formats` - List all worksheet formats
- `/api/export-pdf/:filename` - Convert PNG to PDF
- `/api/batch-generate` - Parallel worksheet generation
- Comprehensive input validation
- Security headers on all responses
- Structured logging

**Changed:**
- Improved error messages (no stack traces exposed)
- Enhanced `/generate` validation

**Security:**
- Fixed path traversal vulnerability in `/view` and `/download`
- Added filename validation
- Implemented secure_filename sanitization
- Added multiple security headers

---

## Support

For issues, feature requests, or questions:
- **GitHub Issues:** https://github.com/charlesmartinedd/ScienceSheetForge/issues
- **Documentation:** See README.md and RELEASE_AUDIT_REPORT.md

---

*API Documentation v2.0.0 - Last Updated: November 6, 2025*
