---
title: "World Model for Dexterous Manipulation"
date: 2026-01-02
draft: True 
---


# Model Predictive Control(MPC)
## Deep Dynamics Models for Learning Dexterous Manipulation
### TLDR
Online Collect data and learn, just like PPO, but learn dynamic model using surpervised learning instead of using reward signal to optimize a policy. 
### Limitation
not good for long horizon, dense reward preferred
### Utility
since the paradigm of demo replay is always short horizon, so a dynamic model may be easily trained?
- how to solve the object geometry problem
    - do not use image, image can not support planning
    - we can use the together learned RL policy to avoid blind sampling at the first stage
    - but one env need sample many traj for planning
    - how to integerate object geometry? a universal encoder?
    - Most importantly, no evidence or justified belief that it will work better than PPO. It may work just as good as PPO at the same training  cost, or even worse. 
    - but still exhibit a high coherence with demo replay paradigm!
    - maybe better, as the interplotation of the state transition is similar to the edtiion mechanism.
    - worth tring, it not work. 
    - by combine them together, may help each other learn. 

## Contact-Implicit Model Predictive Control for Dexterous In-hand Manipulation: A Long-Horizon and Robust Approach
### TLDR
High level MPC(differentiable), add tactile compensation. Online Planning.
### Limitation
Never can conduct real world experiment
### Utility
baseline? guidance in simulator? Not that good, it need too much previlieged information and is somehow time-consuming and unable to batchfied. 

# World Model
## DreamerV2: MASTERING ATARI WITH DISCRETE WORLD MODELS 
### TLDR
Use a sequential VAE as a world model, and train RL in latent space
### Limitation
Atari的环境比较简单，对于更复杂的环境、物理、图像，可能预测的没有那么准
### Utility
如果可以给demoreplay学到一个非常好的world model，比如说在隐空间里，那完全省去了中间的时间，这会很重要

## World Models Can Leverage Human Videos for Dexterous Manipulation
### TLDR
世界状态 = image + 手关键点
action = camera移动 + 手关键点移动