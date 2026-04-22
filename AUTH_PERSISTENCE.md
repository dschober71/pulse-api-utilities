# Authentication Persistence Feature

## Overview

The Authentication Persistence feature allows you to store your Tableau Server credentials securely in your browser for 10 minutes, making it easy to use multiple tools without re-entering your authentication details each time.

## How It Works

### Storing Authentication

1. Navigate to any tool in the application
2. Fill in your authentication details:
   - Server URL
   - Site Content URL
   - Authentication method (Password or PAT)
   - Credentials (username/password or PAT name/token)
3. Check the box: **"💾 Keep authentication data (10 min)"**
4. Submit the form

Your credentials are now stored locally in your browser for 10 minutes.

### Using Stored Authentication

1. Navigate to any other tool in the application
2. Check the box: **"📋 Use stored authentication"**
3. Your authentication fields will automatically fill with the stored credentials
4. Adjust any fields if needed and submit

### Visual Indicator

When authentication is stored, you'll see a green banner at the top of the page showing:
- The server URL you're authenticated to
- The site name
- Time remaining until expiration
- A button to clear stored credentials

## Security Features

### Local Storage Only
- Credentials are stored in your browser's localStorage
- Never sent to any external server except Tableau
- Only accessible by the application on the same domain

### Automatic Expiration
- Credentials automatically expire after **10 minutes**
- The countdown is displayed in the status banner
- Expired credentials are automatically removed

### Manual Clearing
- Click **"Clear Stored Auth"** in the status banner to immediately remove stored credentials
- Closing the browser tab/window does NOT clear the storage (allows multi-tab usage)
- Clearing browser data will remove stored credentials

### What's Stored

The following information is stored:
- Server URL
- Site Content URL  
- Authentication method (password/PAT)
- Username and password OR PAT name and token
- Timestamp of storage

**Note**: Passwords and tokens are stored in plain text in localStorage. Only use this feature on trusted, personal devices.

## Use Cases

### Multiple Tool Workflow
```
1. Use "Copy Definitions" with stored auth
2. Switch to "Manage Followers" - use stored auth
3. Switch to "Analytics" - use stored auth
4. All use the same credentials without re-entering
```

### Different Sites
```
1. Store auth for Site A
2. Work on multiple tools for Site A
3. When done, click "Clear Stored Auth"
4. Store auth for Site B
5. Work on tools for Site B
```

### Testing/Development
```
1. Store test environment credentials
2. Quickly switch between tools during testing
3. No need to copy-paste credentials repeatedly
```

## Cross-Tool Compatibility

All 13 tools support authentication persistence:
- ✅ Copy Definitions (source authentication)
- ✅ Manage Followers
- ✅ Swap Datasources
- ✅ Update Preferences
- ✅ Check Certified Metrics
- ✅ Bulk Create Scoped Metrics
- ✅ Analytics
- ✅ TCM Activity Logs
- ✅ Zero Follower Metrics
- ✅ Remove All Followers
- ✅ Orphaned Metrics Cleanup
- ✅ Export Definitions
- ✅ Favorite Metrics

**Note**: Copy Definitions has both source and destination authentication sections. Only the source section supports persistence.

## Technical Details

### Storage Format
```javascript
{
  "server_url": "https://your-server.com",
  "site_content_url": "yoursite",
  "auth_method": "pat",
  "pat_name": "MyPAT",
  "pat_token": "your-token",
  "timestamp": 1234567890000
}
```

### Browser Compatibility
- Works in all modern browsers (Chrome, Firefox, Safari, Edge)
- Requires localStorage support
- No cookies or session storage used

### Privacy Considerations

⚠️ **Important**: Since credentials are stored in plain text in localStorage:
- Only use on trusted, personal devices
- Don't use on shared or public computers
- Always clear stored auth when finished on shared devices
- Consider using shorter-lived PATs instead of passwords

### Timeout Behavior

The 10-minute timeout is enforced:
- On page load
- Every minute (updates the countdown)
- Before using stored credentials
- When attempting to retrieve stored data

If credentials have expired:
- The status banner is hidden
- "Use stored authentication" checkbox will show an alert
- You must re-enter credentials manually

## Troubleshooting

### "No stored authentication data found"
- No credentials are currently stored
- Or they expired (>10 minutes old)
- Solution: Re-enter credentials and check "Keep authentication data"

### Fields not auto-filling
- Click "Use stored authentication" checkbox
- Stored credentials may have expired
- Check the status banner to see if auth is stored

### Wrong credentials being filled
- You may have stored credentials for a different server/site
- Click "Clear Stored Auth" and re-enter correct credentials

### Can't clear stored auth
- Refresh the page
- Manually clear browser's localStorage for the domain
- Check browser console for errors

## Best Practices

1. **Use PATs instead of passwords** when possible for better security
2. **Clear stored auth** when finished with a session
3. **Don't store on public/shared computers**
4. **Re-authenticate** if you've been away from the browser for a while
5. **Verify the server URL** in the status banner before submitting forms
6. **Use different browser profiles** for different Tableau environments

## Future Enhancements

Potential improvements for future versions:
- Configurable timeout duration
- Encrypted storage
- Multiple saved credentials (profiles)
- Session detection (clear on browser close)
- Credential validation before storage
