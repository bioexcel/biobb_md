#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand:
  - grompp.py
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
    default: "grompp"
  conf_file:
    type: File
    inputBinding:
      position: 3
      prefix: --conf_file
#BB specific
  input_gro_path:
    type: File
    inputBinding:
      position: 4
      prefix: --input_gro_path
  input_top_zip_path:
    type: File
    inputBinding:
      position: 5
      prefix: --input_top_zip_path
  output_tpr_path:
    type: string
    inputBinding:
      position: 6
      prefix: --output_tpr_path
  input_cpt_path:
    type: File?
    inputBinding:
      position: 7
      prefix: --input_cpt_path

outputs:
  output_tpr_file:
    type: File
    outputBinding:
      glob: $(inputs.output_tpr_path)
