import pyspark
import pprint
from ruamel import yaml
from sys import argv
import great_expectations as ge
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest


context = ge.get_context()

datasource_yaml = f"""
name: libio_download 
class_name: Datasource
module_name: great_expectations.datasource
execution_engine:
  module_name: great_expectations.execution_engine
  class_name: PandasExecutionEngine
data_connectors:
    default_runtime_data_connector_name:
        class_name: RuntimeDataConnector
        batch_identifiers:
            - default_identifier_name
    default_inferred_data_connector_name:
        class_name: InferredAssetFilesystemDataConnector
        base_directory: ./data/libcsv/clean/
        default_regex:
          group_names:
            - data_asset_name 
          pattern: (.*)
"""

context.add_datasource(**yaml.load(datasource_yaml))

batch_request = RuntimeBatchRequest(
    datasource_name="libio_download",
    data_connector_name="default_runtime_data_connector_name",
    data_asset_name="Libio CSV",  # This can be anything that identifies this data_asset for you
    runtime_parameters={
        "path": f"./data/libcsv/clean/clean_{argv[1]}.csv"
    },  # Add your path here.
    batch_identifiers={"default_identifier_name": "default_identifier"},
)
validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name="libio_suite"
)

validator.head()
validator.get_expectation_suite()
validation = validator.validate()
printout = f"""
-------------------REPORT START----------------


Expectations in total: {validation["statistics"]["evaluated_expectations"]}

Sucessfully validated: {validation["statistics"]["successful_expectations"]}
Failures : {validation["statistics"]["unsuccessful_expectations"]}
Success in %: {validation["statistics"]["success_percent"]:.2f}


------------------REPORT END-------------------
"""

print(printout)

# pprint.pprint(validation)
