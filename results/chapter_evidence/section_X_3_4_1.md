# Section X.3.4.1: Biological consequence and functional interpretation

**Target words**: 200
**Query**: `bioprinting cell viability stress proliferation phenotype post-printing biological outcome`
**Generated**: 2026-05-13T14:51:30.795597

---

## Part A: Explicitly cited references in outline (with content)

### Quick index

- ✅ **P69** — `10.1038/s41598-023-28286-9` (in library)
- ✅ **P111** — `10.1088/1758-5090/ad17cf` (in library)
- ✅ **P71** — `10.1007/s10845-020-01708-5` (in library)

### Detailed content per cited paper

#### 🎯 P69: Predicting and elucidating the post-printing behavior of 3D printed cancer cells

**DOI**: 10.1038/s41598-023-28286-9

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P69 chunk_5, d=0.705]_

The viability of MDA-MB-231 over 11 days was visualized using live-dead staining, which was in line with MTT assay results. As shown in Fig. 2, most cells were viable after printing, and the viability rate of cells was 76 ± 2% on day 0, which clearly demonstrated minor damage of the bioprinting process on cell viability. The rate of viability increased over the first week and reached 98 ± 1% and 99 ± 1% on day 4 and day 7, respectively. Therefore, the structure was porous enough for oxygen and glucose to diffuse and distribute through the hydrogel scaffold, which could provide a proper living environment for cells. From day 7 to day 11, although some cells died, the majority of cells survived, and the rate of viability reached 96 ± 2% on day 11. By comparing the results of live-dead assay and MTT assay, it can be concluded that a significant portion of cells entered the resting phase after seven days since the maximum capacity of the scaffold had been achieved, and some of the cells began to die during the long-term stationary phase, or due to the lack of resources. Cell death in this experiment is almost negligible, which illustrates the promising potential of gelatin/alginate sca...

_[P69 chunk_15, d=0.738]_

So far, optimal post-printing behaviour of cells growing within the 3D biorinted hydrogel has been achieved using only replicating several experiments, which are time-consuming and expensive. In an attempt to overcome this challenge, we developed a CA model to simulate post-printing cells' dynamics within the 3D bioprinted construct. To this end, we first successfully printed MDA-MB-231/gelatin/alginate bioink and evaluated cellular behaviour in 11 days using MTT, Live-dead and Ki-67 cell proliferation assays. Using in-vitro results, we defined rules in the CA model for cell proliferation, viability, movement and cluster formation within the 3D hydrogel network and calibrated model parameters such as doubling-time, movement speed, and probability of death in 11 days. Our model can quantitatively capture the post-printing in-vitro behaviour of cells in the 3D scaffold and is able to predict and elucidate the cell behaviour for different bioprinting conditions. For example, it replicates the cellular movement and cell crawling toward the pores, followed by forming clusters after seven days due to uneven distribution of nutrients and oxygen. Furthermore, the in-silico data elucidate t...

_[P69 chunk_0, d=0.738]_

## OPEN

Predicting and elucidating the post-printing behavior of ͹D printed cancer cells in hydrogel structures by integrating in-vitro and in-silico experiments
Dorsa Mohammadrezaei  ͷ * , Nafiseh Moghimi  ͷ , Shadi Vandvajdi ͷ , Gibin Powathil ͸ , Sara Hamis  ͹  & Mohammad Kohandel  ͷ
A key feature distinguishing ͹D bioprinting from other ͹D cell culture techniques is its precise control over created structures. This property allows for the high-resolution fabrication of biomimetic structures with controlled structural and mechanical properties such as porosity, permeability, and stiffness. However, analyzing post-printing cellular dynamics and optimizing their functions within the ͹D fabricated environment is only possible through trial and error and replicating several experiments. This issue motivated the development of a cellular automata model for the first time to simulate post-printing cell behaviour within the ͹D bioprinted construct. To improve our model, we bioprinted a ͹D construct using MDA-MB-͸͹ͷ cell-laden hydrogel and evaluated cellular functions, including viability and proliferation in ͷͷ days. The results showed that our model successfully simulated the ͹D biop...

_[P69 chunk_6, d=0.743]_

To visualize the proliferative capacity of MDA-MB-231, cells were fixed, and an anti-Ki-67 antibody was used to image proliferating cells using a confocal microscope (Figs. 3, 4). Ki-67 is a common-used marker that is present for all active phases of the cell cycle but absent in cells at the stationary   phase 23 . The results demonstrated that on days 0 and 4, almost 98 ± 1% and 95 ± 2% of the cells were positive for ki-67, respectively, while this number decreased to 86 ± 2% on day 7, followed by a dramatic drop to about 48.2 ± 2.4 on day 11. This result is in agreement with the data in the previous (Fig. 3), illustrating that within seven days, cells not only survive but also maintain their proliferating ability. From day 7 to day 11, although a high proportion of cells demonstrated to be alive, they were quiescent and were not able to proliferate anymore because of the lack of enough space for cells to proliferate. Additionally, on days 7 and 11, cells became more aggregated, particularly close to the pores, and cells at the center of the cell aggregates were shown to be non-proliferating due to being surrounded by other cells. Therefore, the proliferation process was aborted a...

_[P69 chunk_14, d=0.755]_

Moreover, the proposed model can be integrated with the machine learning algorithms and provide researchers with this opportunity to predict the temporal or structural effect of the hydrogel network on any desired objectives in the biological system. Furthermore, we can use CA simulation to pre-train the ML algorithm and then a transfer learning approach can be applied to train the experimental data.
Another prospect of this model is its application in a heterogeneous environment with multiple cell lines for studying cell-cell interaction and cell-ECM interactions. Besides, by adjusting the rules, this model can be integrated with pharmacokinetic modelling techniques to simulate drug treatment responses in 3D cell culture using 3D bioprinting to help study tumour development and metastasis, drug screening, and other aspects of cancer research.
In the end, we believe that this work or its combination with other modelling techniques can significantly influence the development of 3D bioprinting in the future and avoid conducting costly and time-consuming experiments to a great extent.

## Conclusion

So far, optimal post-printing behaviour of cells growing within the 3D biorinted hydr...

**Background:**
Certainly, here are the extracted sections from the provided research paper text:

### 1. Research Background

**Page 1-2:**
"A key feature distinguishing 3D bioprinting from other 3D cell culture techniques is its precise control over created structures. This property allows for the high-resolution fabrication of biomimetic structures with controlled structural and mechanical properties such as porosity, permeability, and stiffness."

**Page 1-2:**
"However, analyzing post-printing cellular dynamics and optimizing their functions within the 3D fabricated environment is only possible through t...

**Core problem:**
1. **Most Central Problem and Why It Matters (Page 1-2)**

The central problem addressed in this paper is the challenge of optimizing post-printing cellular behavior within 3D bioprinted constructs, which currently relies heavily on trial-and-error experimental approaches due to a lack of precise quantitative techniques for analyzing cell dynamics. This issue matters significantly because it hinders the efficient and cost-effective development of personalized therapies and drug screening methods in regenerative medicine and tissue engineering.

2. **Hardest Technical Difficulties (Page 3-4)**
...

---

#### 🎯 P111: Cell viability prediction and optimization in extrusion-based bioprinting via ne

**DOI**: 10.1088/1758-5090/ad17cf

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P111 chunk_20, d=0.558]_

These outcomes show the efficacy of our neural networks for predicting cell viability in bioprinting and imply that they may offer significant advantages over conventional regression and classification models. Additionally, we believe the models' performance can be enhanced even further by expanding the dataset to capture a broader range of patterns and relationships, reducing overfitting, and enhancing the model's generalization capability. Increasing the number of instances with diverse combinations of bioprinting parameters and corresponding cell viability measurements can be accomplished by collecting additional in-vitro data in the laboratory or incorporating data from other sources.

## 3.2.2. Permutation importance of bioprinting parameters

Permutation Importance was applied to determine the most significant features of bioprinting for predicting cell viability using a neural network for regression. Figure 4 shows ten of the most important features; the x -axis represents the significance score, while the y -axis represents the evaluated bioprinting parameters.
As demonstrated in this figure, the 'Cell type' has the most significant impact on optimizing the bioprinting proc...

_[P111 chunk_23, d=0.607]_

The 'Time of Measurement' parameter is demonstrated to be the 4th important parameter in expected cell viability. Over time, after the printing, cells within the bioprinted structure, depend on their proliferation rate, are likely to grow and repair any damage caused by the bioprinting process. However, after some time, there is a growth capacity threshold beyond which cell viability may plateau or decline. This phenomenon was illustrated in our previous study [22], where we assessed the viability and proliferation of MDA-MB-231 cells over an 11 day period after bioprinting. Our results indicated that the viability of cells was around 76% on the day of printing (day 0), and this viability progressively increased during the first week, reaching about 98% on day 4 and 99% on day 7. Then, from day 7 to day 11, the percentage of viability decreased a little and approximately reached 96% on day 11. Therefore, the time at which measurements are taken has a significant impact on the observed cell viability and should be carefully considered in accordance with the specific objectives of the study.
Fromthematerialperspective, 'Alginate_Concen-tration' and 'Gelatin_Concentration' are shown t...

_[P111 chunk_0, d=0.615]_

## Abstract

The fields of regenerative medicine and cancer modeling have witnessed tremendous growth in the application of 3D bioprinting. Maintaining high cell viability throughout the bioprinting process is crucial for the success of this technology, as it directly affects the accuracy of the 3D bioprinted models, the validity of experimental results, and the discovery of new therapeutic approaches. Therefore, optimizing bioprinting conditions, which include numerous variables influencing cell viability during and after the procedure, is of utmost importance to achieve desirable results. So far, these optimizations have been accomplished primarily through trial and error and repeating multiple time-consuming and costly experiments. To address this challenge, we initiated the process by creating a dataset of these parameters for gelatin and alginate-based bioinks and the corresponding cell viability by integrating data obtained in our laboratory and those derived from the literature. Then, we developed machine learning models to predict cell viability based on different bioprinting variables. The trained neural network yielded regression R 2 value of 0.71 and classification accur...

_[P111 chunk_1, d=0.637]_

However, preserving high cell viability throughout this process is a significant challenge. Cell viability and functionality can be negatively impacted by the stress created in bioprinting procedures, which can alter protein expression levels and disrupt cell signaling networks [17]. This challenge is particularly critical in various applications, such as cancer research, as cell viability directly affects the accuracy of the 3D bioprinted model, the reliability of the results of printing, and the development of new therapies using the 3D model. Consequently, it is significant to address the potential impact and loss of cells that may occur during bioprinting. This involves optimizing the bioprinting conditions to maintain high cell viability, which is essential for achieving successful bioprinting outcomes.
Several efforts have been made to produce biomimetic scaffolds with high cell viability using an extrusion-based bioprinting technique [12]. Cell survival, in the 3D bioprinting process can be affected by different variables, including cell type, bioink formulation, 3D printer parameters, and post-printing treatments. These categories may be subdivided into distinct parameters:...

_[P111 chunk_27, d=0.648]_

By calculating permutation importance for the neural network for regression, we identified the bioprinting parameters significantly impacting cell viability prediction. Among different parameters, 'cell type' emerges as the most critical variable, highlighting the different sensitivities of various cell types to the bioprinting procedure. In addition, 'extrusion pressure' is identified as the second most significant parameter, demonstrating the detrimental impact of excessive pressure on cell viability due to mechanical stress and shear forces on the cell membrane. After the bioprinting procedure, the 'crosslinker (CaCl2) concentration' and 'physical crosslinking time' are identified as the third and fifth significant features, respectively, which balance the structural integrity and cell viability of bioprinted structures. Therefore, we can conclude that tuning these effective parameters can highly impact the survival of cells during the bioprinting procedure.
We finally developed a novel Bayesian optimization model based on the created trained neural network to inversely predict optimal bioprinting crosslinking parameters, achieving the highest cell viability without any trial-an...

**Background:**
Based on the provided text, here are the extracted sections:

**Research Background (Page 1-2)**

"The fields of regenerative medicine and cancer modeling have witnessed tremendous growth in the application of 3D bioprinting. Maintaining high cell viability throughout the bioprinting process is crucial for the success of this technology, as it directly affects the accuracy of the 3D bioprinted models, the validity of experimental results, and the discovery of new therapeutic approaches."

**Core Concepts (Page 2-4)**

"ML, is able to find connections between input parameters and forecast expec...

**Core problem:**
1. **Most Central Problem and Why It Matters:**
   The most central problem addressed in this paper is optimizing cell viability during extrusion-based bioprinting processes, which is crucial for the success of 3D bioprinted constructs used in regenerative medicine and cancer modeling. High cell viability ensures accurate representation of biological tissues, reliable experimental results, and effective therapeutic approaches.

2. **Hardest Technical Difficulties:**
   The hardest technical difficulties include accurately predicting cell viability under various bioprinting conditions using mac...

---

#### 🎯 P71: Prediction of cell viability in dynamic optical projection stereolithography-bas

**DOI**: 10.1007/s10845-020-01708-5

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P71 chunk_2, d=0.570]_

To better understand post-printing cell viability, physicsbased models have been introduced to study how cells are damaged during bioprinting. Wang et al . (Wang et al. 2008) investigated the mechanical loading profile of cells using a mesh-free smooth particle hydrodynamic method, which was useful for understanding and predicting possible impactinduced cell damage. The cells were modeled as linear elastic solids, and the cell damage was determined by the cell membrane rupture due to the shear stresses imposed on the cells. The major conclusions were listed as below: 1) with the induced stresses, the cell membrane had severe deformation and was even damaged; and 2) to better quantify the cell damage, the stresses imposed on the cells from every source should be comprehensively incorporated such as those generated from the ejection process and the travel through air. Wang et al. (2009) used a finite element method (FEM) to investigate the mechanical loading profile of cells induced by the bubble expansion during laser-assisted bioprinting process. A neo-Hookean model was used to represent the living cells. It was found that both the process-induced cell stresses and the duration of ...

_[P71 chunk_0, d=0.727]_

## Abstract

Stereolithography (SLA)-based bioprinting can fabricate three-dimensional complex objects accurately and efficiently. However, the ultraviolet (UV) irradiation in the SLA-based bioprinting process is a significant challenge, which may damage the cells. Physics-based models are not able to predict cell viability with high accuracy because of the complexity of cell biological structures and cell recovery. To overcome this challenge, we developed a predictive model using machine learning to predict cell viability. We designed a set of experiments considering the effects of four critical process parameters, including UV intensity, UV exposure time, gelatin methacrylate concentration, and layer thickness. These experiments were conducted under varying bioprinting conditions to collect experimental data. An ensemble learning algorithm combining neural networks, ridge regression, K-nearest neighbors, and random forest (RF) was developed aiming at predicting cell viability under various bioprinting conditions. The performance of the predictive model was evaluated based on three error metrics. Finally, the importance of each process parameter on cell viability was determined us...

_[P71 chunk_3, d=0.732]_

Apoptosis and necrosis have been recognized as two major types of cell deaths (Matteucci et al. 1999). The apoptosis commonly appearing in the cell growths is either genet- ically controlled or stimuli-induced (Nagata 1997) while the necrosis is caused by the harmful events and pathological conditions (Matteucci et al. 1999). The apoptosis of the cells which is seen as the leading factor of cell injuries during bioprinting (Cotter and Al-Rubeai 1995) can be reflected by several specific features such as membrane blebbing, internucleosomal fragmentation of DNA, chromatincondensation,andcytoplasmiccondensation(Scoltock and Cidlowski 2004; Darzynkiewicz et al. 1997). In the stereolithography-based bioprinting, the major cell damage results from the UV irradiation. The UV light induces the clustering and internalization of the death receptors on the cell membrane (Rosette and Karin 1996) and damages DNAthroughtheformation of cyclobutene pyrimidine dimer (CPD)(Masumaetal.2013).TheUVirradiation-inducedcell apoptosis is caused by the activation of c-JunNH2-terminal kinase/stress-activated protein kinase (JNK/SAPK) (Lu et al. 2003). During this process, there are many different and complex...

_[P71 chunk_1, d=0.748]_

Lauren S. Gollahon lauren.gollahon@ttu.edu pre-formed hydrogel-based acellular scaffold to develop the extracellular matrix (ECM) (Pourchet et al. 2017). Native tissue-like constructs, such as cartilage, have been successfully fabricated with the scaffold-based approach (Kundu et al. 2015). One disadvantage of scaffold-based bioprinting is that the assembly of ECM may have negative effects on cell performance (Norotte et al. 2009). However, during scaffold-free bioprinting, cells are deposited directly to fabricate tissue-like constructs such as nerve tissues (Owens et al. 2013). The scaffold-free approach has drawn more attention due to its better biomimicry.
Depending on the printing mechanisms, 3D bioprinting techniques fall into four categories, including inkjet-based, microextrusion-based, laser-assisted, and stereolithographybased bioprinting (Lee and Yeong 2016). Inkjet-based bioprinting can achieve high printing resolution and precise control of droplet deposition positions on the substrate, but its limitations include nozzle clogging and low cell and polymer concentrations (Xu et al. 2019). Microextrusion-based bioprinting enables high cell and polymer concentrations, but ...

_[P71 chunk_6, d=0.779]_

Cell viability was characterized with fluorescence assays (Biotium, Fremont, CA). The assessment protocol is as follows: calcein AM and ethidium homodimer III were mixed in Dulbecco's Modified Eagle Medium (DMEM, SigmaAldrich, St. Louis, MO) at the appropriate concentrations to form the staining solution; incubate the stained samples in a 37 °C incubator with 5% CO2 and humidity for 20 min; and image the stained cells by a fluorescence microscope (EVOS FL, Thermo Fisher Scientific, Waltham, MA). Calcein-AM stained the living cells into fluorescence green and ethidium homodimer III stained the dead cells into fluorescence red. Cell viability was determined by the ratio of the living (green) cells over the total number of cells. More details regarding the cell viability assessment can be found in the previous paper (Wadnap et al. 2019).

## Experimental setup

Figure 1 illustrates the experimental setup. A digital micromirror device (DMD, DLP Discovery 4100, Texas Instruments Incorporated, Dallas, TX) containing numerous micromirrors whose function was to generate 2D patterns by rotating the micromirrors by ± 10° to manage each pixel to be white or dark in the designed 2D patterns, a...

**Background:**
Certainly, here are the extracted sections from the research paper based on your request:

### 1. Research Background

**Page 996:**
Three dimensional (3D) bioprinting techniques can fabricate functional tissues with biocompatible materials and living cells. Several representative biomimetic tissues and organs such as blood vessels, skins, bones, and cartilages have been fabricated with various 3D bioprinting techniques (Mandrycky et al. 2016). Two bioprinting mechanisms have been developed: scaffold-based and scaffold-free bioprinting.

**Page 997:**
To better understand post-printing cell vi...

**Core problem:**
1. **Most Central Problem and Why It Matters (Page 995-996)**

The central problem addressed in this paper is predicting cell viability during dynamic optical projection stereolithography-based bioprinting, which is crucial for the successful fabrication of functional tissues with high cellular performance. This matters because UV irradiation used in the process can damage cells, and accurately predicting cell viability under varying conditions helps optimize printing parameters to enhance tissue functionality.

2. **Hardest Technical Difficulties (Pages 996-997)**

The hardest technical diffi...

---

## Part B: Semantic search results (Chroma top N)

### P37: A review on cell damage, viability, and functionality during 3D bioprinting

**DOI**: 10.1186/s40779-022-00429-5
**Best distance**: 0.510
**Chunks retrieved**: 5

**Retrieved chunks:**

_[P37 chunk_6, d=0.510]_

Even  though  3D  bioprinting  techniques  have  experienced significant improvements during the past decade, maintaining high cell viability and functionality after the bioprinting processes remains challenging [56]. All these four 3D bioprinting techniques were found to adversely affect cell viability due to the stresses during the bioprinting  process  [57].  In  addition,  cell  viability  may  further decrease while being cultured within a nutrition-deficient environment  [58].  Generally,  stresses  generated  during the  bioprinting  processes  affect  cell  viability  and  functionality by influencing cell signaling and protein expression  [59].  To  reduce  the  percentage  of  cell  death  and ensure post-printing cell functionality, the overall stress must be carefully controlled. In brief, the stress imposed on  the  cells  is  either  due  to  the  shear  stress  generated from  the  imposed  pressure  and  nozzle  size  during  the nozzle-based bioprinting process [60, 61], or the thermal and radiative stress generated by the light sources during light-based printing processes [62]. For example, during extrusion-based  bioprinting,  the  stress  mainly  comes from the...

_[P37 chunk_24, d=0.534]_

## Methods to reduce cell damage

3D  bioprinting  has  achieved  significant  advancements over the past decade, enabling the fabrication of 3D artificial  tissues/organs  with  high  precision  and  resolution. However, enduring various stresses during the bioprinting  processes  may  lead  to  the  decrease  of  cell  viability, loss  of  cell  functionality,  and  eventual  mis-functionality of the 3D artificial tissues/organs. Maintaining high cell viability  is  critical  to  ensure  desirable  biological  printing  performance  since  only  the  surviving  cells  during the  bioprinting  processes  have  the  potential  to  retain their  pluripotency  such  as  the  proliferation  and  differentiation ability, and thus ensure proper functionality of the  3D-bioprinted  constructs.  Generally,  cell  viability  is determined by the overall stress mainly coming from two sources including that from the materials and that from the  printing  process.  For  example,  in  nozzle-based  bioprinting such as inkjet-based bioprinting and extrusionbased bioprinting, cells are experiencing the shear stress while being ejected out of the nozzle, and in light sourceincorporated bioprintin...

_[P37 chunk_7, d=0.567]_

This review discusses the factors resulting in cell damage during each type of bioprinting, and summarizes several typical studies on cell viability and functionality after different  bioprinting  processes.  The  aim  of  this  review is to gain a better understanding of each type of 3D bioprinting by summarizing the mechanism of cell damage and explore possible ways to maintain high cell viability and  functionality  after  the  printing  processes  and  thus achieve better printing performance.

## Cell damage during 3D bioprinting

Due to the complicated cellular behaviors, living cells are more complicated than other normal engineered materials (e.g., nano-particles) [64]. Therefore, it is necessary to understand  the  relationship  between  biological  damage pathways and cell damage to manage the unwanted cell viability loss. During the bioprinting processes, cell injury may  source  from  various  inducements/stimuli  such  as shear stress, thermal stress, and radiative stress. The percentage  of  cell  injury  is  dependent  on  the  strength  and duration  of  the  stimuli.  If  the  imposed  stresses  exceed the loading capacity of a single cell, irreversible cell damage...

_[P37 chunk_22, d=0.577]_

## Cell functionality during 3D bioprinting

High cell viability is an initial key step in successful bioprinting  of  constructs  that  are  geometrically,  mechanically  and  functionally  similar  to  native  tissues/organs. Maintenance of cell functionality is another major concern of 3D bioprinting to ultimately ensure the functionality  of  the  3D  artificial  tissues/organs  during  culture [154].  Therefore,  researchers  should  not  only  focus  on the retainment of cell viability, but also the maintenance of cell functionality such as proliferation and differentiation  abilities  of  the  living  cells  both  during  the  printing and  culturing  processes  of  the  3D-printed  tissue  constructs  [149].  More  specifically,  surviving  cells  during bioprinting  are  expected  to  attach,  proliferate,  differentiate,  and  interact  with  the  hydrogels  that  mimic  native ECM. When stem cells are selected for bioprinting, they are expected to maintain the potency to differentiate into different cell types under the specific guidance and perform  the  corresponding  gene  expressions  following  the bioprinting processes [155]. For example, under specific guidance,  ...

_[P37 chunk_10, d=0.582]_

## Cell damage in extrusion-based bioprinting

Extrusion-based  bioprinting  has  been  widely  involved in various tissue engineering applications due to its easy implementation, low cost, and allowance on bioink's viscosities and concentrations [103-105]. During extrusionbased  bioprinting,  due  to  the  selected  bioink  with  high viscosity for better printability and support, a great percentage of cells endures the printing-induced cell stresses and  gets  injured/killed,  resulting  in  relatively  low  cell viability compared to other printing techniques [60, 106]. In addition, a mechanical-driven  (e.g.,  screw-driven) dispensing  system  generates  a  higher  pressure  when bioprinting  the  bioink  with  high  viscosity  and  simultaneously kills more cells [107]. The relationship between shear  stress  and  various  printing  parameters  such  as nozzle size and viscosity of the bioink and the effects of various  printing  parameters  on  cell  viability  have  been comprehensively  studied. Generally, the shear stress mainly comes from the printing process and the materials. From the process's perspective, when the bioink containing the living cells is extruded out of ...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

**Research Background (Page 2 of 15):**
"The demand for the transplantation of organs is consistently increasing due to the severe organ failure problem and shortage of suitable donors [1, 2]. Three-dimensional (3D) bioprinting which fabricates 3D functional tissues/organs (e.g., human skin [3]) by precisely positioning the bioink containing biological materials and living cells in a layer-by-layer manner has shown great promises for tissue engineering [4, 5]."

**Core Concepts:**
- **Cell Viability:** Affected by stress and environ...

**Core problem & critique:**
1) **Most Central Problem and Why It Matters:**
The most central problem addressed in this review is maintaining high cell viability and functionality during 3D bioprinting processes. This matters significantly because the success of fabricating functional tissues/organs relies heavily on the survival and proper functioning of living cells post-printing. Ensuring that cells remain viable and retain their ability to proliferate, differentiate, and interact with engineered matrices is crucial for creating artificial tissues/organs that mimic native biological structures in both form and function...

---

### P51: Towards the Experimentally-Informed In Silico Nozzle Design Optimization for Ext

**DOI**: 10.3389/fbioe.2021.701778
**Best distance**: 0.554
**Chunks retrieved**: 2

**Retrieved chunks:**

_[P51 chunk_1, d=0.554]_

Despite the extensive experimental work carried out on extrusion-based 3D bioprinting, a comprehensive view on the individual and combined effects of various parameters on cell fate is not straightforward to derive (Nair et al., 2009; Murphy and Atala, 2014; Mandrycky et al., 2016; Paxton et al., 2017; Moroni et al., 2018a). Cell viability has been reported to be as low as 40% (Mandrycky et al., 2016) and shear stress has been identi fi ed as one of the main causes (Gillispie et al., 2020). Fluid shear stress has been shown to in fl uence cell functionality in vivo (Wittkowske et al., 2016) and in vitro (Pedersen et al., 2016; Silvani et al., 2021). Probing into the maintenance of cell viability and functionality, many studies have made it clear that higher shear stresses (beyond physiological ranges) almost always lead to lower cell viability and altered functionality (Li et al., 2009; Nair et al., 2009; Ozbolat, 2016). Blaeser et al. found that shear stress should be controlled within 5 kPa to have more than 90% cell survival for mouse fi broblasts in a microvalve-based printing process (Blaeser et al., 2016). Higher dispensing pressure can allow ejecting highly viscous bioinks, ...

_[P51 chunk_22, d=0.567]_

Apartfrom printability, cell viability is the key aspect in evaluating the performance of a 3D bioprinted scaffold or construct (Sharma et al., 2020). However, no consensus has been reached on the relation between the in fl uential parameters and cell viability. For example, shear stress has been shown to affect the cells adversely in many studies (Nair et al., 2009; Li et al., 2011; Billiet et al., 2014; Wüst et al., 2015; Paxton et al.,
2017), whereas some studies report little or no in fl uence (Khalil and Sun, 2009). The reason for this can be of methodological or of intrinsic nature. Firstly, the time point when reporting cell viability ranges from immediate post-printing to a much longer timescale, e.g., up to 7 days (Blaeser et al., 2016). Secondly, different cell lines are used in the literature to perform cell viability evaluation, each having inherently different abilities to recover and regain viability as reported by Chang et al. (Chang et al., 2008). Combining these elements with the different materials and print settings leads to the situation where direct comparison of the different studies is neither feasible nor advisable. Figure 3 and ( Table 3 ) show that, given ...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

1) **Research Background** (Page 1-2)
"Bioprinting is a research-intensive field within regenerative medicine combining additive manufacturing technologies and tissue engineering concepts for reproducing functional organs and complex living tissues in the laboratory... However, there are still many challenges in order to guarantee cell survival and good printability. The three predominant techniques used for bioprinting are inkjet printing (or drop-by-drop bioprinting), extrusion bioprinting and laser-induced patterning. When using ...

**Core problem & critique:**
1) **Most Central Problem and Why It Matters:**
The most central problem addressed in this paper is quantifying how nozzle geometry and material properties affect shear stress during extrusion-based bioprinting, which directly impacts cell viability. This matters because optimizing these parameters can significantly improve the survival rate of cells post-printing, thereby enhancing the efficacy of 3D bioprinted tissues for regenerative medicine applications.

2) **Hardest Technical Difficulties:**
The hardest technical difficulties include accurately modeling complex nozzle geometries and mat...

---

### P27: Cell viability prediction and optimization in extrusion-based bioprinting via ne

**DOI**: 10.1088/1758-5090/ad17cf
**Best distance**: 0.558
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P27 chunk_20, d=0.558]_

These outcomes show the efficacy of our neural networks for predicting cell viability in bioprinting and imply that they may offer significant advantages over conventional regression and classification models. Additionally, we believe the models' performance can be enhanced even further by expanding the dataset to capture a broader range of patterns and relationships, reducing overfitting, and enhancing the model's generalization capability. Increasing the number of instances with diverse combinations of bioprinting parameters and corresponding cell viability measurements can be accomplished by collecting additional in-vitro data in the laboratory or incorporating data from other sources.

## 3.2.2. Permutation importance of bioprinting parameters

Permutation Importance was applied to determine the most significant features of bioprinting for predicting cell viability using a neural network for regression. Figure 4 shows ten of the most important features; the x -axis represents the significance score, while the y -axis represents the evaluated bioprinting parameters.
As demonstrated in this figure, the 'Cell type' has the most significant impact on optimizing the bioprinting proc...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

### 1. Research Background

The research background is outlined in the introduction and early parts of the paper:
"In the domains of regenerative medicine and cancer modeling, 3D bioprinting has witnessed rapid growth and is rising in popularity [1]. 3D bioprinting is a biofabrication process that refers to computer-guided additive manufacturing that allows the development of extremely accurate and complex 3D constructs utilizing biological elements in a pre-designed configuration [2–4]." (Page 2)

### 2. Core Concepts

Core concept...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters:**
   The most central problem addressed in this paper is optimizing cell viability during extrusion-based bioprinting processes. This matters significantly because maintaining high cell viability is crucial for the success of 3D bioprinted constructs, which are used extensively in regenerative medicine and cancer modeling. High cell viability ensures accurate representation of biological tissues, reliable experimental results, and effective therapeutic approaches.

2. **Hardest Technical Difficulties:**
   The hardest technical difficulties include...

---

### P111: Cell viability prediction and optimization in extrusion-based bioprinting via ne 🎯 (also cited in outline)

**DOI**: 10.1088/1758-5090/ad17cf
**Best distance**: 0.558
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P111 chunk_20, d=0.558]_

These outcomes show the efficacy of our neural networks for predicting cell viability in bioprinting and imply that they may offer significant advantages over conventional regression and classification models. Additionally, we believe the models' performance can be enhanced even further by expanding the dataset to capture a broader range of patterns and relationships, reducing overfitting, and enhancing the model's generalization capability. Increasing the number of instances with diverse combinations of bioprinting parameters and corresponding cell viability measurements can be accomplished by collecting additional in-vitro data in the laboratory or incorporating data from other sources.

## 3.2.2. Permutation importance of bioprinting parameters

Permutation Importance was applied to determine the most significant features of bioprinting for predicting cell viability using a neural network for regression. Figure 4 shows ten of the most important features; the x -axis represents the significance score, while the y -axis represents the evaluated bioprinting parameters.
As demonstrated in this figure, the 'Cell type' has the most significant impact on optimizing the bioprinting proc...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

**Research Background (Page 1-2)**

"The fields of regenerative medicine and cancer modeling have witnessed tremendous growth in the application of 3D bioprinting. Maintaining high cell viability throughout the bioprinting process is crucial for the success of this technology, as it directly affects the accuracy of the 3D bioprinted models, the validity of experimental results, and the discovery of new therapeutic approaches."

**Core Concepts (Page 2-4)**

"ML, is able to find connections between input parameters and forecast expec...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters:**
   The most central problem addressed in this paper is optimizing cell viability during extrusion-based bioprinting processes, which is crucial for the success of 3D bioprinted constructs used in regenerative medicine and cancer modeling. High cell viability ensures accurate representation of biological tissues, reliable experimental results, and effective therapeutic approaches.

2. **Hardest Technical Difficulties:**
   The hardest technical difficulties include accurately predicting cell viability under various bioprinting conditions using mac...

---

### P71: Prediction of cell viability in dynamic optical projection stereolithography-bas 🎯 (also cited in outline)

**DOI**: 10.1007/s10845-020-01708-5
**Best distance**: 0.570
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P71 chunk_2, d=0.570]_

To better understand post-printing cell viability, physicsbased models have been introduced to study how cells are damaged during bioprinting. Wang et al . (Wang et al. 2008) investigated the mechanical loading profile of cells using a mesh-free smooth particle hydrodynamic method, which was useful for understanding and predicting possible impactinduced cell damage. The cells were modeled as linear elastic solids, and the cell damage was determined by the cell membrane rupture due to the shear stresses imposed on the cells. The major conclusions were listed as below: 1) with the induced stresses, the cell membrane had severe deformation and was even damaged; and 2) to better quantify the cell damage, the stresses imposed on the cells from every source should be comprehensively incorporated such as those generated from the ejection process and the travel through air. Wang et al. (2009) used a finite element method (FEM) to investigate the mechanical loading profile of cells induced by the bubble expansion during laser-assisted bioprinting process. A neo-Hookean model was used to represent the living cells. It was found that both the process-induced cell stresses and the duration of ...

**Background (from SOP metadata):**
Certainly, here are the extracted sections from the research paper based on your request:

### 1. Research Background

**Page 996:**
Three dimensional (3D) bioprinting techniques can fabricate functional tissues with biocompatible materials and living cells. Several representative biomimetic tissues and organs such as blood vessels, skins, bones, and cartilages have been fabricated with various 3D bioprinting techniques (Mandrycky et al. 2016). Two bioprinting mechanisms have been developed: scaffold-based and scaffold-free bioprinting.

**Page 997:**
To better understand post-printing cell vi...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters (Page 995-996)**

The central problem addressed in this paper is predicting cell viability during dynamic optical projection stereolithography-based bioprinting, which is crucial for the successful fabrication of functional tissues with high cellular performance. This matters because UV irradiation used in the process can damage cells, and accurately predicting cell viability under varying conditions helps optimize printing parameters to enhance tissue functionality.

2. **Hardest Technical Difficulties (Pages 996-997)**

The hardest technical diffi...

---

### P73: Cell viability in extrusion bioprinting: the impact of process parameters, bioin

**DOI**: 10.1007/s00397-025-01504-z
**Best distance**: 0.587
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P73 chunk_3, d=0.587]_

Although a wider range of bioinks is processible in extrusion bioprinting, the bioink rheology constrains the throughput and minimum feature size of the print to prevent cell damage from extrusion forces (Boularaoui et al. 2020). Extrusion bioprinting experiments find broadly that cell viability (reported as the fraction of live cells in a volume) decreases as shear stress increases beyond a threshold value (Ouyang et al. 2016; Yu et al. 2013; Nair et al. 2009). Consequently, changes to the bioink rheology or process parameters that increase the extrusion shear stress are generally observed to reduce cell viability, including increasing bioink viscosity, flow rate, or extrusion pressure, or decreasing nozzle diameter (Blaeser et al. 2016; Chang et al. 2008; Nair et al. 2009; Li et al. 2010; Ouyang et al. 2016). An example experimental data set from Ouyang et al. (2016) is shown in Fig.1, where increasing shear stress by varying the bioink rheology reduced cell viability. These qualitative relationships aid in designing extrusion bioprinting processes to mitigate cell damage. For example, increasing the bioink viscosity may restrict the maximum flow rate or minimum nozzle diameter t...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

1) **Research Background** (Page 497-498)
   > "Extrusion bioprinting is a rapidly developing technology that prints cell-laden materials or “bioinks” to create complex, three-dimensional tissue constructs. This technology could play a key role in tissue engineering, drug screening, and cancer research. However, cells can be damaged or killed by extrusion forces during printing, limiting throughput and feature resolution."

2) **Core Concepts** (Page 498-501)
   > "The design flexibility, reproducibility, and accuracy of bioprinting...

**Core problem & critique:**
1) **Most Central Problem and Why It Matters:**
The most central problem addressed in this paper is predicting cell viability during extrusion bioprinting, which is crucial for optimizing the design of bioprinting processes. Cell viability directly impacts the success of tissue engineering applications, drug screening, and cancer research by ensuring that printed tissues maintain their biological function and integrity.

2) **Hardest Technical Difficulties:**
The hardest technical difficulties include accurately modeling cell deformation under varying extrusion conditions (shear stress, reside...

---

### P57: More than just life and death: advances in imaging and analysis for 3D-bioprinte

**DOI**: 10.3389/fbioe.2025.1600077
**Best distance**: 0.591
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P57 chunk_3, d=0.591]_

Printing methodologies can be categorized into pressure-based (Figure 1A) and light-based (Figure 1B) (Graham et al., 2017; Ozbolat and Hospodiuk, 2016; Murphy and Atala, 2014; Regehly et al., 2020). Each printing methodology uses cells encapsulated in compatible bioinks (natural or synthetic hydrogels) to create 3D structures and exerts various stresses on the cells that are not seen in traditional cell culture. It is vital to understand how the cell handling could affect the cells (i.e., shear stress in extrusion or droplet-based printing methods and phototoxicity in light-based methods). For example, shear stress can affect not only cell viability but also adhesion, proliferation, morphology and metabolic activity (Deo et al., 2020; Blaeser et al., 2016; Shi et al., 2018; Ng and Shkolnikov, 2024). In the cancer fi eld, it has been shown that shear stress can cause epithelial-to-mesenchymal transition, a hallmark of cancer, and change gene expression (Choi et al., 2019; Alvarado-Estrada et al., 2021; Nauseef et al., 2012). Phototoxicity from UV or near-UV light can cause DNA damage, leading to carcinogenesis (de Gruijl et al., 2001; Wang et al., 2018). It therefore seems prudent ...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

**Research Background:**
The research background is encapsulated in the introduction and early parts of the paper. It highlights that 3D bioprinting is a rapidly growing field with applications in microphysiological systems and tissue engineering but lacks sufficient validation and characterization tools (Page 1). The authors emphasize the need for robust imaging techniques and analysis methods to better understand the effects of 3D bioprinting on cell identity, behavior, and organelles. They also mention that while viability has be...

**Core problem & critique:**
1) **Most Central Problem and Why It Matters:**
The most central problem addressed in this paper is the inadequacy of current criteria for defining a successful 3D-bioprinted product, particularly beyond mere cell viability. This matters because as bioprinting technology advances, it becomes increasingly important to have robust standards that ensure the quality and reliability of these models for applications such as drug screening or disease modeling. Without comprehensive characterization methods, the utility and reproducibility of 3D-bioprinted tissues are compromised.

2) **Hardest Techni...

---
