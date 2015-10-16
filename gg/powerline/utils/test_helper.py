from unittest import TestCase, TestLoader, TestSuite


__author__ = 'Stefan Hackmann'


class ParametrizedTestCase(TestCase):

    def __init__(self, name, param=None):
        super(ParametrizedTestCase, self).__init__(name)
        ParametrizedTestCase.param = param


def parametrize(klass, param=None):
    test_loader = TestLoader()
    test_names = test_loader.getTestCaseNames(klass)
    test_suite = TestSuite()
    for name in test_names:
        test_suite.addTest(klass(name, param=param))
    return test_suite
