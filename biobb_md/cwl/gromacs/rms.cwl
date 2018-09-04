#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand:
  - rms.py
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
    default: "rms"
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
  input_traj_path:
    type: File
    inputBinding:
      position: 5
      prefix: --input_traj_path
  output_xvg_path:
    type: string
    inputBinding:
      position: 6
      prefix: --output_xvg_path

outputs:
  output_xvg_file:
    type: File
    outputBinding:
      glob: $(inputs.output_xvg_path)
