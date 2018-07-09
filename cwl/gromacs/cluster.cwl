#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand:
  - cluster.py
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
    default: "cluster"
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
  input_traj_path:
    type: File
    inputBinding:
      position: 5
      prefix: --input_traj_path
  output_pdb_path:
    type: string
    inputBinding:
      position: 6
      prefix: --output_pdb_path
outputs:
  output_pdb_file:
    type: File
    outputBinding:
      glob: $(inputs.output_pdb_path)
