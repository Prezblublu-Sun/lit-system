# Section X.2.1: Extrusion-based bioprinting (EBB)

**Target words**: 200
**Query**: `extrusion-based bioprinting rheology shape fidelity cell viability`
**Generated**: 2026-05-13T14:51:27.711251

---

## Part A: Explicitly cited references in outline (with content)

_No explicitly cited DOIs in outline._

## Part B: Semantic search results (Chroma top N)

### P73: Cell viability in extrusion bioprinting: the impact of process parameters, bioin

**DOI**: 10.1007/s00397-025-01504-z
**Best distance**: 0.577
**Chunks retrieved**: 6

**Retrieved chunks:**

_[P73 chunk_0, d=0.577]_

## Abstract

Extrusion bioprinting is a rapidly developing technology that prints cell-laden materials or 'bioinks' to create complex, three-dimensional tissue constructs. This technology could play a key role in tissue engineering, drug screening, and cancer research. However, cells can be damaged or killed by extrusion forces during printing, limiting throughput and feature resolution. Here, we propose a critical strain-based cell model for predicting cell viability during extrusion that incorporates process parameters, bioink rheology, and cell mechanical properties. We extract parameters from practical nozzle diameters and extrusion flow rates, from power law and Herschel-Bulkley fits to bioink bulk rheology, and from single-cell rheology measurements of cell stiffness and fluidity, and then combine them for the first time to predict viability. This model agrees well with existing cell viability studies and further predicts that cell viability decreases with increasing flow rate, increasing bioink viscosity, increasing nozzle length, or decreasing nozzle radius. Mechanistically, these effects are linked to changes in shear stress or residence time of cells within the nozzle, wh...

_[P73 chunk_3, d=0.596]_

Although a wider range of bioinks is processible in extrusion bioprinting, the bioink rheology constrains the throughput and minimum feature size of the print to prevent cell damage from extrusion forces (Boularaoui et al. 2020). Extrusion bioprinting experiments find broadly that cell viability (reported as the fraction of live cells in a volume) decreases as shear stress increases beyond a threshold value (Ouyang et al. 2016; Yu et al. 2013; Nair et al. 2009). Consequently, changes to the bioink rheology or process parameters that increase the extrusion shear stress are generally observed to reduce cell viability, including increasing bioink viscosity, flow rate, or extrusion pressure, or decreasing nozzle diameter (Blaeser et al. 2016; Chang et al. 2008; Nair et al. 2009; Li et al. 2010; Ouyang et al. 2016). An example experimental data set from Ouyang et al. (2016) is shown in Fig.1, where increasing shear stress by varying the bioink rheology reduced cell viability. These qualitative relationships aid in designing extrusion bioprinting processes to mitigate cell damage. For example, increasing the bioink viscosity may restrict the maximum flow rate or minimum nozzle diameter t...

_[P73 chunk_5, d=0.641]_

Current correlation-based models do not capture the breadth of newly available bioinks and cell types. The cell viability models described previously consider a narrow range of bioinks that are predominantly alginate hydrogel precursor solutions (Table 1). Yield stress fluid bioinks are being developed due to their unique and advantageous biological and mechanical properties (Seymour et al. 2021; Qazi et al. 2022). However, cell viability has not been modeled in these bioinks and experimental data is limited (Aguado et al. 2012). Existing models could be extended to yield stress fluids, but they fail to address differences in cell mechanical properties. Additionally, due to the empirical nature of current cell damage models, extrusion cell viability cannot be quantitatively or qualitatively predicted for cells where extrusion viability data is unavailable. The scope of modeling efforts must expand to match the growing diversity of bioink microstructures and cell types in extrusion bioprinting.
An approach to address these limitations is to develop a cell viability model based on cell deformation that can draw upon an extensive body of work investigating single-cell rheology of vari...

_[P73 chunk_4, d=0.655]_

Identifying the processing limits for an extrusion bioprinting system is challenging due to the difficulty of measuring cell viability. Collecting each data point requires performing cellular assays that are often quantified using image analysis (Stoddart 2011). Therefore, viability is assessed after extrusion, and testing a broad set of conditions is a discrete, time-intensive process. Cell viability is also sensitive to measurement time. Delaying viability measurements allows cells time to recover or potentially proliferate, increasing viability and masking extrusion-based cell damage (Yu et al. 2013). Another complication is that cell viability can be impacted by factors other than extrusion forces. Dehydration, lack of nutrients, and non-optimal temperature or salinity can also damage cells (Freshney 2015). Because of these challenges, many investigations report cell viability for a limited set of processing conditions (Yu et al. 2013; Nair et al. 2009; Blaeser et al. 2016). Additionally, cell viability data is sparse for bioinks other than prevalent hydrogel precursors (Table 1).
Simple models and simulations have helped predict cell damageduringextrusion and expedite the desi...

_[P73 chunk_6, d=0.668]_

An approach to address these limitations is to develop a cell viability model based on cell deformation that can draw upon an extensive body of work investigating single-cell rheology of various cell types. Cells have complex rheological behavior, exhibiting viscoelasticity, viscoplasticity, stiffening, softening, and poroelasticity (Jung et al. 2020) that notably differ across cell types. For example, stem cells are relatively sensitive to applied stresses (Boraas et al. 2016) whereas endothelial cells, which are commonly exposed to shear stresses from blood flow, are more resilient (Chistiakov et al. 2017). The mechanical properties of cells are also dynamic, evolving to facilitate cell functions in different physiological environments (Urbanska and Guck 2024). These rheological behaviors stem from the complex structure of cells which includes actin and intermediate filaments, microtubules, and the cell nucleus, each contributing unique aspects to the cell rheology (see Table 1 in Jung et al. 2020). Despite their complexity, the mechanical behavior of numerous cell types can be broadly described by relatively simple models and measured using techniques such as micropipette aspira...

_[P73 chunk_2, d=0.684]_

For dropletand laser-based bioprinting, bioinks are restricted to mostly hydrogel precursors, where the viscosity should be less than η ∼ 30 mPa · s and η ∼ 300 mPa · s, respectively, to maintain satisfactory printability (Saunders and Derby 2014; Mandrycky et al. 2016). In comparison, extrusion bioprinting accommodates the most diverse range of bioinks such as those with high cell densities (Ozbolat and Hospodiuk2016;Donderwinkeletal.2017),highviscosities, or paste-like rheology characterized by a yield stress. Polymeric hydrogel precursors are commonly used as extrusion bioprinting inks. More recent advances in bioink formulation exploit multiphase microstructures including granular hydrogels (Muir et al. 2021; Qazi et al. 2022), emulsions (Ying et al. 2018), and foams (Condi Mainardi et al. 2022), which are soft material classes used in other extrusion-based additive manufacturing applications (Wei et al. 2023). These bioinks have greater porosity than bulk hydrogels, which promotes faster cell proliferation and spreading (Griffin et al. 2015) while maintaining, and in some cases enhancing, mechanical strength and printability.
Although a wider range of bioinks is processible in...

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

### P37: A review on cell damage, viability, and functionality during 3D bioprinting

**DOI**: 10.1186/s40779-022-00429-5
**Best distance**: 0.627
**Chunks retrieved**: 2

**Retrieved chunks:**

_[P37 chunk_19, d=0.627]_

*Table 1 Summary of typical cell viability studies*


## Cell viability in extrusion-based bioprinting

Similar to inkjet-based bioprinting, extrusion-based bioprinting is also a nozzle-based bioprinting technique and its cell viability is mainly determined by the shear stress and thermal and radiative stresses if photocrosslinkable materials  are  selected.  However,  due  to  its  larger  nozzle size, bioink with a viscosity range from 30 to 6 × 10 8 mPa · s  can  be  extruded  out  of  the  extrusion  nozzle  to form filaments and form the 3D constructs as designed with a layer-by-layer approach [150]. The increase in the bioink concentration and viscosity unavoidably increase the shear stress and kill more cells. Because of the high stresses  imposed  on  the  living  cells  during  the  bio-fabrication  process,  extrusion-based  bioprinting  typically provides a low cell viability ranging from 40 to 80%. However, better printing performance with higher cell viability can also be achieved by optimizing the experimental design  and  operation  conditions  [151].  Extrusion-based bioprinting  has  been  widely  used  in  various  biomedical applications  due  to  its  low  cost,...

_[P37 chunk_21, d=0.669]_

## Cell viability in stereolithography-based bioprinting

As  a  rapidly  developing  technique,  stereolithographybased bioprinting is also a nozzle-free bioprinting technique. Cell viability during stereolithography-based bioprinting  is  mainly  determined  by  the  thermal  and radiative stresses. Benefiting from its nozzle-free mechanism, high cell viability can usually be achieved [23]. It is noted that cell viability can exceed 90% and the printing  resolution  can  reach  10  μm  [132,  153].  Therefore, stereolithography-based  bioprinting  has  been  recently favored  for  the  fabrication  of  artificial  tissues/organs due to its high printing resolution and cell viability. For example,  Wang  et  al.  [21]  selected  stereolithographybased  bioprinting  to  construct  3D  structures  using  the bioink  with  a  mixture  of  polyethylene  glycol  diacrylate (PEGDA), GelMA, eosin Y (EY) and 3T3 fibroblast cells. It was found that a minimum resolution of 50 μm can be achieved and more than 85% cell viability can be maintained for at least 5 d. Later, the same group investigated the effects of GelMA and EY concentrations on the printing performance (e.g., cell viability) w...

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

### P42: Rheology-informed hierarchical machine learning model for the prediction of prin

**DOI**: 10.36922/ijb.1280
**Best distance**: 0.652
**Chunks retrieved**: 2

**Retrieved chunks:**

_[P42 chunk_3, d=0.652]_

Hence, printability prediction is critical to the accurate and  effective  fabrication  of  tissue-engineered  constructs using the extrusion-based bioprinting technique. In several existing  studies,  the  physical  model-based  computation was adopted for printability prediction [33-38] . More precisely, the physical model of printability prediction was derived  from  hydrodynamic  equations  combined  with the rheological modeling of generalized Newtonian fluid, mainly  power-law  fluid.  Using  the  physical  model,  the printing  resolution  of  the  output  filament  was  simulated with multiple printing parameters and compared with the actual printing resolution. Although several studies using the physical model reported interesting results, the model holds  many assumptions and simplifications, limiting its application in various bioprinting tasks. For instance, the physical prediction model is highly sensitive to the power law  index,  which  can  be  obtained  by  the  line  fitting  of the  measured viscosity.  Thus,  small  errors  in  rheological measurement and line fitting may have a significant effect on prediction accuracy. Additionally, the assumptions in the phys...

_[P42 chunk_2, d=0.680]_

However, the advantages of the generous availability of bioink candidates including hydrogels, extracellular matrix, bioceramic particles, and shear thickening materials create difficulties  in  tuning  bioink  compositions  and  finding appropriate  printing  conditions [17,18] .  Thus,  to  overcome these  challenges  and  complexities  in  the  preparation  of bioinks and extrusion-based bioprinting, printability has recently  attracted  considerable  attention.  Although  the definition  of  printability  in  extrusion-based  bioprinting is  still  in  discussion,  it  is  obvious  that  better  printability can  improve  the  printing  accuracy  and  shape  fidelity  of the printed constructs, leading to faster fabrication speed and  long-term  stable  functionality [19-22] .  Further,  recent printability studies have quantitatively evaluated printing accuracy and shape fidelity using the assessment of various outcomes, such as printing resolution relative to the nozzle diameter, distance between filaments, pore size and shape in a grid structure, and height of the stacked layers [23-25] . In addition, these studies have demonstrated that printability is deeply linked to how ...

**Background (from SOP metadata):**
(missing)

**Core problem & critique:**
1) **Most Central Problem and Why It Matters (Page 309-310):**
The central problem addressed in this paper is the difficulty in predicting printability for extrusion-based bioprinting, which involves finding optimal printing conditions given a wide range of bioink candidates. This matters because it directly impacts the efficiency and accuracy of tissue engineering processes, enabling faster fabrication speeds and improved shape fidelity.

2) **Hardest Technical Difficulties (Pages 310-314):**
The hardest technical difficulties include developing a machine learning model that can handle small ...

---

### P74: Machine learning-based prediction and optimisation framework for as-extruded cel

**DOI**: 10.1080/17452759.2024.2400330
**Best distance**: 0.658
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P74 chunk_0, d=0.658]_

## ABSTRACT

Extrusion-based 3D bioprinting has revolutionised tissue engineering, enabling complex biostructure manufacturing. However, extrusion imposes substantial shear stress on cells, compromising  cell  viability.  Predicting  and  optimising  cell  viability  remains  challenging  due  to rheological  modelling  complexity  and  cell-type  dependency.  To  address  these  challenges,  this study developed a quantitative framework integrating numerical simulation and machine learning.  Support  vector  regression  and  simulation  were  utilised  to  evaluate  alginate  ink  viscosity and  shear  stress  profiles,  while  multi-layer  perceptron  regressors  were  trained  on  experimental datasets  for  diverse  cell  types  to  predict  as-extruded  cell  viability  based  on  wall  shear  stress magnitude and exposure time. Results showed vascular endothelial cells were most susceptible to shear  stress,  with  viability  dropping  to  80%  at  2.05  kPa  for  400  ms,  while  mesenchymal  stem, cervical  cancer,  and  embryonic  fibroblast  cells  showed  such  decrease  at  2.65,  2.85,  and  3.72  kPa, respectively. This versatile framework enables rapid bioink optimis...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

**Research Background (Page 2-3):**
"Three-dimensional (3D) bioprinting is a transformative technology in tissue engineering and regenerative medicines that utilises additive manufacturing techniques to produce complex and heterogeneous bios tructures [1, 2]. Bioink, a printable cell-containing biomaterial, is the building material in the printing process [3]. The most commonly available 3D bioprinting methods include extrusion-based, inkjet-based, laser-assisted, and stereolithography-based bioprinting [4]. Compared with other biop...

**Core problem & critique:**
1) **Most Central Problem and Why It Matters:**
The most central problem addressed in this paper is predicting and optimizing cell viability during extrusion-based 3D bioprinting. This matters significantly because the process imposes substantial shear stress on cells, which can compromise their survival and functionality. Accurate prediction of how different bioinks and cell types respond to these stresses enables more precise control over tissue engineering outcomes, potentially leading to better quality printed tissues for medical applications.

2) **Hardest Technical Difficulties:**
The ha...

---

### P123: Machine learning-based prediction and optimisation framework for as-extruded cel

**DOI**: 10.1080/17452759.2024.2400330
**Best distance**: 0.658
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P123 chunk_0, d=0.658]_

## ABSTRACT

Extrusion-based 3D bioprinting has revolutionised tissue engineering, enabling complex biostructure manufacturing. However, extrusion imposes substantial shear stress on cells, compromising  cell  viability.  Predicting  and  optimising  cell  viability  remains  challenging  due  to rheological  modelling  complexity  and  cell-type  dependency.  To  address  these  challenges,  this study developed a quantitative framework integrating numerical simulation and machine learning.  Support  vector  regression  and  simulation  were  utilised  to  evaluate  alginate  ink  viscosity and  shear  stress  profiles,  while  multi-layer  perceptron  regressors  were  trained  on  experimental datasets  for  diverse  cell  types  to  predict  as-extruded  cell  viability  based  on  wall  shear  stress magnitude and exposure time. Results showed vascular endothelial cells were most susceptible to shear  stress,  with  viability  dropping  to  80%  at  2.05  kPa  for  400  ms,  while  mesenchymal  stem, cervical  cancer,  and  embryonic  fibroblast  cells  showed  such  decrease  at  2.65,  2.85,  and  3.72  kPa, respectively. This versatile framework enables rapid bioink optimis...

**Background (from SOP metadata):**
Based on the provided research paper text, here are the extracted sections:

**1. Research Background (Page 2-3)**

"Three-dimensional (3D) bioprinting is a transformative technology in tissue engineering and regenerative medicines that utilises additive manufacturing techniques to produce complex and heterogeneous bios tructures [1, 2]. Bioink, a printable cell-containing biomaterial, is the building material in the printing process [3]. The most commonly available 3D bioprinting methods include extrusion-based, inkjet-based, laser-assisted, and stereolithography-based bioprinting [4]. Compar...

**Core problem & critique:**
1) **Most Central Problem and Why It Matters:**
The most central problem addressed in this paper is predicting and optimizing cell viability during extrusion-based 3D bioprinting, particularly concerning the effects of shear stress on different cell types. This matters because accurate prediction can lead to better bioink formulations that maintain high cell viability, which is crucial for successful tissue engineering applications.

2) **Hardest Technical Difficulties:**
The hardest technical difficulties include accurately modeling the complex rheological properties of bioinks and predicting...

---
