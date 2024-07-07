from inspect import iscoroutine

from django.template.response import SimpleTemplateResponse
from django.utils.translation import gettext_lazy as _

from debug_toolbar.panels import Panel


class RedirectsPanel(Panel):
    """
    Panel that intercepts redirects and displays a page with debug info.
    """

    is_async = True
    has_content = False

    nav_title = _("Intercept redirects")

    def _process_response(self, response):
        """
        Common response processing logic.
        """
        if 300 <= response.status_code < 400:
            redirect_to = response.get("Location")
            if redirect_to:
                status_line = f"{response.status_code} {response.reason_phrase}"
                cookies = response.cookies
                context = {"redirect_to": redirect_to, "status_line": status_line}
                response = SimpleTemplateResponse(
                    "debug_toolbar/redirect.html", context
                )
                response.cookies = cookies
                response.render()
        return response

    async def aprocess_request(self, request):
        response = await super().process_request(request)
        return self._process_response(response)

    def process_request(self, request):
        response = super().process_request(request)
        if iscoroutine(response):
            return self.aprocess_request(request)
        return self._process_response(response)
