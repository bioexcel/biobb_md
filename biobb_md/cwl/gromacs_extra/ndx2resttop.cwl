#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand:
  - ndx2resttop.py
inputs:
  system:
    type: string
    inputBinding:
      position: 1
      prefix: --system
    default: "linux"
  step:
    type: string
    inputBinding:
      position: 2
      prefix: --step
    default: "ndx2resttop"
  conf_file:
    type: File
    inputBinding:
      position: 3
      prefix: --conf_file
  input_ndx_path:
    type: File
    inputBinding:
      position: 4
      prefix: --input_ndx_path
  input_top_zip_path:
    type: File
    inputBinding:
      position: 4
      prefix: --input_top_zip_path
  output_top_zip_path:
    type: string
    inputBinding:
      position: 5
      prefix: --output_top_zip_path
outputs:
  output_top_zip_file:
    type: File
    outputBinding:
      glob: $(inputs.output_top_zip_path)
