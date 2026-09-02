# FoundationPose Object Registration Accuracy

The repository provides the raw RGB-D sequences, textured 3D models, 
ground-truth and estimated poses, and the scripts needed to reproduce 
the reported registration-accuracy results.

> **Paper:** Masuhr, Koch, Oels, Schüppstuhl (2025). *FoundationPose evaluation
> for AR-guided industrial inspection.* Institute of Aircraft Production Technology (IFPT),
> Hamburg University of Technology (TUHH).

---

## Overview

The goal of the evaluation is to quantify how accurately FoundationPose registers
industrial components under a realistic eye-in-hand setup, where the camera is
mounted on a robot end-effector. For each object we compare:

- the **estimated pose** returned by FoundationPose
- a **ground-truth pose** derived from robot forward kinematics and manual object placement

expressed in a common robot base frame. Two FoundationPose operating modes are
evaluated:

- **One Shot** — single-frame model-based registration
- **Tracking** — pose propagated across the sequence

All translations are given in **millimetres (mm)**; rotations are the upper-left
3×3 block of each 4×4 homogeneous transform.

## Repository structure

```
.
├── 3D_models/                     # Scaled, textured OBJ meshes used in the evaluation
│   ├── SS-400-9-scaled_mesh.obj
│   ├── SS-810-3-scaled_mesh.obj
│   ├── SS-810-61-4-scaled_mesh.obj
│   └── flange_scaled_mesh.obj
│
├── raw_data_all/                  # RGB-D capture sequences, one folder per object
│   ├── Flange/
│   │   ├── rgb/                    # Colour frames  (1280×720, 8-bit PNG)
│   │   ├── depth/                  # Aligned depth  (1280×720, 16-bit PNG, mm)
│   │   ├── masks/                  # Seed masks for FoundationPose initialisation
│   │   ├── mesh/                   # Object mesh + material used for this sequence
│   │   └── cam_K.txt               # 3×3 camera intrinsics
│   ├── SS-400-9/out/               # (same layout)
│   ├── SS-810-3/
│   ├── SS-810-61-4/
│   └── textures/                   # Shared surface texture (Metal024_4K)
│
├── Additional_Data.xlsx           # Ground-truth & estimated poses + raw kinematics
├── pose_calculation.py            # Eye-in-hand pose composition (worked example)
├── realsense_foundationpose.py    # RealSense .bag → FoundationPose input converter
└── README.md
```

## Objects

| Folder / mesh   | Component                | Manufacturer |
|-----------------|--------------------------|--------------|
| `SS-400-9`      | Tube fitting             | Swagelok     |
| `SS-810-61-4`   | Tube fitting             | Swagelok     |
| `SS-810-3`      | Tube fitting             | Swagelok     |
| `Flange`        | F-GFA1-150-4Li flange    | Schwer       |

## Dataset details

Each object folder contains an RGB-D sequence of roughly 540–555 frames captured
with an Intel RealSense camera:

- **`rgb/`** — 1280×720 colour frames, 8-bit PNG.
- **`depth/`** — 1280×720 depth frames, 16-bit PNG, aligned to the colour stream,
  with values in millimetres.
- **`masks/`** — a small set of segmentation masks used to seed FoundationPose.
- **`mesh/`** — the object mesh, material (`.mtl`) and texture used for that
  sequence.
- **`cam_K.txt`** — the 3×3 pinhole intrinsic matrix for the aligned stream, in
  the FoundationPose format:

  ```
  fx  0   cx
  0   fy  cy
  0   0   1
  ```

### Pose data — `Additional_Data.xlsx`

- **`GT and EP`** — per part and pose, the 4×4 **ground-truth** and **estimated**
  transforms for both the *One Shot* and *Tracking* modes.
- **`raw`** — the underlying robot forward-kinematics data (base→TCP transforms)
  used to construct the ground truth.

## Scripts

### `realsense_foundationpose.py`

Extracts colour frames, colour-aligned depth frames, and the camera intrinsics
from a RealSense `.bag` recording into the directory layout FoundationPose
expects (`out/rgb/`, `out/depth/`, `out/cam_K.txt`).

```bash
pip install pyrealsense2 numpy opencv-python
python realsense_foundationpose.py
```

Set `bag_file_path` at the top of the script to your recording before running.

### `pose_calculation.py`

A worked, self-contained example of the eye-in-hand pose composition used to
place a FoundationPose result into the robot base frame:

```
T_base_obj = T_base_tcp · T_tcp_cam · T_cam_obj
```

where `T_base_tcp` comes from robot forward kinematics, `T_tcp_cam` is the
tranformation from TCP to the camera, and `T_cam_obj` is the FoundationPose output. All
transforms are 4×4 in millimetres.

```bash
pip install numpy
python pose_calculation.py
```

## Reproducing the evaluation

1. (Optional) Convert your own `.bag` recording with
   `realsense_foundationpose.py`, or use the sequences already provided in
   `raw_data_all/`.
2. Run FoundationPose on a sequence using the matching mesh from `3D_models/`,
   the seed mask, and `cam_K.txt`, in either *One Shot* or *Tracking* mode. See
   the [FoundationPose repository](https://github.com/NVlabs/FoundationPose) for
   setup and inference instructions.
3. Compose the camera-frame result into the base frame following
   `pose_calculation.py`.
4. Compare against the ground-truth poses in `Additional_Data.xlsx`.

## Citation

If you use this dataset or code, please cite:

```bibtex
@misc{masuhr2025foundationpose,
  title  = {TBD},
  author = {Masuhr and Koch and Oels and Schüppstuhl},
  year   = {2025},
  note   = {Institute of Aircraft Production Technology (IFPT),
            Hamburg University of Technology (TUHH)}
}
```

## Licensing

Unless stated otherwise, the contents of this repository are released under
**CC BY 4.0** (data) and the **MIT License** (code); see `LICENSE`.

### 3D models (`3D_models/`)

The mesh files in `3D_models/` were prepared in Blender from the nominal CAD
data published by the component manufacturers (Swagelok SS-400-9, SS-810-61-4,
SS-810-3; Schwer F-GFA1-150-4Li). Our contribution consists of the conversion to
textured OBJ format, scaling, alignment to the object coordinate system used in
the evaluation, and UV unwrapping. The underlying geometry originates from the
manufacturers' CAD data, and any rights therein remain with the respective
manufacturer.

These files are provided to document the models used in the reported evaluation.
The repository licence does not extend to them, and they are not offered for
commercial reuse or redistribution. If you intend to use the component geometry
beyond reproducing the results presented here, please obtain the CAD data
directly from the manufacturer under their terms of use.

The object coordinate system of each model is defined as shown in Figure 4 of
the accompanying publication; all ground-truth and estimated poses in
`Additional_Data.xlsx` refer to this definition.
