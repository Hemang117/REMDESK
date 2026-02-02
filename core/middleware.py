class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # LOGIC: Only prevent caching for HTML pages (where the Nonce lives).
        # We let CSS/Images (handled by WhiteNoise) keep their cache for speed.
        # This ensures the cryptographic Nonce is always fresh for every visitor.
        if 'text/html' in response.get('Content-Type', ''):
            response['Cache-Control'] = 'private, no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            
        return response
