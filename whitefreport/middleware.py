# whitefreport/middleware.py

from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.utils import timezone

class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            print("User is not authenticated")
            return None

        current_time = request.session.get('last_activity')
        if current_time:
            elapsed_time = (timezone.now() - current_time).total_seconds() / 60
            print(f"Elapsed time: {elapsed_time} minutes")
            if elapsed_time > settings.AUTO_LOGOUT['IDLE_TIME']:
                print("Session expired. Redirecting to signin.")
                messages.info(request, settings.AUTO_LOGOUT['MESSAGE'])
                return redirect('signin')  # Replace 'signin' with your actual login URL pattern name

        print("Updating last_activity timestamp")
        request.session['last_activity'] = timezone.now()
