Book Chapter Title

1\. Introduction to 3D In Vitro Models: Historical Perspectives and
Current Trends

[2. Biomaterials for 3D In Vitro Models]{.mark}

[3. 3D Printing Techniques and Biofabrication Strategies for Tissue
Engineering]{.mark}

4\. Microfluidics and Organ-on-a-Chip Technologies for 3D In Vitro
Systems

5\. 3D In Vitro Models for Cancer Research and Drug Screening

6\. Stem Cell-Based 3D In Vitro Models for Regenerative Medicine

7\. 3D In Vitro Models in Cardiovascular Research

8\. Applications of 3D In Vitro Models in Neurological Disorders

9\. Organ-Specific 3D Organoids: Disease Modeling, Drug Discovery, and
Therapeutic Screening

# 10. Artificial Intelligence and Robotic-Assisted Approaches in 3D Bioprinting

11\. Challenges, Future Directions, and Outlook

XX Artificial Intelligence and Robotic-Assisted Approaches in 3D
Bioprinting

Robotic-based

A. Author^a^, B. Author^b^ and C. Author^a\*^.

^a^ Institution Address, ^b^ Institution Address (one line after author
names)

\*corresponding email address: XXX

[ABSTRACT]{.underline}

Single paragraph of 50 -- 200 words maximum, summarising the chapter.
CANNOT include bullet points, references or footnotes.

# X.1 Introduction 800 words-400 words

3D bioprinting, which uses the spatially controlled deposition of cells
and biomaterials to build living constructs, has emerged as a key
biofabrication approach in regenerative medicine, tissue engineering,
and the development of advanced three-dimensional in vitro models. More
than a biological extension of additive manufacturing, it is a means of
constructing living and spatially organized biological systems in which
geometry, material composition, and biological potential can be
specified together. This capability creates new possibilities for tissue
repair and, in the longer term, for implantable tissues and organ
substitutes. As 3D bioprinting technologies continue to advance, the key
question is no longer simply how to print engineered biological
constructs, but how to make bioprinting more predictive, integrated, and
controllable across the full workflow, so that it can better meet the
growing demands of regenerative medicine, tissue engineering, and
advanced three-dimensional in vitro models.

However, there are intrinsic difficulties in bioprinting itself.
Bioprinting does not produce an inert object with fixed properties. It
produces a living construct whose structural, mechanical, and biological
outcomes remain tightly coupled over time. A formulation that extrudes
well may fail to retain shape after deposition. A material that improves
geometric fidelity may compromise nutrient diffusion, cell spreading, or
long-term remodeling. A crosslinking strategy that stabilizes a printed
structure may also weaken cytocompatibility or later tissue development.
The challenge, therefore, is not simply to print complex forms, but to
reconcile manufacturability with biological permissiveness, and
immediate process success with later functional maturation. This
difficulty becomes more pronounced as bioprinting moves beyond
relatively simple printing scenarios toward more advanced applications
that involve multi-material, multi-cellular, multiscale, and dynamically
evolving systems.

These tensions appear across the full workflow. In the pre-printing
stage, researchers must define bioink composition, rheological behavior,
cellular requirements, construct design, and feasible processing windows
within a large and only partly mapped design space. In the in-printing
stage, outcomes remain sensitive to parameter drift, extrusion defects,
geometric distortion, and batch-to-batch inconsistency. In the
post-printing stage, further uncertainty arises from crosslinking
effects, cell stress, culture conditions, maturation trajectories, and
the persistent difficulty of linking early fabrication quality to later
biological function. Current bioprinting is therefore constrained less
by a single technical gap than by a workflow-wide problem of
coordination, traceability, and quality control.

It is under these conditions that artificial intelligence (AI) becomes
important. In bioprinting, AI should not be treated as a universal
solution. Its value lies in helping researchers deal with
high-dimensional, nonlinear, and only partially standardized bioprinting
workflows that are difficult to optimize by intuition or
one-variable-at-a-time experimentation. By extracting patterns from
imaging, rheological measurements, sensor data, and process outcomes, AI
can support tasks such as inverse design, printability prediction,
parameter optimization, anomaly detection, process monitoring, and
adaptive decision-making. In this sense, the adoption of AI in
bioprinting creates stronger demands for sensing, standardization, and
automation, while AI in turn offers capabilities such as prediction,
classification, optimization, and decision support across the workflow.

A balanced view remains essential. The most credible current uses of AI
in bioprinting are still relatively near-term: printability prediction,
bioink and parameter optimization, image-based quality assessment,
anomaly detection, and limited local feedback control. By contrast,
comprehensive prediction of long-term biological function, universally
transferable decision systems, and fully autonomous tissue manufacturing
remain much less mature. Post-printing biological prediction is
especially difficult because viability, maturation, remodeling, and
function depend on sparse data, biological variability, and weak
standardization. AI in bioprinting should therefore be understood as a
developing methodological layer within intelligent bioprinting, not as a
complete solution in itself.

This also shows that intelligent bioprinting is not simply a matter of
adding separate algorithms to individual tasks, but a broader shift from
stage-specific optimization toward system-level organization across the
workflow. This shift depends on cross-cutting infrastructure, including
multimodal sensing, structured data pipelines, standardized quality
descriptors, and process models that connect design, fabrication, and
evaluation, and it also explains the growing importance of
robotic-assisted approaches as the execution layer of intelligent
bioprinting. In this context, closed-loop bioprinting, digital twin
concepts, and self-driving bioprinting laboratories point to the next
stage of the field by showing how bioprinting may become more
integrated, adaptive, and increasingly autonomous.

Accordingly, this chapter approaches intelligent bioprinting as a
workflow-spanning and system-level shift in how bioprinting is designed,
executed, and evaluated. The discussion follows the full chain from
pre-printing decisions to in-process control and post-printing
biological consequence, while also emphasizing that these stages cannot
be treated in isolation if bioprinting is to become more reproducible,
adaptive, and practically useful. It therefore extends from
stage-specific intelligence to the enabling roles of infrastructure,
automation, and robotic integration, with the broader aim of showing how
intelligent bioprinting may help transform 3D bioprinting from a
fragmented experimental practice into a more coordinated and
controllable platform for regenerative medicine, tissue engineering, and
advanced three-dimensional in vitro models.

Workflow

pre-printing intelligence｜in-printing intelligence｜post-printing
biological intelligence｜workflow-spanning intelligence

Bioprinting

living constructs｜bioink｜printability｜shape fidelity｜cell
viability｜maturation｜functional outcome

AI

prediction｜optimization｜classification｜segmentation｜monitoring｜control｜decision
support｜interpretation

Infrastructure

standardization｜data infrastructure｜objective quality
descriptors｜automated readouts｜multimodal sensing｜digital twin

Cutting-edge concept

robotic integration｜in situ bioprinting｜geometric
adaptation｜sensor-guided control｜process orchestration｜self-driving
bioprinting laboratory

**Starting from the complex objects of 3D bioprinting, through the
phased intervention of AI, it progresses towards cross-stage
infrastructure and system-level automation.**

# X.2 3D Bioprinting 500 words

3D bioprinting provides the biological and technological foundation for
constructing spatially organized living systems in which geometry,
biomaterials, cells, and functional potential must be coordinated
simultaneously.

#### <https://doi.org/10.1002/adma.202408032>

![](media/image2.png){width="4.401073928258968in"
height="3.29169072615923in"}

### X.2.1 Extrusion-based bioprinting, EBB.

Extrusion-based bioprinting remains the most widely adaptable strategy
for depositing cell-laden bioinks, but its success depends on balancing
rheological printability, shape fidelity, extrusion stress, and cell
viability.

### X.2.2 Inkjet Bioprinting, IJB

Inkjet bioprinting enables precise and high-throughput droplet-based
patterning, yet its application is constrained by bioink viscosity,
droplet stability, nozzle clogging, and cell encapsulation requirements.

### X.2.3 light-assisted bioprinting, LAB

Light-assisted bioprinting offers high-resolution and spatially
controlled fabrication through photopolymerization, but its biological
utility depends on carefully managing light dose, curing depth,
photoinitiator chemistry, and cytocompatibility.

# X.3 AI FOR 3D BIOPRINTING

AI contributes to 3D bioprinting not as a single algorithmic solution,
but as a set of predictive, visual, optimization, and decision-support
tools that can operate across pre-printing, in-printing, and
post-printing stages.

## X.3.1 AI AS A TOOL 300 words

The evolution of AI from symbolic reasoning to machine learning, deep
learning, foundation models, and agentic systems provides a
methodological basis for transforming bioprinting from empirical
trial-and-error into data-supported intelligent manufacturing.

![](media/image3.jpeg){width="6.268055555555556in"
height="3.5694444444444446in"}

<https://doi.org/10.1002/adfm.202509530>

![](media/image4.png){width="6.268055555555556in"
height="3.689583333333333in"}

[Draw by ourselves]{.mark}

AI has evolved from a conceptual ambition into a set of technologies
that are now deeply embedded in scientific, industrial, and everyday
contexts. In 1950, Alan Turing's discussion of machine intelligence
raised the classic question of whether machines could exhibit
intelligent behaviour, while the 1956 Dartmouth Summer Research Project
on Artificial Intelligence is widely regarded as a key moment in the
formal establishment of AI as a research field. Early AI was strongly
influenced by symbolic artificial intelligence, which attempted to
simulate reasoning through logic, rules, search procedures, and
knowledge representation. Expert systems were among the most
representative applications of this period. They relied on manually
encoded rules, knowledge bases, and inference engines to reproduce
expert-like decision-making within specific domains. Although these
systems were relatively interpretable and logically structured, they
struggled with complex, uncertain, high-dimensional, and dynamically
changing real-world problems.

AI subsequently shifted from rule-based reasoning toward data-driven
learning, with machine learning becoming a central technical route.
Traditional machine learning methods, such as regression, support vector
machines, decision trees, and random forests, learn statistical
relationships between inputs and outputs from training data. These
methods have been widely used for classification, regression,
prediction, clustering, and anomaly detection. When features are well
designed and the problem boundaries are relatively clear, traditional
machine learning can still perform effectively, especially in small- to
medium-sized datasets. However, these approaches often depend heavily on
manual feature engineering and have limitations when dealing with
high-dimensional unstructured data such as images, speech, and natural
language.

Deep learning further transformed the field. With the development of
backpropagation, GPU computing, and multilayer neural networks, AI
models became capable of automatically learning hierarchical
representations from large-scale training data. This enabled major
breakthroughs in computer vision, speech recognition, and natural
language processing. Many early successes of deep learning relied on
supervised learning and human-labelled datasets, but self-supervised
learning, reinforcement learning, and large-scale pretraining later
became increasingly important. AlphaGo Zero provides a representative
example of the potential of reinforcement learning: instead of relying
on human game records, it learned through self-play under the rules of
Go and demonstrated how AI systems can develop high-level strategies
through exploration and feedback optimization.

The emergence of Transformer architecture and large-scale pretraining
further shifted AI from task-specific models toward foundation models.
The development of the GPT series showed that increasing model
parameters, training data, and computational resources can substantially
improve contextual learning, task transfer, and few-shot performance.
GPT-3 demonstrated the importance of scaling for task-agnostic language
modelling. A cautious interpretation is that large-scale data, model
architecture, and optimization jointly produce complex forms of
generalization and pattern-based reasoning.In recent years, instruction
tuning, reinforcement learning from human feedback, retrieval-augmented
generation, multimodal learning, and tool use have further expanded the
capabilities of large language models. Retrieval-augmented generation
allows models to incorporate external knowledge sources, improving
factual grounding and traceability in knowledge-intensive tasks.
Multimodal learning enables AI systems to process text, images, speech,
video, and other data types within integrated frameworks. Agentic
systems further allow AI to call tools, decompose tasks, interact with
external environments, and participate in more complex workflows.

It should be noted that although AI can assist in scientific research,
in actual application, it still has problems such as hallucinations,
data dependence, black box nature, and generalization vulnerability.
Therefore, it cannot be directly regarded as a reliable source for
scientific judgment. It is necessary to rely on experimental
verification, domain knowledge and scientific rigor to constrain its
use.

Overall, AI is evolving from a local prediction tool into a system-level
technological platform capable of integrating information, supporting
decision-making, generating content, executing tasks, and assisting
scientific innovation. Today, AI is no longer merely a speculative
concept from science fiction. It has become an important technological
force reshaping everyday life, engineering practice, and scientific
research workflows.

#### [[https://doi.org/10.1088/1758-5090/ad2189]{.mark}](https://doi.org/10.1088/1758-5090/ad2189)

![](media/image5.png){width="5.812542650918635in"
height="3.1927318460192478in"}

## X.3.2 AI FOR PRE-PRINTING 800 words

Pre-printing intelligence uses AI to explore large design spaces before
fabrication, linking construct design, bioink formulation, nozzle
configuration, and parameter selection to manufacturable and
biologically meaningful outcomes.

#### <https://doi.org/10.1002/adma.202408032>

![](media/image6.png){width="6.268055555555556in"
height="3.1555555555555554in"}

#### <https://doi.org/10.1002/adfm.202509530>

![](media/image7.png){width="6.268055555555556in"
height="3.2840277777777778in"}

### X.3.2.1 Blueprint generation and manufacturable design

AI-assisted blueprint generation can translate anatomical, biological,
and manufacturing constraints into printable construct designs, helping
bridge the gap between desired tissue architecture and feasible
fabrication.

### X.3.2.2 Nozzle and Bioink design 

AI can support nozzle and bioink design by modelling the coupled effects
of rheology, extrusion conditions, material composition, and cell
response on printability and construct quality.

### X.3.2.3 Process window and parameters optimization

AI-driven process optimization helps identify robust operating windows
in which printing parameters can satisfy multiple objectives, including
geometric fidelity, structural stability, and biological
compatibility.X.3.3 AI FOR IN-PRINTING 800 words

In-printing intelligence focuses on making the fabrication process
visible, measurable, and correctable through real-time monitoring,
defect recognition, process-state classification, and local feedback
control.

## X.3.3 AI FOR IN-PRINTING 500 words

In-printing intelligence focuses on making the fabrication process
visible, measurable, and correctable through real-time monitoring,
defect recognition, process-state classification, and local feedback
control.

### X.3.3.1 print pattern anomaly detection

Print pattern anomaly detection enables AI systems to identify visible
defects such as over-extrusion, under-extrusion, filament discontinuity,
line-width deviation, and surface irregularity during or immediately
after deposition.

### X.3.3.2 process-state classification/online process visibility

Process-state classification transforms raw imaging or sensor data into
interpretable information about nozzle position, bioink distribution,
deposition quality, and evolving print conditions.

### X.3.3.3 local corrective action

Local corrective action represents a key step toward closed-loop
bioprinting by allowing detected errors to inform adaptive changes in
pressure, flow rate, tool path, or printing commands within the same
fabrication process.

## X.3.4 AI FOR POST-PRINTING 500 words

Post-printing intelligence extends AI analysis beyond fabrication
quality toward the prediction and interpretation of cell viability, cell
behaviour, scaffold--cell interaction, maturation, differentiation, and
functional outcomes.

### X.3.4.1 biological consequence and functional interpretation

Post-printing evaluation should move beyond simple viability assessment
toward a more functional interpretation of how printing conditions
influence cell stress, proliferation, phenotype, and long-term
biological performance.

### X.3.4.2 Post-printing cell behavior and scaffold--cell interaction modeling

Modelling post-printing cell behaviour can help explain how printed
scaffold architecture, hydrogel microenvironment, pore structure, and
cell--matrix interactions shape migration, aggregation, redistribution,
and tissue organization.

### X.3.4.3 Toward predictive maturation, differentiation, and functional outcomes

The long-term goal of post-printing AI is to predict maturation,
differentiation, and functional trajectories from early imaging,
fabrication, and culture data, although this remains limited by sparse
datasets and biological variability.

# [X.4 Cross-cutting infrastructure for intelligent bioprinting Zhang]{.mark} 800 words

**[A figure for cross-cutting infrastructure]{.mark}**

Cross-cutting infrastructure provides the common data, sensing,
standardization, and quality-assessment foundation required to connect
stage-specific AI tools into a coherent intelligent bioprinting
workflow.

## X.4.1 Reproducibility, comparability, and standardization

Reproducibility and comparability are prerequisites for intelligent
bioprinting because AI models can only generalize across studies and
platforms when protocols, metrics, and reporting practices are
sufficiently standardized.

## X.4.2 Data infrastructure, literature-mined datasets, and digital twins

Robust data infrastructure, curated datasets, and digital twin concepts
can transform fragmented experimental observations into reusable,
model-updatable resources for simulation, prediction, and process
optimization.

## X.4.3 Objective quality descriptors and automated readouts

Objective quality descriptors and automated readouts convert printed
constructs from visually assessed products into quantitatively
measurable systems suitable for AI training, benchmarking, and quality
control.

## X.4.4 Context-aware and adaptive bioprinting platforms

Context-aware bioprinting platforms integrate sensing, decision support,
and adaptive fabrication so that printing systems can respond to
material, geometric, and biological variation rather than merely execute
fixed instructions.

## X.4.5 Open-loop And Closed-loop AI printing

The distinction between open-loop and closed-loop AI printing clarifies
whether AI is used only for offline recommendation and planning or is
directly coupled to real-time sensing, decision-making, and process
actuation.

# [X.5 System-level automation, robotic integration, and in-situ intelligent bioprinting Tian]{.mark} 800 words

**[A figure for robotic system used for in-situ bioprinting]{.mark}**

#### [[https://doi.org/10.18063/ijb.v9i1.629]{.mark}](https://doi.org/10.18063/ijb.v9i1.629)

![](media/image8.png){width="6.268055555555556in"
height="5.596527777777778in"}

System-level automation and robotic integration extend intelligent
bioprinting from algorithmic analysis toward physically adaptive
execution, enabling more flexible, context-aware, and clinically
relevant fabrication scenarios.

#### <https://doi.org/10.1002/adfm.202509530>

![](media/image9.png){width="6.268055555555556in"
height="3.558333333333333in"}

## X.5.1 Robotic-assisted in situ bioprinting

Robotic-assisted in situ bioprinting uses robotic motion, customized
end-effectors, and defect-specific positioning to bring bioprinting
closer to patient-specific repair within complex anatomical or surgical
environments.X.5.2 Geometric adaptation and path planning

Geometric adaptation and path planning are essential for translating
irregular tissue defects, reconstructed surfaces, or patient-specific
geometries into executable robotic trajectories and printable tool
paths.

## X.5.3 Sensor-guided process control and curing control

Sensor-guided process and curing control allow robotic bioprinting
systems to adjust deposition, positioning, light exposure, and
stabilization strategies according to real-time feedback from the
fabrication environment.

## X.5.4 Multi-tool, multi-material, and process-orchestration intelligence

Multi-tool and multi-material orchestration enables robotic platforms to
coordinate different deposition modes, materials, crosslinking steps,
and fabrication modules within a single integrated bioprinting workflow.

## X.5.5 Digital twins and self-driving architectures as system-level futures

Digital twins and self-driving architectures represent a future
direction in which bioprinting systems may combine modelling, sensing,
autonomous experimentation, and human oversight to support
self-optimization across the workflow.

# X.6 Challenges, open questions, and outlook 

The future of intelligent bioprinting depends on overcoming persistent
challenges in data scarcity, biological variability, standardization,
model generalization, interpretability, clinical translation, and
responsible human oversight.

Other contents consist of 700 words

The main text of the article should appear here with headings as
appropriate. Standard IUPAC nomenclature must be used.

Figures should be provided as separate files. Figures must be cited
within the text like so (see Figure X.1) and have a placement note in
the chapter, below.

\[Insert Figure X.1 here\]

Chemical structures should be supplied as ChemDraw files and must be
cited in the text like so (see Scheme X.1).

\[Insert Scheme X.1 here\]

Tables MUST be supplied in WORD format and must be cited within the
text, like so (see Table x.1).

\[Insert Table x.1 here\]

**X. 1. 1. Sub Section Heading -- Must be in BOLD**

**X. 1. 1. 1. Lower Sub Section Heading -- Must be in BOLD**

**References**

References must be superscripted in the text^1,2,3^. A list of
references in numerical order (following the Vancouver system) must
appear at the end of the chapter. For authors using EndNote, the style
file is available here
<https://www.rsc.org/journals-books-databases/book-authors/prepare-submit-book-or-chapter/#templates>.
All our reference guides can be found in our referencing guidelines
(below are some examples)

1\. A. Name, B. Name and C. Name, *Journal Title*, year, **volume**,
first page.

2\. A. Name, B. Name and C. Name, *Book Title*, Publisher, Publisher\'s
Location, edition, year. For example, S. T. Beckett, Science of
Chocolate, Royal Society of Chemistry, Cambridge, 2000.

3\. A. Name, PhD thesis, University Name, year.

4\. A. Name, presented in part at Conference Title, Place, Month, year.

**FIGURE AND TABLE CAPTIONS**

*Figure X. 1* *Explanation of the figure. If book is being printed in
black and white no colour references should appear in the figure
captions.* **Reproduced/Adapted from Ref. XX with permission from
\[Original Publisher\], Copyright \[YEAR\].**

*Table X. 1 Explanation of the table.* **Reproduced/Adapted from Ref. XX
with permission from \[Original Publisher\], Copyright \[YEAR\].**

Permission guidelines can be found here:
<https://www.rsc.org/journals-books-databases/book-authors/copyright-permissions/>

**ABBREVIATIONS**

Abbreviations must be defined at first mention in the chapter and
abbreviated thereafter. A list of abbreviations may be provided at the
end of the chapter if necessary.
