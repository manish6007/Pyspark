inputs:
  - type: file
    format: csv
    alias: csv_to_parquet

outputs:
  - type: file
    format: parquet
    mode: overwrite
    path: <your_path_here> # replace with your actual path
    delimiter: "\t" # assuming tab delimiter, otherwise replace with the correct one

transformations:
  - input: csv_parquet # this might be a typo and should be something else
    action: transform
    list:
      - dw_lod_tmp: "timestamp=2024-03-07 20:17:55"
