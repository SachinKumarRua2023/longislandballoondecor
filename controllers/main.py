import json
import base64
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

try:
    import anthropic
except ImportError:
    _logger.warning("anthropic library not installed. Install with: pip install anthropic")


class VenueDecoratorController(http.Controller):

    @http.route('/venue-decorator/analyze', type='json', auth='public', methods=['POST'], csrf=False)
    def analyze_venue(self):
        """
        Analyzes venue image using Claude API and returns 4 decoration suggestions
        """
        try:
            # Get image data from request
            image_data = request.jsonrequest.get('image')
            if not image_data:
                return {'error': 'No image provided', 'status': 400}

            # Remove data:image prefix if present
            if image_data.startswith('data:'):
                image_data = image_data.split(',')[1]

            # Get media type
            media_type = request.jsonrequest.get('mediaType', 'image/jpeg')

            # Initialize Claude client with API key from Odoo system parameters
            api_key = request.env['ir.config_parameter'].sudo().get_param(
                'venue_decorator.claude_api_key'
            )

            if not api_key:
                _logger.error("Claude API key not configured in Odoo")
                return {
                    'error': 'Claude API key not configured. Please set it in Odoo Settings.',
                    'status': 500
                }

            client = anthropic.Anthropic(api_key=api_key)

            # Call Claude API with vision
            message = client.messages.create(
                model="claude-opus-4-8",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_data
                                }
                            },
                            {
                                "type": "text",
                                "text": """Analyze this venue image and suggest 4 different decoration approaches using balloons, banners, gifts, and greeting cards.

For each option, provide:
1. Option name (e.g., "Elegant Minimalist", "Festive Colorful", "Classic Romance", "Modern Chic")
2. Color scheme (primary colors to use)
3. Key decoration elements
4. Greeting card theme
5. Overall vibe/mood

Format as JSON with 4 options:
{
  "options": [
    {
      "name": "Option Name",
      "colors": "Color scheme",
      "balloons": "Balloon style",
      "banners": "Banner style",
      "gifts": "Gift arrangement",
      "cards": "Greeting card theme",
      "vibe": "Overall mood"
    }
  ],
  "venue_analysis": "Brief analysis"
}"""
                            }
                        ]
                    }
                ]
            )

            # Parse response
            response_text = message.content[0].text

            # Extract and parse JSON
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                decoration_suggestions = json.loads(json_str)
                return {'success': True, 'data': decoration_suggestions}
            else:
                return {'error': 'Could not parse Claude response', 'status': 500}

        except anthropic.APIError as e:
            _logger.error(f"Claude API error: {str(e)}")
            return {'error': f'Claude API error: {str(e)}', 'status': 500}
        except Exception as e:
            _logger.error(f"Venue decorator error: {str(e)}", exc_info=True)
            return {'error': f'Server error: {str(e)}', 'status': 500}

    @http.route('/venue-decorator/submit-order', type='json', auth='public', methods=['POST'], csrf=False)
    def submit_order(self):
        """
        Submits venue decoration order to Odoo
        """
        try:
            data = request.jsonrequest

            # Create a lead/opportunity in Odoo for the order
            lead_obj = request.env['crm.lead'].sudo()
            lead = lead_obj.create({
                'name': f"Venue Decoration - {data.get('event_date')}",
                'contact_name': data.get('name'),
                'email_from': data.get('email'),
                'phone': data.get('phone'),
                'description': f"""
Event Date: {data.get('event_date')}
Selected Decoration Style: {data.get('selected_option')}
Special Requests: {data.get('notes')}
                """,
                'type': 'lead',
            })

            _logger.info(f"New venue decoration order created: Lead ID {lead.id}")

            return {
                'success': True,
                'message': 'Order submitted successfully! We will contact you soon.',
                'lead_id': lead.id
            }

        except Exception as e:
            _logger.error(f"Order submission error: {str(e)}", exc_info=True)
            return {'error': str(e), 'status': 500}
