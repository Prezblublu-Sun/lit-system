# Section X.3.3.1: Print pattern anomaly detection

**Target words**: 200
**Query**: `bioprinting anomaly detection over-extrusion under-extrusion filament defect computer vision`
**Generated**: 2026-05-13T14:51:29.635268

---

## Part A: Explicitly cited references in outline (with content)

### Quick index

- ✅ **P6** — `10.1016/j.procir.2022.06.040` (in library)
- ✅ **P66** — `10.1021/acsbiomaterials.0c01761` (in library)
- ✅ **P22** — `10.18063/ijb.v9i1.624` (in library)

### Detailed content per cited paper

#### 🎯 P6: In-situ monitoring of defects in extrusion-based bioprinting processes using vis

**DOI**: 10.1016/j.procir.2022.06.040

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P6 chunk_9, d=0.659]_

Accuracy in bioprinting process is currently limited by the lack of error monitoring techniques. Although the identification and the study of relationships between printing outcomes  and  process  parameters  were widely  investigated, repeatability  of  the  printing  process  is  still  far  from  being reached, especially in extrusion-based bioprinting[25]. Strauß, S. et al. used in their work non-invasive image-based analysis methods as tool for line construct characterization. It was an automated method to enable comparison of 3D printed lines to evaluate  the  influence  of  rheological  properties  and  printing parameters on them[16]. Armstrong et al. used point cloud data from a laser scanner to obtain images of the printed samples. They  then  use  a  custom  image  processing  algorithm  to determine the error between the reference and printed trajectory[11 -13]. A different approach was used by Wang, L. et al. In this study, optical coherence tomography was applied to  acquire  high-resolution  images  of  hydrogel  scaffolds.  An image analysis algorithm was proposed to accurately quantify some morphological parameters (pore size, pore shape, surface area, porosity, an...

_[P6 chunk_10, d=0.660]_

The method used in our work identified  drift  phenomena during the printing process. These were certainly more evident where the artificially added errors were introduced, with values of Over  Extrusion above  20%. These  errors could simulate rheological changes within bioinks, usually caused by uncontrolled changes in process parameters (temperature changes,  presence  of  bubbles,  etc.).  Drifting  processes  were also  detected  in 'in -control'  samples ,  where,  as  expected, increasing the layers perpetuated the pre-existing condition of excessively extruded material. In both cases we were able to build  a map of defects. The work  here presented  describe  a simple monitoring experiment in which the feasibility of using visible  imaging  for  geometry  detection  of  printed  constructs was demonstrated. More specifically,  we  have  demonstrated the effectiveness in being able to discriminate defect between layers. The automated monitoring system has proven to be able to  detect  defects  in deposition,  giving  to  the  operator  a  full understanding of the moment and the layer where the defect occurred, enabling the adoption of countermeasures in subsequent prints.
D...

_[P6 chunk_8, d=0.684]_

*Table 1. Results of visual inspection: green boxes show layers with minor  or  no  defects;  blue boxes  show  layers  where  errors  were manually added; red boxes show layers with major defects.*

Layer
Condition
Sample
1
2
3
4
5
6
7
8
9
10
𝑃𝑃 = 22 𝑘𝑘𝑃𝑃𝑘𝑘
𝑉𝑉 = 10 𝑚𝑚𝑚𝑚/𝑠𝑠
1
2
3
4
5

## 1.1. Image and statistical results

A  complete  dataset  of  50  images  has  been  obtained  and analyzed. Visual interpretation of all the obtained segmented and  binarized  images  (example  in  Figure  2)  confirmed  the suitability of the chosen value for k .
Each  image  was  automatically  divided  into  36  cells. For each cell, a value of Over Extrusion was obtained. Interval plots with 95% confidence intervals of the means of the 36 values of each layer are shown in Figure 4. The Over Extrusion metric showed an  increasing  trend  as  the  layers  increase in  all  the samples, even if with different slopes. It is possible to see that, although samples 1, 2 and 3 were ' in control ' , a slight drifting process in subsequent layers took place up to an Over Extrusion of 10%. Regarding sample 4 and 5 the introduction of major defects of over extrusion are clearly visible after layer 7, with...

_[P6 chunk_2, d=0.706]_

Nowadays, extrusion-based bioprinting is the most common and studied printing technology in the field, but, despite recent technological advances, the fabrication of good quality constructs remains a major challenge. The main limitations of extrusion bioprinted constructs are  the low spatial resolution and  the  low  accuracy  in  depositing  materials  (discontinuity, nonuniformity and irregularity[14]).
The  lack of quality assurance of parts produced  via bioprinting is a key technological barrier to the development of products of increasing complexity, like vascularization. Moreover,  the  development  of  non-destructive  monitoring systems  would  allow  the  implementation  of  in-line  control methods for the printing processes themselves.
Bioprinting technology is growing very fast and in the last few years the interest is increasing also in the industrial sector, from biopharmaceuticals to food[3]. While, from the biological point of view there are several vital and metabolic assays that can be used (although most of them are destructive tests), for metrological control of bioprinted constructs there is not a wide range of useful technologies implemented in both commerci...

_[P6 chunk_1, d=0.708]_

Bioprinting is an additive manufacturing (AM) technology whose goal is to fabricate parts that mimic the functionality of real  tissues  and  organs  by  combining  cells  and  biomaterials with a specific three-dimensional (3D) spatial organization. As in  traditional  AM,  the  goal  is  achieved  with  the  use  of computer-aided design (CAD) to generate 3D models of the geometry of the tissue or organ of interest in order to produce bioconstructs  that  have  many  applications  in  regenerative medicine,  tissue  engineering,  reconstructive  surgery,  drug discovery, pharmacokinetics, and  basic medical  and  cell biology research[1, 2]. Thus, one of the main challenges is to avoid the death of living cells not only during the process but also  in the  post-printing phases  where  the  geometry  of  the printed constructs can influence the feeding possibilities of the cells.
In  light  of  these  numerous  applications  and  due  to  the increasing  interest  in  personalized  medicine,  bioprinting  has gained the attention of both academia and industry in recent years[3].  During  the  last  decade,  many  new  techniques  and technologies related to bioprinting have emerge...

**Background:**
Based on the provided text, here are the extracted sections:

**Research Background:**
The research background is outlined in the Introduction and State of the Art sections. According to page 219:
"Bioprinting is an additive manufacturing (AM) technology whose goal is to fabricate parts that mimic the functionality of real tissues and organs by combining cells and biomaterials with a specific three-dimensional (3D) spatial organization."

**Core Concepts:**
The core concepts are detailed in the Introduction, State of the Art, and Materials and Methods sections. According to pages 219-220:
"Bio...

**Core problem:**
1. **Most Central Problem and Why It Matters (Page 220)**

The central problem addressed in this paper is the lack of effective quality assurance methods for bioprinting, particularly extrusion-based processes. This matters significantly because ensuring high-quality printed constructs is crucial for advancing applications in regenerative medicine, tissue engineering, reconstructive surgery, and drug discovery. Without reliable quality control measures, it's challenging to produce consistent and functional bioconstructs that can be used safely and effectively in clinical settings.

2. **Hardes...

---

#### 🎯 P66: Monitoring Anomalies in 3D Bioprinting with Deep Neural Networks

**DOI**: 10.1021/acsbiomaterials.0c01761

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P66 chunk_17, d=0.654]_

- Gobert, C.; Reutzel, E. W.; Petrich, J.; Nassar, A. R.; Phoha, S. Application of supervised machine learning for defect detection during metallic powder bed fusion additive manufacturing using high resolution imaging. Additive Manufacturing 2018 , 21 , 517 -528.
- Jin, Z.; Zhang, Z.; Ott, J.; Gu, G. X. Precise localization and semantic segmentation detection of printing conditions in fused filament fabrication technologies using machine learning. Additive Manufacturing 2021 , 37 , 101696.
- Hanakata, P. Z.; Cubuk, E. D.; Campbell, D. K.; Park, H. S. Accelerated search and design of stretchable graphene kirigami using machine learning. Phys. Rev. Lett. 2018 , 121 (25), 255304.
- Jin, Z.; Zhang, Z.; Gu, G. X. Automated Real-Time Detection and Prediction of Interlayer Imperfections in Additive Manufacturing
Processes Using Artificial Intelligence. Advanced Intelligent Systems 2020 , 2 (1), 1900130.
- Kim, S. H.; Lim, T. H.; Park, C. H. Silk Fibroin Bioinks for Digital Light Processing (DLP) 3D Bioprinting. In Bioinspired Biomaterials ; Springer: 2020; pp 53 -66, DOI: 10.1007/978-981-153258-0_4.
- Alonzo, M.; Dominguez, E.; Alvarez-Primo, F.; Quinonez, A.; Munoz, E.; Puebla, J.; Barr...

_[P66 chunk_14, d=0.678]_

In summary, the established anomaly system and developed machine learning method are able to successfully detect and recognize the type of different anomalies in a layer-by-layer configuration for bioprinted materials. The best CNN model reaches an overall accuracy of 0.901 and F1-score of 0.955 on the testing and validation data sets, respectively. Among all three anomalies, nonuniformity detection reaches the best performance, while discontinuity performs the worst. It is believed that the results can be further improved by improving the balance of different anomalies within the data set and fixing the environment's conditions (e.g., lighting) during the data collection. It is hypothesized that dyeing the material with colors can be helpful for this problem. However, mixing the extra additive (food coloring) could potentially change the printability of the material and requires further tuning of the printing parameters. Additionally, transfer learning can also be applied to this problem in the future to minimize the manual labeling process and enhance its general application capability.

## ■ AUTHOR INFORMATION


## Corresponding Author

Grace X. Gu -Department of Mechanical Engi...

_[P66 chunk_0, d=0.683]_

## 1. INTRODUCTION

Additive manufacturing, otherwise well-known as 3D printing, has been widely applied to various fields including the aerospace industry, biological engineering, and autonomous vehicles. 1 -6 Recent advances in tissue engineering have realized 3D bioprinting of biological components such as living tissues and human organs. 7 -9 3D bioprinting is now actively applied to create biocompatible materials and structures for functional living cells. Among the bioprinted materials, hydrogels are one of the most widely applied materials for their cross-linking capability to create scaffold structures for tissue engineering applications. 10,11 For biological constructs such as tissues, it is critical to obtain a highquality print as close to the desired design as possible to ensure robust functionality. However, unlike typical 3D-printing methods using polymers or metal powder, the challenge of achieving high-quality prints during the 3D-bioprinting process lies in understanding the rheological property of the hydrogels as they are sensitive to the additive concentration (e.g., methylcellulose, alginate) as well as the choice of printing parameters during fabrication. 12 F...

_[P66 chunk_1, d=0.696]_

Biomaterials
INGELENGNEN
SPECIAL ISSUE

*Figure 1. (a) Experimental setup of the anomaly detection system for a 3D-bioprinting platform. (b) Raw image data showing four different infill pattern examples and three anomaly cases. (c) An illustration visualizing the image processing procedure. The area of interest shown in the green bounding box is first determined and cropped into an 800 × 800 pixels size. Smaller image patches (input images) are then extracted uniformly and randomly.*

(a)
(b)
Good-quality
Discontinuity
Temperature
controlled
printhead
Grid
Rectilinear
Irregujarity
Nonuniformity
Camera
Nozzle
Gyroid
Honeycomb
(c)
Extract
image
patches
Uniform distribution
Randomdistribution
proper line width) are explored for the first layer of the print which is considered the important foundation of the entire print. Due to the transparent and complex features of these anomalies, machine learning methods are actively incorporated for this problem to explore and distinguish the underlying hidden patterns behind real-time printing images. Recently, machine learning methods have progressed dramatically in terms of efficiency and have seen promising applications in predictive material...

_[P66 chunk_16, d=0.759]_

- You, F.; Wu, X.; Chen, X. 3D printing of porous alginate/ gelatin hydrogel scaffolds and their mechanical property characterization. Int. J. Polym. Mater. 2017 , 66 (6), 299 -306.
- Webb, B.; Doyle, B. J. Parameter optimization for 3D bioprinting of hydrogels. Bioprinting 2017 , 8 , 8 -12.
- Ribeiro, A.; Blokzijl, M. M.; Levato, R.; Visser, C. W.; Castilho, M.; Hennink, W. E.; Vermonden, T.; Malda, J. Assessing bioink shape fidelity to aid material development in 3D bioprinting. Biofabrication 2018 , 10 (1), No. 014102.
- He, Y.; Yang, F.; Zhao, H.; Gao, Q.; Xia, B.; Fu, J. Research on the printability of hydrogels in 3D bioprinting. Sci. Rep. 2016 , 6 (1), 29977.
- Naghieh, S.; Sarker, M.; Sharma, N.; Barhoumi, Z.; Chen, X. Printability of 3D printed hydrogel scaffolds: Influence of hydrogel composition and printing parameters. Appl. Sci. 2020 , 10 (1), 292.
- Das, S.; Basu, B. An Overview of Hydrogel-Based Bioinks for 3D Bioprinting of Soft Tissues. J. Indian Inst. Sci. 2019 , 99 (3), 405 -428.
- Zhang, Z.; Jin, Y.; Yin, J.; Xu, C.; Xiong, R.; Christensen, K.; Ringeisen, B. R.; Chrisey, D. B.; Huang, Y. Evaluation of bioink printability for bioprinting applications. Appl. Phys....

**Background:**
Certainly! Here are the extracted sections based on your request:

### 1. Research Background

**Page 3946:**
"Additive manufacturing, otherwise well-known as 3D printing, has been widely applied to various fields including the aerospace industry, biological engineering, and autonomous vehicles."

**Page 3947:**
"Recent advances in tissue engineering have realized 3D bioprinting of biological components such as living tissues and human organs. Among the bioprinted materials, hydrogels are one of the most widely applied materials for their cross-linking capability to create scaffold structures ...

**Core problem:**
1. **Most Central Problem and Why It Matters:**
   The most central problem addressed in this paper is the accurate detection and classification of anomalies during 3D bioprinting processes, particularly for transparent hydrogel-based materials. This matters because ensuring high-quality prints with minimal defects is crucial for maintaining the structural integrity and functionality of tissue-engineered constructs. Accurate anomaly detection can lead to real-time adjustments in printing parameters, thereby improving print quality and reducing waste.

2. **Hardest Technical Difficulties:**
   ...

---

#### 🎯 P22: In situ defect detection and feedback control with three-dimensional extrusion-b

**DOI**: 10.18063/ijb.v9i1.624

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P22 chunk_0, d=0.670]_

## Abstract

Extrusion-based  three-dimensional  (3D)  bioprinting  is  one  of  the  most  common methods  used  for  tissue fabrication and  is the most  widely  used  additive manufacturing technique in all industries. In extrusion-based bioprinting, printing defects  related  to  material  deposition  errors  lead  to  a  significant  deviation  from shape  to  function  between  the  printed  construct  and  design  model.  Using  3D extrusion-based  bioprinter-associated  optical  coherence  tomography  (3D  P-OCT), an in situ defect detection and feedback system was presented based on the accurate defect analysis and location, and a pre-built feedback mechanism. Using 3D P-OCT, multi-parameter  quantification  of  the  material  deposition  was  carried  out  in  real time,  including  the  filament  size,  layer  thickness,  and  layer  fidelity.  The  material deposition  errors  under  different  paths  were  quantified  and  located  specifically, including  the  start-stop  points,  straight-line  path,  and  turnarounds. The  pre-built feedback mechanism involving the control inputs, such as printing path, pressure, and velocity, provided the basis for in situ defect d...

_[P22 chunk_1, d=0.677]_

Keywords: Optical coherence tomography; Extrusion-based bioprinting; Process monitoring; Defect detection; Feedback control; High fidelity

## 1. Introduction

With its potential to fabricate three-dimensional (3D) biomimetic functional tissue  constructs  and  organs,  3D  bioprinting  has  been  applied  in  organ  printing [1,2] , microvasculature  printing [3] ,  disease  modeling [4] ,  and  scaffold  fabrication  for  tissue regeneration [5,6] .  According  to  different  prototyping  principles  and  printed  materials, 3D bioprinting follows three main approaches: droplet-based, extrusion-based, and photocuring-based bioprinting. Extrusion-based bioprinting employs pneumatic, mechanical or ram extruders  to dispense  materials, and  other  biological molecules. Using extrusion-based bioprinters, various biopolymers and multiple cell types encapsulated in hydrogels  can  be  deposited  in  a  defined  trajectory  to fabricate  constructs  with  specific  biological  features [7] . Extrusion-based bioprinting has been widely used with the main advantages of a wide selection of biomaterials, lowcost equipment, and the ability to maintain great control of porosity and pore inte...

_[P22 chunk_3, d=0.759]_

The  incorporation  of  sensing  and  feedback  control in  extrusion  bioprinting  is  one  way  to  reduce  material deposition errors and improve the fidelity of the constructs.  At  present,  X-ray  CT [14,15] ,  MRI [16] ,  industrial camera [13] ,  and  3D  digital  image  correlation  (3D-DIC) [17] are the main detection technologies commonly used in 3D printing;  however,  there  are  some  limitations  for in  situ monitoring and 3D imaging detection of internal defects in  3D  bioprinting.  Simeunović  and  Hoelzle  developed non-linear and linearized models of extrusion-based printing  dynamics  to  avoid  adversely  impacting  flow rate  and  achieve  accurate  material  delivery  at  start-stop points [13] .  Armstrong et al .  presented  an  iteration-toiteration  process  monitoring  system  that  enabled  direct process  feedback  in  material  deposition  based  on  the laser  displacement  scanner  integrated  to  the  printing platform [6,18] . They modified the spatial material placement error and the material width error, and developed process control strategies based on the measured errors to adjust control inputs and ultimately eliminate material deposition e...

_[P22 chunk_4, d=0.771]_

In the previous work, 3D extrusion-based bioprinterassociated optical coherence tomography (3D P-OCT) has been  proposed [19] .  OCT  is  a  non-destructive,  label-free, high-resolution, and fast tomographic imaging technique that  are  widely  used  in  the  biomedical  and  industrial testing  fields [20,21] .  OCT  enables  3D  volumetric  imaging with micron-scale resolution over centimeter length scales and 3D P-OCT enables large-field full-depth imaging to meet  the  imaging  requirements  of  large  structures.  3D P-OCT can provide in situ process monitoring and multiparameter  evaluation  layer  by  layer  during  extrusionbased bioprinting including LT, FS, layer fidelity, and 3D structure quantitative analysis, including material volume, VP, and PC [19] . This study mainly focuses on in situ defect detection and timely feedback control for print parameter compensation and defect repair.
In this study, three types of defects related to material deposition were considered, including material deposition path,  FS,  and  LT.  Moreover,  the  improved  quantification methods  using  3D  P-OCT  reconstructed  results  were proposed for defect detection and location. On this b...

_[P22 chunk_2, d=0.774]_

Material  deposition  errors  result  in  deviations  in  the material path, filament size (FS), layer thickness (LT), pore size (PS), volume porosity (VP), and porosity connectivity (PC) between the printed structure and design model. In tissue-engineering scaffolds, specific PS values are required to accommodate cell growth and tissue regeneration [8,9] . 3D porous interconnected structures can facilitate cell growth and the transport of nutrients and metabolic waste, which is  beneficial  for  large-size  tissue  repair [9,10] .  High-fidelity structures can ensure that the constructs perfectly match the  tissue  defect  site  and  provide  sufficient  mechanical support, particularly for bone defect repair [11] .  Moreover, low  fidelity  can  affect  the  consistency  between  drug screening  and  disease  models [12] .  Insufficient  product  quality assurance could lead to increased lead-times, operational costs, and part waste. Therefore, an increasing number of researchers have become aware of the significance of highfidelity structures and the importance of precise material deposition [13] .  Material  deposition  errors  usually  lead  to low structural fidelity, poor co...

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

## Part B: Semantic search results (Chroma top N)

### P44: Recent Computer Vision-Aided Bioprinting for Bone Research

**DOI**: 10.1038/s41413-022-00192-2
**Best distance**: 0.594
**Chunks retrieved**: 3

**Retrieved chunks:**

_[P44 chunk_3, d=0.594]_

Since most AM techniques have printing defects, including extrusion-based bioprinting, it is necessary to use computer vision and process control to repair defects and correct errors, including biomedical areas, 27,28 aerospace, 29 tooling, 30 and metals. 31 For instance, it has been observed that bone scaffold failure is often accompanied by local stress concentrations during porous scaffold printing. The utilization of computer vision to collect stress data following the optimization and improvement of the stress concentration state can lead to enhanced scaffold quality. 32 A nondestructive evaluation by computer vision can be accomplished by collecting a large number of pictures of defects during the printing process. 33
Furthermore, deep learning has been demonstrated to be a useful method for a wide range of computer vision image tasks. In particular, convolutional neural networks (CNNs) can segment a bone image region of interest. For instance, input radiographs can be standardized and preprocessed, and bone age assessments can be performed. 34 Since CNNs can automatically recognize the hierarchy of discriminative features by training a set of labeled bone images, this techni...

_[P44 chunk_2, d=0.601]_

Currently, extrusion-based bioprinting has been one of the most widely used bioprinting methods in the bone scaffold printing fi eld; however, its low printing resolution (~100 μ m) 22 remains one limitation. Resolution is a signi fi cant parameter that in fl uences the fi nal printing performance of bone scaffolds. For instance, an investigation of the effect of 3D bioprinting on the differentiation and mineral precipitation of bone cells compared to the fi lm area indicated improved results under 3D conditions. 23 This suggests that bone structure needs higher requirements for lattice structure accuracy and printing process resolution since different morphologies affect osteoblast precursor cell differentiation and mineral precipitation. To improve the bone structure accuracy and increase the resolution, reducing the size of the nozzle diameter was proposed, but this led to increased shear stress values in the nozzle head, which may damage cells. 24 Therefore, depending on the choice of the nozzle diameter, the fi nal cell viability will vary from 45% to 95%. 25
Computer vision provides new insights to address the problems of low accuracy and low resolution in extrusion-based bio...

_[P44 chunk_4, d=0.645]_

*Fig. 1 Computer vision-aided bioprinting for bone research. a Schematic illustration of computer vision to improve the bioprinting performance for bone research. From top to bottom, the top part illustrates the processes of trajectory detection and correction during the bioprinting process control, which include the original print, scan original print, data process, corrected print, and veri fi cation. The middle part shows the application of deep learning in the diagnosis of bone diseases, and the bone disease data are collected and analyzed to determine the condition of the disease. The bottom part illustrates the collection of cell viability under different pressures to determine the balance between pressure and cell viability. b Example of typical cases of computer vision optimizing the bioprinting process to improve the fi nal bone bioprinting quality*

PRESSURE
CELL VIABILITY
BLANCE
BALANCE
ORIGINAL PRINT
SCAN ORIGINAL PRINT
DATA PROCESS
CORRECTED PRINT
VERIFICATION
DEEP
LEARNING
PROCESS
CONTROL
ABNORMAL
NORMAL
DATA COLLECTION
CELL
VIABILITY
CORRECTION AND EXECUTION
Computer vision-aided bioprinting for bone research
a
PRESSURE DETECTION
CELL OBSERVATION
1
2
4
1.Trajectory c...

**Background (from SOP metadata):**
This research paper focuses on enhancing bioprinting for bone tissue engineering by integrating computer vision technology to address current limitations such as low accuracy and resolution. Bioprinting, an additive manufacturing technique, holds significant promise in creating precise bone implants but faces challenges due to insufficient shape accuracy of printed parts. The study highlights that the use of computer vision can improve various aspects of bioprinting including accuracy, resolution, and cell survival rates.

Prior work has struggled with achieving high-resolution printing and ma...

**Core problem & critique:**
The research paper focuses on the application of computer vision to enhance bioprinting processes for bone research, addressing critical issues such as low accuracy and resolution that hinder widespread clinical adoption. The central problem lies in achieving precise control over the shape, size, and spatial placement of printed scaffolds or bioengineered grafts, which is crucial for successful bone implantation and repair.

One of the hardest technical difficulties highlighted in the paper involves improving the resolution of extrusion-based bioprinting while maintaining cell viability. This ...

---

### P63: Autonomous Control of Extrusion Bioprinting Using Convolutional Neural Networks

**DOI**: 10.1002/adfm.202424553
**Best distance**: 0.640
**Chunks retrieved**: 2

**Retrieved chunks:**

_[P63 chunk_3, d=0.640]_

## 2. Results and Discussion


## 2.1. Training Convolutional Neural Networks for Extrusion Error Detection During Bioprinting

Wefirst focused on training CNN models that could rapidly identify extrusion anomalies during bioprinting. To enable this, we leveraged a bioprinting hardware platform with integrated quality monitoring functionality that was recently developed in our group. [39] This hardware solution comprises a readily available and low-cost bed-slinger fused deposition modeling 3D printer (Prusa MK3S + ) with the thermoplastic extruder swapped for a progressive cavity pump extruder (Puredyne kit B), thus converting the printer into a bioprinter ( Figure 1 a). The printer is further modified with a second x -axis located below the extruder x -axis that is fitted with a Raspberry Pi 1.6-megapixel global shutter camera and macro scale lens that focuses directly up toward the tip of the extruder and follows its movements. The result is a system that can print on any transparent medium with an unobstructed view up at the extruder depositing material (Figure 1a; Movie S1, Supporting Information). For initial testing, a 10 w/v% alginate biomaterial ink (without cells) was emp...

_[P63 chunk_13, d=0.645]_

was 90% for single-line extrusion and 75% for infill extrusion conditions (Figure 3b). This is likely due to the more complex and variable extrusion imagery produced during infill extrusion, where the newly deposited ink fuses with previously deposited ink. We also found that our CNN model was adaptable to different nozzle sizes and shapes, demonstrating successful classification of good, over-, and under-extrusion across multiple gauges (17G, 20G, 23G) and shapes (conical and straight) (Figure S1, Supporting Information). Altogether, our results demonstrate that our trained CNN models could be deployed to detect extrusion errors during bioprinting, with the transfer learning trained ResNet50 andXception models being the most promising. Building on this, we next sought to use our computer vision platform and error detection algorithms to introduce extrusion corrections during bioprinting.

## 2.3. Closed-Loop Bioprinting Error Detection and Correction Using Convolutional Neural Networks

Next, we developed an extrusion error correction system using the classification output of the best-performing CNN models (Xception and ResNet50) ( Figure 4 a). This algorithm involved classifying ...

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

### P86: Precision improvement of robotic bioprinting via vision-based tool path compensa

**DOI**: 10.1038/s41598-024-68597-z
**Best distance**: 0.645
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P86 chunk_3, d=0.645]_

The imprecise tracking of printing trajectories in bioprinting that leads to low resolution and issues such as filament overlap, unwanted pore coverage, and overlapping   corners 28 has been investigated to be overcome. In this context, Liu et al. introduced computer vision techniques to address these issues, resulting in the attainment of highly accurate bioprinted structures, along with precise control over both geometry and   biomaterials 29 . However, it' s important to note that a potential drawback of their work is the increased computational complexity associated with implementing these computer vision techniques, which may require substantial computing resources and could affect the overall efficiency of the bioprinting process. Computer vision plays a significant role in diverse additive manufacturing (AM) applications, including object identification, size measurement, sorting, fault detection, and optimal   positioning 30-35 . Previous studies have explored vision-based monitoring and control methods in AM, covering various areas such as 3D construction printing, extrusion flow rate regulation, real-time control for concrete deposition, and anomaly detection in 3D biopri...

**Background (from SOP metadata):**
Certainly, here are the extracted sections from the provided text:

**Research Background:**
"Robotic 3D bioprinting is a rapidly advancing technology with applications in organ fabrication, tissue restoration, and pharmaceutical testing. While the stepwise generation of organs characterizes bioprinting, challenges such as non-linear material behavior, layer shifting, and trajectory tracking are common in freeform reversible embedding of suspended hydrogels (FRESH) bioprinting, leading to imperfections in complex organ construction."

**Core Concepts:**
"To overcome these limitations, we propo...

**Core problem & critique:**
1) **Most Central Problem and Why It Matters:**
   - The most central problem addressed in this paper is the precision and accuracy issues inherent in robotic 3D bioprinting, particularly with respect to curved layers and side-by-side filaments. This matters because achieving high precision is crucial for creating functional biological structures that mimic native tissues accurately. Precision directly influences the mechanical properties and biological performance of printed constructs, which are essential for applications such as tissue engineering and organ transplantation.

2) **Hardest Te...

---

### P43: Monitoring Anomalies in 3D Bioprinting with Deep Neural Networks

**DOI**: 10.1021/acsbiomaterials.0c01761
**Best distance**: 0.654
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P43 chunk_17, d=0.654]_

- Gobert, C.; Reutzel, E. W.; Petrich, J.; Nassar, A. R.; Phoha, S. Application of supervised machine learning for defect detection during metallic powder bed fusion additive manufacturing using high resolution imaging. Additive Manufacturing 2018 , 21 , 517 -528.
- Jin, Z.; Zhang, Z.; Ott, J.; Gu, G. X. Precise localization and semantic segmentation detection of printing conditions in fused filament fabrication technologies using machine learning. Additive Manufacturing 2021 , 37 , 101696.
- Hanakata, P. Z.; Cubuk, E. D.; Campbell, D. K.; Park, H. S. Accelerated search and design of stretchable graphene kirigami using machine learning. Phys. Rev. Lett. 2018 , 121 (25), 255304.
- Jin, Z.; Zhang, Z.; Gu, G. X. Automated Real-Time Detection and Prediction of Interlayer Imperfections in Additive Manufacturing
Processes Using Artificial Intelligence. Advanced Intelligent Systems 2020 , 2 (1), 1900130.
- Kim, S. H.; Lim, T. H.; Park, C. H. Silk Fibroin Bioinks for Digital Light Processing (DLP) 3D Bioprinting. In Bioinspired Biomaterials ; Springer: 2020; pp 53 -66, DOI: 10.1007/978-981-153258-0_4.
- Alonzo, M.; Dominguez, E.; Alvarez-Primo, F.; Quinonez, A.; Munoz, E.; Puebla, J.; Barr...

**Background (from SOP metadata):**
Certainly! Here are the extracted sections from the provided research paper text, adhering to your request for exact quotes and including page numbers when applicable:

### 1. Research Background

**Quote:**
"Additive manufacturing technologies have progressed in the past decades, especially when used to print biofunctional structures such as scaffolds and vessels with living cells for tissue engineering applications."

**Page Number:** 3945

---

### 2. Core Concepts

**Quote:**
"In this study, an anomaly detection system based on layer-by-layer sensor images and machine learning algorithms i...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters:**
   The most central problem addressed in this paper is the development of an anomaly detection system for 3D bioprinting using deep neural networks (CNNs). This matters because ensuring high-quality prints with minimal anomalies is crucial for tissue engineering applications, where structural integrity and biocompatibility are paramount. Accurate real-time detection can prevent wasted materials and improve the efficiency and reliability of the printing process.

2. **Hardest Technical Difficulties:**
   The hardest technical difficulties include ...

---

### P66: Monitoring Anomalies in 3D Bioprinting with Deep Neural Networks 🎯 (also cited in outline)

**DOI**: 10.1021/acsbiomaterials.0c01761
**Best distance**: 0.654
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P66 chunk_17, d=0.654]_

- Gobert, C.; Reutzel, E. W.; Petrich, J.; Nassar, A. R.; Phoha, S. Application of supervised machine learning for defect detection during metallic powder bed fusion additive manufacturing using high resolution imaging. Additive Manufacturing 2018 , 21 , 517 -528.
- Jin, Z.; Zhang, Z.; Ott, J.; Gu, G. X. Precise localization and semantic segmentation detection of printing conditions in fused filament fabrication technologies using machine learning. Additive Manufacturing 2021 , 37 , 101696.
- Hanakata, P. Z.; Cubuk, E. D.; Campbell, D. K.; Park, H. S. Accelerated search and design of stretchable graphene kirigami using machine learning. Phys. Rev. Lett. 2018 , 121 (25), 255304.
- Jin, Z.; Zhang, Z.; Gu, G. X. Automated Real-Time Detection and Prediction of Interlayer Imperfections in Additive Manufacturing
Processes Using Artificial Intelligence. Advanced Intelligent Systems 2020 , 2 (1), 1900130.
- Kim, S. H.; Lim, T. H.; Park, C. H. Silk Fibroin Bioinks for Digital Light Processing (DLP) 3D Bioprinting. In Bioinspired Biomaterials ; Springer: 2020; pp 53 -66, DOI: 10.1007/978-981-153258-0_4.
- Alonzo, M.; Dominguez, E.; Alvarez-Primo, F.; Quinonez, A.; Munoz, E.; Puebla, J.; Barr...

**Background (from SOP metadata):**
Certainly! Here are the extracted sections based on your request:

### 1. Research Background

**Page 3946:**
"Additive manufacturing, otherwise well-known as 3D printing, has been widely applied to various fields including the aerospace industry, biological engineering, and autonomous vehicles."

**Page 3947:**
"Recent advances in tissue engineering have realized 3D bioprinting of biological components such as living tissues and human organs. Among the bioprinted materials, hydrogels are one of the most widely applied materials for their cross-linking capability to create scaffold structures ...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters:**
   The most central problem addressed in this paper is the accurate detection and classification of anomalies during 3D bioprinting processes, particularly for transparent hydrogel-based materials. This matters because ensuring high-quality prints with minimal defects is crucial for maintaining the structural integrity and functionality of tissue-engineered constructs. Accurate anomaly detection can lead to real-time adjustments in printing parameters, thereby improving print quality and reducing waste.

2. **Hardest Technical Difficulties:**
   ...

---

### P6: In-situ monitoring of defects in extrusion-based bioprinting processes using vis 🎯 (also cited in outline)

**DOI**: 10.1016/j.procir.2022.06.040
**Best distance**: 0.659
**Chunks retrieved**: 2

**Retrieved chunks:**

_[P6 chunk_9, d=0.659]_

Accuracy in bioprinting process is currently limited by the lack of error monitoring techniques. Although the identification and the study of relationships between printing outcomes  and  process  parameters  were widely  investigated, repeatability  of  the  printing  process  is  still  far  from  being reached, especially in extrusion-based bioprinting[25]. Strauß, S. et al. used in their work non-invasive image-based analysis methods as tool for line construct characterization. It was an automated method to enable comparison of 3D printed lines to evaluate  the  influence  of  rheological  properties  and  printing parameters on them[16]. Armstrong et al. used point cloud data from a laser scanner to obtain images of the printed samples. They  then  use  a  custom  image  processing  algorithm  to determine the error between the reference and printed trajectory[11 -13]. A different approach was used by Wang, L. et al. In this study, optical coherence tomography was applied to  acquire  high-resolution  images  of  hydrogel  scaffolds.  An image analysis algorithm was proposed to accurately quantify some morphological parameters (pore size, pore shape, surface area, porosity, an...

_[P6 chunk_10, d=0.660]_

The method used in our work identified  drift  phenomena during the printing process. These were certainly more evident where the artificially added errors were introduced, with values of Over  Extrusion above  20%. These  errors could simulate rheological changes within bioinks, usually caused by uncontrolled changes in process parameters (temperature changes,  presence  of  bubbles,  etc.).  Drifting  processes  were also  detected  in 'in -control'  samples ,  where,  as  expected, increasing the layers perpetuated the pre-existing condition of excessively extruded material. In both cases we were able to build  a map of defects. The work  here presented  describe  a simple monitoring experiment in which the feasibility of using visible  imaging  for  geometry  detection  of  printed  constructs was demonstrated. More specifically,  we  have  demonstrated the effectiveness in being able to discriminate defect between layers. The automated monitoring system has proven to be able to  detect  defects  in deposition,  giving  to  the  operator  a  full understanding of the moment and the layer where the defect occurred, enabling the adoption of countermeasures in subsequent prints.
D...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

**Research Background:**
The research background is outlined in the Introduction and State of the Art sections. According to page 219:
"Bioprinting is an additive manufacturing (AM) technology whose goal is to fabricate parts that mimic the functionality of real tissues and organs by combining cells and biomaterials with a specific three-dimensional (3D) spatial organization."

**Core Concepts:**
The core concepts are detailed in the Introduction, State of the Art, and Materials and Methods sections. According to pages 219-220:
"Bio...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters (Page 220)**

The central problem addressed in this paper is the lack of effective quality assurance methods for bioprinting, particularly extrusion-based processes. This matters significantly because ensuring high-quality printed constructs is crucial for advancing applications in regenerative medicine, tissue engineering, reconstructive surgery, and drug discovery. Without reliable quality control measures, it's challenging to produce consistent and functional bioconstructs that can be used safely and effectively in clinical settings.

2. **Hardes...

---

### P23: Error assessment and correction for extrusion-based bioprinting using computer v

**DOI**: 10.18063/ijb.v9i1.644
**Best distance**: 0.670
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P23 chunk_0, d=0.670]_

## Abstract

Bioprinting offers a new approach to addressing the organ shortage crisis. Despite recent technological advances, insufficient printing resolution continues to be one of the reasons that impede the development of bioprinting. Normally, machine axes movement cannot be reliably used to predict material placement, and the printing path tends to deviate from the predetermined designed reference trajectory in varying degrees. Therefore, a computer vision-based method was proposed in this study to correct trajectory deviation and improve printing accuracy. The image algorithm calculated the deviation between the printed trajectory and the reference trajectory to generate an error vector. Furthermore, the axes trajectory was modified according to the normal vector approach in the second printing to compensate for the deviation error. The highest correction efficiency that could be achieved was 91%. More significantly, we discovered that the correction results, for the first time, were in a normal distribution instead of a random distribution.
Keywords
: Bioprinting; Computer vision; Error detection; Sobel operator

## 1. Introduction

Organ shortage is a serious social health...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted details:

**Research Background:**
"Organ shortage is a serious social health crisis. A report from the University of Minnesota states that approximately 90,000 people require kidney transplant, but only 1,500 people have undergone kidney transplants in 2018 [1]. The shortage of fitting and propitious organs for transplantation has always been a medical concern[2-4]." (Page 300)

**Core Concepts:**
"Building organs from scratch to explore entirely new cell configurations is the main feature of bioprinting, which is an emerging scientific field...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters (Page 299-300)**

The central problem addressed in this paper is the low printing resolution in extrusion-based bioprinting, which limits its advancement across various fields such as tissue engineering and organ fabrication. This issue matters significantly because high-resolution printing is crucial for creating complex biological structures with precise cell configurations necessary for functional organs.

2. **Hardest Technical Difficulties (Pages 301-304)**

The hardest technical difficulties include accurately detecting and correcting the devi...

---

### P22: In situ defect detection and feedback control with three-dimensional extrusion-b 🎯 (also cited in outline)

**DOI**: 10.18063/ijb.v9i1.624
**Best distance**: 0.670
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P22 chunk_0, d=0.670]_

## Abstract

Extrusion-based  three-dimensional  (3D)  bioprinting  is  one  of  the  most  common methods  used  for  tissue fabrication and  is the most  widely  used  additive manufacturing technique in all industries. In extrusion-based bioprinting, printing defects  related  to  material  deposition  errors  lead  to  a  significant  deviation  from shape  to  function  between  the  printed  construct  and  design  model.  Using  3D extrusion-based  bioprinter-associated  optical  coherence  tomography  (3D  P-OCT), an in situ defect detection and feedback system was presented based on the accurate defect analysis and location, and a pre-built feedback mechanism. Using 3D P-OCT, multi-parameter  quantification  of  the  material  deposition  was  carried  out  in  real time,  including  the  filament  size,  layer  thickness,  and  layer  fidelity.  The  material deposition  errors  under  different  paths  were  quantified  and  located  specifically, including  the  start-stop  points,  straight-line  path,  and  turnarounds. The  pre-built feedback mechanism involving the control inputs, such as printing path, pressure, and velocity, provided the basis for in situ defect d...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

### 1. Research Background

**Page 47-48:**
"With its potential to fabricate three-dimensional (3D) biomimetic functional tissue constructs and organs, 3D bioprinting has been applied in organ printing [1,2], microvasculature printing [3], disease modeling [4], and scaffold fabrication for tissue regeneration[5,6]. According to different prototyping principles and printed materials, 3D bioprinting follows three main approaches: droplet-based, extrusion-based, and photocuring-based bioprinting. Extrusion-based bioprinting employs pne...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters (Page 47-48)**

The central problem addressed in this paper is the lack of real-time defect detection and feedback control mechanisms during extrusion-based bioprinting, which leads to low structural fidelity between printed constructs and design models. This matters significantly because high-fidelity structures are crucial for applications such as tissue engineering, drug screening, and disease modeling, where precise replication of biological tissues or organs is essential.

2. **Hardest Technical Difficulties (Pages 49-50)**

The hardest technic...

---
