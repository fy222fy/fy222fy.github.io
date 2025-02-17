---
layout: post
title: 大模型微调技术梳理
date: 2024-05-01 00:32:13
description: this is what included tabs in a post could look like
tags: llm
categories: ai
tabs: true
thumbnail: assets/img/9.jpg
---

# 背景知识
**FineTune（微调）**
大模型微调技术是指在**已经预训练好**的大型语言模型基础上，使用特定的数据集进行**进一步**的训练，以使模型适应**特定任务**或领域。这种方式有如下的优势：

1. 微调后的模型仍具备原有大模型的特征；
2. 仅需要少量数据集就可以达到不错的效果，免去了重新训练模型；
3. 训练成本低。

大模型微调技术主要分为如下两类：

1. 全量微调（Full Fine-Tuning，FFT）：即**全部参数**都微调，但对于大模型来说，参数量巨大导致全量微调需要消耗大量算力，实用性不高，此外，全量微调会造成灾难性遗忘，会在把某领域方面表现变好的同时，把原来表现好的其他领域的能力变差；
2. 高效微调（Parameter-Efficient Fine-Tuning，PEFT）：针对**部分参数**进行训练和调整，解决了全量微调的缺陷，使大模型在某个领域的能力提升。

本篇主要介绍高效微调，包括如下几种：

1. **Freeze Tuning**
2. **Adapter Tuning**
3. **Prompt Tuning**
4. **P-Tuning**
5. **Prefix-Tuning**
6. **P-Tuning V2**
7. **LoRa Tuning**


# Freeze Tuning

Freeze参数冻结，对大模型的大部分参数进行冻结，仅训练少部分参数，以此来减少显存占用，完成微调。


# Adapter Tuning
[《Parameter-Efficient Transfer Learning for NLP》](https://arxiv.org/pdf/1902.00751.pdf)
2019 论文指出，Freeze Tuning难以达到较好的效果。

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/1.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>


[//]: # (![image.png]&#40;./2024-04-05-llm-fintune-img/1.png&#41;)

Adapter Tuning主要是在Transformer模块中增加了一个适配层。

子层1：将Transformer块的输出作为输入，将原始维度d投影到m维度，m的大小决定了Adapter模块的参数量，m<<d。

子层2：在输出时，通过第二个子层还原输入维度，将m投影到d。

优点：

主要解决了灾难性遗忘，任务之间的干扰和训练不稳定的问题。

# Prompt Tuning

Prompt：提示词，用于引导模型生成文本的一段输入，帮助模型更好理解用户意图，这种输入可以是明确的单词（Hard Prompt，离散Prompt），也可以是一个一个向量（Soft Prompt，连续Prompt）。

- Prompt Engineering：通过人工开发和优化Prompt，帮助语言模型用于各个应用场景和领域。
- Prompt Tuning：通过AI优化Prompt，达到最好的Prompt效果，适配各个场景。


## 背景

大模型本身具备很强的推理和理解能力，
GPT3在[《Language Models are Few-Shot Learners》](https://arxiv.org/abs/2005.14165)提出in-context learning概念，
无需修改模型，通过few-shot/zero-shot/demonstrate-learning，让模型知道和标签相似的语义，提升推理能力。
在真实场景中，例如在GPT3不那么大的模型中，Prommpt直接用在zero-shot上效果下降，且对于一些具体的任务场景，需要单独设计组件实现。
于是出现了PET（Pattern-Exploiting Training）模型
[《Exploiting Cloze Questions for Few Shot Text Classification and Natural Language Inference》](https://arxiv.org/pdf/2001.07676)。

以NLI（预测两句话之间的关系）为例：

[//]: # (![image.png]&#40;https://i-blog.csdnimg.cn/blog_migrate/4d2a59becf8b513bdd678b3dd77a322a.png&#41;)

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/2.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

## 基本原理
Prompt-Tuning的主要组件称为Pattern-Verbalizer-Pair。

- Pattern：带[mask]标记的短文本，是希望模型预测的标记，可以是任何词。
- PLM：预训练的模型。
- Verbalizer：标签词映射，对于具体分类任务，选择指定的标签词。

[//]: # (![image.png]&#40;https://i-blog.csdnimg.cn/blog_migrate/59c0006aa0a58cda2620565e9759badd.png&#41;)

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/3.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

为达到更好的效果，可以有多种方法：

- Patterns Ensembling：为一个句子设计不同的Pattern；
- Verbalizers Ensembling：标签词可以有多个，例如great、nice都可以是积极的；
- PVPs Ensembling：多个PVP组件，采用加权、投票等形式获得结果。

[//]: # (![image.png]&#40;https://i-blog.csdnimg.cn/blog_migrate/5bbcd8d261a5d89cd39800152d2b0b03.png&#41;)

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/4.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

基于PVP框架，Prompt Tuning的重点就在于如何选择和构造合适的Pattern和Verbalizer。
### 微调模板
最简单的方式就是人工设计模板，但自动化的方式更好。
离散模板构建法（Hard Template 、 Hard Prompt 、 Discrete Template 、 Discrete Prompt），在训练过程中保持不变，且是离散的词向量。包括：

- 人工构建（Manual Template） ：在前文已经描述过，不再详细说明；
- 启发式法（Heuristic-based Template） ：通过规则、启发式搜索等方法构建合适的模板；
- 生成（Generation） ：根据给定的任务训练数据（通常是小样本场景），生成出合适的模板；

连续模板构建（Soft Template 、 Soft Prompt 、 Continuous Template 、 Continuous Prompt），在连续的向量空间寻找合适的标记，解决离散模版容易陷入局部最优的问题。

- 词向量微调（Word Embedding） ：显式地定义离散字符的模板，但在训练时这些模板字符的词向量参与梯度下降，初始定义的离散字符用于作为向量的初始化；
- 伪标记（Pseudo Token） ：不显式地定义离散的模板，而是将模板作为可训练的参数；

[//]: # (- ![image.png]&#40;https://i-blog.csdnimg.cn/blog_migrate/29e3dab4d67b5baa6c4ca021aa7b91ec.png&#41;)

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/5.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

#### 启发式构建模板
采用规则、正则化的模板构建出Pattern，或用启发式的搜索算法获得Pattern。
例如，可以利用启发式的规则定义若干个子模板，自动组合形成最终Pattern。
例如，[AutoPrompt](https://arxiv.org/pdf/2010.15980.pdf)给定原始的输入，额外定义若干离散的字符作为trigger，
并组成Template，喂入MLM中预测对应label word的概率。而这些trigger最终通过梯度搜索的方法进行挑选。

[//]: # (![image.png]&#40;https://i-blog.csdnimg.cn/blog_migrate/7b8c61a9af964ca255b6edf3d01349d1.png&#41;)

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/6.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

#### 生成法构建
直接让模型来生成合适的模板。
首先定义一个Template的母版，将这些母版与原始文本拼接后喂入T5模型（T5模型属于自回归式的生成模型）后在<X>和<Y>占位符部分生成相应的字符，
最终形成对应的Template。然后再基于生成的Template和label word进行训练。

![image.png](https://i-blog.csdnimg.cn/blog_migrate/de969f0730c54b7e302caf54078b035d.png)

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/7.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

#### 连续提示模板
不论是启发式方法，还是通过生成的方法，都需要为每一个任务单独设计对应的模板，因为这些模板都是可读的离散的token（这类模板我们称作Discrete Prompt或Hard Prompt），
这导致很难寻找到最佳的模板。
另外，即便是同一个任务，不同的句子也会有其所谓最佳的模板，而且有时候，即便是人类理解的相似的模板，也会对模型预测结果产生很大差异。
为避免这种问题，将模板转换为可进行优化的连续向量，不同的任务、数据可以自适应地在语义空间中寻找若干合适的向量，来代表模板中的每一个词，
相较于显式的token，这类token称为 **伪标记（Pseudo Token）**。

代表的几种方法有：

- [《The Power of Scale for Parameter-Efficient Prompt Tuning》](https://arxiv.org/pdf/2104.08691.pdf?trk=public_post_comment-text)2021：代表方法为Prompt Tuning
- [《GPT Understands, Too》](https://arxiv.org/abs/2103.10385)2021：P-tuning
- [《P-Tuning v2: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks》](https://arxiv.org/pdf/2110.07602.pdf)2021
- [《PPT: Pre-trained Prompt Tuning for Few-shot Learning》](https://arxiv.org/pdf/2109.04332.pdf)2021：代表方法PPT
- [《Prefix-Tuning: Optimizing Continuous Prompts for Generation》](https://arxiv.org/pdf/2101.00190.pdf%EF%BC%89)2021


### 微调Verbalizer

Verbalizer也会影响预测的结果，和模板类似，Verbalizer也分为离散和连续两种类型。

- 人工设计：根据对每个任务的经验来人工指定这些label word。但是人工设计需要依赖大量的人力；
- 领域知识指导搜索离散的label word，代表方法为KPT，[《Knowledgeable Prompt-tuning:Incorporating Knowledge into Prompt Verbalizer for Text Classification》](https://arxiv.org/pdf/2108.02035.pdf)；
- 原型网络动态生成label representations：[《Prototypical Verbalizer for Prompt-based Few-shot Tuning》](https://arxiv.org/pdf/2203.09770.pdf)，代表方法为ProtoVerb

## Prompt Tuning
这里说的是[《The Power of Scale for Parameter-Efficient Prompt Tuning》](https://arxiv.org/pdf/2104.08691.pdf?trk=public_post_comment-text)
里的Prompt Tuning。其实是Prefix Tuning的一个简化版本。
基本概念：给每个任务定义prompt tokens，只在输入层加入这些tokens（训练的就是这些tokens）。

[//]: # (![image.png]&#40;https://i-blog.csdnimg.cn/blog_migrate/58202278e30880bdfff28b2d6298719a.png&#41;)


<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/8.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

Prompts提出了Prompt Ensembling，在一个批次里面可以同时训练一个任务的不同prompt（采用多种不同方式询问同一个问题），提升了效率。

## P-Tuning

[《GPT Understands, Too》](https://arxiv.org/abs/2103.10385)
P-Tuning用MLP + LSTM（长短期记忆网络）的方式对Prompt Embedding进行一层处理，其虚拟token可以插入到除了前缀的任意位置。

[//]: # (![image.png]&#40;https://i-blog.csdnimg.cn/blog_migrate/f8028ab8ecc68dfed8a47939f55b4f86.png&#41;)

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/9.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>


在训练过程中，PML模型的参数全部固定，微调的事Prompt Encoder，也就是LSTM的参数，这个参数是所有任务共享的。
预测过程中不需要这个组件，针对特定任务，LSTM输出独一无二的虚拟token embedding，插入到输入token中即可。

## Prefix Tuning
[《Prefix-Tuning: Optimizing Continuous Prompts for Generation》](https://arxiv.org/pdf/2101.00190)
基本概念：固定训练的LM，添加任务特定的，可训练的前缀（训练的是这个embedding的前缀）。

[//]: # (![image.png]&#40;https://i-blog.csdnimg.cn/blog_migrate/71cbf8e0601d31d068838190a1de03bd.png&#41;)

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/10.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>


具体原理：
在输入token之前构造一段任务相关的virtual tokens作为Prefix，然后训练的时候只更新Prefix部分的参数，而PLM中的其他部分参数固定。
针对不同的模型结构，需要构造不同的Prefix。

- 针对自回归架构模型：在句子前面添加前缀，得到 z = [PREFIX; x; y]，合适的上文能够在固定 LM 的情况下去引导生成下文（比如：GPT3的上下文学习）。
- 针对编码器-解码器架构模型：Encoder和Decoder都增加了前缀，得到 z = [PREFIX; x; PREFIX0; y]。
- Encoder端增加前缀是为了引导输入部分的编码，Decoder 端增加前缀是为了引导后续token的生成。

[//]: # (![image.png]&#40;https://i-blog.csdnimg.cn/blog_migrate/8bb99ac2718d47f23e27db13612ec879.png&#41;)

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/11.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

为了达到更好的效果：

1. Deep Continuous Prompt：一般做法是在embedding层加入可训练的virtual token，但实际上可以在每一层都加入可训练的prefix。
2. 套MLP：因为直接优化可能导致不稳定和性能下降，所以在训练的过程中增加MLP映射矩阵。

[//]: # (![image.png]&#40;https://i-blog.csdnimg.cn/blog_migrate/1b3706c093af69739f8f6edc6ff099b5.png&#41;12)

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/12.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>


## P-Tuning V2
[《P-Tuning v2: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks》](https://arxiv.org/pdf/2110.07602.pdf)2021
背景：

从原理上，P-Tuning V2和Prefix Tuning是一样的，只不过Prefix Tuning针对NLG（自然语言生成）任务，
而P-Tuning v2进行了改进，可以用于NLU（自然语言理解）任务，如语义识别，情感分析等。

[//]: # (![image.png]&#40;https://i-blog.csdnimg.cn/blog_migrate/f16a0e24c5b3b1197a5dc70ae8c1621b.png&#41;)

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/posts/2024-04-05-llm-fintune-img/13.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

# LoRA Tuning

[《LORA: LOW-RANK ADAPTATION OF LARGE LANGUAGE MODELS》](https://arxiv.org/pdf/2106.09685.pdf)

LoRa（Low-Rank Adaptation）基于一个假设：现有大模型的参数量是过度的，其背后有一批生成关键结果的参数，被称作低维本质模型。

## 原理

全量微调：

图左是全量微调的模型，表示预训练模型的权重矩阵，在反向传播的过程中，更新一个，更新后的权重矩阵为，如果模型有6B个参数，则也有6B个参数，非常消耗资源。

Lora微调：

图右是Lora微调，Lora将分解为两个低秩的矩阵，的行数和相同，的列数和相同，另外一个维度的长度是一个超参数，那么。微调时只需要训练A和B即可，因为的值很小（如4，8，16），所以资源消耗很少。

原理：

在Lora微调过程中，权重固定不变，控制矩阵为随机初始化矩阵，矩阵为0矩阵。
在前向过程中，初始权重和旁路矩阵都会作用于输入：
反向传播过程中，更新矩阵。
预测时同理。

## 优点

1. 节省资源：秩 r 是一个超参数。例如，如果 ΔW 有 10,000 行和 20,000 列，则需存储 200,000,000 个参数。如果我们选择 r=8 的 A 和 B，则 A 有 10,000 行和 8 列，B 有 8 行和 20,000 列，即 10,000×8 + 8×20,000 = 240,000 个参数，比 200,000,000 个参数少约 830 倍。
2. 预测性能损耗低
3. 便于切换场景：每个场景对应于一个矩阵，切换场景进需要做矩阵加减法即可：
4. 效果好


## 开源实现
目前 LORA 已经被 HuggingFace 集成在了 [PEFT（Parameter-Efficient Fine-Tuning）](https://link.zhihu.com/?target=https%3A//github.com/huggingface/peft) 代码库里。


