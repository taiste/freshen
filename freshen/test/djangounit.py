#-*- coding: utf8 -*-

from freshen.test.base import FreshenTestCase

from django.test import TestCase

from freshen.context import scc


class DjangoTestCase(FreshenTestCase, TestCase):
    """Support Django tests."""

    def __init__(self, step_runner, step_registry, feature, scenario, feature_suite):
        FreshenTestCase.__init__(self, step_runner, step_registry,
                                 feature, scenario, feature_suite)
        TestCase.__init__(self, scenario.name)

    def setUp(self):
        super(DjangoTestCase, self).setUp()

        for hook_impl in self.step_registry.get_hooks('before', self.scenario.get_tags()):
            hook_impl.run(self.scenario)

        if scc.fixtures:
            self.fixtures = scc.fixtures

        if hasattr(self, '_pre_setup'):
            self._pre_setup()

    def runScenario(self):
        for step in self.scenario.iter_steps():
            self.runStep(step, 3)
        self.last_step = None

    def tearDown(self):
        for hook_impl in reversed(self.step_registry.get_hooks('after', self.scenario.get_tags())):
            hook_impl.run(self.scenario)
