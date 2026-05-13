# Section X.3.2.2: Nozzle and bioink design

**Target words**: 300
**Query**: `nozzle bioink design rheology extrusion printability ML prediction formulation`
**Generated**: 2026-05-13T14:51:28.451984

---

## Part A: Explicitly cited references in outline (with content)

### Quick index

- ✅ **P31** — `10.1088/1758-5090/ab8707` (in library)
- ✅ **P59** — `10.3390/gels11010045` (in library)
- ✅ **P42** — `10.36922/ijb.1280` (in library)
- ✅ **P62** — `10.1002/adhm.202402727` (in library)
- ✅ **P73** — `10.1007/s00397-025-01504-z` (in library)

### Detailed content per cited paper

#### 🎯 P31: Machine learning-based design strategy for 3D printable bioink: elastic modulus 

**DOI**: 10.1088/1758-5090/ab8707

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P31 chunk_24, d=0.674]_

In the absence of systematic studies on bioink development based on empirical knowledge in the development of bioinks, investigators currently invest considerable effort and cost in determining the criteria of bioinks through empirical experimentation, and they apply their findings to tissue engineering. We found a universal relationship between rheological properties of ink and printability; a high elastic modulus improves shape fidelity, and extrusion is possible below the critical yield stress, as supported by machine learning results. Based on this relationship, we derived various formulations of naturally derived bioinks that provide high shape fidelity using multiple regression analysis. This is the first study to introduce machine learning and mathematical models for the design and prediction of bioinks, although this predictive model does not directly support predictive tissue engineering research at the present level.
Further research is needed to predict the role of materials in terms of the biodegradability of bioinks and in biological functions, such as cell proliferation and differentiation. Furthermore, if the effectiveness of the bioinks in tissue regeneration is ver...

_[P31 chunk_23, d=0.701]_

The first method keeps the nozzle temperature at 4 ◦ Cto extrude the liquid ink and then maintains the substrate at 37 ◦ C to cause thermo-gelation immediately after printing to obtain the required shape fidelity. In this case, important properties determining printing quality are high viscosity to maintain the filament when the ink at 4 ◦ C is discharged, and fast gelation immediately after printing. Because both properties require chemical additives for control, this approach is not ideal to obtain 3D printable bioinks.
The second method is to pass the ink through the printing nozzle in the gel state. This is advantageous for forming filaments owing to the high viscosity of the gel, and the shape can be maintained because of its elasticity. However, the flowability of bioink during processing can decrease when mechanical properties such as yield stress and elasticity are too high. In this study, we adopted the second method to obtain a suitable printing ink by determining and controlling the appropriate range of elasticity and flowability of the bioink.
This work demonstrates a comprehensive approach to acquire printable bioinks with high shape fidelity for 3D printing, beginning...

_[P31 chunk_16, d=0.743]_

The dominant factor determining extrusion was τ y, as indicated in figure 4(c). When τ y is in the range of 74-5506 Pa (i.e. 14 inks in table 1), 92.90% of inks show extrusion (denoted by an output parameter of 1 for extrusion), indicating that ink was ejected from the nozzle. When τ y is in the range of 3960-50 000 Pa (seven inks in table 1), 85.70% of the inks are not ejected from the nozzle, clogging the nozzle (indicated by an output parameter of 0 for extrusion). Consequently, the main contributing factor determining extrusion is τ y, accounting for 89.5% (with an unexplained factor of 10.5%, figure 4(d)). The tendencies of all results in figure 4 are confirmed in supplementary figure 7.

## 3.4. Predictions for 3D printable bioinks

Asaresult of machine learning analysis, we found that the printable ink should have a high G ′ for high shape fidelity and low τ y for extrusion. To obtain a printable ink with high shape fidelity, we describe the prediction algorithm (equation (1)) used to achieve a high G ′ and low τ y using multiple regression.
where NV is the normalization value to obtain a high G ′ and low τ y , C is the concentration of collagen, H is the concentration of HA...

_[P31 chunk_4, d=0.747]_

Tissue engineering is a multidisciplinary study that is labor intensive and expensive, making predictive approaches necessary for successful future development. 3D bioprinting is a promising technology for predictive tissue engineering because it allows for standard manufacturing. To implement predictive tissue engineering based on 3D bioprinting, it is necessary to study mathematical models that can predict the properties of bioinks for efficient bioink development. Further, it is important to find and control the physical properties of materials that can be used to develop bioinks because these materials should be able to control printability and shape fidelity. Until now, there have been few well-established studies on the development of bioinks based on the empirical knowledge in the development of bioinks [29-33]. Investigating the universal factors to determine printability is challenging owing to significant ink-to-ink variability and the complex nonlinear relationship between ink composition and mechanical properties in hydrogels containing two or more ECM components. Further, it is nearly impossible to perform experiments one by one for an infinite number of cases with var...

_[P31 chunk_5, d=0.771]_

*Figure 1. Scheme of bioink development based on a mathematical model for predictive tissue engineering.*

Collagen
Fibrin
HA
Orthogonal design of
biopolymers mixture
Rheological analysis&
Orthogonaldesignofbioinks
printing
Collagen(%)
Machine learning&
multiple regression
Fibrin (%)
5
10
HA
olo
Mathematical modeling
Rheological analysis
Extrusion-basedprinting
of bioinks
Design ofprintable
bioinks
Biomedical application
Yield stress·Viscoelasity
·Extrusion·Shapefidelity
Invitrotissuemodel
·Machinelearning
·Mathematicalmodel
Regenerativemedicine
Bioink1
Bioink2
·Scaffolddegradation
Printablebioinks
·Cellgrowth
.Cell function
Bioinkn

## 2. Materials and methods


## 2.1. Materials

Six types of Type I collagen consisting of three native collagen (NC) and three atelocollagen (AC) purchased from various manufacturers were used in this study. The three types of NC were rat tail type I collagen (Corning Inc.), bovine type I collagen (Collagen Solutions), and calf skin type I collagen (MP Biomedical). The first two types were provided as liquids and the last one was provided lyophilized. All AC types were porcine skin type I collagen from different manufacturers (Sewon Sellontech, SK Bi...

**Background:**
Certainly, here are the extracted sections from the provided research paper text:

### 1. Research Background

**Page 1-2:**
"Three-dimensional (3D) printing technology has emerged as a promising tool to fabricate tissue and organ analogues to meet the needs of patients on organ donor waiting lists and to develop in vitro models for the preclinical testing of new drugs [1–4]. Owing to its potential to control the spatial arrangement of cells, 3D printing offers multiple degrees of freedom to imitate natural tissue systems. 3D printing also provides a platform to develop heterogeneous construct...

**Core problem:**
1. **Most Central Problem and Why It Matters:**
   The most central problem addressed in this paper is developing a machine learning-based method to design 3D-printable bioinks with optimal rheological properties for high shape fidelity and printability. This matters because the ability to create biocompatible, printable bioinks that maintain their structure during printing and support cell viability post-printing is crucial for advancing tissue engineering applications. Current limitations in bioink development hinder the practical implementation of 3D bioprinting technologies in clinical set...

---

#### 🎯 P59: Characterization and Machine Learning-Driven Property Prediction of a Novel Hybr

**DOI**: 10.3390/gels11010045

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P59 chunk_4, d=0.643]_

We hypothesized that various percentages of hydrogel mixes and shear rates could result from required rheological properties suitable for the extrusion-based bioprinting process. Current bioink optimization practices rely on extensive experimentation with hybrid hydrogel constituents to assess printability, shape fidelity, and biocompatibility. This approach is time-consuming, resource-intensive, and may yield suboptimal results due to the complex solution space. Predicting bioink properties is challenging due to polymer characteristics and chain entanglements [43]. While simple models like Einstein's linear prediction [44] can work for dilute and Newtonian fluids, and the Cross model can predict viscosity at different shear rates for non-Newtonian fluids [45], these models have limitations. They assume homogeneity and continuity, which may not apply to heterogeneous hybrid hydrogel systems. Additionally, determining rheological factors (n and K) for complex systems can be difficult and require extensive testing. In biomanufacturing, specifically for 3D bioprinting, predicting viscosity across different compositions is more valuable than predicting it for a single composition at va...

_[P59 chunk_33, d=0.735]_

During 3D printing, we observed the direct effect of gelatin as a form of 'gelatin/ (alginate × TONFC)' on the filament shape fidelity that can drive users to select the right ratio of bioink constituents to print defined filament width and consequently the pore geometry and 3D construct. Reportedly, gelatin has a better effect on cellular activities; therefore, the predictive model can help fine-tune the viscosity of a bioink to achieve printed construct with defined architecture and higher cell viability. Microstructural analysis using SEM supports this claim. Two examples of printed construct indicate the capability to fabricate large-scale (cm-scale) constructs using one of the hybrid hydrogels, e.g., A5G2T1. Finally, the growth trend of hMSCs mixing with A5G2T1 in various incubation days shows a great prospect for these hydrogels to be used as potential bioinks for extrusion-based 3D bioprinting purposes.

## 3. Conclusions

This study presents a framework for developing hybrid hydrogels for extrusion-based bioprinting. Various ML algorithms were compared by performance to predict viscosity in the context of constituents' weight and shear rate. After comparing polynomial fit, ...

_[P59 chunk_5, d=0.792]_

Very few of the reported articles considered the constituents' weights and shear rate simultaneously as a function of predicting viscosity. Moreover, a comparison of viscosity prediction performances of various ML algorithms can help choose the effective one. In this paper, a machine learning framework has been utilized to predict the viscosity of bioink prepared with hybrid hydrogels, aiming to enhance extrusion-based bioprinting techniques. The proposed approach incorporates a series of machine learning algorithms such as polynomial fit, decision tree, and random forest algorithms to determine the viscosity relating to the bioink constituents' weights and the shear rates. Polynomial fit, decision tree, and random forest were selected because they provide robust and effective predictive modeling capabilities for bioink viscosity [56-58]. Table 1 summarizes the features, advantages, and challenges of three ML algorithms used in this article along with a description using the results we observed. These algorithms allow for the simultaneous consideration of key factors, such as bioink formulation and shear rate, which are critical for enhancing extrusion-based bioprinting techniques....

_[P59 chunk_32, d=0.831]_

predictive model of viscosity in terms of constituents' weight and shear rate can redu the exhaustive experiments and assist in finding an effective combination of materials an process parameters to fabricate constructs with defined architecture and ensure better ce lular activities. In this study, three different ML algorithms were employed to predict the viscosit of a series of novel hybrid hydrogels composed of alginate, gelatin, TO-NFC, and consi The results of this study align with previous research demonstrating the effectiveness of Random Forest models in capturing complex, non-linear relationships in rheological data, outperforming simpler models like polynomial fit regression and decision tree [73]. Similar findings have been reported for predictive frameworks in bioink and polymeric systems, where random forest consistently achieves superior accuracy and reliability in viscosity modeling under varying shear rates [74,75].
ering shear rate: a polynomial fit model, a decision tree model, and a random forest mode
Each model's performance was evaluated using the coefficient of determination (R 2 ) an
mean absolute error (MAE). The comparison of R 2  value and MAE is shown in ...

_[P59 chunk_39, d=0.868]_

Utilizing an extrusion-based 3D bioprinter (BioX, CELLINK, Boston, MA, USA), filaments and scaffolds were fabricated. Hybrid hydrogels were prepared as described in Section 4.1, loaded into a 3.0 mL disposable nozzle, and extruded pneumatically onto a stationary build platform. The nozzle and bed temperatures of the 3D bioprinter were adjusted based on the amount of gelatin in the composition and ranged from 30 to 55 ◦ C. However, when bioprinting with cell-laden bioink, the nozzle temperature is expected to be constrained to 37 ◦ C to ensure maximum cell viability. In such cases, we plan to adjust the printing process parameters as outlined in our earlier publications to ensure the accuracy of filament and scaffold geometries [79,80]. The design and vectorized toolpath of a scaffold were created using Rhino 6.0 (https://www.rhino3d.com, accessed on 16 June 2024) (Robert McNeel and Associates, Seattle, WA, USA), a Visual Basic-based Computer-Aided Design (CAD) software. Slicer (https://www.slicer.org, V: 1.3.0, accessed on 16 June 2024), a G-code generator software, was used to create a Bio-X compatible file containing toolpath coordinates and process parameters. The bioprinting pr...

**Background:**
Based on the provided text, here are the extracted sections:

1. **Research Background** (Page 4 of 26)
   > Bioprinting is an evolving technology that utilizes computer-controlled 3D printing to create scaffolds for tissue engineering. According to the American Society for Testing and Materials (ASTM) standards [ 1], the most common bioprinting techniques include extrusion-based methods (e.g., microextrusion, direct writing) [2,3], jetting-based methods (e.g., inkjet, laser-assisted) [4–6], and vat polymerization techniques like stereolithography (SLA) [7,8]. These methods involve the spatial...

**Core problem:**
1. **Most Central Problem and Why It Matters**
   - The most central problem addressed in this paper is the prediction of bioink viscosity as a function of component weights and shear rate for extrusion-based 3D bioprinting. This matters because accurate viscosity predictions are crucial for optimizing the rheological properties of bioinks, which directly impact printability, shape fidelity, and mechanical integrity of printed scaffolds in tissue engineering applications.

2. **Hardest Technical Difficulties**
   - The hardest technical difficulties include:
     1. Developing predictive model...

---

#### 🎯 P42: Rheology-informed hierarchical machine learning model for the prediction of prin

**DOI**: 10.36922/ijb.1280

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P42 chunk_4, d=0.516]_

Furthermore, the rheological properties, such as viscosity and shear modulus, of bioinks have been verified to be closely related to the printing parameters to optimize  the  printability  of  extrusion-based  bioprinting (Figure  1) [47-53] .  For  instance,  even  though  the  viscosity of bioink increases, the flow rate can be maintained if the printing parameters such as pressure and nozzle size are appropriately increased. Even with the same flow rate, the printing resolution significantly correlates with the shear modulus and nozzle velocity. Despite the deep correlation between  rheology  and  printability,  there  have  been  no studies  that  actively  applied  rheological  measurements of  various  bioinks  and  multiple  printing  parameters  to machine learning.
Therefore, in this study, a rheology-informed hierarchical machine learning (RIHML) model was developed to predict printability in extrusion-based bioprinting.  Among  previously  suggested  methods  to quantify printability, the assessment of printing resolution, which  has  been  widely  applied  in  numerous  printability studies,  was  mainly  adopted.  To  construct  a  dataset  for training the models, the...

_[P42 chunk_3, d=0.572]_

Hence, printability prediction is critical to the accurate and  effective  fabrication  of  tissue-engineered  constructs using the extrusion-based bioprinting technique. In several existing  studies,  the  physical  model-based  computation was adopted for printability prediction [33-38] . More precisely, the physical model of printability prediction was derived  from  hydrodynamic  equations  combined  with the rheological modeling of generalized Newtonian fluid, mainly  power-law  fluid.  Using  the  physical  model,  the printing  resolution  of  the  output  filament  was  simulated with multiple printing parameters and compared with the actual printing resolution. Although several studies using the physical model reported interesting results, the model holds  many assumptions and simplifications, limiting its application in various bioprinting tasks. For instance, the physical prediction model is highly sensitive to the power law  index,  which  can  be  obtained  by  the  line  fitting  of the  measured viscosity.  Thus,  small  errors  in  rheological measurement and line fitting may have a significant effect on prediction accuracy. Additionally, the assumptions in the phys...

_[P42 chunk_0, d=0.601]_

## Abstract

In  this  study,  a  rheology-informed  hierarchical  machine  learning  (RIHML)  model was  developed  to  improve  the  prediction  accuracy  of  the  printing  resolution  of constructs fabricated by extrusion-based bioprinting. Specifically, the RIHML model, as  well  as  conventional  models  such  as  the  concentration-dependent  model  and printing parameter-dependent model, was trained and tested using a small dataset of bioink properties and printing parameters. Interestingly, the results showed that the RIHML model exhibited the lowest error percentage in predicting the printing resolution for different printing parameters such as nozzle velocities and pressures, as well as for different concentrations of the bioink constituents. Besides, the RIHML model could predict the printing resolution with reasonably low errors even when using a new material added to the alginate-based bioink, which is a challenging task for conventional models. Overall, the results indicate that the RIHML model can be a useful tool to predict the printing resolution of extrusion-based bioprinting, and it is versatile and expandable compared to conventional models since the RIHML mode...

_[P42 chunk_2, d=0.601]_

However, the advantages of the generous availability of bioink candidates including hydrogels, extracellular matrix, bioceramic particles, and shear thickening materials create difficulties  in  tuning  bioink  compositions  and  finding appropriate  printing  conditions [17,18] .  Thus,  to  overcome these  challenges  and  complexities  in  the  preparation  of bioinks and extrusion-based bioprinting, printability has recently  attracted  considerable  attention.  Although  the definition  of  printability  in  extrusion-based  bioprinting is  still  in  discussion,  it  is  obvious  that  better  printability can  improve  the  printing  accuracy  and  shape  fidelity  of the printed constructs, leading to faster fabrication speed and  long-term  stable  functionality [19-22] .  Further,  recent printability studies have quantitatively evaluated printing accuracy and shape fidelity using the assessment of various outcomes, such as printing resolution relative to the nozzle diameter, distance between filaments, pore size and shape in a grid structure, and height of the stacked layers [23-25] . In addition, these studies have demonstrated that printability is deeply linked to how ...

_[P42 chunk_27, d=0.614]_

Although  the  RIHML  model  has  the  potential  for accurate and robust prediction of printability, there is still room for improvement. Due to the generalizability of the bioink properties, a wider range of rheological properties of  bioinks  can  enhance  the  prediction  accuracy  of  the RIHML model. For instance, in the results presented in Figure  7C,  relatively  high  errors  were  observed  in  F127 with a concentration of 45%. Specifically, this may occur because its viscosity and storage modulus were the highest around  the  upper  bound  of  the  rheological  data  range. In terms of future work, it would be beneficial to further validate the performance of the RIHML model from other types  of  bioprinting  methods,  such  as  inkjet-based  or laser-assisted bioprinting, to demonstrate the feasibility of rheology-based prediction of printability across different bioprinting  methods.  Additionally,  future  studies  could investigate the potential of the RIHML model in predicting other  aspects  of  printability,  such  as  the  extrudability, pore  size,  pore  shape,  and  shape  fidelity  of  the  stacked layers.

## 5. Conclusion

In conclusion, this study suggest...

**Background:**
(missing)

**Core problem:**
1) **Most Central Problem and Why It Matters (Page 309-310):**
The central problem addressed in this paper is the difficulty in predicting printability for extrusion-based bioprinting, which involves finding optimal printing conditions given a wide range of bioink candidates. This matters because it directly impacts the efficiency and accuracy of tissue engineering processes, enabling faster fabrication speeds and improved shape fidelity.

2) **Hardest Technical Difficulties (Pages 310-314):**
The hardest technical difficulties include developing a machine learning model that can handle small ...

---

#### 🎯 P62: 3D Bioprinting and Artificial Intelligence-Assisted Biofabrication of Personaliz

**DOI**: 10.1002/adhm.202402727

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P62 chunk_17, d=0.729]_

An ideal bioink should be able to be printed into filaments with controlled dimensions. [30,56] The printability of a bioink and the resultant resolution of printed filaments is dependent on multiple factors including the viscosity of the bioink, print nozzle diameter, pressure, speed, and features of the print structure. [ 30,59] First, to assess the printability and print resolution, a representative bioink formulation (ink/MX-2.0) was printed as a line using different nozzle diameters (22-27G), printing pressures (626 kPa), and print speeds (2.5-20 mm -1 s). The thickness of the printed filaments was quantified as a measure of print resolution. The 3 conical nozzles of 22G, 25G, and 27G correspond to an internal diameter of 0.41, 0.25, and 0.20 mm, respectively. For the 5 print pressures and 8 print speeds tested for each nozzle diameter, the range of printed fiber diameters was widely tunable from ≈ 170 µ mand ≈ 2.2 mm ( Figure 4 A). Further, for the 3 nozzle diameters tested, the filament diameter showed an increasing trend with increasing print pressure and a decreasing trend with increasing print speed (Figure 4A). The test also provided a range of print speed and print pres...

_[P62 chunk_11, d=0.775]_

## 2.9. Statistical Analysis

Quantitative data were expressed as mean ± standard deviation. Comparison between groups was performed using one-way ANOVA with Bonferroni corrections. Differences were considered significant if p ≤ 0.05. The AI-derived platform analyzed and correlated parameter combinations and bioprinting diameters via the built-in function of stepwise regression in MATLAB R2020b (MathWorks Inc.). The platform-estimated coefficients were analyzed using the sum of square Ftest. The statistical significance (p-values) of estimated coefficients served as the exclusion criteria for the stepwise regression analysis.

## 3. Results and Discussion


## 3.1. Rheological Properties of Polysaccharide/Fibrinogen-Based Bioink

The rheological characteristics of hydrogels and bioinks play a crucial role in the context of extrusion-based bioprinting. For extrusion-based bioprinting, an ideal bioink must undergo extrusion smoothly with a uniform flow rate to prevent nozzle clogging during printing and quickly stabilize to withstand deformation post-printing, ensuring structural integrity throughout the
www.advhealthmat.de
lifespan of the printed construct. [ 30,54] This necessitate...

_[P62 chunk_19, d=0.784]_

21922659, 2025, 13, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/adhm.202402727 by NICE, National Institute for Health and Care Excellence, Wiley Online Library on [20/04/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License www.advancedsciencenews.com www.advhealthmat.de the bioprinted structures leading to swelling of the bioprinted structures. [ 65,66] While this affects the precision of the bioprinted structures, this could be utilized to overcome the potential contraction of hydrogels over time owing to cellular activity.
ADVANCED
SCIENCENEWS

*Figure 4. Characterization of print resolution of polysaccharide/fibrinogen-based bioink formulations. A) Print resolution (diameter of printed filament) of a representative bioink formulation (ink/MX-2.0) printed using different nozzles, printing pressures, and print speeds. The dotted line in each graph represents the internal diameter of the print nozzle. B) Heat maps show the spreading ratios (print filament width divided by needle diameter) of the printed filament...

_[P62 chunk_23, d=0.791]_

26
27
26
Nozzle(G)
25
24
23
22
10
12
0.4
0.5
Ink (%)
1.5
12
Printing Speed (mm/s)
Printing Speed (mm/s)
E
F
G
1.1
6'0
2.5
2.5
2.5
2
2
2
0.8
1.5
1.5
(uw)
1.5
60
Diameter(mm)
1.5
0.8
0.7
0.5
0.5
0.7
0.5
9'0
0
0.6
0.5
27
12
0.5
2.5
Ink (%)
1.5
9
10
Pressure (kPa)
11
12
13
26
Nozzle(G)
25
24
23
22
9
10
Pressure (kPa)
11
12
13
0.4
0.5
10
6
10
Pressure (kPa)
11
12
13
0.4

*Figure 6. AI-derived optimization for bioprinting parameters. A) Validation of combinations pinpointed by the platform. Each combination is represented in mean ± SD ( n = 5) and the gray dots represent each replicate. B-G) Interaction surfaces of every pair of parameters while holding the remaining 2 parameters constant at mid-level ( n = 5).*

in a diameter of 0.529 ± 0.034 mm ( n = 5). Another pinpointed combination (printing speed 13 mm -1 s, 9 kPa, nozzle size 22 G (inner diameter-0.41 mm), 3% ink resulted in a diameter of 0.462 ± 0.006 mm ( n = 5). However, it is important to note that due to factors like batch-to-batch variations in bioink preparation and/or air bubbles in the bioink, some combinations pinpointed by the AI-derived optimization platform may not consistently align with the predictions. For example,...

_[P62 chunk_16, d=0.795]_

This trend reflects the inverse relationship between shear rate and viscosity for shear-thinning bioinks, wherein formulations with higher viscosities (higher MX content) at zero-shear undergo less flow rate through the same nozzle geometry and applied pressure. The results also indicate that the incorporation of higher MX concentrations resulted in a proportional increase in bioprinting viscosity ( /u1D702 b ), consistent with the higher values of the power-law coefficient K observed for these formulations (Figure 3G and Table 2). The bioprinting shear rates and viscosities observed for all 4 bioink formulations were lower or similar to those observed for alginate, agarose, xanthan gum, and gelatinbased bioinks. [32,41,44] The bioprinting viscosities ( ≈ 2-14 Pa s -1 ) observed in this study are higher than those reported for gelatin and fibrin hydrogels ( ≈ 1-7.5 mPa s), which could be attributed to the incorporation of polysaccharide-based thickeners namely, NFC, maltodextrin, and xanthan gum.
21922659, 2025, 13, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/adhm.202402727 by NICE, National Institute for Health and Care Excellence, Wiley Online Library on ...

**Background:**
Based on the provided text, here are the extracted sections:

**Research Background:**
"The gingival mucosa, commonly known as the gums, plays a vital role in protecting the teeth and underlying structures from various threats, including mechanical, chemical, and microbial factors. Mucogingival defects, including gingival recession, inadequate keratinized tissue, and mucosal dehiscence are prevalent in the population.[1–3] If left untreated, mucogingival defects, particularly gingival reces- sions tend to undergo progressive tissue breakdown resulting in attachment loss between the gingiva and...

**Core problem:**
1. **Most Central Problem and Why It Matters (Page 2-3):**
   The central problem addressed in this paper is the development of personalized oral soft tissue grafts using 3D bioprinting, which aims to overcome limitations associated with traditional autologous graft methods for treating mucogingival defects. This matters because current approaches are limited by donor site morbidity and lack of availability, making a novel approach highly desirable.

2. **Hardest Technical Difficulties (Pages 4-7):**
   The hardest technical difficulties include optimizing the rheological properties of bioinks...

---

#### 🎯 P73: Cell viability in extrusion bioprinting: the impact of process parameters, bioin

**DOI**: 10.1007/s00397-025-01504-z

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P73 chunk_0, d=0.581]_

## Abstract

Extrusion bioprinting is a rapidly developing technology that prints cell-laden materials or 'bioinks' to create complex, three-dimensional tissue constructs. This technology could play a key role in tissue engineering, drug screening, and cancer research. However, cells can be damaged or killed by extrusion forces during printing, limiting throughput and feature resolution. Here, we propose a critical strain-based cell model for predicting cell viability during extrusion that incorporates process parameters, bioink rheology, and cell mechanical properties. We extract parameters from practical nozzle diameters and extrusion flow rates, from power law and Herschel-Bulkley fits to bioink bulk rheology, and from single-cell rheology measurements of cell stiffness and fluidity, and then combine them for the first time to predict viability. This model agrees well with existing cell viability studies and further predicts that cell viability decreases with increasing flow rate, increasing bioink viscosity, increasing nozzle length, or decreasing nozzle radius. Mechanistically, these effects are linked to changes in shear stress or residence time of cells within the nozzle, wh...

_[P73 chunk_7, d=0.638]_

In this work, extrusion of bioinks described by power law and Herschel-Bulkley rheological models is examined and coupled to a mechanical model of cell deformation to predict the fraction of viable cells after extrusion. The flow geometry is a nozzle of length, L , and diameter, D = 2 R , from which bioink is extruded at a flow rate, Q (Fig. 2a). The radial, azimuthal, and axial coordinates are ( r , θ, z ) , respectively. Blunt-tipped syringe needles are common nozzles in bioprinting experiments and commercially available in standard sizes or 'gauges' with inner diameters ranging from a few millimeters (low gauge) to fifty microns (high
Fig. 2 Extrusion bioprinting flow problem. a Illustration of a standard syringe needle often used as nozzles in extrusion bioprinting, with length, L ; diameter, 2 R ; and flow rate, Q . b Velocity profiles ( v ) for power law and Herschel-Bulkley fluids and the underlying shear stress ( σ ) profile within the nozzle. Shear stress is zero at the center of the nozzle and maximal at the walls. c Correspondingly, the critical strain cell viability model predicts that cells traveling closer to the wall are more likely to be damaged by shear than those ...

_[P73 chunk_6, d=0.705]_

An approach to address these limitations is to develop a cell viability model based on cell deformation that can draw upon an extensive body of work investigating single-cell rheology of various cell types. Cells have complex rheological behavior, exhibiting viscoelasticity, viscoplasticity, stiffening, softening, and poroelasticity (Jung et al. 2020) that notably differ across cell types. For example, stem cells are relatively sensitive to applied stresses (Boraas et al. 2016) whereas endothelial cells, which are commonly exposed to shear stresses from blood flow, are more resilient (Chistiakov et al. 2017). The mechanical properties of cells are also dynamic, evolving to facilitate cell functions in different physiological environments (Urbanska and Guck 2024). These rheological behaviors stem from the complex structure of cells which includes actin and intermediate filaments, microtubules, and the cell nucleus, each contributing unique aspects to the cell rheology (see Table 1 in Jung et al. 2020). Despite their complexity, the mechanical behavior of numerous cell types can be broadly described by relatively simple models and measured using techniques such as micropipette aspira...

_[P73 chunk_1, d=0.710]_

Catherine A. Fromen cfromen@udel.edu cally accurate ear cartilage (Kang et al. 2016) or aortic valves (Hockaday et al. 2012; Song et al. 2020), as well as others that produced functional vascular channels (Kolesky et al. 2014; Skylar-Scott et al. 2019) or liver models (Ma et al. 2020). The success of these applications was enabled by carefully tuning the rheology of the cell-laden soft materials for printing. These living materials-known as bioinks-have widely ranging rheology depending on the material deposition modality of the bioprinter, which include droplet-, laser-, or extrusion-based processes (Dababneh and Ozbolat 2014; Eskizengin and Ergun 2024).
1 Department of Chemical & Biomolecular Engineering, University of Delaware, 150 Academy Street, Newark, DE 19716, USA
2 Department of Biomedical Engineering, University of Delaware, 590 Avenue 1743, Newark, DE 19713, USA
For dropletand laser-based bioprinting, bioinks are restricted to mostly hydrogel precursors, where the viscosity should be less than η ∼ 30 mPa · s and η ∼ 300 mPa · s, respectively, to maintain satisfactory printability (Saunders and Derby 2014; Mandrycky et al. 2016). In comparison, extrusion bioprinting accom...

_[P73 chunk_5, d=0.727]_

Current correlation-based models do not capture the breadth of newly available bioinks and cell types. The cell viability models described previously consider a narrow range of bioinks that are predominantly alginate hydrogel precursor solutions (Table 1). Yield stress fluid bioinks are being developed due to their unique and advantageous biological and mechanical properties (Seymour et al. 2021; Qazi et al. 2022). However, cell viability has not been modeled in these bioinks and experimental data is limited (Aguado et al. 2012). Existing models could be extended to yield stress fluids, but they fail to address differences in cell mechanical properties. Additionally, due to the empirical nature of current cell damage models, extrusion cell viability cannot be quantitatively or qualitatively predicted for cells where extrusion viability data is unavailable. The scope of modeling efforts must expand to match the growing diversity of bioink microstructures and cell types in extrusion bioprinting.
An approach to address these limitations is to develop a cell viability model based on cell deformation that can draw upon an extensive body of work investigating single-cell rheology of vari...

**Background:**
Based on the provided text, here are the extracted sections:

1) **Research Background** (Page 497-498)
   > "Extrusion bioprinting is a rapidly developing technology that prints cell-laden materials or “bioinks” to create complex, three-dimensional tissue constructs. This technology could play a key role in tissue engineering, drug screening, and cancer research. However, cells can be damaged or killed by extrusion forces during printing, limiting throughput and feature resolution."

2) **Core Concepts** (Page 498-501)
   > "The design flexibility, reproducibility, and accuracy of bioprinting...

**Core problem:**
1) **Most Central Problem and Why It Matters:**
The most central problem addressed in this paper is predicting cell viability during extrusion bioprinting, which is crucial for optimizing the design of bioprinting processes. Cell viability directly impacts the success of tissue engineering applications, drug screening, and cancer research by ensuring that printed tissues maintain their biological function and integrity.

2) **Hardest Technical Difficulties:**
The hardest technical difficulties include accurately modeling cell deformation under varying extrusion conditions (shear stress, reside...

---

## Part B: Semantic search results (Chroma top N)

### P42: Rheology-informed hierarchical machine learning model for the prediction of prin 🎯 (also cited in outline)

**DOI**: 10.36922/ijb.1280
**Best distance**: 0.516
**Chunks retrieved**: 6

**Retrieved chunks:**

_[P42 chunk_4, d=0.516]_

Furthermore, the rheological properties, such as viscosity and shear modulus, of bioinks have been verified to be closely related to the printing parameters to optimize  the  printability  of  extrusion-based  bioprinting (Figure  1) [47-53] .  For  instance,  even  though  the  viscosity of bioink increases, the flow rate can be maintained if the printing parameters such as pressure and nozzle size are appropriately increased. Even with the same flow rate, the printing resolution significantly correlates with the shear modulus and nozzle velocity. Despite the deep correlation between  rheology  and  printability,  there  have  been  no studies  that  actively  applied  rheological  measurements of  various  bioinks  and  multiple  printing  parameters  to machine learning.
Therefore, in this study, a rheology-informed hierarchical machine learning (RIHML) model was developed to predict printability in extrusion-based bioprinting.  Among  previously  suggested  methods  to quantify printability, the assessment of printing resolution, which  has  been  widely  applied  in  numerous  printability studies,  was  mainly  adopted.  To  construct  a  dataset  for training the models, the...

_[P42 chunk_3, d=0.572]_

Hence, printability prediction is critical to the accurate and  effective  fabrication  of  tissue-engineered  constructs using the extrusion-based bioprinting technique. In several existing  studies,  the  physical  model-based  computation was adopted for printability prediction [33-38] . More precisely, the physical model of printability prediction was derived  from  hydrodynamic  equations  combined  with the rheological modeling of generalized Newtonian fluid, mainly  power-law  fluid.  Using  the  physical  model,  the printing  resolution  of  the  output  filament  was  simulated with multiple printing parameters and compared with the actual printing resolution. Although several studies using the physical model reported interesting results, the model holds  many assumptions and simplifications, limiting its application in various bioprinting tasks. For instance, the physical prediction model is highly sensitive to the power law  index,  which  can  be  obtained  by  the  line  fitting  of the  measured viscosity.  Thus,  small  errors  in  rheological measurement and line fitting may have a significant effect on prediction accuracy. Additionally, the assumptions in the phys...

_[P42 chunk_0, d=0.601]_

## Abstract

In  this  study,  a  rheology-informed  hierarchical  machine  learning  (RIHML)  model was  developed  to  improve  the  prediction  accuracy  of  the  printing  resolution  of constructs fabricated by extrusion-based bioprinting. Specifically, the RIHML model, as  well  as  conventional  models  such  as  the  concentration-dependent  model  and printing parameter-dependent model, was trained and tested using a small dataset of bioink properties and printing parameters. Interestingly, the results showed that the RIHML model exhibited the lowest error percentage in predicting the printing resolution for different printing parameters such as nozzle velocities and pressures, as well as for different concentrations of the bioink constituents. Besides, the RIHML model could predict the printing resolution with reasonably low errors even when using a new material added to the alginate-based bioink, which is a challenging task for conventional models. Overall, the results indicate that the RIHML model can be a useful tool to predict the printing resolution of extrusion-based bioprinting, and it is versatile and expandable compared to conventional models since the RIHML mode...

_[P42 chunk_2, d=0.601]_

However, the advantages of the generous availability of bioink candidates including hydrogels, extracellular matrix, bioceramic particles, and shear thickening materials create difficulties  in  tuning  bioink  compositions  and  finding appropriate  printing  conditions [17,18] .  Thus,  to  overcome these  challenges  and  complexities  in  the  preparation  of bioinks and extrusion-based bioprinting, printability has recently  attracted  considerable  attention.  Although  the definition  of  printability  in  extrusion-based  bioprinting is  still  in  discussion,  it  is  obvious  that  better  printability can  improve  the  printing  accuracy  and  shape  fidelity  of the printed constructs, leading to faster fabrication speed and  long-term  stable  functionality [19-22] .  Further,  recent printability studies have quantitatively evaluated printing accuracy and shape fidelity using the assessment of various outcomes, such as printing resolution relative to the nozzle diameter, distance between filaments, pore size and shape in a grid structure, and height of the stacked layers [23-25] . In addition, these studies have demonstrated that printability is deeply linked to how ...

_[P42 chunk_27, d=0.614]_

Although  the  RIHML  model  has  the  potential  for accurate and robust prediction of printability, there is still room for improvement. Due to the generalizability of the bioink properties, a wider range of rheological properties of  bioinks  can  enhance  the  prediction  accuracy  of  the RIHML model. For instance, in the results presented in Figure  7C,  relatively  high  errors  were  observed  in  F127 with a concentration of 45%. Specifically, this may occur because its viscosity and storage modulus were the highest around  the  upper  bound  of  the  rheological  data  range. In terms of future work, it would be beneficial to further validate the performance of the RIHML model from other types  of  bioprinting  methods,  such  as  inkjet-based  or laser-assisted bioprinting, to demonstrate the feasibility of rheology-based prediction of printability across different bioprinting  methods.  Additionally,  future  studies  could investigate the potential of the RIHML model in predicting other  aspects  of  printability,  such  as  the  extrudability, pore  size,  pore  shape,  and  shape  fidelity  of  the  stacked layers.

## 5. Conclusion

In conclusion, this study suggest...

_[P42 chunk_26, d=0.618]_

Since  the  formulation  of  bioinks  and  the  process  of bioprinting  are  more  complicated  and  correlated,  the prediction  of  printability  in  3D  bioprinting  has  become more  challenging.  Recently,  there  have  been  attempts related to the prediction of bioprinting printability using machine  learning.  However,  unlike  other  fields  such  as medical  imaging  and  genetics,  3D  bioprinting  suffers from  data  size,  which  may  hardly  be  large  because  the preparation  of  bioinks  with  various  compositions  and their 3D printing with multiple parameters are sequential and  highly  time-consuming [55-57] .  Therefore,  it  is  crucial to  develop  an  efficient  machine  learning  model  that is  suitable  for  small  dataset  sizes  while  ensuring  high prediction accuracy. With the hierarchical architecture of the  developed model, RIHML can effectively predict the printing  resolution  of  extrusion-based  bioprinting  using small datasets. In this study, the dataset of 537 numbers of bioink rheological properties and printing process was used for training,  validation,  and  testing  of  the  machine learning  model.  Several  bioprinting  studies  em...

**Background (from SOP metadata):**
(missing)

**Core problem & critique:**
1) **Most Central Problem and Why It Matters (Page 309-310):**
The central problem addressed in this paper is the difficulty in predicting printability for extrusion-based bioprinting, which involves finding optimal printing conditions given a wide range of bioink candidates. This matters because it directly impacts the efficiency and accuracy of tissue engineering processes, enabling faster fabrication speeds and improved shape fidelity.

2) **Hardest Technical Difficulties (Pages 310-314):**
The hardest technical difficulties include developing a machine learning model that can handle small ...

---

### P40: Application of machine learning in 3D bioprinting of cultivated meat

**DOI**: 10.36922/ijamd.2279
**Best distance**: 0.559
**Chunks retrieved**: 3

**Retrieved chunks:**

_[P40 chunk_6, d=0.559]_

Another  study  has  constructed  ML  algorithms  using decision tree (DT), RF, and DL to predict the printability of  biomaterials  with  a  train/test  ratio  of  7:3. 43 A  total of  210  biomaterial  formulations  were  3D  printed  using an  extrusion-based  printing  technique  under  constant conditions  (e.g.,  nozzle  diameter,  layer  thickness,  print speed, and print temperature), and the printability of each formulation was categorized based on the shape fidelity of the printed structures. All ML methods successfully learned and predicted the printability of various bioinks based on their biomaterial formulations. The RF algorithm achieved the  highest  accuracy  (88.1%),  precision  (90.6%),  and F1 -score (870%), indicating superior overall performance among the three algorithms, while DL exhibited the highest recall percentage (87.3%). In addition, the ML algorithms could generate a printability map of biomaterials to guide bioink development using a standardized combination of printing conditions (Figure 2).
In another study, a hierarchical ML model, governed by rheology data, was implemented to enhance the accuracy of predicting the printing resolution of construc...

_[P40 chunk_7, d=0.615]_

*Figure 2. A comprehensive overview of printing outcomes for two distinct types of bioinks: (A) hydrogel-based F127/LP bioinks and (B) polymer-based PCL/nHA bioinks. In addition, it encompasses (C) a ML-generated printability map for both bioinks using DT, RF, and DL algorithms. The green triangles and red crosses within these maps denote printable and unprintable formulations based on the training data. The green and red areas correspond to the predicted printable and unprintable regions extrapolated from the testing results. Scale bar = 0.5 mm. Figure reproduced from Chen et al. 43 Abbreviations: F: Pluronic F127; LP: Laponite nanoclay; nHA: Hydroxyapatite nanoparticles; PCL: Polycaprolactone; SF: Shape fidelity.*

B
C
A
20F
15F/6LP
15F/8LP
8LP
Extrusion
morphology
1-layer
structure
4-layer0°90°
structure
0.5mm
SF
22%
45%
91%
N/A
Printability
X No
VYes
VYes
X No
30PCL
50PCL
50PCL/20nHA
50PCL/30nHA
Extrusion
morphology
IIII
1-layer
Nozzle
structure
clogging
4-layer0°90°
structure
0.5mm
SF
17%
51%
88%
N/A
Printability
X No
/Yes
VYes
X No
DecisionTree(DT)
一
RandomForest(RF)
Deep Learning (DL)
一
10
10
10
Laponite (wt%)
Laponite(wt%)
Laponite(wt%)
Printable
Printable
region
region
Pri...

_[P40 chunk_5, d=0.619]_

(mechanical or pneumatic), layer height, extrusion multiplier, print  pressure,  and  infill  density.  A  total  of  345  videos (115 videos per classification) were used for model training and evaluation, with a train/test ratio of 9:1. The DL model demonstrated  an  overall  prediction  accuracy  of  94.3%; a precision value of 87.2% with a recall value of 96.5% for 'good print outcome, ' a precision value of 97.6% with a recall value  of  92.2%  for  'under-extrusion  print  outcome, '  and a precision value of 98.3% with a recall value of 94.5% for 'over-extrusion print outcome. '
In  another  study,  response  surface  methodology  was employed  to  evaluate  the  relationship  between  rheological properties and printability. Thirteen bioink formulations were used  to  print  filaments  and  optical  microscopy  images  were  used to assess printability based on filament width and roughness. 42 Random forest (RF) classification models were constructed using  three  feature  sets  -  rheological  measurements  and formulation  parameters,  rheological  measurements  alone, or  formulation  parameters  alone.  Predictions  for  filament width  showed  that  training  with  for...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections as requested:

**Research Background:**
"Cultivated meat production, an innovative and sustainable alternative to conventional animal farming, has gained significant attention in recent years. As the demand for ethical and environmentally friendly protein sources continues to rise, the need for efficient and scalable production strategies becomes critical." (Page 3)

"Traditional livestock farming has a large ecological footprint; intensive factory farming and poor animal welfare conditions are common causes of foodborne illnesses, an...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters**
   - The most central problem addressed in this paper is the optimization and quality control of 3D bioprinting processes for cultivated meat using machine learning (ML). This matters because traditional methods are time-consuming, resource-intensive, and often lack precision. ML can potentially streamline these processes by predicting printability, optimizing printing parameters, characterizing meat flavor, and ensuring quality control, thereby making the production of cultivated meat more efficient and scalable.

2. **Hardest Technical Difficult...

---

### P73: Cell viability in extrusion bioprinting: the impact of process parameters, bioin 🎯 (also cited in outline)

**DOI**: 10.1007/s00397-025-01504-z
**Best distance**: 0.581
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P73 chunk_0, d=0.581]_

## Abstract

Extrusion bioprinting is a rapidly developing technology that prints cell-laden materials or 'bioinks' to create complex, three-dimensional tissue constructs. This technology could play a key role in tissue engineering, drug screening, and cancer research. However, cells can be damaged or killed by extrusion forces during printing, limiting throughput and feature resolution. Here, we propose a critical strain-based cell model for predicting cell viability during extrusion that incorporates process parameters, bioink rheology, and cell mechanical properties. We extract parameters from practical nozzle diameters and extrusion flow rates, from power law and Herschel-Bulkley fits to bioink bulk rheology, and from single-cell rheology measurements of cell stiffness and fluidity, and then combine them for the first time to predict viability. This model agrees well with existing cell viability studies and further predicts that cell viability decreases with increasing flow rate, increasing bioink viscosity, increasing nozzle length, or decreasing nozzle radius. Mechanistically, these effects are linked to changes in shear stress or residence time of cells within the nozzle, wh...

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

### P2: AI-driven 3D bioprinting for regenerative medicine

**DOI**: _missing_
**Best distance**: 0.618
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P2 chunk_21, d=0.618]_

## 3.4. Design of bioink materials

Owing to the tissue- and function-specific nature of the repaired part [113], personalized design for bioink materials is necessary to fulfill specific properties (or CQA) [114 -118]. Typically, this entails significant  domain  expertise  and  extensive  trial  and  error,  which  are  both time-consuming and expensive. However, ML methods offer avenues for improvement in two key aspects: (i) reduction of time and cost associated with property characterization for high-throughput screening of bioink materials, and (ii) modeling the intricate mapping relationship between  the  fingerprints  and  properties  of  bioink  materials,  thereby enabling the property prediction and expediting the design process.
ML-based property characterization of bioink materials: Rheological properties are paramount in characterizing bioink materials, yet traditional characterization methods relying on rheometers suffer from high cost and limited throughput. These challenges can be addressed through ML-based characterization methods. For instance, Min Zhang ' s group [119] has used characterization data from near-infrared (NIR) spectroscopy  and  low-field  nuclear ...

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
**Best distance**: 0.618
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P120 chunk_21, d=0.618]_

## 3.4. Design of bioink materials

Owing to the tissue- and function-specific nature of the repaired part [113], personalized design for bioink materials is necessary to fulfill specific properties (or CQA) [114 -118]. Typically, this entails significant  domain  expertise  and  extensive  trial  and  error,  which  are  both time-consuming and expensive. However, ML methods offer avenues for improvement in two key aspects: (i) reduction of time and cost associated with property characterization for high-throughput screening of bioink materials, and (ii) modeling the intricate mapping relationship between  the  fingerprints  and  properties  of  bioink  materials,  thereby enabling the property prediction and expediting the design process.
ML-based property characterization of bioink materials: Rheological properties are paramount in characterizing bioink materials, yet traditional characterization methods relying on rheometers suffer from high cost and limited throughput. These challenges can be addressed through ML-based characterization methods. For instance, Min Zhang ' s group [119] has used characterization data from near-infrared (NIR) spectroscopy  and  low-field  nuclear ...

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
