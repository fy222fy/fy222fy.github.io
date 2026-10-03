---
page_id: about
layout: home
title: About
permalink: /
photo: prof_pic.jpg # file in assets/img/
# The self-description below: the first two paragraphs appear under the name, the rest in the "About me" section.
# The rest of the home page lives in _data/en-us/home.yml and _data/en-us/projects.yml.
---

I am a Ph.D. student in the School of Cyberspace Security at Beijing University of Posts and Telecommunications.
My main research interests include **AI for security**, **formal analysis** and **privacy computing**.

Currently, I am researching how large models can be applied to formal analysis,
and how formal analysis can be used to study the security of interactions among groups of AI agents.
I welcome discussions on related topics.

During my undergraduate and master’s studies, I focused on the formal analysis of security protocols,
mainly verifying the FIDO UAF authentication protocol with formal methods.
I proposed a formal modeling method for inter-process communication and a method for identifying the minimal security assumptions of a protocol.
I developed and open-sourced an automated analysis tool,
published papers at **NDSS 2021** and **IEEE TDSC 2023**,
and reported a medium-risk vulnerability to CNNVD.
I also found a bug in the ProVerif formal analysis tool and contributed to its fix.

From 2021 to 2024, I worked as a cybersecurity engineer at Ant Group,
on confidential computing for large models, federated learning, secure multi-party computation (MPC) and trusted execution environments (TEE).

Confidential computing for large models: in 2024, Ant Group launched the SecretFlow Cloud confidential computing platform for large models,
which combines software and hardware trusted privacy-computing technologies to keep data encrypted while models are hosted and run.
I worked on confidential LLM inference in TEEs,
and proposed a federated-learning scheme for privacy-preserving joint fine-tuning and inference across institutions.

Federated learning: I built an automated attack-and-defense framework for federated learning and open-sourced it in SecretFlow.
Given a set of attack and defense algorithms, the framework automatically searches their hyperparameters to find the best practices.
It also implements mainstream machine-learning models and state-of-the-art attack and defense algorithms,
producing benchmarks across models and attack-defense scenarios.

MPC and TEE: I was a core developer of the Trusted-Environment-based Cryptographic Computing system (TECC)
and did nearly half of its work, from algorithms and engineering to production deployment and operations,
including obtaining its software copyright and its evaluation certificate from the China Academy of Information and Communications Technology (CAICT).
By combining multiple heterogeneous TEEs with MPC running within the same network,
TECC is more secure than a single TEE and faster than conventional MPC.
Ant Group released it in 2022, and it was selected as one of the “Top Ten Hardcore Technologies” at the 5th Digital China Summit.
