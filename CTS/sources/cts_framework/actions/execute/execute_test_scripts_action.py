"""
 * @section LICENSE
 *
 * @copyright
 * Copyright (c) 2017 Intel Corporation
 *
 * @copyright
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * @copyright
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * @copyright
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @section DESCRIPTION
"""

import ConfigParser

import sys

from cts_framework.actions.action import Action
from cts_framework.build_information import BuildInformation
from cts_framework.commons.color_printer import ColorPrinter
from cts_framework.commons.logging_helper import LoggingHelper
from cts_framework.tests_managing.test_package.tests_packages_container import TestsPackagesContainer
from cts_framework.tests_managing.tests_manager import TestsManager
from cts_framework.tests_running.execution_feed import ExecutionFeed
from cts_framework.tests_running.test_run import TestRun
from cts_framework.commons.config_reader import get_configuration_from_files, certificates_files_are_valid


class ExecuteTestScriptsAction(Action):
    ACTION = "tests"
    PARAM_NAME = "EXECUTE_TYPE"

    def __init__(self, *params, **kwargs):
        Action.__init__(self, *params, **kwargs)

        self._logger = LoggingHelper(__name__)

    def fill_parser_arguments(self):
        self.parser.add_argument("package", help="Test package to execute", type=str, nargs=1)
        self.parser.add_argument("-s", "--test_suites", type=str, nargs="+", help="Test suites to execute")
        self.parser.add_argument("-t", "--test_scripts", type=str, nargs="+", help="Test scripts to execute")
        self.parser.add_argument("-c", "--config_files", help="Configuration files for test scripts", required=True,
                                 nargs="+")
        self.parser.add_argument("-T", "--timeout", help="Timeout for scripts", type=int, nargs=1)
        self.parser.add_argument("-g", "--debug", default=False, action="store_true",
                                 help="Enables debugging mode which will stop tests execution after first failed test")
        self.parser.add_argument("-x", "--return_tests_status_as_exit_code", action="store_true", default=False,
                                 help="When flag set CTS framework will return calculate exit code basing on tests results.")

    def process_action(self, configuration):
        print "Using CTS in version %s" % (ColorPrinter.format_text(BuildInformation.BUILD_VERSION, bold=True))
        tests_manager = TestsManager()

        configuration_files = configuration.config_files
        test_scripts_configuration = get_configuration_from_files(configuration_files)
        if test_scripts_configuration is None:
            sys.exit(-1)

        if not certificates_files_are_valid(test_scripts_configuration):
            sys.exit(-1)

        test_plan = TestsPackagesContainer()

        if configuration.test_suites or configuration.test_scripts:
            if configuration.test_suites:
                test_suites_found = tests_manager.get_packages()
                test_suites_found.filter(packages=configuration.package, suites=configuration.test_suites,
                                         remove_empty=True)
                test_plan += test_suites_found
            if configuration.test_scripts:
                test_scripts_found = tests_manager.get_packages()

                test_scripts_found.filter(packages=configuration.package, scripts=configuration.test_scripts,
                                          remove_empty=True)
                test_plan += test_scripts_found
        else:
            test_plan += tests_manager.get_packages()

        test_plan.filter(packages=configuration.package)

        if not test_plan.packages:
            print "No script selected to execute"
            exit(64)  # EX_USAGE = 64    command line usage error

        message = "Executing "
        print "Executing:"
        for package in test_plan.packages:
            for suite in package.suites:
                for script in suite.scripts:
                    print "\t* %s from suite %s from package %s" % (script.name, suite.name, package.name)
                    message += "%s from suite %s from package %s, " % (script.name, suite.name, package.name)

        self._logger.log_debug(message)

        if configuration.timeout is not None:
            message = "setting timeout execution to %s" % configuration.timeout[0]
            self._logger.log_debug(message)
            print "\n%s" % message
            test_plan.set_scripts_timeout(configuration.timeout[0])

        execution_feed = ExecutionFeed(test_plan, test_scripts_configuration)

        ExecuteTestScriptsAction.execute_configuration_group(execution_feed, test_status_as_exit_code=configuration.return_tests_status_as_exit_code)

    @staticmethod
    def execute_configuration_group(configuration_group, test_status_as_exit_code=None):
        """
        :type configuration_group: cts_framework.tests_running.execution_feed.ExecutionFeed
        :type test_status_as_exit_code: bool
        """
        test_run = TestRun()
        test_run.add_execution_feed(configuration_group)
        test_run.register_all()
        execution_status = test_run.run_all()
        if not execution_status and test_status_as_exit_code:
            print "Tests finished with status failed, exit code set to 4"
            exit(4)
