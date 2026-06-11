{
    'name': 'Long Island Balloon Decor - AI Venue Decorator',
    'version': '1.0',
    'category': 'Website',
    'summary': 'AI-powered venue decoration suggestions using Claude API',
    'author': 'Long Island Balloon Decor',
    'depends': ['web', 'website'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'external_dependencies': {
        'python': ['anthropic'],
    },
}
