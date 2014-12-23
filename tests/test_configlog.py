
import unittest
import logging
import os

import configlog

from .logging_dict import logging_dict


# Py3 compatibility
if 'reload' not in dir(__builtins__):
    from imp import reload


logging_json = 'tests/logging.json'
logging_yaml = 'tests/logging.yml'
logging_file = 'tests/logging.cfg'


class TestConfiglog(unittest.TestCase):
    """Tests for configlog module."""

    def setUp(self):
        """Set up logging module to initial state."""
        logging.getLogger().setLevel(logging.NOTSET)

    def tearDown(self):
        """Reset logging module to remove current configuration."""
        logging.shutdown()
        reload(logging)

    def assert_config(self):
        """Assert that root logger is configured via configuration method."""
        logger = logging.getLogger()
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertTrue(len(logger.handlers) > 0)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)

    def test_from_json(self):
        """Test that from_json loads config object."""
        configlog.from_json(logging_json)
        self.assert_config()

    def test_from_yaml(self):
        """Test that from_yaml loads config object."""
        configlog.from_yaml(logging_yaml)
        self.assert_config()

    def test_from_file(self):
        """Test that from_file loads config object."""
        configlog.from_file(logging_file)
        self.assert_config()

    def test_from_dict(self):
        """Test that from_dict loads config object."""
        configlog.from_dict(logging_dict)
        self.assert_config()

    def test_from_filename_json(self):
        """Test that from_filename loads config object from json."""
        configlog.from_filename(logging_json)
        self.assert_config()

    def test_from_filename_yaml(self):
        """Test that from_filename loads config object from yaml."""
        configlog.from_filename(logging_yaml)
        self.assert_config()

    def test_from_filename_file(self):
        """Test that from_filename loads config object from file."""
        configlog.from_filename(logging_file)
        self.assert_config()

    def test_from_filename_exception(self):
        """Test that from_autodetect() throws exception on invalid object."""
        self.assertRaises(configlog.ConfigLogException,
                          configlog.from_filename,
                          'invalid')

    def test_from_autodetect_dict(self):
        """Test that from_autodetect() loads config object from dict."""
        configlog.from_autodetect(logging_dict)
        self.assert_config()

    def test_from_autodetect_json(self):
        """Test that from_autodetect() loads config object from json."""
        configlog.from_autodetect(logging_json)
        self.assert_config()

    def test_from_autodetect_yaml(self):
        """Test that from_autodetect() loads config object from yaml."""
        configlog.from_autodetect(logging_yaml)
        self.assert_config()

    def test_from_autodetect_file(self):
        """Test that from_autodetect() loads config object from file."""
        configlog.from_autodetect(logging_file)
        self.assert_config()

    def test_from_autodetect_exception(self):
        """Test that from_autodetect() throws exception on invalid object."""
        self.assertRaises(configlog.ConfigLogException,
                          configlog.from_autodetect,
                          'invalid')

        self.assertRaises(configlog.ConfigLogException,
                          configlog.from_autodetect,
                          [])

    def test_from_env(self):
        """Test that from_env() loads config object from filename via
        environment variable.
        """
        var = 'CL_TESTING'
        os.environ[var] = logging_json
        configlog.from_env(var)
        self.assert_config()
        del os.environ[var]