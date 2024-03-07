# Configuration Details

This document provides a detailed explanation of the configuration settings defined in the INI file. Each setting is critical for the correct operation of the data framework. The table below outlines the fields, their descriptions, and whether they are Mandatory or Optional.

| Field Name       | Description                                                                                       | Mandatory/Optional |
|------------------|---------------------------------------------------------------------------------------------------|--------------------|
| `test datatypes` | This is the name of the dataset/table that will be created in mesh/glue.                         | Mandatory          |
| `path`           | Path to the file, which must be a CSV file.                                                       | Mandatory          |
| `delimiter`      | Specifies the delimiter of the file. If nothing is given, the comma (`,`) will be used.          | Optional           |
| `partition`      | This partition will be used purely for our glue/s3 table. The label sent to mesh will be business date. | Optional       |
| `rebuild table`  | This flag will indicate whether the table needs to be rebuilt.                                    | Optional           |
| `metadata`       | Optional metadata for setting headers and types. Without it, headers are inferred, and all types are strings. | Optional       |
| `description`    | Description that will be used to update the mesh catalogue.                                       | Optional           |
| `summary`        | Summary of the dataset.                                                                           | Optional           |
| `dataset_type`   | Specifies the type of the dataset, as per governance rules.                                       | Mandatory          |
| `dataset_source` | The source of the dataset.                                                                       | Mandatory          |
| `database_name`  | The name of the database the file will be uploaded to.                                           | Mandatory          |
| `tenant_name`    | The name of the tenant.                                                                           | Mandatory          |
| `table_name`     | The name of the table in s3/glue.                                                                | Mandatory          |
| `update_mesh`    | Sends a request to the mesh catalogue, either creating a new dataset definition or updating an existing one. | Mandatory    |
| `crawler`        | Runs a crawler on the database, updating the schema so that the data can be queried.             | Optional           |

Please ensure that you fill out the configuration file accurately to ensure proper data handling and integration into the mesh/glue framework.
