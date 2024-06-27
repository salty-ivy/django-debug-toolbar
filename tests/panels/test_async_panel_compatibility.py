from django.http import HttpResponse
from django.test import AsyncRequestFactory, RequestFactory, TestCase
from django.test.utils import override_settings

from debug_toolbar.toolbar import DebugToolbar


@override_settings(DEBUG_TOOLBAR_CONFIG={"DISABLE_PANELS": {}})
class PanelAsyncCompatibilityTestCase(TestCase):
    def setUp(self):
        self.factory = AsyncRequestFactory()
        self.request = self.factory.get("/")
        self.toolbar = DebugToolbar(self.request, lambda request: HttpResponse())

    def test_disable_nonasync_panel_with_asgi(self):
        for panel in self.toolbar.panels:
            panel.is_async = False
            self.assertFalse(panel.enabled)

    def test_enable_async_panel_with_asgi(self):
        for panel in self.toolbar.panels:
            panel.is_async = True
            self.assertTrue(panel.enabled)

    def test_enable_all_panels_with_wsgi(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.toolbar = DebugToolbar(self.request, lambda request: HttpResponse())
        for panel in self.toolbar.panels:
            panel.is_async = True
            self.assertTrue(panel.enabled)
            panel.is_async = False
            self.assertTrue(panel.enabled)
