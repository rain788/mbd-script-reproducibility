# Constraints Summary

## GLOBAL
[RULE][GLOBAL][STAGE] L1 Modeling Base: units/model/parts/markers/CM/basic geometry; L2 Joints & Constraints: joints/grounding/topology/constraint relations; L3 Loads & Drives: gravity/forces/torques/motion drives; L4 Measurements: measures/observables for required physical quantities; L5 Simulation: configure and run the simulation/analysis; L6 Results & Export: extract results, print target values, and export files

[RULE][GLOBAL][API] Do not fabricate APIs and do not execute functions that do not belong to the current repair level. Before executing L6, file export operations cannot be involved.

[RULE][GLOBAL][API] For any constraint, force, marker, or simulation topology operation, all referenced parts and markers must belong to the same model. Do not mix objects retrieved from one imported model with constraints or ground markers created on another model.

[RULE][GLOBAL][API] All retrieved imported parts, ground markers, constraints, and forces must belong to and be created on that same imported model. Do not mix imported parts from one model with constraints, forces, or ground markers created on another model container.

[RULE][GLOBAL][API] Never invent or import any additional API, helper, initializer, convenience wrapper, file content, or call pattern that is not explicitly present in the provided API surface.

[RULE][GLOBAL][API] Ground is a built-in Part, not a Marker. When grounding is needed, access the ground part first and create an explicit ground marker on it only if the selected APIs explicitly support that workflow.

[RULE][GLOBAL][REPAIR] When the target repair stage does not include L1, do not recreate or rename modeling-base entities that already exist in the current assembled L1 section, including parts, center-of-mass markers, grounding markers, and joint markers. Reuse the existing variables unless L1 is explicitly included in the repair target.

[RULE][GLOBAL][FORMAT] Stage output must be raw executable Python only. Do not emit prose, markdown fences, headings, or explanations.

[RULE][GLOBAL][STAGE] Must include geometric features when generating models in L1, excluding importing existing models

[RULE][GLOBAL][STAGE] When using APIs, not all inputs required by the API must be passed in. Choose the inputs required by the task for input

[RULE][GLOBAL][FORMAT] Code must contain only ASCII characters and must not contain any Chinese characters anywhere, including comments, strings, variable names, and output text.

## API d.units.setUnits
[RULE][L1][d.units.setUnits] Use this API only to set the global default units once near the start of L1.

[RULE][L1][d.units.setUnits] Before calling d.units.setUnits, define d exactly as d = Adams.defaults in L1. Do not call d.units.setUnits before d exists.

[RULE][L1][d.units.setUnits] Use only enum values that are explicitly present in the selected API surface.

## API Adams.Models.create

[RULE][L1][Adams.Models.create] Use this API to create the top-level model object in L1.

[RULE][L1][Adams.Models.create] Do not invent separate model initialization helpers before or after this call unless they are explicitly present in the selected API surface.


## API Adams.read_parasolid_file

[RULE][L1][Adams.read_parasolid_file] When the task explicitly requires importing one Parasolid assembly as a full model, prefer a single full-assembly import call such as Adams.read_parasolid_file(file_name=x_t_path, model_name='<model_name>') instead of multiple guessed per-part import calls.

[RULE][L1][Adams.read_parasolid_file] If the required bodies are already named members inside one Parasolid assembly, do not import them by repeating Adams.read_parasolid_file(..., part_name='Model.PartName') for each body unless the task or selected API surface explicitly requires per-part import.

[RULE][L1][Adams.read_parasolid_file] After a full Parasolid assembly import, treat the imported assembly as the source of truth for all required named parts in the task.

[RULE][L1][Adams.read_parasolid_file] Forbidden repair pattern: repeated per-part Parasolid imports for named assembly members when the task explicitly depends on parts already present inside one imported assembly.

[RULE][L1][Adams.read_parasolid_file] After the full Parasolid assembly import, retrieve each required imported part explicitly by full Adams name using Adams.stoo(...).

[RULE][L1][Adams.read_parasolid_file] When the task explicitly names imported assembly members, access them by full Adams name such as Adams.stoo('.ModelName.PartName') rather than by guessed model containers, guessed part dictionaries, guessed getters, or reconstructed import workflows.

[RULE][L1][Adams.read_parasolid_file] Forbidden access patterns for imported assembly members include guessed owner paths, or any other container/getter not explicitly proven by the selected API surface.

[RULE][L1][Adams.read_parasolid_file] Do not recreate, re-import, or guess lookup paths for imported assembly parts when Adams.stoo(full_name) can retrieve the required object directly by full Adams name.

[RULE][L1][Adams.read_parasolid_file] After importing a Parasolid assembly and retrieving the required parts by Adams.stoo(...), every imported dynamic part used in simulation must be assigned an explicit center-of-mass marker and an explicit positive mass before joints, forces, or simulation are created. Do not treat imported geometry as dynamically complete without cm and mass definition.

[RULE][L1][Adams.read_parasolid_file] For the benchmark file 04_data/cad_models/Buffer_models/buffer_system.x_t, use model_name='three_stage_recoil_model' and retrieve the validated imported part names exactly as Adams.stoo('.three_stage_recoil_model.Support_gp-fixed'), Adams.stoo('.three_stage_recoil_model.First-stage-assembly'), and Adams.stoo('.three_stage_recoil_model.Second-stage-assembly'). Do not guess lowercase aliases such as support, stage1, or stage2.

## API model_object.Parts.createRigidBody

[RULE][L1][model_object.Parts.createRigidBody] L1 is only for model setup, rigid bodies, markers, and optional geometry. Do not place joints, loads, simulation, analyses, or extraction in L1.

[RULE][L1][model_object.Parts.createRigidBody] Unless the selected API surface explicitly proves a different accepted pattern, the ONLY accepted dynamic-rigid-body construction order is: (1) createRigidBody(...) without mass/location/cm kwargs, (2) create a same-part CM marker, (3) assign body.cm = cm_marker, and only then (4) assign body.mass = a positive value. Do not read body.cm before step (3). Do not attach geometry through body.cm before step (3). Do not pass mass=..., cm=..., or location=... to createRigidBody(...).

[RULE][L1][model_object.Parts.createRigidBody] Avoid risky location kwargs unless the selected API surface explicitly proves they are accepted for this call.

## API part_object.Geometries.createEllipsoid
[RULE][L1][part_object.Geometries.createEllipsoid] For part_object.Geometries.createEllipsoid. To change the ellipsoid's orientation, rotate or redefine the center_marker.

## API part_object.Markers.create

[RULE][L1][part_object.Markers.create] Create markers on the same Part that will own or consume them. Do not create a marker on one part and use it as if it belonged to another part.

[RULE][L1][part_object.Markers.create] When a marker is intended to become a rigid body's center of mass, create it on that rigid body and then assign body.cm to that marker.

[RULE][L1][part_object.Markers.create] Marker names and geometry names must be unique within the owning part/model. Do not give a marker and a geometry the same name; use suffixes such as _marker and _geom.

[RULE][L2][part_object.Markers.create] When a constraint or force needs an explicit ground-side marker, first access the model's built-in ground part through model_object.ground_part, then create the marker on that ground part by calling model_object.ground_part.Markers.create(...).

[RULE][L2][part_object.Markers.create] Do not guess unsupported ground owner paths such as model_object.Ground, model_object.parts, model_object.Parts.get("ground"), or defaults-side containers unless that exact owner path is explicitly proven by the selected API surface.

[RULE][L2][part_object.Markers.create] Ground-side markers, body-side joint markers, geometry markers, and force-application markers must be created separately according to role. Do not reuse them across roles unless the task explicitly allows it.

[RULE][L2][part_object.Markers.create] When the target repair stage is L2 only and the current assembled code already contains marker variables created in L1 for the required grounding or joint roles, do not recreate those markers in L2. Reuse the existing marker variables directly unless L1 is explicitly included in the target stages.

[RULE][L2][part_object.Markers.create] Forbidden repair pattern: recreating a marker in L2 with the same semantic role or the same name as a marker already created in the current assembled L1 section.

[RULE][L2][part_object.Markers.create] For revolute-joint closed-chain mechanisms, the two markers passed to each revolute joint must be located at the same physical point in the initial global configuration. Do not place a coupler-side marker at local [0,0,0] when the connected crank-side marker is globally at [100,0,0]; make the two marker locations globally coincident.

[RULE][L2][part_object.Markers.create] For a four-bar benchmark, avoid a fully collinear locked initial configuration. Use a non-degenerate planar layout with distinct joint coordinates, for example ground left [0,0,0], crank-coupler [100,40,0], coupler-rocker [180,40,0], and ground right [220,0,0], and create both markers of each revolute joint at the corresponding global coordinate using a shared ground reference.

## API model_object.Constraints.createFixed

[RULE][L2][model_object.Constraints.createFixed] When the task explicitly requires a support, base, housing, or other named reference structure to be fixed on the ground or remain stationary throughout the simulation, model_object.Constraints.createFixed must be selected and used explicitly in L2; do not treat a support part as grounded only by naming, imported geometry status, or by connecting other bodies to it.

[RULE][L2][model_object.Constraints.createFixed] To fix a support part to ground, first create one marker on the support part and one marker on model_object.ground_part at the same physical location and orientation, then call model_object.Constraints.createFixed(name=joint_name, i_marker=support_side_marker, j_marker=ground_side_marker); do not replace this grounding step with translational, revolute, or other non-fixed constraints.

[RULE][L2][model_object.Constraints.createFixed] For grounding a support, base, housing, or other stationary reference part, both i_marker and j_marker must be real Marker objects. The ground-side j_marker must come from model_object.ground_part.Markers.create(...), not from FloatingMarkers, names, strings, or any non-Marker placeholder.

[RULE][L2][model_object.Constraints.createFixed] Forbidden repair pattern: using FloatingMarkers.create(...) or any non-Marker object as the j_marker of model_object.Constraints.createFixed(...).

## API model_object.Constraints.createTranslational

[RULE][L2][model_object.Constraints.createTranslational] A translational joint must connect two real Marker objects, one created on each owning part of the two constrained bodies. For support-second-stage and first-stage-second-stage topology, create or reuse exactly one marker on each side and pass them as i_marker and j_marker.

[RULE][L2][model_object.Constraints.createTranslational] Forbidden repair pattern: reusing one marker object as both sides of a translational joint, mixing marker roles across different joints, or passing an object that is not an explicitly created Marker on the corresponding owning part.

## API part_object.FloatingMarkers.create

[RULE][L3][part_object.FloatingMarkers.create] Use this API only when a downstream force or torque API explicitly requires a FloatingMarker argument.

[RULE][L3][part_object.FloatingMarkers.create] A FloatingMarker is not interchangeable with an ordinary Marker created by part_object.Markers.create.

[RULE][L3][part_object.FloatingMarkers.create] Creating a FloatingMarker on the same part as the body-side i_marker does not satisfy the cross-part requirement for force/torque definitions. Ownership by different parts still matters.

[RULE][L3][part_object.FloatingMarkers.create] When a task needs an external reference for a force or torque, prefer creating the FloatingMarker on model_object.ground_part if that owner path is explicitly available in the selected API surface.

## API model_object.Forces.createForceVector
[RULE][L3][model_object.Forces.createForceVector] The body-side application marker i_marker and the reference-side j_floating_marker must belong to different parts of the same model. Never place both ends of a ForceVector on the same moving rigid body.

[RULE][L3][model_object.Forces.createForceVector] When j_floating_marker is required, it must be a true FloatingMarker object created from a FloatingMarkers container. Never substitute an ordinary Marker for j_floating_marker.

[RULE][L3][model_object.Forces.createForceVector] For push/load tasks on a moving body, prefer creating i_marker on the driven body and creating j_floating_marker on model_object.ground_part unless the selected API surface explicitly proves another required reference part.

[RULE][L3][model_object.Forces.createForceVector] Use ForceVector in L3 only for externally applied translational force loads.

[RULE][L3][model_object.Forces.createForceVector] A ForceVector should explicitly separate the body-side application marker from the floating marker used by the force definition. When the task requires a FloatingMarker as j_floating_marker, create that FloatingMarker explicitly and do not substitute an ordinary Marker for it.

[RULE][L3][model_object.Forces.createForceVector] When a task applies a force to a moving rigid body, create a dedicated ordinary marker on that body for the force application point, and create a separate FloatingMarker on the required reference part according to the API surface.

[RULE][L3][model_object.Forces.createForceVector] Do not reuse joint markers, geometry markers, barrel reference markers, or CM markers as force-application markers unless the selected API surface or task explicitly proves that reuse is valid.

[RULE][L3][model_object.Forces.createForceVector] If a ground-side reference part is needed for the force definition, prefer using model_object.ground_part as the owner path when the selected API surface exposes ground_part on the model object.

[RULE][L3][model_object.Forces.createForceVector] For a constant 3D force vector, prefer bracketed vector literal syntax such as xyz_force_function='[fx, fy, fz]' when that form has been validated in-task. Do not rewrite it into comma-separated scalar text, semicolon-separated text, whitespace-separated text, or undocumented wrapper expressions.

## API model_object.Forces.createGravity

[RULE][L3][model_object.Forces.createGravity] Benchmark default vertical direction is -Y for free-fall tasks unless the task explicitly overrides it. For metric units, the value is -9.81

[RULE][L3][model_object.Forces.createGravity] For free-fall tasks, prefer the gravity API directly rather than faking gravity with another force API.

## API model_object.Forces.createTorqueVector

[RULE][L3][model_object.Forces.createTorqueVector] Use TorqueVector in L3 only for externally applied rotational loads or driving torques.

[RULE][L3][model_object.Forces.createTorqueVector] The j_floating_marker argument must receive a true FloatingMarker object, not an ordinary Marker.

[RULE][L3][model_object.Forces.createTorqueVector] The body-side i_marker and the reference-side j_floating_marker must belong to different parts of the same model. Do not place both ends of a TorqueVector on the same rigid body.

[RULE][L3][model_object.Forces.createTorqueVector] If Adams reports that the J marker is not a Floating_Marker, repair the marker type first instead of changing torque magnitude, simulation settings, or unrelated stage code.

## API model_object.Measures.createPoint
[RULE][L4][model_object.Measures.createPoint] Use only measurable characteristics and components that are explicitly supported by the selected API surface.

[RULE][L4][model_object.Measures.createPoint] Characteristic and component must match physically: translational with translational channels, angular with angular channels.

[RULE][L4][model_object.Measures.createPoint] Do not guess unsupported measurable characteristics such as cm_position or undocumented object-level channels unless that exact characteristic is explicitly present in the selected API surface.

[RULE][L4][model_object.Measures.createPoint] When the task requires a directly measurable kinematic quantity, prefer a selected and explicitly supported measure API over reconstructing that quantity early in L4 with undocumented function expressions.

## API model_object.Measures.createObject
[RULE][L4][model_object.Measures.createObject] If Adams reports that a measure defines an unknown characteristic, do not repeat that same characteristic. For revolute-joint angular displacement, prefer createAngle(...) when selected, or use yaw_pitch_roll with an angle component instead of euler_angles.

[RULE][L4][model_object.Measures.createObject] For angular velocity of a rigid body rotating about the revolute marker Z axis in Adams 2025.1.1, use the owning rigid body as object and prefer characteristic='cm_angular_velocity' with component='z_component'. Do not attach angular_velocity to the CM marker object (for example object=sphere.cm), because Adams reports that the marker has no such measurable characteristic.

[RULE][L4][model_object.Measures.createObject] Do not use createObject to measure translational_displacement of a Marker object. For a coupler point, marker point, path, or trajectory, prefer model_object.Measures.createPoint(point=<marker>, characteristic='translational_displacement' or 'cm_position', component='x_component'/'y_component'/'mag_component') when createPoint is selected.

## API model_object.Measures.createPoint
[RULE][L4][model_object.Measures.createPoint] For marker path or coupler point position tasks, use createPoint with the coupler marker as the point argument. Do not use createObject with object=<marker> for marker translational displacement.

## API model_object.Measures.createAngle
[RULE][L4][model_object.Measures.createAngle] For revolute-joint angular displacement, create or reuse one fixed-side reference marker, one joint-center marker, and one moving-side marker, then call createAngle(...). Do not use coincident first/middle/last points.

## API model_object.Simulations.create

[RULE][L5][model_object.Simulations.create] L5 is only for simulation creation, run configuration, and simulate().

[RULE][L5][model_object.Simulations.create] Do not rebuild bodies, joints, markers, or loads in L5.

[RULE][L5][model_object.Simulations.create] Simulation duration and step count must be long enough to make the required physical behavior visibly measurable.

## API m.Analyses.keys
[RULE][L6][m.Analyses.keys] For custom scalar measures created with Measures.createObject(...), scalar object-measure results may be stored under subkeys TIME and Q, where Q is the measured quantity and TIME is only the sampling time vector.

[RULE][L6][m.Analyses.keys] When extracting measurement data from a custom object measure, prefer analysis.results[measure_name]['Q'].values only after confirming that the measure name and key Q both exist.

[RULE][L6][m.Analyses.keys] Never treat analysis.results[measure_name]['TIME'] as the measurement value; use it only for time indexing, interpolation, or nearest-sample lookup.

[RULE][L6][m.Analyses.keys] In analysis.results, TIME is always the time axis; for object measures, do not assume Q is always the target value, because result data may be stored under other subcomponents.

## API Adams.write_binary_file

[RULE][L6][Adams.write_binary_file] Use this API for task-required binary export only when the selected API surface explicitly includes this call.

[RULE][L6][Adams.write_binary_file] When the task explicitly requires a binary export file, use the exact task-required filename in the call shape Adams.write_binary_file('<required_binary_filename>'). 

[RULE][L6][Adams.write_binary_file] If simulation succeeds but a task-required binary export file is missing or stale, repair only L6 export logic and keep earlier stable stages unchanged.
