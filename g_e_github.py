import pyspark
import pprint
from ruamel import yaml

import great_expectations as ge
from great_expectations import DataContext
from great_expectations.core import ExpectationSuite
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.data_context.util import file_relative_path
from great_expectations.validator.validator import Validator


context = ge.get_context()
suite = context.get_expectation_suite("gh_clean_suite")

#
datasource_yaml = f"""
name: Github_API_Clean
class_name: Datasource
module_name: great_expectations.datasource
execution_engine:
    module_name: great_expectations.execution_engine
    class_name: SparkDFExecutionEngine
data_connectors:
    my_runtime_data_connector:
        class_name: RuntimeDataConnector
        batch_identifiers:
            - Github
"""
context.add_datasource(**yaml.load(datasource_yaml))
#

runtime_batch_request = RuntimeBatchRequest(
    datasource_name="Github_API_Clean",
    data_connector_name="my_runtime_data_connector",
    data_asset_name="github data",
    batch_spec_passthrough={"reader_options": {"header": True}},
    runtime_parameters={"path": "data/github/clean/gh_clean.csv"},
    batch_identifiers={"Github": "Clean"},
)

my_validator: Validator = context.get_validator(
    batch_request=runtime_batch_request,
    expectation_suite=suite,  # OR
    # expectation_suite_name=suite_name
)
my_validator.head()
my_validator.get_expectation_suite()
validation = my_validator.validate()
printout = f"""
-------------------REPORT START----------------



Expectations in total: {validation["statistics"]["evaluated_expectations"]}

Sucessfully validated: {validation["statistics"]["successful_expectations"]}
Failures : {validation["statistics"]["unsuccessful_expectations"]}
Success in %: {validation["statistics"]["success_percent"]:.2f} 


------------------REPORT END-------------------
"""
print(printout)
