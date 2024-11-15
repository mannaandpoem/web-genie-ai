# WebGenieAI Subnet

Welcome to WebGenieAI Subnet, a pioneering Bittensor-based subnet designed to revolutionize project generation through advanced AI models. WebGenieAI aims to transform diverse prompts—ranging from text and voice to images and Figma designs—into fully functional, ready-to-deploy projects. This subnet is tailored for developers, designers, and innovators who seek to accelerate their project development process with high-quality, AI-generated outputs.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Incentive Mechanism](#incentive-mechanism)
- [Roadmap](#roadmap)

## Overview

WebGenieAI Subnet leverages state-of-the-art AI models to interpret and convert various types of prompts into complete, deployable projects. Whether you're starting with a simple HTML/CSS framework or aiming to develop a complex React application, WebGenieAI can generate the entire codebase, ensuring it meets your specified requirements and is ready for immediate deployment.

### Vision

WebGenieAI envisions a future where project creation is seamless, automated, and efficient, empowering developers to focus more on innovation and less on repetitive coding tasks. By harnessing the capabilities of the Bittensor network, WebGenieAI fosters a competitive environment that drives continuous improvement in AI-generated outputs.

### Purpose

The primary purpose of WebGenieAI is to:

- Automate Project Generation: Provide a platform that can autonomously generate high-quality projects from diverse input prompts.
- Enhance Productivity: Reduce the time and effort required for project development, enabling developers to quickly bring their ideas to life.
- Promote Innovation: Encourage innovative solutions and optimizations in project generation through competitive incentivization.

## Features

- **Text Prompt**: Generate projects by describing them in text.
- **Voice Prompt**: Create projects by giving voice commands.
- **Image Prompt**: Upload an image of a website or app, and WebGenieAI will generate a pixel-perfect project.
- **Figma Prompt**: Convert Figma designs into functional projects.
- **Automated Downloads**: Directly download the generated projects as complete folders.

## Incentive Mechanism v1

The WebGenieAI subnet incentivizes miners and validators to ensure high-quality outputs. Here’s how it works specifically for this subnet:

- Task Assignment: Subnet miners are assigned tasks related to generating and improving machine learning models based on various prompts (text and image).
- Performance Evaluation: Validators evaluate the outputs produced by miners. The evaluation criteria include accuracy, efficiency, and innovation.
- Ranking and Rewarding: Validators rank the miners according to their performance. The Bittensor blockchain’s Yuma Consensus mechanism determines the TAO rewards distribution based on these rankings.

## Evaluation Process

### Automatic evaluation of ImageToHTML task for design-wise
We automatically evaluate generated webpages by calculating the similarity between the original input image and the rendered screenshot of generated webpage.
We break down the evaluation into both high-level visual similarity and low-level element matching.

#### High-level Visual Similarity

To evaluate the visual similarity of IR and IG, we use the similarity of their CLIP embedding, denoted as CLIP(IR, IG). Specifically, we extract features by CLIP-ViT-B/32 after resizing screenshots to squares. 
To rule out the texts in the screenshots, we use the inpainting algorithm from [Telea](https://docs.opencv.org/4.3.0/df/d3d/tutorial_py_inpainting.html) to mask all detected text boxes using their bounding box coordinates.

#### Low-level Element Matching

Metrics like CLIP similarity only capture the similarity of the overall images rather than the matching of all the details like text. Moreover, the metric itself does not offer any fine-grained breakdown to help diagnose model weaknesses. 

To complement that, we introduce a suite of element-matching metrics. Specifically, we consider whether the generated webpages manage to recall all visual elements, and whether the corresponding visual elements in the input image and generated webpages have aligned text content, position, and color.

Given a reference webpage screenshot $I_R$ and a generated webpage screenshot $I_G$, we use a text detection module to output a set of detected visual element blocks for each: R = {$r_1$, $r_2$, ..., $r_m$} and G = {$g_1$, $g_2$, ..., $g_n$}, where each block contains its textual content and bounding box coordinates.

Based on the two sets of detected blocks, we use the Jonker-Volgenant algorithm to get the optimal matching M between R and G based on text similarity, where (p, q) ∈ M indicates $r_p$ is matched with $g_q$.

Given R, G, and matched pairs in M, we evaluate similarity along the following aspects:
- **Block-Match**: The first desideratum of the task is that all visual elements from the image should be reproduced in the generated webpage, and the generated webpage should not hallucinate non-existent new elements. We measure this by computing the total sizes of all matched blocks divided by the total sizes of all blocks, including unmatched ones (either because the generated webpages missed them or because the generated webpages contain hallucinated blocks):

$$
\mathbf{match}_{\text{block}}(r_p, g_q) = \frac{S(r_p) + S(g_q)}{\sum_{(i,j) \in M} (S(r_i) + S(g_j)) + \left(\sum_{i \in U_R} S(r_i) + \sum_{j \in U_G} S(g_j)\right)}
$$

$$
\mathbf{match}_{\text{block}}(R, G) = \sum_{(p,q) \in M} \mathbf{match}_{\text{block}}(r_p, g_q)
$$

where S(·) returns the size of the blocks, $U_R$ and $U_G$ denotes the unmatched blocks in R
and G. The intuition here is that unmatched blocks will lower the score as they indicate
missing original blocks or generating hallucinated blocks, and the larger the unmatched
blocks are, the lower this score is.

- **Text**: Given two strings from two matched blocks $r_p$ and $g_q$, the text similarity **sim**<sub>text</sub>($r_p$, $g_q$) is calculated as twice the number of overlapping characters divided by the total number of characters in the two strings (character-level Sørensen-Dice similarity). The overall score is averaged across all matched pairs.

- Position: The positioning of the blocks largely impacts the overall layout. For each matched pair (p, q), we calculate the position similarity **sim**<sub>pos</sub>($r_p$, $g_q$) = 1 − max(abs($x_q$ − $x_p$), abs($y_q$ − $y_p$)), where ($x_p$, $y_p$) and ($x_q$, $y_q$) are normalized coordinates (in [0, 1]) of $r_p$ and $g_q$’s centors. The overall score is averaged across all matched pairs.

- Color: We use the [CIEDE2000](https://en.wikipedia.org/wiki/Color_difference) color difference formula to assess the perceptual difference between the colors of the generated text in block $g_q$ and the reference text in block $r_p$, denoted as **sim**<sub>color</sub>(rp, gq), where the formula considers the complexities of human color vision. The overall score is averaged across all matched pairs.


### Example Scenario

- Prompt: A miner receives a prompt to create a front-end focus application.
- Generation: The miner generates the code for the application and submits it.
- Evaluation: Validators review the submission:
  - Accuracy: Does the application have all the features mentioned in the prompt?
  - Efficiency: Is the code optimized for performance?
  - Innovation: Does the application include any additional features or optimizations not explicitly requested but beneficial?
- Ranking: Validators rank this submission against others.
- Rewarding: Based on the ranking, the miner receives TAO rewards.

## Roadmap

### Phase 1: Foundation (Q4 2024)
- [x] Launch on testnet (214)
- [] Launch front-end application v1 (webgenieai.co)
    - Enable Text & image inputs
- [] Incentive mechanism v1
    - Generate pure HTML/CSS web pages from text & image based prompts
- [] Begin marketing for brand awareness and interest
- [] Launch on mainnet

### Phase 2: Upgrade (Q1 2025)
- [] Build dashboard to track miner performance and progress
- [] Upgrade front-end application to v2
    - Enable figma design inputs
- [] Upgrade incentive mechanism to v2
    - Generate full framework based on React, Vue, and Next.js projects from text, image, and figma prompts

### Phase 3: Expand (Q2 2025)
- [] Add features to monetize the application
   - Add payment gateways
   - Automate the downloading of fully functional projects
- [] Market and B2B sales expansion
- [] Grow the team