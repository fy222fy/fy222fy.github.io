---
page_id: about
layout: about
title: about
permalink: /
subtitle: Ph.D. Student, <a href='https://scss.bupt.edu.cn/'>School of Cyberspace Security</a>, <a href='https://www.bupt.edu.cn/'>Beijing University of Posts and Telecommunications</a>

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p>Beijing, China</p>
    <p>fenghaonan222@gmail.com</p>
news: true # includes a list of news items
latest_posts: false # includes a list of the newest posts
selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page
---

I am a Ph.D. student in the School of Cyberspace Security at Beijing University of Posts and Telecommunications (BUPT).
My research interests include **AI security**, **formal analysis**, and **privacy-preserving computation**.

Currently, I am exploring how large language models can be applied to formal analysis,
and how formal analysis techniques can be used to study the security of interactions among groups of AI agents.
I am always happy to discuss related topics — feel free to reach out.

#### Formal analysis of security protocols

During my undergraduate and master's studies, I focused on the formal analysis of security protocols,
mainly the formal verification of the FIDO UAF authentication protocol.

- Proposed a formal modeling method for inter-process communication and a method to identify the minimal security assumptions of a protocol.
- Developed and open-sourced an automated analysis tool, [UAFVerif](https://github.com/CactiLab/UAFVerif).
- Published papers at **NDSS 2021** and **IEEE TDSC**, filed two patents, and reported a medium-risk vulnerability to CNNVD.
- Found a bug in the ProVerif formal verification tool and contributed to its fix.

#### Industry experience at Ant Group (2021 – 2024)

I worked as a cybersecurity engineer at Ant Group on confidential LLMs, federated learning, secure multi-party computation (MPC), and trusted execution environments (TEE).

- **Confidential LLM computing.** In 2024 Ant Group launched the SecretFlow Cloud confidential computing platform for large models,
  which combines software and hardware trusted privacy-computing technologies to keep data encrypted during model hosting and inference.
  I worked on confidential LLM inference inside TEEs, built a confidential knowledge-graph platform,
  and designed a federated-learning-based scheme for privacy-preserving joint fine-tuning and inference across institutions.
- **Federated learning.** I built an automated attack-and-defense framework for federated learning, open-sourced in [SecretFlow](https://github.com/secretflow/secretflow).
  Given a set of attack and defense algorithms, it automatically searches hyperparameters to find the best practices,
  and ships mainstream models and state-of-the-art attack/defense algorithms, producing benchmarks across models and scenarios.
- **MPC & TEE.** In 2022 Ant Group released the Trusted-Environment-based Cryptographic Computing system (TECC),
  selected as one of the "Top Ten Hardcore Technologies" at the 5th Digital China Summit.
  TECC combines multiple heterogeneous TEEs with MPC to be more secure than a single TEE and faster than conventional MPC.
  I worked on MPC operators, product development, SGX and HyperEnclave adaptation, and cloud deployment,
  and obtained one software copyright and an evaluation certificate from the China Academy of Information and Communications Technology (CAICT).
