#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
requirements:
- class: InlineJavascriptRequirement

baseCommand:
  - mdrun.py
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
    default: "mdrun"
  conf_file:
    type: File
    inputBinding:
      position: 3
      prefix: --conf_file
#BB specific
  input_tpr_path:
    type: File
    inputBinding:
      position: 4
      prefix: --input_tpr_path
  output_trr_path:
    type: string
    inputBinding:
      position: 5
      prefix: --output_trr_path
  output_gro_path:
    type: string
    inputBinding:
      position: 6
      prefix: --output_gro_path
  output_edr_path:
    type: string
    inputBinding:
      position: 7
      prefix: --output_edr_path
  output_log_path:
    type: string
    inputBinding:
      position: 8
      prefix: --output_log_path
  output_xtc_path:
    type: string?
    inputBinding:
      prefix: --output_xtc_path
  output_cpt_path:
    type: string?
    inputBinding:
      prefix: --output_cpt_path

outputs:
  output_trr_file:
    type: File
    outputBinding:
      glob: $(inputs.output_trr_path)
  output_gro_file:
    type: File
    outputBinding:
      glob: $(inputs.output_gro_path)
  output_edr_file:
    type: File
    outputBinding:
      glob: $(inputs.output_edr_path)
  output_log_file:
    type: File
    outputBinding:
      glob: $(inputs.output_log_path)
  output_xtc_file:
    type: File?
    outputBinding:
      glob: $(inputs.output_xtc_path)
  output_cpt_file:
    type: File?
    outputBinding:
      glob: $(inputs.output_cpt_path)
