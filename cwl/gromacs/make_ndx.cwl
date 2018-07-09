#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand:
  - make_ndx.py
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
    default: "make_ndx"
  conf_file:
    type: File
    inputBinding:
      position: 3
      prefix: --conf_file
#BB specific
  input_structure_path:
    type: File
    inputBinding:
      position: 4
      prefix: --input_structure_path
  output_ndx_path:
    type: string
    inputBinding:
      position: 5
      prefix: --output_ndx_path
  input_ndx_path:
    type: File?
    inputBinding:
      prefix: --input_ndx_path

outputs:
  output_ndx_file:
    type: File
    outputBinding:
      glob: $(inputs.output_ndx_path)
