# Section X.3.3.2: Process-state classification / online process visibility

**Target words**: 200
**Query**: `bioprinting process state classification segmentation real-time imaging CNN U-Net`
**Generated**: 2026-05-13T14:51:29.983286

---

## Part A: Explicitly cited references in outline (with content)

### Quick index

- ✅ **P65** — `10.1016/j.addma.2021.102251` (in library)
- ✅ **P21** — `10.18063/ijb.v8i4.620` (in library)
- ❌ `10.48550/arXiv.2509.06690` (NOT in library — need to ingest separately)
- ✅ **P68** — `10.1007/s10845-023-02167-4` (in library)

### Detailed content per cited paper

#### 🎯 P65: In situ process monitoring and automated multi-parameter evaluation using optica

**DOI**: 10.1016/j.addma.2021.102251

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P65 chunk_0, d=0.874]_

## 1. Introduction

As a technique in tissue engineering, three-dimensional (3D) bioprinting follows the typical 3D printing process, which involves generating a computer-aided design (CAD) model, converting it to a STL file, slicing and finally printing [1]. With its potential to fabricate 3D biomimetic  functional  tissue  constructs  and  organs,  3D  bioprinting  has been applied in organ printing [2], microvasculature printing [3], disease modeling [4] , and scaffold fabrication for tissue regeneration [5,6]. In  the  past  decade,  the  number  of  3D  bioprinting  publications  has increased by 6400% according to the analysis in the Web of Science, and the rapid growth is partially driven by the need of organ transplantation and accurate tissue models for drug screening and medical mechanism studies [7]. A milestone in tissue engineering was the development of 3D scaffolds that guide cells to form functional tissue. In 3D scaffold bioprinting, a combination of cells and biomaterials is usually employed as the printing precursor. As templates for cell interaction, scaffolds can provide physical support to the freshly developed tissue. In addition, scaffolds can serve as deliv...

_[P65 chunk_2, d=0.876]_

According to different prototyping principles and printing materials, 3D bioprinting mainly follows three approaches: droplet-based, extrusion-based,  and  photocuring-based  bioprinting  [7].  Among  them, extrusion-based  bioprinting  which  has  been  widely  used  in  scaffold fabrication, employs a pneumatic, mechanic or ram extruder to extrude or dispense materials and other biological molecules. Extrusion-based bioprinters  can  deposit  various  biopolymers,  and  multiple  cell  types encapsulated in hydrogels in a defined trajectory to produce constructs with specific biological features [9]. The wide selection of biomaterials and low-cost equipment are among the main advantages of extrusion-based  bioprinting  [10] . In  extrusion-based  bioprinting,  the rheologic properties of the ink, the extrusion rate and mechanical motion error should be carefully tuned to maintain a sufficient morphology and stiffness for scaffold fabrication. A constant extrusion rate causes material over-extrusion during the acceleration and deceleration phases of the printing head, especially during corner rounding. Comminal et al.
Contents lists available at ScienceDirect

## Additive Manufact...

_[P65 chunk_3, d=0.923]_

In much of the previous work related to in situ monitoring in 3D printing, metal additive manufacturing has been mainly explored with high-speed  visible  or  infrared  cameras,  especially  in  selective  laser melting  [12].  In  addition  to  two-dimensional(2D)  image  monitoring, high-precision metrology based on structured light and 3D digital image correlation have been further studied in laser beam melting and fused deposition modeling. Although 3D surface reconstruction can be achieved layer by layer, the integration system for imaging are complex and cumbersome [13,14]. In extrusion-based bioprinting, Armstrong et al. implemented  a  process  monitoring  with  a  compact  laser  scanner  to measure errors, and provided a control strategy to intelligently update the process control inputs in order to reduce defects and improve spatial fidelity [6,15,16]. However, it still has some surface profile measurement limitations,  such  as  the  inability  to  penetrate  and  detect  inner defects.
Micro-computed tomography ( μ CT) was identified as having various key advantages over other techniques, such as its non-destructiveness and the ability to assess many 3D parameters beca...

_[P65 chunk_1, d=0.925]_

In three-dimensional (3D) bioprinting, errors during the printing process leads to lower structural fidelity, and the desired structural and functional performances cannot be fully satisfied. Process monitoring with high-speed imaging techniques is helpful for identifying material deposition errors. 3D reconstruction of printed objects enables comprehensive evaluation of structural characteristics, with wide-field full-depth imaging being necessary for large objects. In this study, we demonstrate 3D extrusion-based bioprinter-associated optical coherence tomography (3D P-OCT) to achieve high-speed, wide-field and full-depth imaging, and provide in situ process monitoring and comprehensive evaluation for 3D bioprinting. In 3D P-OCT, a wide field was achieved with a lateral image mosaic using the simplified iterative closest point algorithm, and the extension of imaging depth was achieved with a longitudinal image mosaic using image fusion based on maximum intensity values. During the  printing  process,  3D  P-OCT  enables  real-time  multi-parameter  quantification  for  intelligent  feedback.  In conclusion, with in situ process monitoring and evaluation, 3D P-OCT contributes to e...

_[P65 chunk_5, d=0.967]_

In this study, a pneumatic-based extrusion printing system associated with OCT (P-OCT) was developed for in situ process monitoring and quality assessment during scaffold fabrication. In P-OCT, an OCT probe was mounted next to the print nozzle with very little additional space, and OCT imaging can be performed alternately with the printing process layer by layer. Based on the traditional advantages of OCT, such as its non-destructiveness, and label-free and high-resolution imaging, a widefield and full-depth imaging strategy was specially designed for largevolume constructs. In wide-field imaging, the checkerboard scanning protocol  was  adopted,  and  the  overlapped  areas  were  extracted  for lateral fine registration based on point cloud registration. For full-depth imaging, the stacking scanning protocol was used for longitudinal image fusion with the gray value maximum method. Furthermore, a custom image processing script was developed using wide-field, full-depth OCT data to provide multi-parameter in situ monitoring, including layer-tolayer  thickness  (LT),  filament  size  (FS),  and  pore  size  (PS).  By comparing the measured parameters with the designed model, intell...

**Background:**
Based on the provided research paper, here are the extracted sections:

1. **Research Background** (Page 1-2)
   > "In three-dimensional (3D) bioprinting, errors during the printing process leads to lower structural fidelity, and the desired structural and functional performances cannot be fully satisfied. Process monitoring with high-speed imaging techniques is helpful for identifying material deposition errors."

2. **Core Concepts** (Page 1-4)
   > "In this study, we demonstrate 3D extrusion-based bioprinter-associated optical coherence tomography (3D P-OCT) to achieve high-speed, wide-fiel...

**Core problem:**
1. **Most Central Problem and Why It Matters**

The most central problem addressed in this paper is the lack of real-time process monitoring and feedback during 3D bioprinting, which leads to structural inaccuracies and reduced functional performance of printed scaffolds. This matters because accurate and consistent fabrication of tissue-engineered constructs is crucial for their successful application in regenerative medicine and organ transplantation.

2. **Hardest Technical Difficulties**

The hardest technical difficulties include achieving wide-field and full-depth imaging with high resol...

---

#### 🎯 P21: A Deep Learning Quality Control Loop of the Extrusion-based Bioprinting Process

**DOI**: 10.18063/ijb.v8i4.620

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P21 chunk_7, d=0.851]_

For example, Jin et al. used a CNN to implement a real-time feedback loop on solid (no infill) FDM-printed layer.  The  authors  identified  three  main  classes  (i.e., under-extrusion,  over-extrusion,  and  good  quality)  and built a dataset of images using a top view of the printing process. The collected data were used to test and validate the  DL  model,  reaching  a  high  classification  accuracy (around 98%) [31] . In another work, Tonnaer et al. tackled the  problem  of  detecting  anomalies  on  the  surface  of FDM-printed  parts  using  a  semi-supervised  approach. The  authors employed  a  variational autoencoder, a type  of  deep  architecture  which,  when  trained  with images from non-faulty parts, can learn their probability distribution. When fed with images from error containing parts, the model can then assign a value to those images representing the probability that they come from the same distribution of non-faulty images. As a result, by setting a proper threshold, the model can effectively distinguish between  good  and  erroneous  prints [32] .  The  work  by Zhang et al. highlighted how  multiple information coming from different sensors can be integra...

_[P21 chunk_6, d=0.894]_

The properties of DNNs make them good candidates for multiple applications in the field of AM, including: (i) designing new composite materials and topologies (e.g., given  a  target Young's  modulus,  optimize  the  structure to  achieve  it  considering  the  constraints  of  AM),  (ii) optimizing the process parameters, and (iii) monitoring the printing process to detect defects (e.g., cracks, delamination,  and  porosity) [24,25] .  Regarding  these  last two points, several works have focused on applying DL to  fused  deposition modeling (FDM) [26,27] ,  inkjet [28] ,  and powder sintering/melting processes [29,30] .
For example, Jin et al. used a CNN to implement a real-time feedback loop on solid (no infill) FDM-printed layer.  The  authors  identified  three  main  classes  (i.e., under-extrusion,  over-extrusion,  and  good  quality)  and built a dataset of images using a top view of the printing process. The collected data were used to test and validate the  DL  model,  reaching  a  high  classification  accuracy (around 98%) [31] . In another work, Tonnaer et al. tackled the  problem  of  detecting  anomalies  on  the  surface  of FDM-printed  parts  using  a  semi-super...

_[P21 chunk_0, d=0.899]_

## 1. Introduction

In recent years, the field of bioprinting has seen a strong increase of interest as a promising solution to fabricate tissues and organs for tissue engineering applications [1,2] . Among the technologies  currently  available,  extrusionbased bioprinting  (EBB)  has  been  adopted  as  the  most popular  approach  thanks  to  its  simple  and  affordable hardware, a wide array of processable materials, and the ability  to  print  clinically  sized  constructs [3] .  The  typical EBB  set-up  consists  of  an  extrusion  tool-head,  either mechanical  (i.e.,  piston  actuated  and  screw  assisted) or  pneumatic,  which  is  attached  to  a  three-dimensional (3D) positioning system. By applying a pressure on the material (usually a hydrogel) inside a reservoir (usually a syringe) while moving it over a printing plate, a 3D shape can be obtained in a layer-by-layer fashion [4,5] .
Significant  efforts  have  been  made  to  develop novel biomaterial inks [6] that  show  enhanced  biological response  and  appropriate  physical-chemical  properties for the target tissue, while also being processable through EBB with good printability (i.e., a combination of severa...

_[P21 chunk_5, d=0.924]_

To  overcome  these  limitations,  researchers  have moved  toward  DL  and  deep  neural  networks  (DNNs), which have demonstrated to scale much better with the increase of data size [21] . In general, DL algorithms can be classified into three main groups depending on the type of data available. In supervised learning, the network is used as a binary or multiclass classifier using labeled data instances. Semi-supervised models use a small amount of labeled data together with a larger amount of unlabeled data,  while  in  unsupervised  learning,  no  labeled  data are  available [22] .  At  its  core,  DNNs  use  a  complex composition of linear  and  non-linear  functions  to  learn an expressive representation of the data. The term 'deep' refers to stacking multiple layers (i.e., a set of neurons) to obtain more complex function approximators [23] .  The type of layer to be used in a neural network depends on the type of data and processing of interest. For example, the  basic  architecture  of  a  CNN,  designed  to  operate on data in array format (e.g., a stack of three 2D arrays corresponding  to  the  pixel  values  of  a  color  image),  is given  by  the  repetition  of ...

_[P21 chunk_14, d=0.928]_

*Table 3. Summary of the optimized parameters as well as other relevant hyperparameters for the training process*

The subscript i in the Equations II and III indicates one of the three classes. For example, the precision for the  'ok'  class  is  defined  as  the  ratio  between  the  'ok' frames classified as 'ok' (true positives, TP i in Equation II) over the overall number of frames classified as 'ok' (sum of true  positives, TP i ,  and  false  positives, FP i ,  in Equation III). This last term may include frames that were classified as 'ok,' but their 'true' value is from another of the two remaining classes.
Finally, although metrics are useful to quantitatively evaluate  model  performance,  it  is  also  important  in practice to verify that the model is behaving as expected. To  this  end,  we  first  tested  its  performance  by  taking snapshots  of  the  same  print  under  different  conditions, including  different  zoom  and  focus  levels.  For  each snapshot,  we  verified  that  the  model  was  predicting the  image  class  correctly  and  consistently.  Then,  we employed the gradient-weighted class activation mapping (grad-CAM)  technique  to  verify  that  t...

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

_[P68 chunk_1, d=0.867]_

Over the years, there is an increased interest in the use of 3D bioprinting  technologies  for  tissue  engineering,  regenerative medicine, and biomedical applications due to its exceptional ability to precisely deposit highly viable cells during the bioprinting process to fabricate biomimetic 3D tissueengineered constructs (He et al., 2021; Levato et al., 2020; Ng et al., 2016a, 2019, 2020a; Sun et al., 2020). These 3D bioprinting technologies can be categorized into 3 distinct groups  according  to  the ASTM  standards  -  jetting-based (Choe  &  Kim,  2020;  Li  et  al.,  2020b;  Ng  et  al.,  2016b), extrusion-based (Meng et al., 2020; Ng et al., 2014; Ozbolat and Hospodiuk, 2016) and vat photopolymerization-based (Li et al., 2020a;  Ng et al., 2020b). Each bioprinting technology has its distinctive advantages and limitations and the selection  of  an  appropriate  bioprinting  technology  should
Xi Huang and Wei Long Ng have contributed equally towards this paper.
- Wei Long Ng ng.wl@ntu.edu.sg
- Wai Yee Yeong wyyeong@ntu.edu.sg
1 HP-NTU Digital Manufacturing Corporate Lab, Nanyang Technological University (NTU), 65 Nanyang Drive, Singapore 637460, Singapore
2 Singapore Centr...

_[P68 chunk_2, d=0.870]_

be dependent on its intended application (Lee et al., 2019). The  key  advantages  of  each  bioprinting  technology  are as  follows:  the  jetting-based  bioprinting  approach  facilitates contactless on-demand bioprinting of different living cells and biomaterials to enhance cell-cell and cell-matrix interactions (Ng et al., 2017a, 2018b), the extrusion-based bioprinting approach facilitates printing highly viscous bioinks with fast fabrication speed (Yang et al., 2022; Zhuang et  al.,  2019),  and  lastly  the  vat  polymerization-based  bioprinting approach can achieve high printing resolution and printable cell concentration (Nieto et al., 2020).
For bioprinting applications, the living cells are usually encapsulated  within  hydrogel-based  bio-inks  and  printed using  different  bioprinting  technologies  which  have  their own  specific  bio-ink  requirements.  The  printed  cells  in jetting-based bioprinting approach are usually encapsulated within un-crosslinked bio-inks of low viscosity (Ng et al., 2022, 2023), whereas the printed cells in  extrusion-based and  vat  polymerization-based  bioprinting  approaches  are usually encapsulated within highly-viscous crosslink...

_[P68 chunk_6, d=0.902]_

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

_[P68 chunk_4, d=0.904]_

Hence, the goal of this study is to utilize machine learning approaches on high-speed images captured to predict the number of encapsulated cells  during  the  droplet  bioprinting process. Machine learning is a subset of artificial intel -ligence  which  can  identify  the  relationship  between  large datasets  efficiently,  resulting  in  a  model  that  is  useful  in the prediction of new inputs (Xames et al., 2022). Machine learning is useful when statistical relationships exist in the dataset but the model for the dataset cannot be determined analytically, such as optimizing printing parameters (Bonatti et  al.,  2022;  Fu  et  al.,  2021;  Law et al., 2023), predicting the cell viability from the process parameter and identifying the significant process parameters for high cell viabil -ity  (Xu  et  al.,  2022).  There  are  three  basic  approaches  to apply machine learning for different situations; supervised learning (Caruana & Niculescu-Mizil, 2006), unsupervised learning (Ghahramani, 2004; Hastie et al., 2009), and reinforcement learning (Arulkumaran et al., 2017; Kaelbling et al., 1996; Wiering & Van Otterlo, 2012). Supervised learning creates a model from labeled da...

_[P68 chunk_28, d=0.928]_

The main goal of this work is to demonstrate the possibility of using droplet velocity at 2 different points along the nozzle-substrate distance to predict the number of printed cells  within  each  ejected  droplet  during  the  inkjet-based bioprinting process. This work demonstrates two different applications  such  as  cell  detection  within  single  droplets (presence/absence of cells) and prediction of the total number of printed cells within multiple droplets by comparing 5 machine learning algorithms to determine the performance of  each  model.  The  first  method  predicts  the  presence  of a  cell  in  a  single  droplet  with  an  accuracy  of  82%  when the velocity of the droplet at 1.0 and 2.0 mm are taken as input  through  random  forest  regression.  This  method  is suitable  for  droplets  with  low  cell  occupancy  but  is  inaccurate for droplets with high cell occupancy (more than 0.1 cell per droplet). The second method reduced the error in the cell count prediction by a factor of √ N through cell count prediction in N droplets instead of single droplet. In the validation set, a mean error of 12% for cell counts in 20 droplets with high cell occupancy (1....

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

### P90: The Synergy of Artificial Intelligence and 3D Bioprinting: Unlocking New Frontie

**DOI**: 10.1002/adfm.202509530
**Best distance**: 0.639
**Chunks retrieved**: 2

**Retrieved chunks:**

_[P90 chunk_46, d=0.639]_

Recent advancements in CNN and DL have significantly impacted the field of bioprinting, offering new approaches for optimizing and automating various stages of bioprinting processes. One notable example is the work by Bonatti et al., who developed a DL-based CNN quality control system for EBB. [47] By leveraging CNNs, their system was able to optimize bioprinting parameters and monitor the process using machine vision in real time. Highresolution video data of different bioprinting outcomes, such as under-extrusion or over-extrusion, were recorded and used to train the CNN model. This allowed the system to predict print quality as 'ok,' 'under extrusion,' or 'over extrusion,' reaching above 90% of accuracy, and make automatic adjustments to bioprinting parameters, which significantly reduced bioink waste and improved overall print fidelity. This innovative integration of machine vision with CNNs sets the stage for a fully automated quality control loop, ensuring consistent and reliable bioprinting outcomes.
Tebon et al. introduced a novel pipeline combining bioprinting, high-speed live cell interferometry (HSLCI), and ML for high-throughput drug screening at the single-organoid lev...

_[P90 chunk_47, d=0.722]_

16163028, 2026, 1, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/adfm.202509530 by NICE, National Institute for Health and Care Excellence, Wiley Online Library on [11/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License www.advancedsciencenews.com innovations in the field. DL models are proving instrumental in overcoming challenges related to print fidelity, tissue development, and organoid analysis, setting the stage for future advancements in personalized medicine and bioprinting technologies.
ADVANCED
SCIENCENEWS

*Figure 13. A) Architecture of a CNN for image analysis and feature extraction. The network processes an input image through two convolutional layers for feature detection, each followed by a pooling layer to reduce spatial dimensions. The features are then flattened into a 1D vector and passed through a fully connected layer for classification and regression tasks. The output includes type classification and coordinate predictions ( x, y , and volume), showcasing the network's ability to perform ...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

**Research Background:**
The review examines the transformative role of artificial intelligence (AI) in 3D bioprinting, focusing on how advanced AI technologies enhance its precision, functionality, and scalability. The integration of AI enables automated quality control and predictive maintenance, improving bioprinting outcomes by increasing cell viability and structural fidelity, and reducing the amount of bioink wasted.

**Core Concepts:**
AI involves the development of algorithms and systems that allow machines to perform tasks ...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters**
   - The most central problem addressed in this paper is the challenge of achieving precise control over cell deposition during 3D bioprinting, which is crucial for ensuring the functionality and viability of printed tissues. This matters because accurate placement of cells is essential for replicating complex biological structures with intricate microarchitectures such as capillaries, nerve networks, and osseous tissue (Page 1). Without precise control, the structural integrity and biological function of bioprinted constructs can be compromised, ...

---

### P5: Challenges and Advances in 3D Bioprinting for Tissue Engineering and Regenerativ

**DOI**: 10.1002/adfm.202509530
**Best distance**: 0.640
**Chunks retrieved**: 3

**Retrieved chunks:**

_[P5 chunk_45, d=0.640]_

Recent advancements in CNN and DL have significantly impacted the field of bioprinting, offering new approaches for optimizing and automating various stages of bioprinting processes. One notable example is the work by Bonatti et al., who developed a DL-based CNN quality control system for EBB. [47] By leveraging CNNs, their system was able to optimize bioprinting parameters and monitor the process using machine vision in real time. Highresolution video data of different bioprinting outcomes, such as under-extrusion or over-extrusion, were recorded and used to train the CNN model. This allowed the system to predict print quality as 'ok,' 'under extrusion,' or 'over extrusion,' reaching above 90% of accuracy, and make automatic adjustments to bioprinting parameters, which significantly reduced bioink waste and improved overall print fidelity. This innovative integration of machine vision with CNNs sets the stage for a fully automated quality control loop, ensuring consistent and reliable bioprinting outcomes.
Tebon et al. introduced a novel pipeline combining bioprinting, high-speed live cell interferometry (HSLCI), and ML for high-throughput drug screening at the single-organoid lev...

_[P5 chunk_46, d=0.722]_

16163028, 2026, 1, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/adfm.202509530 by NICE, National Institute for Health and Care Excellence, Wiley Online Library on [20/04/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License www.advancedsciencenews.com innovations in the field. DL models are proving instrumental in overcoming challenges related to print fidelity, tissue development, and organoid analysis, setting the stage for future advancements in personalized medicine and bioprinting technologies.
ADVANCED
SCIENCENEWS

*Figure 13. A) Architecture of a CNN for image analysis and feature extraction. The network processes an input image through two convolutional layers for feature detection, each followed by a pooling layer to reduce spatial dimensions. The features are then flattened into a 1D vector and passed through a fully connected layer for classification and regression tasks. The output includes type classification and coordinate predictions ( x, y , and volume), showcasing the network's ability to perform ...

_[P5 chunk_13, d=0.725]_

An important aspect of bioprinting involves scanning and analyzing medical data to reconstruct tissues or organs. However, processing these scanned data, which includes segmentation and reconstruction, can be hard and error-prone due to the limitation on 3D perceptions of 2D images. CV algorithms are capable of segmenting 3D images, such as those of the liver, heart, and brain, and enhancing the final resolution of scans [ 55,56] (Figure 3B). At this stage, CV and computer graphics are significant. While CV algorithms automate and improve the segmentation and identification of anatomical features from the scans, computer graphics techniques reconstruct these features into highly accurate 3D models. Advances in commercial software, like those equipped with ML and DL, have also been shown to improve the accuracy of organ segmentation and anomaly detection, providing automated solutions with a success rate of 98.8%. [ 57]
Kengla et al. integrated medical imaging with bioprinting to create patient-specific bone constructs. [ 58] They used CV to convert patient anatomy into bioprinted constructs, ensuring that shapes and architectures matched the individual's anatomy. Using 3D scanners,...

**Background (from SOP metadata):**
The research paper examines the transformative role of artificial intelligence (AI) in 3D bioprinting and how advanced AI technologies enhance precision, functionality, and scalability. Key challenges in traditional bioprinting include achieving precise cell placement, real-time process monitoring, quality control, and managing bioink variability. These limitations hinder the production of complex tissues with high fidelity and consistency.

The paper aims to address these issues by integrating various branches of AI such as machine learning (ML), computer vision (CV), robotics, natural langua...

**Core problem & critique:**
The paper explores the transformative role of artificial intelligence (AI) in 3D bioprinting and its potential to enhance precision, functionality, and scalability. The central problem addressed is the technical challenge of achieving precise control over cell deposition and maintaining high-quality tissue fabrication despite biological variability and mechanical limitations inherent in current bioprinters. This issue is significant because it hinders the transition from laboratory settings to clinical applications where reproducibility and reliability are paramount.

One of the hardest techni...

---

### P99: Optimizing 3D Bioprinting Using Advanced Deep Learning Techniques A Comparative 

**DOI**: 10.1002/9781394204878.ch8
**Best distance**: 0.640
**Chunks retrieved**: 4

**Retrieved chunks:**

_[P99 chunk_4, d=0.640]_

In 3D bioprinting, CNN can be trained on a data set of 3D images of printed structures, such as tissue samples. The network can then be used to classify different types of cells, such as stem cells or mature cells, or to identify defects in the printed structures. CNN can also be used to segment the different parts of the structure, such as the vasculature or the extracellular matrix. It's worth noting that CNN is not the only type of deep learning algorithm that can be used for 3D image analysis and segmentation, other algorithms, such as U-Net and 3D-CNN are also being used in this field and are showing promising results.

## 8.3 RNN in Optimization of 3D Bioprinting

Recurrent neural networks (RNN) are a kind of deep learning algorithm that  is  especially  well-matched  for  particular  tasks  involving  sequential data,  such  as  time-series  analysis  [5].  In  the  context  of  3D  bioprinting, RNN can be used to model and predict the behaviour of cells and tissues over time, based on the printing conditions and other factors. This can be useful for optimizing the printing process and for predicting the long-term behaviour of the printed structures. Unlike traditional feedf...

_[P99 chunk_15, d=0.642]_

Advanced deep learning techniques, such as CNN, RNN, and GAN, can be effectively used to optimize 3D bioprinting. CNNs can be used for image analysis  and  segmentation,  quality  control,  and  other  tasks  that  involve analysing  2D  images.  RNNs,  particularly  LSTM  architecture,  are  wellsuited for monitoring and predicting the printing process, and for predictive maintenance. GANs can be used for generating new 3D models or for improving the resolution of 3D images.
Using  these  techniques,  3D  bioprinting  precision,  accuracy,  and  efficiency can all be improved, which can ultimately lead to better outcomes in regenerative medicine, tissue engineering, and other fields. However, it's important to note that the implementation of these techniques requires a good understanding of the 3D bioprinting process, the data, and the deep learning  techniques,  as  well  as  the  ability  to  evaluate  and  interpret  the results.
10.1002/9781394204878.ch8, Downloaded from https://onlinelibrary.wiley.com/doi/10.1002/9781394204878.ch8 by University College London, Wiley Online Library on [17/03/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditi...

_[P99 chunk_13, d=0.683]_

## 8.13 Process of Combined Model

Data Preparation is the first step in optimizing 3D bioprinting using deep learning techniques. We must acquire and prepare the appropriate data to train and test the algorithms. For image analysis and segmentation using a CNN, the 3D Slicer Medical Image Segmentation dataset is publicly available and contains 3D images of various structures such as organs and blood vessels, along with their corresponding segmentation masks. This dataset can be used to train the CNN to identify specific structures in images. For monitoring and predicting the printing process using RNN Long ShortTerm Memory (LSTM), sensor data such as temperature, pressure, and movement of the printing head should be collected in real time during the printing process.
Next, we need to choose a network architecture for the optimization of 3D bioprinting. A popular choice for image analysis and segmentation is  a  U-Net  architecture,  as  it  is  well-suited  for  this  task  and  can  handle 3D data. The U-Net contains an encoder network, which extracts features from the input image, that generates the segmentation mask. For monitoring and predicting the printing process, a popular...

_[P99 chunk_3, d=0.702]_

Generative Adversarial Networks (GAN), Recurrent Neural Networks (RNN), and Convolutional Neural Networks (CNN) can learn from large amounts  of  data  and  make  predictions  or  generate  new  data.  Recent trends and advances in 3D bioprinting optimization using deep learning include the use of CNN for image analysis and segmentation, RNN for monitoring  and  predicting  the  printing  process,  and  GAN  for  generating 3D models and design optimization. A range of datasets is being used for deep learning-based 3D bioprinting optimization, including medical imaging datasets for image analysis, sensor data from the printing process, and  datasets  of  3D  models  of  structures  to  be  printed.  The  availability of  large  datasets  and  advances  in  computation  power  has  enabled  these deep learning-based approaches to be applied to 3D bioprinting. Overall, deep  learning-based  approaches  have  the  potential  to  revolutionize  3D bioprinting by enabling the optimization of the printing process and the design of new structures. However, these techniques are still in starting stage of establishment and further to realize their full potential research is needed.
10.1002/...

**Background (from SOP metadata):**
Certainly, here is the extracted information from the provided text:

### 1. Research Background

**Page 158:**
"3D bioprinting is a rapidly growing field that uses advanced technology to create 3D structures that mimic the complex architecture and function of living tissue."

**Page 160:**
"In 3D bioprinting, CNN can be trained on a data set of 3D images of printed structures, such as tissue samples. The network can then be used to classify different types of cells, such as stem cells or mature cells, or to identify defects in the printed structures."

**Page 162:**
"In 3D bioprinting, GAN ca...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters (Page 158)**: The central problem addressed in this paper is optimizing the 3D bioprinting process using advanced deep learning techniques such as CNN, RNN, and GAN. This matters because improving the accuracy, efficiency, and scalability of 3D bioprinting can significantly advance fields like regenerative medicine and tissue engineering by enabling more precise and functional printed tissues.

2. **Hardest Technical Difficulties (Pages 160-172)**: The hardest technical difficulties include effectively integrating multiple deep learning models to op...

---

### P18: BioLite U-Net: Edge-Deployable Semantic Segmentation for In Situ Bioprinting Mon

**DOI**: _missing_
**Best distance**: 0.687
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P18 chunk_2, d=0.687]_

Efforts to further optimize U-Net have produced various lightweight U-Net architectures. Chen et al. [20] introduced a cascaded multi-receptive-field version of UNet with significantly fewer parameters while maintaining high Dice scores in medical segmentation. Okman et al. [21] proposed L 3 U-net, which runs real-time segmentation ( ≈ 10 FPS) on low-power CNN accelerators like the MAX78000. JetSeg [22], designed for Jetson Xavier, demonstrates strong real-time throughput with lightweight encoderdecoder blocks and optimized depthwise-dilated convolutions. Additionally, hardware-aware segmentation research has demonstrated promising performance on constrained platforms. Posso et al. [23] benchmarked a compact U-Net on CPU, GPU, and FPGA platforms, showing substantial latency improvements through hardware-specific optimization. Similarly, Kwon et al. recently introduced HARD-Edge, achieving real-time (33 FPS) semantic segmentation on ARM Cortex-M microcontrollers [24].
In summary, while classification and thresholding methods have been applied in bioprinting monitoring, real-time dense semantic segmentation remains largely unexplored. Our work builds on advances in lightweight CNNs a...

**Background (from SOP metadata):**
Based on the provided text from the research paper "BioLite U-Net: Edge-Deployable Semantic Segmentation for In Situ Bioprinting Monitoring," here are the requested extracts:

1. **Research Background**
   - The background of this research is rooted in the field of bioprinting, which involves precisely depositing cell-laden bioinks to fabricate tissue and organ models.
     > "Bioprinting is a transformative technology at the intersection of tissue engineering, regenerative medicine, and additive manufacturing [1]–[3]. By precisely depositing cell-laden bioinks in a layer-by-layer manner, biop...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters:**
   The most central problem addressed in this paper is achieving real-time semantic segmentation for bioprinting monitoring on resource-constrained embedded hardware. This matters because it enables the development of intelligent, closed-loop bioprinting systems capable of adaptive control and real-time feedback, which can significantly improve print quality and reduce failure rates. Bioprinting requires precise control over extrusion processes, and real-time monitoring is essential for maintaining high-resolution spatial fidelity and structural ...

---

### P63: Autonomous Control of Extrusion Bioprinting Using Convolutional Neural Networks

**DOI**: 10.1002/adfm.202424553
**Best distance**: 0.721
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P63 chunk_11, d=0.721]_

www.afm-journal.de

## 2.2. Deployment of Trained Convolutional Neural Networks on Bioprinting Hardware for Real-Time Error Detection

Next, we evaluated CNN model accuracy on the physical bioprinting hardware setup with integrated computer vision ( Figure 3 a). Live imagery from the computer vision camera is more variable than the hold-out dataset as there are changes in lighting, unseen printing paths will be used, and minor visual artifacts can arise, such as dust and liquid droplets. The validation hardware comprises the modified printer previously described in section 2.1(Figure 3a (ii, iii)), a separate, more powerful computer (Macbook M1) running the Tensorflow backend for the CNN classification models (Figure 3a (v)), and a monitor for live analysis of the print by the operator (Figure 3a (i)). The Raspberry Pi sends a vector representation of the Region of Interest (ROI) from the captured image over a User Datagram Protocol (UDP) packet to the computer, which is running a server awaiting these small images (Figure 3a (v)). The computer processes the image to undergo classification by the model running in Tensorflow, and a response is sent back to the Raspberry Pi containin...

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

### P102: The Emergence of Bioprinting and Computational Intelligence

**DOI**: 10.1002/9781394204878.ch1
**Best distance**: 0.731
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P102 chunk_18, d=0.731]_

One of the most promising applications of bioprinting is in the field of tissue engineering and regenerative medicine. Bioprinting technologies have been used to create functional, living tissues and organs that can be used for transplantation, and this has the potential to revolutionize the way that this study treat a wide range of medical conditions. For example, researchers have used bioprinting technologies to create functional liver tissue, heart tissue, and blood vessels, which can be used to repair or replace damaged or diseased tissue in patients. The nest exciting application of bioprinting is in drug development and testing. Bioprinted tissues and organs can be used to create more accurate and predictive models of human physiology, which can help researchers to develop new treatments and drugs more quickly and effectively. For example, researchers have used bioprinted tissues to test the efficacy and safety of new drugs, which can help to reduce the time and cost of drug development and ensure that new treatments are safe and effective for patients. In computational intelligence, there are also a number of exciting case studies that demonstrate the potential of these tech...

**Background (from SOP metadata):**
Based on the provided text, here's an extraction of the requested information:

### 1. Research Background

**Quote:**
"The enthralling era of computational intelligence and bioprinting technologies decides the future of the health care and biological world."

"Bioprinting deals with the high dimensional printing of the biomedical products like cells, tissues and even organs in a controlled environment, with high accuracy."

"In order to fully understand the intersection of bioprinting and computational intelligence, it is important to first have a good grasp of the basics of each technology. ...

**Core problem & critique:**
1) **Most Central Problem and Why It Matters:**
   - The most central problem addressed in this paper is the challenge of creating viable, functional tissues and organs through bioprinting. This matters significantly because it directly impacts the potential for regenerative medicine to provide solutions for patients suffering from organ failure or severe tissue damage. If bioprinted tissues can be made viable and functional, they could revolutionize medical treatments by providing personalized, patient-specific alternatives to traditional organ transplants.

2) **Hardest Technical Difficultie...

---
