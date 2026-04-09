# Project Plan for Voice Signal Noise Reduction
<a id="English"></a>

[Chinese](Project_plan_cn_1.1.md#Chinese)

This document records the working plan for the ECE0402 presentation project:
**Designing a Noise Reduction Filter for Voice Signals**.

The project focuses on a **high-frequency additive noise** scenario for voice denoising and follows a **balanced theory + demo** presentation style.

## Project Summary

The overall workflow is organized into three major phases:

1. all members complete literature review and system definition together
2. the work splits into a Testing Group and a PPT Group after the system design is fixed
3. the whole team completes final integration, rehearsal, and Q&A preparation

To keep the presentation focused and explainable, the project scope is intentionally limited to:

- one main noise scenario
- one basic and interpretable filtering direction
- one clear classroom demo
- one set of before-and-after comparison results

## Technical Scope

The system flow is defined as:

`clean voice -> add high-frequency noise -> noisy voice -> filter -> filtered voice`

Current defaults for this version:

- **Noise scenario:** high-frequency additive noise
- **Presentation style:** balanced theory + demo
- **Tooling:** Python + MATLAB
- **Main method:** start from a basic low-pass or band-pass filter, then keep the one that is easier to explain and gives clearer results

### Core Concepts

- Fourier Transform
- frequency-domain interpretation
- filtering
- LTI-system viewpoint
- tradeoff between noise reduction and speech distortion

### Main Questions to Answer

- which part of the signal is voice and which part is noise
- why filtering is a reasonable solution in this scenario
- how the filter is designed
- how much improvement the system achieves
- what the limitations of the method are

## Phase A: Literature Review and System Definition

All members participate in this phase.

### Main Tasks

- collect references on speech frequency characteristics
- collect references on high-frequency noise models
- collect references on basic digital filter design
- collect references on simple voice denoising through filtering
- define the final problem statement
- decide the filter type to present
- decide the system flowchart
- decide which outputs will be shown in class
- unify terminology used in slides and discussion

### Expected Outputs

- final project title
- one clear problem definition paragraph
- one system block diagram
- one chosen filter-design direction
- one reference list for theory support

### Completion Standard

Phase A is complete when:

- the whole team agrees on the same system design
- the PPT Group can start working without waiting for experiment results

## Phase B: Split Execution After System Design Is Fixed

After the system design is fixed, the project splits into two groups.

### Testing Group

Members:

- Xiejz
- Xuzf
- Chenm

### Main Tasks

- prepare clean voice samples
- prepare or generate high-frequency noise samples
- construct noisy voice signals under controlled settings
- implement the filtering pipeline using Python and/or MATLAB
- compare candidate parameters
- select the best version for classroom presentation
- generate result materials:
  - waveform comparison
  - spectrum comparison
  - filtered and unfiltered audio samples
  - short written findings
- summarize limitations and failure cases

### Expected Outputs

- one reproducible denoising pipeline
- one recommended parameter setting
- one 2-minute classroom demo package
- slide-ready figures
- one short explanation of why the chosen filter works

### PPT Group

Members:

- Luowt
- Chenym
- Xiejz

### Main Tasks

- start slide construction immediately after Phase A
- prepare motivation and background slides
- prepare theory slides on:
  - voice signal basics
  - high-frequency noise characteristics
  - frequency-domain analysis
  - filter idea and rationale
- reserve pages for results and demo
- update slides daily based on Testing Group progress
- maintain visual consistency and references
- prepare speaker notes and transition logic

### Expected Outputs

- one complete draft before test results are fully polished
- one final slide deck with integrated charts, results, and references
- one presentation flow that matches the demo

## Phase C: Final Integration and Rehearsal

All members participate in this phase.

### Main Tasks

- verify that the theory pages match the implemented system
- verify that figures and spoken explanation use consistent terminology
- remove unnecessary technical detail
- finalize the in-class demo sequence
- assign speaking parts
- practice Q&A
- submit slides at least three days before presentation day

### Expected Outputs

- final slide deck
- final demo package
- final references
- final contribution record
- rehearsal-adjusted presentation version

## Collaboration Rules

- the project follows a high-level serial workflow:
  - first: joint literature review and system design
  - second: split into Testing Group and PPT Group
  - third: final integration and rehearsal
- during the split-work phase, the Testing Group must sync with the PPT Group once every day
- each daily sync should include:
  - current progress
  - latest figures or audio outputs
  - design changes
  - findings that affect slide wording
- the PPT Group should begin theory and structure slides immediately after Phase A
- final claims in slides must be supported by references or actual test results


## Test Plan and Acceptance Criteria

### Required Test Items

- clean voice sample
- noisy voice sample with high-frequency noise
- filtered voice sample
- waveform comparison before and after filtering
- frequency-spectrum comparison before and after filtering
- one short classroom demo audio

### Acceptance Criteria

The project is ready for presentation when:

- the denoising pipeline runs end-to-end
- at least one waveform comparison clearly shows the improvement
- at least one spectrum comparison clearly shows the improvement
- the audio demo is understandable in under 2 minutes
- the chosen filter can be explained with course concepts
- the slides match the actual implemented system
- each member's contribution can be stated clearly

## Notes

- the default scenario remains high-frequency noise unless later testing shows it does not produce a stable demo
- Python and MATLAB may both be used, but the final presentation must show one coherent system
- the filtering method should remain basic and interpretable unless a stronger method becomes necessary
