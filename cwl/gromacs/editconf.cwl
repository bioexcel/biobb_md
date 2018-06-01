#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand:
  - editconf.py
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
    default: "editconf"
  conf_file:
    type: File
    inputBinding:
      position: 3
      prefix: --conf_file
  input_gro_path:
    type: File
    inputBinding:
      position: 4
      prefix: --input_gro_path
  output_gro_path:
    type: string
    inputBinding:
      position: 5
      prefix: --output_gro_path
outputs:
  output_gro_file:
    type: File
    outputBinding:
      glob: $(inputs.output_gro_path)
