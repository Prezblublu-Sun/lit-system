# Section X.3.3.3: Local corrective action (closed-loop)

**Target words**: 200
**Query**: `closed-loop bioprinting feedback control corrective action G-code adaptive printing`
**Generated**: 2026-05-13T14:51:30.352997

---

## Part A: Explicitly cited references in outline (with content)

### Quick index

- ✅ **P63** — `10.1002/adfm.202424553` (in library)
- ✅ **P22** — `10.18063/ijb.v9i1.624` (in library)
- ✅ **P21** — `10.18063/ijb.v8i4.620` (in library)
- ✅ **P68** — `10.1007/s10845-023-02167-4` (in library)

### Detailed content per cited paper

#### 🎯 P63: Autonomous Control of Extrusion Bioprinting Using Convolutional Neural Networks

**DOI**: 10.1002/adfm.202424553

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P63 chunk_2, d=0.690]_

Recent attention has been directed toward implementing monitoring and closed-loop control technology to improve the quality of 3D-printed components. In contrast to traditional openloop 3D printing, where parameters are fixed before printing, closed-loop 3D printing refers to techniques that dynamically adjust printing parameters to compensate for changes such as printing defects, ink flow irregularities, nozzle functionality, and spatial displacement errors. [ 13] In the fused-deposition modeling field, closed-loop control mechanisms have been implemented using traditional [19-23] or AI-based [24-28] approaches, incorporating sensors into the printing process to evaluate the quality of the print. [ 14,29] Camera-based sensors are the most widely adopted, [10,11,20,30] with some examples of combining camera feeds with convolutional neural networks (CNNs), a powerful approach to identify printing defects and provide feedback to the material-feeding and motion-control systems to correct printing errors. [ 24,31-33] More recently, closed-loop extrusion controllers applied through reinforced learning and trained on simulation data have been developed. [ 34] Although closed-loop techniq...

_[P63 chunk_14, d=0.706]_

When deployed on poisoned g-code files we found that the closed-loop controller could correct extrusion errors and improve overall print quality (Figure 4a (iii); Movie S1, Supporting Information). Compared to standard open-loop bioprinting (no correction), our closed-loop controller enhanced extrusion quality across both line and infill structures printed using the dyed al- ginate ink (Figure 4a (iii),b (i)). For example, for line structures containing a deliberate over-extrusion, the closed-loop controllers increased the percentage of the print classified as good from 50% upto65%(Figure4b(i)). Similarly, for infill structures containing a deliberate over-extrusion, the closed-loop controller increased the percentage of the print classified as good from 70% up to 90% (Figure 4b (i)). The closed-loop controllers also improved overall print quality for infill and line structures containing deliberate under-extrusions (Figure 4b (i)). In the case of single-filament extrusion for a 10w/v% alginate bioink labeled red, we observed that our CNN models typically transitioned from a 'good extrusion' classification to 'under- or over-extrusion' when the filament width deviated by ≈ 0.36X th...

_[P63 chunk_8, d=0.720]_

*Figure 3. Validation of trained CNN on live printing process: a) System overview of experimental setup. i) User interface running Mainsail (Klipper graphical user interface) and our extrusion monitoring HUD. ii) Raspberry Pi 4b handling movement and vision tasks using Klipper, OpenCV, and libcamera. iii) modified bioprinting hardware. iv) Extrusion monitoring HUD with panels showing the current detection results (classification confidence, ratio of classifications over the print, and classification label), the camera information (time, current frame number, and frames per second), and the accumulated error over time. v) Tensorflow server that runs on a separate computer for classification of images sent from printer. The server parses the image to the appropriate model for classification before sending a response back to the printer. b) Accuracy (mean ± one standard deviation) of the detection system on prints with known areas of bad extrusion for each model (n = 5 runs). The experiment was performed using a 20G extrusion nozzle (603 µ mbore diameter). c) Examples of correct classification of extrusion types on each type of print by the best-performing architecture (Xception).*

A...

_[P63 chunk_1, d=0.724]_

(e.g., ink viscosity, flow rate, print speed, temperature, and layer height), requiring extensive experimentation by specialists. [ 9,10] Even under optimized processing conditions, extrusion bioprinting remains susceptible to errors and potential failures. These errors can arise from various factors, including ink inconsistencies, viscosity fluctuations due to crosslinking, and environmental variations. These challenges are exacerbated by the high cost of bioinks and biomaterial inks, along with the stringent regulatory requirements that will exist for bioprinted Advanced Therapy Medicinal Products (ATMPs) or Medical Devices, underscoring the need for reproducible and reliable protocols. [ 5,11,12] The limitations described above largely stem from the open-loop nature of existing bioprinting hardware, which lacks real-time process monitoring and adaptive control over extrusion parameters. Process parameters are fixed before printing, which prevents live editing of extrusion parameters to correct errors. Addressing this open-loop limitation will be crucial for advancing bioprinting beyond academic labs and into practical, industrial applications.
The challenges with open-loop print...

_[P63 chunk_16, d=0.750]_

This work advances the state-of-the-art in extrusion bioprinting by introducing closed-loop process controls that can detect and correct extrusion errors using CNNs. While machine learning has been previously employed for anomaly detection and quality monitoring in bioprinting, [ 35-38] existing approaches have focused on assessing quality across whole print layers using wide camera views, limiting the potential for real-time error correction within individual filaments. Our high-resolution quality monitoring platform overcame this limitation, enabling on-the-fly extrusion error detection and correction. With error detection and correction cycles occurring within 8-12 s, depending on the nature of the initial extrusion error, our system offers a significant advantage over approaches that rely on post-print or layer-by-layer analysis, enabling rapid adjustments and preventing the propagation of errors throughout the fabrication process. This real-time error correction capability is important in bioprinting applications, where the high cost of ink materials necessitates precise control and minimization of waste.
Theability of our system to operate on unseen inks is an important step ...

**Background:**
Based on the provided research paper text, here are the extracted sections:

**Research Background:**
The background of this research is rooted in the challenges faced by extrusion bioprinting technology. The current hardware systems for bioprinting operate in an open-loop manner, lacking real-time process monitoring and adaptive control over extrusion parameters. This leads to reproducibility issues due to errors arising from ink inconsistencies, viscosity fluctuations, environmental variations, and other factors (Page 1).

**Core Concepts:**
The core concept of this research is the developme...

**Core problem:**
1. **Most Central Problem and Why It Matters (Page 1-2):**
   The central problem addressed in this paper is the lack of real-time process monitoring and adaptive control over extrusion parameters in current bioprinting hardware, which leads to reproducibility challenges due to its open-loop nature. This matters significantly because it hinders the translation of bioprinting technology from academic research into practical industrial applications, especially for manufacturing complex tissues or organs that require precise control over material deposition.

2. **Hardest Technical Difficulties (...

---

#### 🎯 P22: In situ defect detection and feedback control with three-dimensional extrusion-b

**DOI**: 10.18063/ijb.v9i1.624

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P22 chunk_32, d=0.777]_

However,  there  are  still  some  limitations  to  our current  research  that  need  to  be  studied  further.  For example,  only  the  common  lattice  printing  path  was considered  in  this  study,  and  complex  graded  scaffold patterns [22] or  curved  paths  were  not  analyzed.  The printing  material  was  focused  on  Hap  without  cells inside.  Future  work  could  apply  the  'monitoring  and feedback-as-you-build' mechanism using different material  with  different  rheological  properties,  such  as hydrogel with cell encapsulated. In addition, the prebuilt feedback mechanism in this study relied heavily on preexperimental data with the target material, target FS, and LT values. The prebuilt feedback mechanism requires new pre-experiments with the different nozzles and different bioinks  that  are  selected  for  the  printing  task.  Large databases must be built by collecting multiple groups of experimental data to realize fast and intelligent selection of  printing  parameters  for  better  feedback  control.  In addition, machine learning and deep learning algorithms have  gradually  been  applied  to  camera-based  anomaly detection in 3D printing [23,24] , ...

_[P22 chunk_28, d=0.784]_

As shown in Figure 9, 3D P-OCT  data enabled mechanical  analysis  and  3D  structural  analysis  of  the overall  construct.  After  feedback,  the  VP  and  PC  of  the construct  increased  from  37.68%  and  98.14%  to  46.32% and  98.78%,  respectively  (Figure 9D).  Furthermore,  3D P-OCT data of the printed construct can be converted to STL format files using MIMICS. The mechanical stiffness of the printed constructs before and after feedback can be compared with  the  designed  model  using  finite  element analysis  (FEA),  which  was  implemented  to  simulate  the stress and strain process of constructs under compression using ANSYS Workbench 17.0 (Figure 9A-C). After feedback, the compressive modulus  of  the construct improved from 84.4374% to 33.3622%, which was closer to that of the design model (22.09%).

## 4. Discussion and conclusion

3D bioprinting provides new technology for tissue and organ  regeneration,  drug  screening,  disease  modeling, and  other  fields.  3D  printing  technology  with  highfidelity  structure  and  function  is  key  to  promoting  the large-scale application of 3D bioprinting in biomedical field. However, printing defects lead to low...

_[P22 chunk_30, d=0.793]_

Based  on  large-field  full-depth  imaging  with  3D P-OCT, and FS and LT quantitative analyses, the feedback control mechanism can be pre-built to adjust the  input  parameters  and  defect  repair.  In  this  study, material  deposition  errors  under  three  different  paths were considered for the pre-built feedback mechanism, including start-stop points, straight-line paths, and the turnarounds.  The  first  pre-experiment  was  carried  out to  explore  the  relationship  between  the  target  material and two printing parameters, velocity and pressure, and FS  and  LT  of  the  filament  extruded  through  a  nozzle. Under the same pressure value, the FS value and velocity exhibited  a  linear  relationship,  which  can  be  used  as  a follow-up  feedback  support.  The  response  delay  of  the pressure  might  cause  a  delay  in  material  deposition  at the path starting point and excess deposition of material at  the  path  ending  point.  To  avoid  material  deposition errors at start-stop points, a second pre-experiment was carried  out  with  the  target  material  and  the  optimum input parameters of velocity and pressure to determine the degree of delay respons...

_[P22 chunk_7, d=0.817]_

In  extrusion-based  3D  bioprinting,  FL  and  LT  errors usually occur due to the mismatch between the rheological properties of the printing materials and the control inputs of  pressure  and  velocity.  Determining  the  appropriate pressure and velocity, and reducing FL and LT errors are the premise of high-fidelity 3D bioprinting. Therefore, new quantification methods for FL and LT were first determined, and then,  the  corresponding  feedback  mechanisms  were pre-built  for  different  defects  during  3D  bioprinting.  By combining 3D P-OCT data and the design model, the layer fidelity and overall fidelity could be further assessed for the construct.

*Figure 1. The closed-loop feedback control loop (A) and the algorithm flow (B) for in situ defect detection and feedback control with 3D P-OCT. 3D P-OCT: Three-dimensional extrusion-based bioprinter-associated optical coherence tomography.*

B
A
3D structure model、
TargetValues
material、FS、LT
3D Bioprinting&
monitoring devices
3D P-OCT system
regulator
speed and pressure
Pathgeneration software,
Controlled system
FS、LT、Fidelity
based 3D point cloud
Improvedquantification
FS、LT、Fidelity
ResultValue
Pre-builtfeedbackmechanism
...

_[P22 chunk_18, d=0.822]_

× (mm)
FilamentSize
Layer Thickness
0.8
0.8
(ww)
0.6
0.6
0.4
0.4
5
0.2
5
0.2
2mm
-10
-5
x (mm)
10
-10
-5
x (mm)
5
10
FilamentSize
LayerThickness
mm
5
0.8
0.8
(ww)
0.6
(mm）
0.6
R
0.5
0.4
0.4
0.2
0.2
-5
-5
100
t2(ms)
300300
2mm
-10
-5
0
5
10
-10
-5
0
10
X
(mm)
X
(mm)

## 2.4.3. Defects around the turnarounds and feedback mech

In addition to the straight path and end points mentioned above, material deposition errors often occur at  turnarounds.  There  is  a  velocity  change  around  the turnarounds, which leads to material deposition errors when  the  velocity  does  not  match  the  pressure  and rheological properties of the material. Armstrong et al . corrected the path error using reverse compensation [18] . This  section  mainly  focuses  on  compensating  for  FS and LT defects around the turnarounds with feedback control for the common  right-angle corner path (Figure 6A). In 3D  bioprinting, GCode  nodes  are typically set at the corners in the path (see asterisk). Due to  the  acceleration  and  deceleration  zones  before  and after the node, a lower average velocity typically leads to excessive material deposition, and FS and LT defects. To compensate for the FS and LT ...

**Background:**
Based on the provided text, here are the extracted sections:

### 1. Research Background

**Page 47-48:**
"With its potential to fabricate three-dimensional (3D) biomimetic functional tissue constructs and organs, 3D bioprinting has been applied in organ printing [1,2], microvasculature printing [3], disease modeling [4], and scaffold fabrication for tissue regeneration[5,6]. According to different prototyping principles and printed materials, 3D bioprinting follows three main approaches: droplet-based, extrusion-based, and photocuring-based bioprinting. Extrusion-based bioprinting employs pne...

**Core problem:**
1. **Most Central Problem and Why It Matters (Page 47-48)**

The central problem addressed in this paper is the lack of real-time defect detection and feedback control mechanisms during extrusion-based bioprinting, which leads to low structural fidelity between printed constructs and design models. This matters significantly because high-fidelity structures are crucial for applications such as tissue engineering, drug screening, and disease modeling, where precise replication of biological tissues or organs is essential.

2. **Hardest Technical Difficulties (Pages 49-50)**

The hardest technic...

---

#### 🎯 P21: A Deep Learning Quality Control Loop of the Extrusion-based Bioprinting Process

**DOI**: 10.18063/ijb.v8i4.620

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P21 chunk_21, d=0.873]_

In  this  work,  we  proposed  for  the  1 st time  an  AIbased  quality  control  loop  that  can  be  used  to  both automatically  optimize  the  printing  parameters  for  a given  material  and  printing  set-up,  as  well  as  monitor the printing status online with a fast response time. We developed a comprehensive dataset (available at https:// doi.org/10.5281/zenodo.7024007)  of  the  EBB  process by taking videos of different prints with a combination of multiple parameters, including LH, EM, infill density, extrusion system, and material color.
Regarding  the  dataset  creation,  we  used  Pluronic F-127  since  it  is  well  known  for  its  printability.  It  is important to stress out that the use of other materials has been accounted for by introducing color to the Pluronic solution and converting the RGB frame to grayscale. As a  result,  since  the  CNN  model is only interested in the appearance of the material and not on its properties (e.g., viscosity and yield stress), the frames for other materials will appear like those for the Pluronic, effectively limiting the number of tests to be performed.
A CNN architecture was trained and comprehensively evaluated on t...

_[P21 chunk_0, d=0.919]_

## 1. Introduction

In recent years, the field of bioprinting has seen a strong increase of interest as a promising solution to fabricate tissues and organs for tissue engineering applications [1,2] . Among the technologies  currently  available,  extrusionbased bioprinting  (EBB)  has  been  adopted  as  the  most popular  approach  thanks  to  its  simple  and  affordable hardware, a wide array of processable materials, and the ability  to  print  clinically  sized  constructs [3] .  The  typical EBB  set-up  consists  of  an  extrusion  tool-head,  either mechanical  (i.e.,  piston  actuated  and  screw  assisted) or  pneumatic,  which  is  attached  to  a  three-dimensional (3D) positioning system. By applying a pressure on the material (usually a hydrogel) inside a reservoir (usually a syringe) while moving it over a printing plate, a 3D shape can be obtained in a layer-by-layer fashion [4,5] .
Significant  efforts  have  been  made  to  develop novel biomaterial inks [6] that  show  enhanced  biological response  and  appropriate  physical-chemical  properties for the target tissue, while also being processable through EBB with good printability (i.e., a combination of severa...

_[P21 chunk_1, d=0.934]_

Significant  efforts  have  been  made  to  develop novel biomaterial inks [6] that  show  enhanced  biological response  and  appropriate  physical-chemical  properties for the target tissue, while also being processable through EBB with good printability (i.e., a combination of several aspects of the EBB process, including material, scaffold geometry, and printing apparatus that determines a priori if  the  printing  process  will  be  successful  or  not) [7-9] . However, there is often a delicate balance between these different  requirements,  which  results in careful  and time-consuming optimization of the material properties, printing parameters, and scaffold geometry to obtain good print quality results. Furthermore, since no standardized method is currently available for the printing parameters optimization, the results from this trial-and-error process may  not  be  reproducible  across  labs. Altogether,  these limitations pose a significant obstacle to the translation of a promising ink/bioprinted product to more impactful clinical applications, as it is more difficult to comply to relevant healthcare-related standards [10] .
© 2022 Author(s). This is an Open-Access art...

_[P21 chunk_3, d=0.951]_

Despite  the  good  results  of  these  few  preliminary studies, much research is still needed for the implementation  of  a  robust,  AI-based  quality  control system  of  the  EBB  process.  First,  this  system  should be able to analyze the printing outcome and change the printing parameters without any manual involvement to have a completely autonomous control loop. Furthermore, the  quality  assessment  should  focus  on  the  full,  3D scaffold  shape,  and  not  only  on  a  few,  initial  layers, which are not representative of the final shape. Finally, the system should also be able not only to optimize the printing parameters but also monitor the printing session for quality assessment and potential on-the-fly correction of working parameters.
Considering  these  challenges,  we  present  a  novel approach for parameter optimization and in-process monitoring  of  the  EBB  process  using  a  combination  of: (i) a robust DL model (based on an ad hoc optimized neural network) which can classify the print outcome into one of three classes (i.e., good, under, and over extrusion) and (ii) a mathematical model (already published in Bonatti et al. [7] ) to  automatically  tu...

_[P21 chunk_7, d=0.956]_

For example, Jin et al. used a CNN to implement a real-time feedback loop on solid (no infill) FDM-printed layer.  The  authors  identified  three  main  classes  (i.e., under-extrusion,  over-extrusion,  and  good  quality)  and built a dataset of images using a top view of the printing process. The collected data were used to test and validate the  DL  model,  reaching  a  high  classification  accuracy (around 98%) [31] . In another work, Tonnaer et al. tackled the  problem  of  detecting  anomalies  on  the  surface  of FDM-printed  parts  using  a  semi-supervised  approach. The  authors employed  a  variational autoencoder, a type  of  deep  architecture  which,  when  trained  with images from non-faulty parts, can learn their probability distribution. When fed with images from error containing parts, the model can then assign a value to those images representing the probability that they come from the same distribution of non-faulty images. As a result, by setting a proper threshold, the model can effectively distinguish between  good  and  erroneous  prints [32] .  The  work  by Zhang et al. highlighted how  multiple information coming from different sensors can be integra...

**Background:**
Based on the provided text, here are the extracted sections:

1. **Research Background** (Page 308-309)
   > In recent years, the field of bioprinting has seen a strong increase of interest as a promising solution to fabricate tissues and organs for tissue engineering applications [1,2]. Among the technologies currently available, extrusion-based bioprinting (EBB) has been adopted as the most popular approach thanks to its simple and affordable hardware, a wide array of processable materials, and the ability to print clinically sized constructs [3]. The typical EBB set-up consists of an extrus...

**Core problem:**
1. **Most Central Problem and Why It Matters (Page 307-308)**

The central problem addressed in this paper is the lack of a standardized method for optimizing printing parameters in extrusion-based bioprinting (EBB), which leads to non-reproducible results across different laboratories. This issue hinders the translation of promising bioprinted products into impactful clinical applications, as it complicates compliance with healthcare-related standards.

2. **Hardest Technical Difficulties (Page 310-314)**

The hardest technical difficulties include developing a comprehensive dataset that capt...

---

#### 🎯 P68: Predicting the number of printed cells during inkjet-based bioprinting process b

**DOI**: 10.1007/s10845-023-02167-4

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P68 chunk_2, d=0.840]_

be dependent on its intended application (Lee et al., 2019). The  key  advantages  of  each  bioprinting  technology  are as  follows:  the  jetting-based  bioprinting  approach  facilitates contactless on-demand bioprinting of different living cells and biomaterials to enhance cell-cell and cell-matrix interactions (Ng et al., 2017a, 2018b), the extrusion-based bioprinting approach facilitates printing highly viscous bioinks with fast fabrication speed (Yang et al., 2022; Zhuang et  al.,  2019),  and  lastly  the  vat  polymerization-based  bioprinting approach can achieve high printing resolution and printable cell concentration (Nieto et al., 2020).
For bioprinting applications, the living cells are usually encapsulated  within  hydrogel-based  bio-inks  and  printed using  different  bioprinting  technologies  which  have  their own  specific  bio-ink  requirements.  The  printed  cells  in jetting-based bioprinting approach are usually encapsulated within un-crosslinked bio-inks of low viscosity (Ng et al., 2022, 2023), whereas the printed cells in  extrusion-based and  vat  polymerization-based  bioprinting  approaches  are usually encapsulated within highly-viscous crosslink...

_[P68 chunk_1, d=0.920]_

Over the years, there is an increased interest in the use of 3D bioprinting  technologies  for  tissue  engineering,  regenerative medicine, and biomedical applications due to its exceptional ability to precisely deposit highly viable cells during the bioprinting process to fabricate biomimetic 3D tissueengineered constructs (He et al., 2021; Levato et al., 2020; Ng et al., 2016a, 2019, 2020a; Sun et al., 2020). These 3D bioprinting technologies can be categorized into 3 distinct groups  according  to  the ASTM  standards  -  jetting-based (Choe  &  Kim,  2020;  Li  et  al.,  2020b;  Ng  et  al.,  2016b), extrusion-based (Meng et al., 2020; Ng et al., 2014; Ozbolat and Hospodiuk, 2016) and vat photopolymerization-based (Li et al., 2020a;  Ng et al., 2020b). Each bioprinting technology has its distinctive advantages and limitations and the selection  of  an  appropriate  bioprinting  technology  should
Xi Huang and Wei Long Ng have contributed equally towards this paper.
- Wei Long Ng ng.wl@ntu.edu.sg
- Wai Yee Yeong wyyeong@ntu.edu.sg
1 HP-NTU Digital Manufacturing Corporate Lab, Nanyang Technological University (NTU), 65 Nanyang Drive, Singapore 637460, Singapore
2 Singapore Centr...

_[P68 chunk_4, d=0.945]_

Hence, the goal of this study is to utilize machine learning approaches on high-speed images captured to predict the number of encapsulated cells  during  the  droplet  bioprinting process. Machine learning is a subset of artificial intel -ligence  which  can  identify  the  relationship  between  large datasets  efficiently,  resulting  in  a  model  that  is  useful  in the prediction of new inputs (Xames et al., 2022). Machine learning is useful when statistical relationships exist in the dataset but the model for the dataset cannot be determined analytically, such as optimizing printing parameters (Bonatti et  al.,  2022;  Fu  et  al.,  2021;  Law et al., 2023), predicting the cell viability from the process parameter and identifying the significant process parameters for high cell viabil -ity  (Xu  et  al.,  2022).  There  are  three  basic  approaches  to apply machine learning for different situations; supervised learning (Caruana & Niculescu-Mizil, 2006), unsupervised learning (Ghahramani, 2004; Hastie et al., 2009), and reinforcement learning (Arulkumaran et al., 2017; Kaelbling et al., 1996; Wiering & Van Otterlo, 2012). Supervised learning creates a model from labeled da...

_[P68 chunk_6, d=0.977]_

The primary human dermal fibroblasts (HDFs) used in this work were purchased from CellnTec Advanced Cell Systems and  routinely  passaged  in  tissue  culture  flasks  (Passages 3-5).  Fibroblasts  were  cultured  in  CnT-Prime  Fibroblast Proliferation Medium (CnT-PR-F, 1% serum medium supplemented with fully defined growth factors and co-factors) at a temperature of 37 o C, 5% CO 2  and the culture medium were changed once every three days. The adherent fibro -blasts were harvested using CnT Accutase cell detachment solution  (CnT-Accutase  100)  at  90%  confluency.  Based on our previous work, the use of 2% PVP-based bio-inks improved the droplet printing quality and cell viability during the inkjet bioprinting process (Ng, Yeong et al., 2017b). Hence, the detached fibroblast cells were suspended in 2%
LinearRegression
SupportVectorRegressor
Regression
based
X1
X1
y=ao+ax+a2x2+ax3+..
MLTechnique
DecisionTreeRegressor
Ensemble
X>5
Input
Yes
No
Decisiontree
DecisionTree1
DecisionTree2
DecisionTree3
based
y=3
X2>7
Majorityvote/Averaging
Yes
No
Prediction
y=2
y=5
w/v PVP-based bio-inks to obtain different concentrations of cell-laden bio-inks (1-3 million cells/ml).

## Bioprinting...

_[P68 chunk_0, d=0.994]_

## Abstract

In this work, our proof-of-concept study can be used to predict the number of cells within printed droplets based on droplet velocity at two different points along the nozzle-substrate distance using machine learning approaches. A novel highthroughput contactless method that combines the use of an optical system and machine learning algorithms was utilized for various applications such as cell detection within single droplets (presence/absence of cells) and prediction of the total number of printed cells within multiple droplets by measuring the droplet deceleration between two positions along the nozzle-substrate distance. The proposed method in this work has demonstrated good accuracy in cell prediction within single droplet (presence/absence of cells) and low prediction error in determining number of cells within multiple droplets by reducing the error by a factor of √ N for N droplets measured in a batch. The performance of five different machine learning algorithms such as linear regression, support vector regression, decision tree regressor, random forest regression, and extra tree regression were compared to determine the best algorithm for each type of applicat...

**Background:**
Certainly, here are the extracted sections from the provided text:

### 1. Research Background

**Page 2349:**
"Over the years, there is an increased interest in the use of 3D bioprinting technologies for tissue engineering, regenerative medicine, and biomedical applications due to its exceptional ability to precisely deposit highly viable cells during the bioprinting process to fabricate biomimetic 3D tissue-engineered constructs (He et al., 2021; Levato et al., 2020; Ng et al., 2016a, 2019, 2020a; Sun et al., 2020). These 3D bioprinting technologies can be categorized into 3 distinct groups ...

**Core problem:**
1. **Most Central Problem and Why It Matters**

The most central problem addressed in this paper is predicting the number of cells within printed droplets during an inkjet-based bioprinting process using machine learning approaches. This matters because accurately monitoring cell numbers is critical for fabricating scalable, reproducible 3D tissue constructs, which are essential for regenerative medicine and biomedical applications.

2. **Hardest Technical Difficulties**

The hardest technical difficulties include:
- Developing a high-throughput method to predict the number of cells in droplet...

---

## Part B: Semantic search results (Chroma top N)

### P82: 3D Printed Functional and Biological Materials on Moving Freeform Surfaces

**DOI**: 10.1002/adma.201707495
**Best distance**: 0.673
**Chunks retrieved**: 2

**Retrieved chunks:**

_[P82 chunk_3, d=0.673]_

3D printing is an attractive  manufacturing method due to its  versatility  to  directly  fabricate  freeform  functional  devices that  adapt  to  the  geometries  of  target  surfaces.  Previous approaches  relied  on  open-loop  calibrate-then-print  procedures by utilizing cumbersome  reverse-engineering  techniques,  with  demonstrations  such  as  3D  printed  tactile  sensors on a model hand, [27]  microfluidic devices on whole organ models, [28] and bacteria-derived materials on a doll face. [29] Yet, these approaches were only applicable to static target surfaces. To enable adaptive 3D printing on moving freeform surfaces, a  closed-loop  feedback  system  is  required  to  allow  real-time www.advancedsciencenews.com corrections  of  printing  errors  introduced  by  the  dynamically changing  workspace. [30]   Indeed,  previous  attempts  to  track and  ink-jet  print  on  a  moving  human  hand  have  been  carried  out. [31,32] Our  approach  advances  these  technologies  further by: 1) compensating for the full six degrees of freedom of rigid body motions; 2) being applicable to more general tasks with arbitrary shapes of the target surface; 3) being compatible with ...

_[P82 chunk_2, d=0.738]_

This  approach  has  been  highly  successful  in  creating  flexible, stretchable,  and  biointegrated  electrical  circuits, [2,11-14] sensing arrays, [7,15,16] energy  harvesting  devices, [17,18] digital  displays, [9,19] and  optogenetic  controllers. [20] Alternatively,  we  suggest  that devices  can  be  autonomously  fabricated  without  the  need  for microfabrication facilities in freeform geometries that are actively adaptive  to  target  surfaces  in  real  time,  driven  by  advances  in multifunctional 3D printing technologies. With recent progress in printable functional materials and device designs, 3D printing is  not  only  capable  of  replicating  shapes  in  both  macro-  and microscales [21] but  also  interweaving  a  diverse  palette  of  functional, biological, and biocompatible materials. This approach has been used for a variety of applications, such as regenerative pathways, [22] microbial  wearables, [23] fully  3D  printed  quantum  dot light-emitting diodes, [24] and electromagnetic structures. [25]  Highperformance discrete electronics could also be integrated into the 3D printed structure to yield hybrid devices. [26]
3D printing is an attractive  ...

**Background (from SOP metadata):**
Based on the provided research paper, here's an extraction of factual content related to your requested points:

### 1. Research Background

**Quote:**
"Commercial wearable devices are either rigid (e.g., smart fitness watches), or soft but with determinant shapes (e.g., haptic gloves for virtual reality applications). Such properties are often incompatible with target biological surfaces that possess highly arbitrary, dynamically varying geometries, such as skin and tissues. As a result, nonseamless interfaces between wearable devices and target surfaces can be created, compromising user comf...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters (Page 1-2):**
   The central problem addressed in this paper is the challenge of fabricating wearable devices that can conform to highly arbitrary, dynamically varying biological surfaces such as skin and tissues. This issue is significant because conventional rigid or determinate-shaped wearable devices often create nonseamless interfaces with target biological surfaces, leading to user discomfort and compromised device performance.

2. **Hardest Technical Difficulties (Page 3-4):**
   The hardest technical difficulties include developing a functio...

---

### P2: AI-driven 3D bioprinting for regenerative medicine

**DOI**: _missing_
**Best distance**: 0.677
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P2 chunk_42, d=0.677]_

- (ii) Optimization of closed-loop control strategy: Upon achieving 3D reconstruction of the printing surface, AI technology facilitates segmentation of the printing head and analysis of its spatial position, aiding in the correction of the printing path. In addition, AI  technology  can  be  used  to  construct  control  strategies  and enable real-time correction of the printing head ' s position and posture, such as utilizing ANN models to build motion controllers (Fig. 7g) [297]. Reinforcement learning methods have also been employed to automatically plan and adjust the path of surgical robots,  enhancing  movement  precision,  efficiency,  and  adaptability  to  complex  environments  [298 -301].  These  advancements  hold  significant  reference  value  for  in  situ  bioprinting based on surgical robots.

## 6. AI-driven approaches for function regulation

Upon completing the printing of high-quality structures, the final element is the function regulation of the printed structures. Primarily, the design of maturation conditions is imperative to functionalize the printed  structures,  thereby  transforming  them  into  BPPs  with  the requisite biological functions, as descr...

**Background (from SOP metadata):**
1) **Research Background**:
   "In recent decades, 3D bioprinting has garnered significant research attention due to its ability to manipulate biomaterials and cells to create complex structures precisely." (Page 1)

2) **Core Concepts**:
   - Quality by Design (QbD)
   - Artificial Intelligence (AI), particularly Machine Learning (ML)
   - Multi-scale and multi-modal sensing
   - Data-driven design
   - In-line process control

3) **Common Pitfalls or Failure Modes**:
   "The clinical translation of 3D bioprinted products (BPPs) from bench to bedside has been hindered by challenges in terms o...

**Core problem & critique:**
1) **Most central problem and why it matters**: The most central problem addressed by the paper is how to enhance the clinical translation of 3D bioprinted products (BPPs) through AI-driven Quality by Design (QbD) methodologies (page 2). This issue is crucial because current BPPs face significant challenges in personalization and scaling up production, which hinder their practical application in clinical settings. Addressing these challenges could significantly advance the use of regenerative medicine technologies for patient-specific treatments.

2) **2-3 hardest technical difficulties and wh...

---

### P120: AI-driven 3D bioprinting for regenerative medicine: From bench to bedside

**DOI**: 10.1016/j.bioactmat.2024.11.021
**Best distance**: 0.677
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P120 chunk_42, d=0.677]_

- (ii) Optimization of closed-loop control strategy: Upon achieving 3D reconstruction of the printing surface, AI technology facilitates segmentation of the printing head and analysis of its spatial position, aiding in the correction of the printing path. In addition, AI  technology  can  be  used  to  construct  control  strategies  and enable real-time correction of the printing head ' s position and posture, such as utilizing ANN models to build motion controllers (Fig. 7g) [297]. Reinforcement learning methods have also been employed to automatically plan and adjust the path of surgical robots,  enhancing  movement  precision,  efficiency,  and  adaptability  to  complex  environments  [298 -301].  These  advancements  hold  significant  reference  value  for  in  situ  bioprinting based on surgical robots.

## 6. AI-driven approaches for function regulation

Upon completing the printing of high-quality structures, the final element is the function regulation of the printed structures. Primarily, the design of maturation conditions is imperative to functionalize the printed  structures,  thereby  transforming  them  into  BPPs  with  the requisite biological functions, as descr...

**Background (from SOP metadata):**
Based on the provided text from the research paper, here are the extracted sections:

### 1. Research Background

"In recent decades, 3D bioprinting has garnered significant research attention due to its ability to manipulate biomaterials and cells to create complex structures precisely. However, due to technological and cost constraints, the clinical translation of 3D bioprinted products (BPPs) from bench to bedside has been hindered by challenges in terms of personalization of design and scaling up of production."

### 2. Core Concepts

- **Critical Quality Attributes (CQA):** "CQA refer to ...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters**

The most central problem addressed in this paper is the challenge of translating 3D bioprinting from bench to bedside, particularly focusing on personalization of design and scaling up production. This matters significantly because despite advancements in 3D bioprinting technology, clinical applications remain limited due to these challenges. The authors argue that integrating artificial intelligence (AI) technologies within a Quality by Design (QbD) framework can address these issues, thereby accelerating the clinical translation of 3D bioprinte...

---

### P63: Autonomous Control of Extrusion Bioprinting Using Convolutional Neural Networks 🎯 (also cited in outline)

**DOI**: 10.1002/adfm.202424553
**Best distance**: 0.690
**Chunks retrieved**: 5

**Retrieved chunks:**

_[P63 chunk_2, d=0.690]_

Recent attention has been directed toward implementing monitoring and closed-loop control technology to improve the quality of 3D-printed components. In contrast to traditional openloop 3D printing, where parameters are fixed before printing, closed-loop 3D printing refers to techniques that dynamically adjust printing parameters to compensate for changes such as printing defects, ink flow irregularities, nozzle functionality, and spatial displacement errors. [ 13] In the fused-deposition modeling field, closed-loop control mechanisms have been implemented using traditional [19-23] or AI-based [24-28] approaches, incorporating sensors into the printing process to evaluate the quality of the print. [ 14,29] Camera-based sensors are the most widely adopted, [10,11,20,30] with some examples of combining camera feeds with convolutional neural networks (CNNs), a powerful approach to identify printing defects and provide feedback to the material-feeding and motion-control systems to correct printing errors. [ 24,31-33] More recently, closed-loop extrusion controllers applied through reinforced learning and trained on simulation data have been developed. [ 34] Although closed-loop techniq...

_[P63 chunk_14, d=0.706]_

When deployed on poisoned g-code files we found that the closed-loop controller could correct extrusion errors and improve overall print quality (Figure 4a (iii); Movie S1, Supporting Information). Compared to standard open-loop bioprinting (no correction), our closed-loop controller enhanced extrusion quality across both line and infill structures printed using the dyed al- ginate ink (Figure 4a (iii),b (i)). For example, for line structures containing a deliberate over-extrusion, the closed-loop controllers increased the percentage of the print classified as good from 50% upto65%(Figure4b(i)). Similarly, for infill structures containing a deliberate over-extrusion, the closed-loop controller increased the percentage of the print classified as good from 70% up to 90% (Figure 4b (i)). The closed-loop controllers also improved overall print quality for infill and line structures containing deliberate under-extrusions (Figure 4b (i)). In the case of single-filament extrusion for a 10w/v% alginate bioink labeled red, we observed that our CNN models typically transitioned from a 'good extrusion' classification to 'under- or over-extrusion' when the filament width deviated by ≈ 0.36X th...

_[P63 chunk_8, d=0.720]_

*Figure 3. Validation of trained CNN on live printing process: a) System overview of experimental setup. i) User interface running Mainsail (Klipper graphical user interface) and our extrusion monitoring HUD. ii) Raspberry Pi 4b handling movement and vision tasks using Klipper, OpenCV, and libcamera. iii) modified bioprinting hardware. iv) Extrusion monitoring HUD with panels showing the current detection results (classification confidence, ratio of classifications over the print, and classification label), the camera information (time, current frame number, and frames per second), and the accumulated error over time. v) Tensorflow server that runs on a separate computer for classification of images sent from printer. The server parses the image to the appropriate model for classification before sending a response back to the printer. b) Accuracy (mean ± one standard deviation) of the detection system on prints with known areas of bad extrusion for each model (n = 5 runs). The experiment was performed using a 20G extrusion nozzle (603 µ mbore diameter). c) Examples of correct classification of extrusion types on each type of print by the best-performing architecture (Xception).*

A...

_[P63 chunk_1, d=0.724]_

(e.g., ink viscosity, flow rate, print speed, temperature, and layer height), requiring extensive experimentation by specialists. [ 9,10] Even under optimized processing conditions, extrusion bioprinting remains susceptible to errors and potential failures. These errors can arise from various factors, including ink inconsistencies, viscosity fluctuations due to crosslinking, and environmental variations. These challenges are exacerbated by the high cost of bioinks and biomaterial inks, along with the stringent regulatory requirements that will exist for bioprinted Advanced Therapy Medicinal Products (ATMPs) or Medical Devices, underscoring the need for reproducible and reliable protocols. [ 5,11,12] The limitations described above largely stem from the open-loop nature of existing bioprinting hardware, which lacks real-time process monitoring and adaptive control over extrusion parameters. Process parameters are fixed before printing, which prevents live editing of extrusion parameters to correct errors. Addressing this open-loop limitation will be crucial for advancing bioprinting beyond academic labs and into practical, industrial applications.
The challenges with open-loop print...

_[P63 chunk_16, d=0.750]_

This work advances the state-of-the-art in extrusion bioprinting by introducing closed-loop process controls that can detect and correct extrusion errors using CNNs. While machine learning has been previously employed for anomaly detection and quality monitoring in bioprinting, [ 35-38] existing approaches have focused on assessing quality across whole print layers using wide camera views, limiting the potential for real-time error correction within individual filaments. Our high-resolution quality monitoring platform overcame this limitation, enabling on-the-fly extrusion error detection and correction. With error detection and correction cycles occurring within 8-12 s, depending on the nature of the initial extrusion error, our system offers a significant advantage over approaches that rely on post-print or layer-by-layer analysis, enabling rapid adjustments and preventing the propagation of errors throughout the fabrication process. This real-time error correction capability is important in bioprinting applications, where the high cost of ink materials necessitates precise control and minimization of waste.
Theability of our system to operate on unseen inks is an important step ...

**Background (from SOP metadata):**
Based on the provided research paper text, here are the extracted sections:

**Research Background:**
The background of this research is rooted in the challenges faced by extrusion bioprinting technology. The current hardware systems for bioprinting operate in an open-loop manner, lacking real-time process monitoring and adaptive control over extrusion parameters. This leads to reproducibility issues due to errors arising from ink inconsistencies, viscosity fluctuations, environmental variations, and other factors (Page 1).

**Core Concepts:**
The core concept of this research is the developme...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters (Page 1-2):**
   The central problem addressed in this paper is the lack of real-time process monitoring and adaptive control over extrusion parameters in current bioprinting hardware, which leads to reproducibility challenges due to its open-loop nature. This matters significantly because it hinders the translation of bioprinting technology from academic research into practical industrial applications, especially for manufacturing complex tissues or organs that require precise control over material deposition.

2. **Hardest Technical Difficulties (...

---

### P79: Artificial intelligence-augmented bioprinting systems: Data-driven optimization 

**DOI**: 10.36922/IJB025350349
**Best distance**: 0.696
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P79 chunk_11, d=0.696]_

Machine  learning  models  can  serve  multiple  purposes within  bioprinting  workflows. 138 Predictive  models  are trained to forecast biological responses, such as drug efficacy or toxicity, based on construct features and experimental parameters. 139,140 Optimization  models,  often  employing reinforcement  learning  or  Bayesian  optimization,  can identify  optimal  combinations  of  printing  parameters, bioink  compositions,  and  culture  conditions  to  achieve desired  outcomes. 128,141 In  addition,  generative  models, such as variational autoencoders and generative adversarial networks, can be used to design novel tissue architectures with  tailored  functional  properties. 136,142 The  choice  of algorithm depends on the prediction target, dataset size, and desired interpretability.

## 4.3. Closed-loop feedback and real-time adaptation

A defining feature of truly 'smart' bioprinting systems is the  implementation  of  closed-loop  feedback,  where  ML models continuously analyze experimental data and adjust bioprinting  parameters  in  real  time. 143,144 For  example,  if imaging data indicate uneven cell distribution or structural collapse,  the  system  can  a...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

**Research Background (Page 1-2):**
"The high attrition rate of drug candidates in clinical trials is often attributed to the use of conventional two-dimensional cell cultures and animal models that fail to accurately recapitulate human physiology. Three-dimensional (3D) bioprinting has emerged as a transformative technology for creating sophisticated, patient-relevant tissue models for drug screening and toxicity assessment."

**Core Concepts (Pages 2-4):**
"Bioprinting refers to the automated, layer-by-layer fabrication of 3D biol...

**Core problem & critique:**
1) **Most Central Problem and Why It Matters:**
   - The most central problem addressed in this paper is the high attrition rate of drug candidates during clinical trials, which is often due to the limitations of conventional 2D cell cultures and animal models. These traditional methods fail to accurately replicate human physiology, leading to poor predictive power for pharmacological assessments (Page 1). Addressing this issue through advanced technologies like bioprinting combined with machine learning can significantly improve drug development efficiency and reduce costs by providing more a...

---

### P124: 3D-printed multifunctional materials enabled by artificial-intelligenceassisted 

**DOI**: 10.1038/s41578-020-00235-2
**Best distance**: 0.712
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P124 chunk_31, d=0.712]_

*Fig. 5 | 3D printing with closed-loop correction and 3D printing on moving targets. a | Schematic image of the hardware set-up for in situ droplet inspection and closed-loop control of the inkjet-printing process (left). Workflow of a vision-based feedback-control algorithm (right). b |  Workflow of a closed-loop feedback-control algorithm based on a convolutional neural network (CNN) model. c |  Workflow of a layer-wise printing-correction algorithm, with the current layer mask encoding the spatial information of where material is expected to be placed in the current layer (top). Printing correction (bottom). d | In situ 3D printing on a human hand and the resulting 3D-printed alginate hydrogel on the hand. e | 3D rendering of an in situ printing system based on a delta 3D-printing robot (left). 3D printing of an inductive coil on a human hand (right).*

Thickness
(
μ
m)
Monitor
camera
Tracking
camera
Delta 3D
printer
e
f
d
c
a
b
Tracking
camera
Illumination
system
Compute
current
layer mask
Compute
depth within
the mask
Compute
difference with
the model
Compute and
print correction
layer
-71
-35
-0
Before correction
Correction mask
After correction
Satellite
Properties
Features
...

**Background (from SOP metadata):**
Based on the provided text from the research paper, here are the extracted sections:

1) **Research Background** (Page 27-28)
"3D-printing technologies have been in development since the early 1980s and range from fused-filament fabrication of intricate plastic structures to next-generation technologies such as direct ink writing and inkjet printing. These latter approaches can interweave a range of functional materials beyond hard plastics, such as conductors, semiconductors, tissue-mimicking soft materials and cell-laden biomaterials (Fig. 1a). With its inherent customizability and rapid pro...

**Core problem & critique:**
1) **Most Central Problem and Why It Matters:**
The most central problem addressed in this paper is the challenge of fabricating 3D-printed multifunctional wearables and implantables directly on complex, non-planar surfaces such as those found within living organisms. This matters because conventional ex situ printing methods face significant limitations when applied to dynamic biological environments due to issues like geometric mismatches, contamination risks, and difficulties in handling delicate materials. Addressing this problem could enable the creation of personalized medical devices th...

---

### P119: Advancing 3D bioprinting through machine learning and artificial intelligence

**DOI**: 10.1016/j.bprint.2024.e00331
**Best distance**: 0.755
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P119 chunk_20, d=0.755]_

Process control, on the other hand, involves making real-time adjustments based on the data obtained from monitoring. This includes adjusting the extrusion rate, printhead motion, and other relevant parameters to maintain the desired characteristics of the bioprinted parts. For instance, Armstrong et al. integrated a non-contact laser displacement  scanner  into  the  printing  platform  to  print  parts  with  lowdimensional errors [16]. The system scans the material placement and compares it with the as-designed reference path, generating an error vector  to  modify  the  axis  reference  trajectory  for  the  second  print S. Ramesh et al.
iteration. Control systems integrated in commercial bioprinters involve pre-set adjustments to account for rheological behavior. Nevertheless, these  are  not  real-time  and  can  result  in  material  accumulation  and defects due to response delays [224,225].
The integration of ML in 3D bioprinting has opened monitoring and control possibilities. It is currently feasible to develop closed-loop control systems that can autonomously adjust printing parameters, utilizing real-time  feedback  from  sensors  monitoring  various  aspects  of  the...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

**Research Background:**
The research background is encapsulated in the introduction and overview of bioprinting technologies. It highlights that 3D bioprinting, a branch of additive manufacturing (AM), creates three-dimensional biological structures by layering biomaterials and living cells [1-3]. Bioprinting has advanced bioengineering, offering avenues to improve transplantation methods by creating personalized tissues and organs [4,5], facilitating advanced drug testing [6,7], developing in vitro models for disease research and ...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters (Page 2-5):**
   The central problem addressed in this paper is the integration of machine learning (ML) and artificial intelligence (AI) into 3D bioprinting to enhance process efficiency, material selection, parameter optimization, real-time monitoring, and system-wide challenges. This matters because it aims to overcome current limitations in scalability, automation, and data management that hinder the widespread adoption of 3D bioprinting technologies for tissue engineering, drug testing, disease modeling, and other applications.

2. **Hardest Te...

---
