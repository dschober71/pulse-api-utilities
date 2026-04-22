# Orphaned Metrics Cleanup Feature

## Overview

The Orphaned Metrics Cleanup feature helps you identify and delete Pulse metrics whose datasource no longer exists on the Tableau server. This typically happens when:

- A datasource is deleted but metrics depending on it remain
- A datasource is moved or renamed without updating metric definitions
- Migration processes leave behind orphaned references

## Features

- 🔍 **Detect orphaned metrics**: Scans all metrics across all definitions to find those referencing missing datasources
- ⚠️ **Safe deletion with confirmation**: Requires explicit user confirmation before deleting
- 🗑️ **Bulk cleanup**: Delete all orphaned metrics in a single operation
- 📊 **Detailed reporting**: Shows exactly which metrics will be deleted and why

## How It Works

1. **Authentication**: Connects to your Tableau server using credentials or PAT
2. **Discovery Phase**:
   - Retrieves all datasources on the site
   - Retrieves all metric definitions
   - Retrieves all metrics for each definition
3. **Analysis Phase**:
   - Checks each metric's definition for its datasource reference
   - Compares datasource IDs against the list of existing datasources
   - Identifies metrics whose datasource is missing
4. **Cleanup Phase** (optional):
   - Displays all orphaned metrics for review
   - Requires user to type "CONFIRM CLEANUP" to proceed
   - Deletes each orphaned metric
   - Reports success/failure for each deletion

## Usage via Web Interface

1. Navigate to the application home page at `http://localhost:3000`
2. Click on **"🗑️ Orphaned Metrics Cleanup"** utility card
3. Fill in the connection details:
   - Tableau Server URL (e.g., `https://your-server.com`)
   - Site Content URL (leave blank for default site)
   - Choose authentication method (Username/Password or PAT)
   - Enter credentials
4. Click **"🔍 Find Orphaned Metrics"**
5. Review the list of orphaned metrics
6. If you want to delete them:
   - Type **"CONFIRM CLEANUP"** in the confirmation box
   - Click **"🗑️ Delete Orphaned Metrics"**

## Usage via API

### Find Orphaned Metrics

**Endpoint**: `POST /orphaned-metrics`

**Request Body**:
```json
{
  "server_url": "https://your-server.com",
  "api_version": "3.26",
  "site_content_url": "",
  "auth_method": "password",
  "username": "your-username",
  "password": "your-password"
}
```

Or with PAT:
```json
{
  "server_url": "https://your-server.com",
  "api_version": "3.26",
  "site_content_url": "",
  "auth_method": "pat",
  "pat_name": "your-pat-name",
  "pat_token": "your-pat-token"
}
```

**Response**:
```json
{
  "success": true,
  "results": [
    {"success": true, "message": "🔐 Authenticating with Tableau Server..."},
    {"success": true, "message": "🗄️ Retrieving datasource names..."},
    {"success": true, "message": "📊 Retrieving all metric definitions..."},
    {"success": true, "message": "🔍 Retrieving metrics for all definitions..."},
    {"success": true, "message": "🔎 Analyzing metrics for missing datasources..."}
  ],
  "orphaned_metrics": [
    {
      "metric_id": "abc-123",
      "metric_name": "Sales Metric",
      "definition_id": "def-456",
      "definition_name": "Sales Definition",
      "missing_datasource_id": "ds-789"
    }
  ],
  "summary": "Found 1 orphaned metrics out of 50 total metrics."
}
```

### Delete Orphaned Metrics

**Endpoint**: `POST /delete-orphaned-metrics`

**Request Body**:
```json
{
  "server_url": "https://your-server.com",
  "api_version": "3.26",
  "site_content_url": "",
  "auth_method": "password",
  "username": "your-username",
  "password": "your-password",
  "confirmation": "CONFIRM CLEANUP",
  "orphaned_metric_ids": ["abc-123", "def-456"]
}
```

**Response**:
```json
{
  "success": true,
  "results": [
    {"success": true, "message": "🔐 Authenticating with Tableau Server..."},
    {"success": true, "message": "🗑️ Deleting 2 orphaned metrics..."},
    {"success": true, "message": "✅ Deleted metric abc-123"},
    {"success": true, "message": "✅ Deleted metric def-456"}
  ],
  "summary": "Deleted 2 orphaned metrics. Failed: 0."
}
```

## Safety Features

1. **Two-Step Process**: Finding and deleting are separate operations, allowing review before deletion
2. **Explicit Confirmation**: Must type exact phrase "CONFIRM CLEANUP" to enable deletion
3. **Detailed Logging**: Every step is logged with success/failure status
4. **Non-Destructive Discovery**: The find operation is read-only and makes no changes

## Testing

A test script is provided to verify the endpoints are working correctly:

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
python test_orphaned_metrics.py
```

## Implementation Details

### Helper Functions

- `find_orphaned_metrics(definitions, all_metrics, datasource_id_to_name)`: Analyzes metrics to identify orphans
- `get_all_datasources_rest()`: Retrieves all datasources from REST API
- `get_metric_definitions_rest()`: Retrieves all metric definitions
- `get_metrics_for_definition_swap()`: Retrieves metrics for a specific definition

### API Endpoints

- `/orphaned-metrics` (POST): Finds orphaned metrics
- `/delete-orphaned-metrics` (POST): Deletes orphaned metrics with confirmation

### Frontend

- Tab navigation in main UI
- Form for authentication and server connection
- Results display with table view
- Confirmation input for safe deletion
- Real-time progress updates

## Error Handling

The feature handles various error scenarios:

- Authentication failures
- Network timeouts
- Permission issues
- Invalid metric/definition IDs
- API errors

All errors are logged and displayed to the user with helpful messages.

## Troubleshooting

**Problem**: "Authentication failed"
- **Solution**: Verify your credentials and server URL are correct

**Problem**: "No orphaned metrics found" but you expect some
- **Solution**: Check that the datasource was actually deleted and not just renamed

**Problem**: Deletion fails for some metrics
- **Solution**: Check the detailed results to see which metrics failed and why. You may need higher permissions.

**Problem**: Request times out
- **Solution**: If you have many definitions/metrics, the scan can take time. Try with a smaller site or contact support to optimize.

## Notes

- This feature requires appropriate permissions on the Tableau server
- Deleted metrics cannot be recovered - ensure you have backups if needed
- The feature only deletes metrics, not definitions
- Default metrics within definitions are included in the scan
