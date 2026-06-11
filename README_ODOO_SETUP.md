# Long Island Balloon Decor - Odoo AI Venue Decorator Setup

## Overview
This module integrates Claude API (vision capability) with Odoo to analyze venue images and suggest 4 different decoration options.

## Installation Steps

### 1. Install Python Dependencies
```bash
pip install anthropic
```

### 2. Add Module to Odoo
- Copy the entire `longislandballoondecor` folder to your Odoo addons directory:
  ```
  /path/to/odoo/addons/longislandballoondecor
  ```

### 3. Install Module in Odoo
- Go to **Apps** in Odoo
- Search for "Long Island Balloon Decor"
- Click **Install**

### 4. Set Claude API Key
This can be done in two ways:

#### Option A: Via Odoo Settings (Recommended)
1. Go to **Settings** → **Technical** → **Parameters** → **System Parameters**
2. Create a new parameter:
   - **Key**: `venue_decorator.claude_api_key`
   - **Value**: Your Claude API key from https://console.anthropic.com/account/keys
3. Click **Save**

#### Option B: Via Environment Variable
```bash
export ANTHROPIC_API_KEY='your-claude-api-key'
```

## How It Works

### User Flow
1. User uploads venue image via the iframe gallery
2. Image is sent to Odoo backend (`/venue-decorator/analyze`)
3. Claude API analyzes the image with vision capability
4. Returns 4 personalized decoration suggestions
5. User selects one and fills order form
6. Order is saved in Odoo as a CRM Lead

### API Endpoints

#### Analyze Venue
- **URL**: `/venue-decorator/analyze`
- **Method**: POST
- **Content-Type**: application/json
- **Request Body**:
  ```json
  {
    "image": "base64_encoded_image_data",
    "mediaType": "image/jpeg"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "options": [
        {
          "name": "Option Name",
          "colors": "Color scheme",
          "balloons": "Balloon description",
          "banners": "Banner description",
          "gifts": "Gift arrangement",
          "cards": "Card theme",
          "vibe": "Overall mood"
        }
      ],
      "venue_analysis": "Venue layout analysis"
    }
  }
  ```

#### Submit Order
- **URL**: `/venue-decorator/submit-order`
- **Method**: POST
- **Content-Type**: application/json
- **Request Body**:
  ```json
  {
    "name": "Customer Name",
    "email": "customer@email.com",
    "phone": "123-456-7890",
    "event_date": "MM/DD/YYYY",
    "notes": "Special requests",
    "selected_option": "Option Name"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Order submitted successfully!",
    "lead_id": 123
  }
  ```

## Integration with Website

### Embed in Odoo Page
Add this snippet to any Odoo website page:

```html
<div style="width: 100%; max-width: 1200px; margin: 0 auto;">
  <iframe src="/venue-decorator" 
          style="width: 100%; height: 1200px; border: none; border-radius: 8px;">
  </iframe>
</div>
```

### Standalone URL
The gallery is accessible at: `/venue-decorator`

Or access the HTML directly: `/venue-decorator/index.html`

## Features

- **AI-Powered Analysis**: Uses Claude Opus 4.8 with vision to analyze venues
- **4 Customized Options**: Each option includes:
  - Decoration style name
  - Color scheme recommendations
  - Balloon selections
  - Banner styles
  - Gift arrangements
  - Greeting card themes
  - Overall vibe/mood
- **Order Management**: Orders are saved as CRM Leads in Odoo
- **Responsive Design**: Works on desktop and mobile
- **HTTPS Ready**: Full CORS support for iframe embedding

## Troubleshooting

### Error: "Claude API key not configured"
- Check that the system parameter `venue_decorator.claude_api_key` is set in Odoo
- Or set the `ANTHROPIC_API_KEY` environment variable

### Error: "anthropic library not installed"
- Run: `pip install anthropic` in your Odoo environment
- Restart Odoo service

### Image Analysis Fails
- Ensure image size is reasonable (< 5MB)
- Check that image format is supported: JPEG, PNG, GIF, WebP
- Verify Claude API key is valid and has credits

### Orders Not Appearing
- Check Odoo's Sales > Leads section
- Verify CRM module is installed
- Check Odoo logs for errors

## Cost Considerations

- **Claude API Vision**: ~$0.01 per image analysis (typical)
- **Per request**: $0.003 - $0.01 depending on image complexity
- No additional Odoo module costs

## Security Notes

- API key is stored in Odoo system parameters (encrypted in database)
- Images are analyzed in-transit via Claude API
- Images are not stored on your Odoo server
- Orders are stored as regular CRM Leads with access controls

## Support

For issues or questions:
1. Check the module logs: **Settings** → **Technical** → **Logs**
2. Verify Claude API key is valid
3. Check Odoo console for JavaScript errors

## Module Structure

```
longislandballoondecor/
├── __init__.py
├── __manifest__.py
├── index.html              # Gallery and decorator UI
├── controllers/
│   ├── __init__.py
│   └── main.py            # Claude API integration endpoints
├── security/
│   └── ir.model.access.csv
└── README_ODOO_SETUP.md    # This file
```
