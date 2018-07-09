#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand:
  - solvate.py
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
    default: "solvate"
  conf_file:
    type: File
    inputBinding:
      position: 3
      prefix: --conf_file
#BB specific
  input_solute_gro_path:
    type: File
    inputBinding:
      position: 4
      prefix: --input_solute_gro_path
  output_gro_path:
    type: string
    inputBinding:
      position: 5
      prefix: --output_gro_path
  input_top_zip_path:
    type: File
    inputBinding:
      position: 6
      prefix: --input_top_zip_path
  output_top_zip_path:
    type: string
    inputBinding:
      position: 7
      prefix: --output_top_zip_path
outputs:
  output_gro_file:
    type: File
    outputBinding:
      glob: $(inputs.output_gro_path)
  output_top_zip_file:
    type: File
    outputBinding:
      glob: $(inputs.output_top_zip_path)
