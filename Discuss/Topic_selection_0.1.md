# Candidate Topics for ECE0402 Presentation
<a id="English"></a>

[Chinese](Topic_selection_cn_0.1.md#Chinese)

This document summarizes three candidate topics for our ECE0402 course presentation project. Each topic is closely related to core ideas in Signals, Systems & Probability, while also connecting to real-world applications.

The purpose of this note is to compare possible directions before the final topic is selected.

## 1. Aliasing in Audio Signals and How to Prevent It

### Background

Sound in the real world is a continuous-time signal, but digital devices such as phones, computers, and audio recorders process sound as discrete-time samples. In order to convert a continuous signal into a digital one, the signal must be sampled at a certain sampling rate.

If the sampling rate is too low, different frequency components may become indistinguishable after sampling. This creates distortion in the reconstructed signal and introduces frequency components that were not perceived correctly in the original signal. This phenomenon is called aliasing.

Aliasing is an important issue in real audio systems because it directly affects sound quality. To reduce this problem, practical systems often use anti-aliasing filters before sampling.

### Main Question

How does aliasing happen in digital audio, and why can filtering help prevent it?

### Core Concepts Involved

- sampling
- aliasing
- Fourier transform
- spectrum replication after sampling
- low-pass filtering
- reconstruction of sampled signals

### What the Presentation Can Cover

This topic can be presented in a focused and structured way:

- explain the difference between continuous-time and discrete-time signals
- introduce the idea of sampling rate
- show what happens when the sampling rate is high enough
- show what happens when the sampling rate is too low
- explain aliasing from a frequency-domain perspective
- discuss the Nyquist idea in an intuitive way
- explain why an anti-aliasing low-pass filter is used before sampling
- connect the theory to real digital audio devices

### Possible Demo

A simple and effective demo could include:

- the same audio signal sampled at different sampling rates
- waveform comparison before and after poor sampling
- spectrum plots showing overlapping frequency components
- a short comparison between audio with and without anti-aliasing protection

### Strengths

- very closely related to textbook content
- easy to connect theory and practice
- demo is visual and easy to understand
- good for explaining both time-domain and frequency-domain ideas

### Possible Risks

- if the presentation is too theoretical, it may feel less real-world than the other topics
- if not presented carefully, it may become too similar to a standard lecture explanation

## 2. How Noise-Canceling Headphones Work

### Background

Noise-canceling headphones are a common real-world example of signal processing. Their goal is to reduce unwanted environmental noise, especially in places such as airplanes, trains, or busy public spaces.

In active noise cancellation, microphones first capture the surrounding noise. The system then generates another signal designed to cancel part of that noise when it reaches the listener's ear. The basic intuition is that if two signals have similar amplitude but opposite phase, they can partially cancel each other when added together.

Although real commercial systems are more complicated, the core idea can still be explained clearly using basic concepts from signals and systems.

### Main Question

How can a signal processing system reduce environmental noise, and why is active noise cancellation more effective for some sounds than others?

### Core Concepts Involved

- superposition
- phase and signal cancellation
- LTI systems
- filtering
- delay and system response
- practical limitations of real systems

### What the Presentation Can Cover

This topic can be developed through the following structure:

- introduce the real-life problem of unwanted noise
- explain the difference between passive noise isolation and active noise cancellation
- show the role of microphones, signal processing, and speaker output
- explain the idea of inverse-phase cancellation in a simple way
- discuss why timing and delay matter
- explain why low-frequency noise is usually easier to reduce than high-frequency noise
- briefly connect this to real consumer devices

### Possible Demo

A strong demo could include:

- two sinusoidal signals with opposite phase added together
- simple visualization of destructive interference
- a short audio comparison before and after simplified cancellation
- a comparison showing why cancellation becomes harder when delay is present

### Strengths

- highly relatable and interesting to the audience
- strong real-world application
- easy to make visually appealing and intuitive
- good balance between engineering application and course concepts

### Possible Risks

- if the presentation goes too far into product design details, it may drift away from signals and systems
- some practical implementations are complex, so the topic should stay focused on the basic principle

## 3. Echo and Reverberation: Modeling with Convolution

### Background

When sound is produced in a room, it does not only travel directly from the source to the listener. It also reflects from walls, ceilings, floors, and other surfaces. These reflected copies of the original signal arrive at different times and with different amplitudes.

If the reflections are clearly separated, we may hear echo. If many reflections blend together more densely, we perceive reverberation. This makes rooms sound different from one another.

From the viewpoint of signals and systems, a room can be modeled as a system, and the room's effect on sound can be described through its impulse response. The output sound is the convolution of the input signal with the system's impulse response.

### Main Question

How can echo and reverberation be modeled as the output of an LTI system, and why does convolution explain the sound of different spaces?

### Core Concepts Involved

- convolution
- impulse response
- LTI systems
- system modeling
- delayed and scaled copies of a signal
- interpretation of output signals in time domain

### What the Presentation Can Cover

A clear presentation can include:

- introduce the real-world phenomenon of echo and reverberation
- explain direct sound and reflected sound
- show how reflections can be modeled as delayed and scaled copies
- connect this idea to system response
- introduce the concept of impulse response
- explain why convolution gives the output of the system
- show how different impulse responses produce different acoustic effects
- connect the topic to music production, room acoustics, and audio effects

### Possible Demo

This topic supports a very intuitive demo:

- play a dry audio clip and then a reverberated version
- show a simple impulse response made of delayed spikes
- visualize how one input signal becomes multiple delayed copies
- compare the effects of a small room and a large hall through different impulse responses

### Strengths

- one of the best topics for showing convolution in a meaningful way
- very well connected to LTI systems and impulse response
- demo is clear and memorable
- elegant balance between theory and application

### Possible Risks

- if presented too abstractly, some classmates may find it less immediately familiar than headphones or music recognition
- the explanation of convolution needs to be made intuitive, not overly mathematical

## Initial Comparison

Among these three topics, each one has a different strength:

- **Aliasing in Audio Signals** is the most textbook-aligned and theoretically clean.
- **Noise-Canceling Headphones** is the most relatable and audience-friendly.
- **Echo and Reverberation** is the strongest for explaining convolution in a real and intuitive setting.

## Recommendation

If the goal is to choose the topic with the best overall balance between concept clarity, real-world relevance, and demo quality, the strongest candidates are:

1. **How Noise-Canceling Headphones Work**
2. **Echo and Reverberation: Modeling with Convolution**
3. **Aliasing in Audio Signals and How to Prevent It**

