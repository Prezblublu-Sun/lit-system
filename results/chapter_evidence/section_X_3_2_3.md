# Section X.3.2.3: Process window and parameters optimization

**Target words**: 250
**Query**: `bioprinting process window parameter optimization Bayesian Gaussian Process design of experiments`
**Generated**: 2026-05-13T14:51:29.001065

---

## Part A: Explicitly cited references in outline (with content)

### Quick index

- ✅ **P11** — `10.1016/j.apmt.2020.100914` (in library)
- ✅ **P111** — `10.1088/1758-5090/ad17cf` (in library)
- ✅ **P71** — `10.1007/s10845-020-01708-5` (in library)
- ✅ **P64** — `10.1002/advs.202412831` (in library)
- ✅ **P31** — `10.1088/1758-5090/ab8707` (in library)
- ✅ **P74** — `10.1080/17452759.2024.2400330` (in library)

### Detailed content per cited paper

#### 🎯 P11: Coupling machine learning with 3D bioprinting to fast track optimisation of extr

**DOI**: 10.1016/j.apmt.2020.100914

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P11 chunk_14, d=0.702]_

In the experiment, the scoring of a print was manually conducted via a visual assessment by the experimenter. The process involved taking photos, like those shown in Table 3 , and comparing the images against the scale (shown in Fig. 4 ) to decide upon a score. As this is done by sight, much of the scoring is prone to human errors of judgements, and as such may not reflect a consistent objective measure of the print performance. Though the Gaussian Process model can handle errors in measurement (referred to as noise), this can impact the performance of the optimiser and result in more experiments being needed to find the optima. An additional factor contributing to an extension of the number of experiments needed to reach the optima is the experimental batch size. When a batch is recommended by the Bayesian optimiser, the confidence of achieving a good print is ranked down from the first recommendation of a batch (strongest confidence), with the least confident recommendation proposed at the end of the batch. In our experiments we initially started with a batch size of 10. With a large batch size, there is a chance that some experiments in the batch were recommended with far less c...

_[P11 chunk_7, d=0.742]_

Fig. 2 illustrates the framework applied for bioprinting optimisation. The framework began with a set of randomly conducted and scored experiments. These experimental results, made of pairs of printer settings and their associate printing score, were used to initialise the Bayesian optimiser. Within the optimiser, a probabilistic model of the system (as defined in Fig. 3 ) is built and used to recommend the next batch of experiments (printer settings) to be conducted.

*Table 1 Parameter limits at beginning of experimentation.*

The experiments were communicated back to the experimenter who then conducted printer tests with the recommended settings and scored the performance. These results were then fed back into the optimiser and the loop continued until an optimal print was reached. Further details of the framework components are discussed below.

## 2.5.1. The Bayesian Optimiser

The framework begins with the Bayesian Optimiser being provided a randomly conducted set of variable bioink compositions and printer settings and their associated printing score based on the performance of filament formation and layer stacking. Input variables for the bioink compositions consisted of th...

_[P11 chunk_8, d=0.771]_

For this project, experimental recommendations provided by the optimiser were given in a batch to the experimenter in each iteration, to allow the experimenter to conduct and score multiple experiments in one go. Some inputs were constrained in that their values were required to be constant across an experimental batch to allow for ease of experimentation. 3 - 10 experimental recommendations per iteration were deployed and the constrained printer parameters were the temperature of the bioink reservoir and the platform. This method is known as process-constrained batch Bayesian Optimisation and operates by first optimising for the constrained parameters, and then holding them constant across the remaining recommendations in the experimental batch [34] .

## 2.5.2. The search space

Table 1 details the ranges for each of the printer parameters at the start of experimentation including the discretised step size.
Printer settings for each of the six GelMA compositions were sought after, and as such six streams of experimentation were conducted.

*Table 2 Updated parameter discretisation's determined through collaboration between the Bayesian Optimisation algorithm and the experimenter....

_[P11 chunk_13, d=0.797]_

in Eq. (1) . Some examples of varied concentrations of GelMA prints are shown in Table 3 . An overall print score of '0 ′ demonstrates the optimal printing conditions for GelMA and GelMA/HAMA blends (yellow dots in Figs. 5 & 6 ) where a reproducible 3D print is executed from extrusion printing using the EnvisionTEC bioplotter. Table 4 and Figs. 5 & 6 display the experimental results, with the shaded region indicating the range for each of the printing parameters, and the black line segmenting each batch. Out of a space of between 60 0 0 and 10,0 0 0 possible printing settings, the Bayesian Optimisation algorithm was able to discover the optimal printer setting in as few as 19, 4 & 47 experiments for 10%, 7.5% & 5% (w/v) GelMA respectively and 32, 25 & 32 experiments 10%, 7.5% & 5% (w/v) GelMA: 2% (w/v) HAMA in experiments respectively.
Hence, Bayesian Optimisation was able to accelerate the experimentation process, conducting the search for optimal parameters according to conditions specified by the experimenter. Additionally, the algorithm was able to adapt based on insights provided by the researcher during the experimentation process, leading to fast convergence towards optimisa...

_[P11 chunk_0, d=0.813]_

## 1. Introduction

3D bioprinting continues to grow exponentially, gaining significant popularity within the fields of regenerative medicine and disease modelling [1] . The term 3D biofabrication has been used in parallel with the term 3D bioprinting and can be defined as a computer-guided additive manufacturing technique for creating highly precise and complex 3D structures with biologically relevant materials in a pre-designed geometry [ 2 , 3 ]. The cells of interest are either seeded on to the printed constructs or alternatively incor-
✩ This work was conducted using a Bayesian Optimization software developed by A2I2. If you would like to use the software please contact: manisha.senadeera@deakin.edu.au
∗ Corresponding authors.
E-mail addresses:
svetha.venkatesh@deakin.edu.au
gwallace@uow.edu.au (G. Wallace).
# Equally contributed to this study.

## a b s t r a c t

3D bioprinting, a paradigm shift in tissue engineering holds a promising perspective for regenerative medicine and disease modelling. 3D scaffolds are fabricated for subsequent cell seeding or incorporated directly to the bioink to create cell-laden 3D constructs. A plethora of factors relating to bioink properties,...

**Background:**
Certainly, here are the extracted sections from the research paper based on your request:

### 1. Research Background

**Page 2:**
"3D bioprinting continues to grow exponentially, gaining significant popularity within the fields of regenerative medicine and disease modelling [1]. The term 3D biofabrication has been used in parallel with the term 3D bioprinting and can be defined as a computer-guided additive manufacturing technique for creating highly precise and complex 3D structures with biologically relevant materials in a pre-designed geometry [2, 3]."

**Page 2:**
"Bioinks are a fundament...

**Core problem:**
1. **Most Central Problem and Why It Matters (Page 1-2)**

The central problem addressed in this paper is the optimization of printability for extrusion-based bioprinting, specifically focusing on GelMA and GelMA/HAMA bioinks. This matters because achieving optimal printing conditions can significantly enhance the reproducibility and quality of 3D printed constructs, which are crucial for applications in regenerative medicine and disease modeling.

2. **Hardest Technical Difficulties (Page 4-5)**

The hardest technical difficulties include fine-tuning numerous variables such as bioink composit...

---

#### 🎯 P111: Cell viability prediction and optimization in extrusion-based bioprinting via ne

**DOI**: 10.1088/1758-5090/ad17cf

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P111 chunk_24, d=0.670]_

This study utilized a neural network-based Bayesian optimization model to optimize the bioprinting process to obtain the highest possible cell viability. Bayesian optimization is a powerful ML optimization tool that is applied to discover the optimal set of variables for a given objective function [24]. The Bayesian optimization model in this study allows us to quantify the uncertainty in cell viability prediction as well as predict the optimal bioprinting experimental features for maximizing cell viability. This method in extrusion-based bioprinting was used in the study by Ruberu et al [1] for the first time to optimize the printability of the bioink. The researchers utilized Bayesian optimization as a novel method for optimizing some of the printing variables while minimizing the necessary experiments. The study demonstrated the promising outcome of this method in speeding up the extrusion-based bioprinting process compared to conventional optimization.
Our current work aims to eliminate laborious trial-and-error steps in optimizing cell viability in extrusion-based bioprinting by integrating our built neural network with the Bayesian optimization technique. Inspired by the pion...

_[P111 chunk_25, d=0.681]_

To execute Bayesian optimization, we first defined the range space for 'Crosslinking (CaCl2)_Concentration' and 'Physical_crosslinking_ time' by determining the minimum and maximum values. We set the minimum value to be greater than zero because we intended to evaluate optical crosslinking parameters rather than zero for our particular bioprinting parameters. In addition, we defined the range's maximal value as the highest value observed in our dataset. The Bayesian optimization procedure relied on the neural network we developed for regression. During each iteration of the optimizer, the suggested 'Crosslinking (CaCl2)_Concentration' and 'Physical_crosslinking_time' with other predefined and desired variables were fed into the trained neural network to predict cell viability with good accuracy. This approach enabled us to rapidly investigate numerous unexplored parameter possibilities, ultimately identifying the most efficient parameter combination in printing. The Gaussian process in this process model the underlying patterns and correlations in the data, providing a probabilistic estimate of the behavior of cell viability for a set of printing parameters, and discovers the best ...

_[P111 chunk_12, d=0.690]_

The algorithm of this neural network-based Bayesian optimization model is depicted in figure 1. Here, the base Bayesian optimization framework started by constructing the Gaussian Process model using the created dataset of variables in the bioprinting process and their associated cell viability. The Gaussian Process model consists of mean and covariance functions. The Matern kernel, with a smoothness parameter equal to 2.5, is the covariance function in this study, which conveys the smoothness of the function and determines how the cell viability percentage in one spot affects the prediction of the nearby values [26]. Moreover, in the training of the Gaussian Process model, a small positive number, α = 10 -3 , was added to each element on the diagonal of the covariance matrix to modify the numerical stability of this method.
Using the Gaussian Process model's mean and covariance, we developed an acquisition function that suggests the next questioned bioprinting variables to probe. The suggested parameters were chosen to maximize the probability of achieving the highest cell viability while maintaining a balance between exploration and exploitation. In this study, the GP-UCB acquisi...

_[P111 chunk_27, d=0.725]_

By calculating permutation importance for the neural network for regression, we identified the bioprinting parameters significantly impacting cell viability prediction. Among different parameters, 'cell type' emerges as the most critical variable, highlighting the different sensitivities of various cell types to the bioprinting procedure. In addition, 'extrusion pressure' is identified as the second most significant parameter, demonstrating the detrimental impact of excessive pressure on cell viability due to mechanical stress and shear forces on the cell membrane. After the bioprinting procedure, the 'crosslinker (CaCl2) concentration' and 'physical crosslinking time' are identified as the third and fifth significant features, respectively, which balance the structural integrity and cell viability of bioprinted structures. Therefore, we can conclude that tuning these effective parameters can highly impact the survival of cells during the bioprinting procedure.
We finally developed a novel Bayesian optimization model based on the created trained neural network to inversely predict optimal bioprinting crosslinking parameters, achieving the highest cell viability without any trial-an...

_[P111 chunk_26, d=0.734]_

*Table 9. Predicted optimal crosslinking parameters and cell viability using neural network-based Bayesian optimization model and the actual cell viability of Experiment 1 and Experiment 2.*

The findings demonstrate that this approach can successfully improve the bioprinting process by determining the optimum crosslinking condition. There is a good agreement between the actual and predicted cell viabilities for both experiments, showing the promising application of this optimization method for bioprinting. Using this neural networkbased Bayesian optimization model, researchers can determine optimal crosslinking conditions for any set of parameters for alginate-based bioink and optimize the bioprinting without any trial-anderror experiments. Additionally, this optimization method can be extended to predict other bioprinting parameters, such as concentration of materials, printing setting parameters, or combinations of all of them, to optimize cell survival in future studies.
Although there is an agreement between the predicted and actual viabilities, there are still differences. This discrepancy can be attributed to the performance of the neural network. Indeed, our Bayesian optimi...

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

_[P71 chunk_2, d=0.925]_

To better understand post-printing cell viability, physicsbased models have been introduced to study how cells are damaged during bioprinting. Wang et al . (Wang et al. 2008) investigated the mechanical loading profile of cells using a mesh-free smooth particle hydrodynamic method, which was useful for understanding and predicting possible impactinduced cell damage. The cells were modeled as linear elastic solids, and the cell damage was determined by the cell membrane rupture due to the shear stresses imposed on the cells. The major conclusions were listed as below: 1) with the induced stresses, the cell membrane had severe deformation and was even damaged; and 2) to better quantify the cell damage, the stresses imposed on the cells from every source should be comprehensively incorporated such as those generated from the ejection process and the travel through air. Wang et al. (2009) used a finite element method (FEM) to investigate the mechanical loading profile of cells induced by the bubble expansion during laser-assisted bioprinting process. A neo-Hookean model was used to represent the living cells. It was found that both the process-induced cell stresses and the duration of ...

_[P71 chunk_4, d=0.948]_

To address the limitations of the existing physics-based models, a predictive modeling approach based on machine learning is developed to predict cell viability during 3D bioprinting processes for the first time in this paper. Compared to physics-based modeling methods, data-driven predictive modeling approaches have two unique advantages: (1) the complex relationship among multiple bioprinting parameters, such as UV intensity, UV exposure time, GelMA concentration, and layer thickness, can be revealed; and (2) real-time monitoring and accurate prediction of cell viability under varying printing conditions can be achieved. The organization of the remaining of this paper is as follows: "Materials and methods"section specifies the preparation of bioink, analysis of cell viability, setup of experiments, and design of experiments; "Data-driven predictive modeling"section describes the machine learning algorithms; "Results and discussions"section compares the prediction accuracies of different algorithms with the experimental results; and "Conclusions"section summarizes the major conclusions.

## Materials and methods


## Bioink preparation

In this study, GelMA which is an adaptable a...

_[P71 chunk_9, d=0.948]_

*Table 1 Experimental design*


## Data-driven predictive modeling

Machine learning was used to train data-driven predictive models of cell viability. Several studies have investigated the use of machine learning in 3D bioprinting for optimizing printing processes or predicting material properties. For
2 mm
5 mm
(q)
example, Wu and Xu (Wu and Xu 2018) developed a predictive model to predict droplet volume and velocity using ensemble learning methods based on the process parameters in inkjet-based bioprinting. The effects of dwell time, rise time, excitation voltage, and polymer concentration on droplet volume and velocity were investigated. It is demonstrated that the ensemble learning model is able to predict droplet volume and velocity precisely. Shi et al . (Shi et al. 2019) proposed a multi-objective optimization method for drop-on demand (DOD) bioprinting using neural network (NN). Both droplet diameter and speed were optimized to improve the formation of droplets. The experiments showed that NN is capable of optimizing the process parameters in DOD bioprinting to improve the printing fidelity. However, to the best of our knowledge, little research has been reported on the pr...

_[P71 chunk_1, d=0.963]_

Lauren S. Gollahon lauren.gollahon@ttu.edu pre-formed hydrogel-based acellular scaffold to develop the extracellular matrix (ECM) (Pourchet et al. 2017). Native tissue-like constructs, such as cartilage, have been successfully fabricated with the scaffold-based approach (Kundu et al. 2015). One disadvantage of scaffold-based bioprinting is that the assembly of ECM may have negative effects on cell performance (Norotte et al. 2009). However, during scaffold-free bioprinting, cells are deposited directly to fabricate tissue-like constructs such as nerve tissues (Owens et al. 2013). The scaffold-free approach has drawn more attention due to its better biomimicry.
Depending on the printing mechanisms, 3D bioprinting techniques fall into four categories, including inkjet-based, microextrusion-based, laser-assisted, and stereolithographybased bioprinting (Lee and Yeong 2016). Inkjet-based bioprinting can achieve high printing resolution and precise control of droplet deposition positions on the substrate, but its limitations include nozzle clogging and low cell and polymer concentrations (Xu et al. 2019). Microextrusion-based bioprinting enables high cell and polymer concentrations, but ...

_[P71 chunk_3, d=0.967]_

Apoptosis and necrosis have been recognized as two major types of cell deaths (Matteucci et al. 1999). The apoptosis commonly appearing in the cell growths is either genet- ically controlled or stimuli-induced (Nagata 1997) while the necrosis is caused by the harmful events and pathological conditions (Matteucci et al. 1999). The apoptosis of the cells which is seen as the leading factor of cell injuries during bioprinting (Cotter and Al-Rubeai 1995) can be reflected by several specific features such as membrane blebbing, internucleosomal fragmentation of DNA, chromatincondensation,andcytoplasmiccondensation(Scoltock and Cidlowski 2004; Darzynkiewicz et al. 1997). In the stereolithography-based bioprinting, the major cell damage results from the UV irradiation. The UV light induces the clustering and internalization of the death receptors on the cell membrane (Rosette and Karin 1996) and damages DNAthroughtheformation of cyclobutene pyrimidine dimer (CPD)(Masumaetal.2013).TheUVirradiation-inducedcell apoptosis is caused by the activation of c-JunNH2-terminal kinase/stress-activated protein kinase (JNK/SAPK) (Lu et al. 2003). During this process, there are many different and complex...

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

#### 🎯 P64: Machine Learning-Enhanced Optimization for High-Throughput Precision in Cellular

**DOI**: 10.1002/advs.202412831

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P64 chunk_23, d=0.867]_

Among bioprinting parameters, bioink composition plays a critical role in extrusion-based bioprinting. [44] Low concentrations of hydrogel bioink often result in inadequate mechanical stability and printability, complicating the creation of constructs with microliter-sized droplet volumes. Based on the mechanical characterization, 5G0.5A and 5G1A were identified as the most suitable candidates for droplet bioprinting and were subsequently selected for further optimization.
Samples with a high concentration of methacryloyl groups demonstrated rapid initiation of the photocrosslinking reaction, as evidenced by the immediate increase in storage modulus. This behavior is characteristic of highly functionalized GelMA, where the abundance of crosslinkable groups facilitates rapid network formation. [45] Increasing alginate concentration correlated with a slight decrease in the final storage modulus. This phenomenon can be attributed to the interference of alginate with the GelMA photocrosslinking process. Alginate molecules may physically impede the interaction between methacryloyl groups, resulting www.advancedsciencenews.com in a less densely crosslinked network and, consequently, lowe...

_[P64 chunk_24, d=0.881]_

The diverse droplet volumes produced by adjusting bioprinting parameters were input into three traditional ML algorithms and two DL algorithms for training and testing. Before this, hyperparameter optimization was performed for each algorithm to identify the configuration that yielded the best predictive performance. By employing hyperparameter optimization, each algorithm was tuned to ensure the highest predictive accuracy for droplet volume outcomes. In addition, this process enhanced the model's generalization performance, reducing the risk of overfitting. This rigorous approach allowed us to systematically evaluate and improve the performance of our bioprinting process. The combination of multiple algorithms provided a comprehensive understanding of the parameters influencing cell-laden droplet formation, facilitating the development of robust predictive models. These models are crucial for real-time optimization of bioprinting parameters, thereby improving the consistency and quality of bioprinted constructs.
MLoffers a faster and more accurate approach to maintaining consistency in bioprinting compared to traditional methods. To ensure the long-term stability and consistency ...

_[P64 chunk_13, d=0.885]_

To evaluate the performance of the algorithms in predicting printing parameters, our study was structured into two distinct phases: Phase 1, focuses on hyperparameter optimization, and Phase 2, compares the optimized algorithms. In Phase 1, key parameters for each algorithm, such as learning rate, batch size, and tree depth, were systematically tuned to achieve optimal performance. Phase 2 involved assessing the optimized models using metrics like mean absolute error (MAE), root mean square error (RMSE), R-squared, and computation time to provide a comprehensive comparison of their accuracy and efficiency in predicting printing parameters. This section primarily focuses on Phase 1, which addresses hyperparameter optimization.
An optimization process was conducted to determine the optimal hyperparameters for each algorithm. This process involved 10-fold cross-validation to identify the hyperparameters that yielded the best performance. K-fold cross-validation mitigates bias and variance associated with a single data split, resulting in a more robust evaluation of model performance. [38] Additionally, it aids in detecting overfitting issues and facilitates the discovery of a generali...

_[P64 chunk_2, d=0.894]_

In this study, we developed a novel bioprinter designed to address the challenges of high-throughput and precise 3D cellular droplet bioprinting. The system is equipped with a largescale data collection capability tailored for traditional ML and deep learning (DL) applications, enabling efficient optimization of bioprinting parameters. With precise control over micro-scale droplet volumes and compatibility with various bioinks, the bioprinter supports the production of cellular droplets at highthroughput. This versatile technology has the potential to be applied to a wide range of existing bioprinting systems.
The combination of ML with advanced bioprinting technology can potentially accelerate research in tissue engineering and precision medicine. [23] ML refers to computer programs that based on big data, autonomously learn to predict the future or make decisions. [ 24] It is an artificial intelligence (AI) paradigm that goes beyond simple data training, continuously collecting and learning to enhance accuracy. Wu and Xu utilized ensemble learning to predict the velocity and volume of droplets generated dur- www.advancedscience.com ing the inkjet-based bioprinting process. [ 25] ...

_[P64 chunk_1, d=0.900]_

et al. utilized inkjet bioprinting to create droplet-shaped structures with a gelatin methacrylate (GelMA) hydrogel precursor combined with cells, analyzing cell responses to an elastic composite substrate that was periodically stretched. [ 13]
The common challenges frequently encountered in these studies include the intricate process of achieving consistent
R. Kang, K. Kim Department of Electrical and Software Engineering Schulich School of Engineering University of Calgary Calgary, Alberta T2N 1N4, Canada
K. Hyun, S. S. Park, K. Kim Department of Mechanical and Manufacturing Engineering Schulich School of Engineering University of Calgary Calgary, Alberta T2N 1N4, Canada
H. Kumar
Department of Biosciences and Biomedical Engineering Indian Institute of Technology Indore Indore, Madhya Pradesh 453552, India www.advancedsciencenews.com microscale droplets of uniform size. Additionally, optimizing numerous bioprinting parameters, such as temperature, bioink properties, printing time, printing speed, nozzle size, and dispensing pressure, adds to the complexity of the process. [14] The quality of bioprinted outcomes is significantly influenced by these parameters, as even minor changes...

**Background:**
Based on the provided text, here is the extracted information:

**Research Background:**
The research background highlights the challenges in traditional manual pipetting methods for organoid production, which are labor-intensive and result in batch-to-batch variability. Bioprinting offers a more efficient alternative but optimizing multiple printing parameters to achieve desired organoids remains time-consuming and costly. Machine learning is employed to optimize critical bioprinting parameters such as bioink viscosity, nozzle size, printing time, pressure, and cell concentration (Page 1).

*...

**Core problem:**
1. **Most Central Problem and Why It Matters**
   - The most central problem addressed in this paper is optimizing bioprinting parameters to achieve consistent droplet volumes, which is crucial for high-throughput precision cellular bioprinting (Page 2). This matters because traditional manual methods are labor-intensive and yield inconsistent results, leading to variability in organoid quality. Achieving precise control over droplet size ensures better cell viability, functionality, and degree of maturity, making it essential for scalable production of organoids for various applications such ...

---

#### 🎯 P31: Machine learning-based design strategy for 3D printable bioink: elastic modulus 

**DOI**: 10.1088/1758-5090/ab8707

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P31 chunk_4, d=0.875]_

Tissue engineering is a multidisciplinary study that is labor intensive and expensive, making predictive approaches necessary for successful future development. 3D bioprinting is a promising technology for predictive tissue engineering because it allows for standard manufacturing. To implement predictive tissue engineering based on 3D bioprinting, it is necessary to study mathematical models that can predict the properties of bioinks for efficient bioink development. Further, it is important to find and control the physical properties of materials that can be used to develop bioinks because these materials should be able to control printability and shape fidelity. Until now, there have been few well-established studies on the development of bioinks based on the empirical knowledge in the development of bioinks [29-33]. Investigating the universal factors to determine printability is challenging owing to significant ink-to-ink variability and the complex nonlinear relationship between ink composition and mechanical properties in hydrogels containing two or more ECM components. Further, it is nearly impossible to perform experiments one by one for an infinite number of cases with var...

_[P31 chunk_1, d=0.888]_

Three-dimensional (3D) printing technology has emerged as a promising tool to fabricate tissue and organ analogues to meet the needs of patients on organ donor waiting lists and to develop in vitro models for the preclinical testing of new drugs [1-4]. Owing to its potential to control the spatial arrangement of cells, 3D printing offers multiple degrees of freedom to imitate natural tissue systems. 3D printing also provides a platform to develop heterogeneous constructs composed of various cells and bioinks. Printing processes that satisfy these requirements that generally include inkjet, microextrusion, and laserassisted bioprinting. Microextrusion processes have recently become the most commonly used printing technologies, as they provide a platform to print natural constructs and cells under physiological conditions with highly viscous biomaterials [3, 5].
In microextrusion printing, desired constructs can be designed by dispensing biomaterials through nozzles or needles connected to cartridges loaded with ink. Multiple cartridges can be loaded in the printer to print heterogeneous structures. Printing parameters such as speed, dispensing pressure, and movement distance need to...

_[P31 chunk_24, d=0.892]_

In the absence of systematic studies on bioink development based on empirical knowledge in the development of bioinks, investigators currently invest considerable effort and cost in determining the criteria of bioinks through empirical experimentation, and they apply their findings to tissue engineering. We found a universal relationship between rheological properties of ink and printability; a high elastic modulus improves shape fidelity, and extrusion is possible below the critical yield stress, as supported by machine learning results. Based on this relationship, we derived various formulations of naturally derived bioinks that provide high shape fidelity using multiple regression analysis. This is the first study to introduce machine learning and mathematical models for the design and prediction of bioinks, although this predictive model does not directly support predictive tissue engineering research at the present level.
Further research is needed to predict the role of materials in terms of the biodegradability of bioinks and in biological functions, such as cell proliferation and differentiation. Furthermore, if the effectiveness of the bioinks in tissue regeneration is ver...

_[P31 chunk_23, d=0.940]_

The first method keeps the nozzle temperature at 4 ◦ Cto extrude the liquid ink and then maintains the substrate at 37 ◦ C to cause thermo-gelation immediately after printing to obtain the required shape fidelity. In this case, important properties determining printing quality are high viscosity to maintain the filament when the ink at 4 ◦ C is discharged, and fast gelation immediately after printing. Because both properties require chemical additives for control, this approach is not ideal to obtain 3D printable bioinks.
The second method is to pass the ink through the printing nozzle in the gel state. This is advantageous for forming filaments owing to the high viscosity of the gel, and the shape can be maintained because of its elasticity. However, the flowability of bioink during processing can decrease when mechanical properties such as yield stress and elasticity are too high. In this study, we adopted the second method to obtain a suitable printing ink by determining and controlling the appropriate range of elasticity and flowability of the bioink.
This work demonstrates a comprehensive approach to acquire printable bioinks with high shape fidelity for 3D printing, beginning...

_[P31 chunk_22, d=0.953]_

Although bioprinting technology is advancing rapidly, developing suitable bioprinting materials that meet both the demands of mechanical properties and biocompatibility remains a challenge. It is easy to control the mechanical strength of bioinks using synthetic polymers to meet the requirements of high shape fidelity; however, their clinical use has been limited because of the lack of biocompatibility. Even the use of biodegradable polymers such as polycaprolactone and poly (lactic acid) does not guarantee clinical use. On the other hand, hydrogels made from natural biomaterials provide an optimal environment for cell survival and have a higher potential for clinical use; however, their applications have been limited owing to their poor physical properties. Some recent studies have focused on the development of strategies to improve the mechanical strength of nature-derived hydrogels by replacing the molecular structure or using chemical additives. However, the use of chemically substituted proteins to impose high mechanical strength causes toxicity in vivo , rendering this strategy difficult to implement in practical applications. Therefore, an appropriate design of naturally der...

**Background:**
Certainly, here are the extracted sections from the provided research paper text:

### 1. Research Background

**Page 1-2:**
"Three-dimensional (3D) printing technology has emerged as a promising tool to fabricate tissue and organ analogues to meet the needs of patients on organ donor waiting lists and to develop in vitro models for the preclinical testing of new drugs [1–4]. Owing to its potential to control the spatial arrangement of cells, 3D printing offers multiple degrees of freedom to imitate natural tissue systems. 3D printing also provides a platform to develop heterogeneous construct...

**Core problem:**
1. **Most Central Problem and Why It Matters:**
   The most central problem addressed in this paper is developing a machine learning-based method to design 3D-printable bioinks with optimal rheological properties for high shape fidelity and printability. This matters because the ability to create biocompatible, printable bioinks that maintain their structure during printing and support cell viability post-printing is crucial for advancing tissue engineering applications. Current limitations in bioink development hinder the practical implementation of 3D bioprinting technologies in clinical set...

---

#### 🎯 P74: Machine learning-based prediction and optimisation framework for as-extruded cel

**DOI**: 10.1080/17452759.2024.2400330

**Top 3 chunks from this paper (ranked by relevance to section query):**

_[P74 chunk_2, d=0.931]_

Most  bioinks  employed  in  extrusion-based  3D  bioprinting are non-Newtonian fluids and exhibit shear-thinning  properties,  where  the  apparent  viscosity  of  the bioink  decreases  as  the  applied  shear  rate  increases [11,12].  Alginate-based  bioinks  are  especially  prevalent in  extrusion-based  3D  bioprinting  due  to  their  pronounced shear-thinning properties, high biocompatibility,  and  resemblance  to  the  extracellular  matrix  (ECM) [13,14].  The  shear-thinning  property  is  beneficial  as  it can minimise the chances of clogging and enhance cell viability  during  the  extrusion  process  [15,16].  However, the magnitude of shear stress can still be significant for higher extrusion rates and polymer concentrations, leading to a substantial reduction in cell viability [17,18].
Shear  stress  is  the  primary  cause  of  cell  damage during the extrusion-based 3D bioprinting process [19-21].  Previous  studies  indicate  that  exposure  to  a high magnitude of shear stress, even in the short term, can  negatively  impact  cell  viability  [22,23];  however, further  research  is  needed  to  elucidate  and  quantify the relationship between applied shear ...

_[P74 chunk_3, d=0.935]_

The experimental study of cell viability  in  extrusionbased  3D  bioprinting  has  mainly  focused  on  limited cell lines and lacks generalizability. Ouyang et al. investigated  the  cell  viability  of  embryonic  stem  cells  under varying  ink  concentrations,  printing  temperatures,  and holding  time,  highlighting  the  detrimental  effect  of wall shear stress on cell viability, though exposure time to  such  shear  stress  was  not  studied  [32].  Meanwhile, computational fluid dynamics (CFD) simulation provides a  straightforward  way  to  characterise  the  shear  stress profile inside the printhead. Previous studies examined the shear stress  distribution for  various  needle  geometries and dimensions, such as cylindrical needles, tapered  nozzles,  and  customised  printheads  [17,33,34]. However,  these  studies  often  rely  on  cell  viability  data from  other  literature  sources,  limiting  their  ability  to directly  correlate  shear  stress  and  exposure  time  with experimental cell viability outcomes; in this study, multiple cell lines from diverse tissue origins and functionalities were directly compared at the same time, ensuring consistency  and  acc...

_[P74 chunk_0, d=0.949]_

## ABSTRACT

Extrusion-based 3D bioprinting has revolutionised tissue engineering, enabling complex biostructure manufacturing. However, extrusion imposes substantial shear stress on cells, compromising  cell  viability.  Predicting  and  optimising  cell  viability  remains  challenging  due  to rheological  modelling  complexity  and  cell-type  dependency.  To  address  these  challenges,  this study developed a quantitative framework integrating numerical simulation and machine learning.  Support  vector  regression  and  simulation  were  utilised  to  evaluate  alginate  ink  viscosity and  shear  stress  profiles,  while  multi-layer  perceptron  regressors  were  trained  on  experimental datasets  for  diverse  cell  types  to  predict  as-extruded  cell  viability  based  on  wall  shear  stress magnitude and exposure time. Results showed vascular endothelial cells were most susceptible to shear  stress,  with  viability  dropping  to  80%  at  2.05  kPa  for  400  ms,  while  mesenchymal  stem, cervical  cancer,  and  embryonic  fibroblast  cells  showed  such  decrease  at  2.65,  2.85,  and  3.72  kPa, respectively. This versatile framework enables rapid bioink optimis...

_[P74 chunk_38, d=0.961]_

In  summary,  this  study's  numerical  simulations  and machine-learning  models  offer  a  robust  framework  for predicting  and  optimising  cell  viability  based  on  wall shear stress and exposure time. By integrating experimental  data,  numerical  simulations,  and  machine  learning models, a comprehensive approach to enhancing the bioprinting  process  is  established.  This  framework  can  be readily adapted to other bioinks and cell types, facilitating the development of more effective bioprinting protocols. Although the current study provides insights on cell-typespecific  response to shear stress, it focuses primarily on immediate  as-extruded  cell  viability.  Future  research should  explore  the  long-term  effects  of  shear  stress  on cell proliferation and function, as cells experiencing high shear stress may undergo delayed apoptosis [62]. Moreover,  the  framework  does  not  currently  account  for scaffold design parameters such as pore size and porosity. These factors play a crucial role in cell proliferation and overall tissue engineering outcomes, as demonstrated in works  by  Cheah  et  al.  [63,64]  and  Naing  et  al.  [65]. Future iterations of th...

_[P74 chunk_1, d=0.971]_

CONTACT Shinji Sakai sakai@cheng.es.osaka-u.ac.jp Division of Chemical Engineering, Department of Materials Engineering Science, Graduate School of  Engineering Science, Osaka University, 1-3 Machikaneyama-cho, Toyonaka, Osaka, 560-8531, Japan
© 2024 The Author(s). Published by Informa UK Limited, trading as Taylor & Francis Group
This  is  an  Open  Access  article  distributed  under  the  terms  of  the  Creative  Commons  Attribution-NonCommercial  License  (http://creativecommons.org/licenses/by-nc/4.0/),  which permits unrestricted non-commercial use, distribution, and reproduction in any medium, provided the original work is properly cited. The terms on which this article has been published allow the posting of the Accepted Manuscript in a repository by the author(s) or with their consent.

## ARTICLE HISTORY

Received 12 June 2024 Accepted 29 August 2024

## KEYWORDS

3D bioprinting; cell viability; shear stress; numerical analysis; machine learning; alginate-based bioink process [3].  The  most  commonly available 3D bioprinting methods include extrusion-based, inkjet-based, laser-assisted,  and  stereolithography-based  bioprinting [4].  Compared  with  other  bioprinting...

**Background:**
Based on the provided text, here are the extracted sections:

**Research Background (Page 2-3):**
"Three-dimensional (3D) bioprinting is a transformative technology in tissue engineering and regenerative medicines that utilises additive manufacturing techniques to produce complex and heterogeneous bios tructures [1, 2]. Bioink, a printable cell-containing biomaterial, is the building material in the printing process [3]. The most commonly available 3D bioprinting methods include extrusion-based, inkjet-based, laser-assisted, and stereolithography-based bioprinting [4]. Compared with other biop...

**Core problem:**
1) **Most Central Problem and Why It Matters:**
The most central problem addressed in this paper is predicting and optimizing cell viability during extrusion-based 3D bioprinting. This matters significantly because the process imposes substantial shear stress on cells, which can compromise their survival and functionality. Accurate prediction of how different bioinks and cell types respond to these stresses enables more precise control over tissue engineering outcomes, potentially leading to better quality printed tissues for medical applications.

2) **Hardest Technical Difficulties:**
The ha...

---

## Part B: Semantic search results (Chroma top N)

### P88: Advancing 3D bioprinting through machine learning and artificial intelligence

**DOI**: 10.1016/j.bprint.2024.e00331
**Best distance**: 0.622
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P88 chunk_15, d=0.622]_

In  the  future,  combining  the  strengths  of  generative  adversarial networks (GANs) [164 -167], variational autoencoders (VAEs) [168 -170],  and  conditional  variational  autoencoders  (CVAEs)  [171, 172],  along  with  optimization  algorithms  [173 -175],  can  augment design for 3D bioprinting. For example, GANs have been employed in medical imaging to generate realistic textures and patterns [176 -178]. Integrating these technologies into bioprinting can involve generating realistic 3D models from medical imaging data, converting them into STL, AMF, 3MF, or other appropriate file types, and further tuning the design using optimization algorithms.

## 5.4. Selection and optimization of bioprinting parameters

Successful bioprinting relies on the geometric accuracy of material deposition (i.e., strand diameter, strand spacing, strand buckling, etc.) and  the  preservation  of  cell  viability,  both  influenced  by  numerous machine parameters [179,180]. This stage aims to identify the ' biofabrication  window ' for  repeatable  production  of  high-fidelity  structures with cell-containing bioinks [181]. Conventional approaches to identifying optimal design parameters invo...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

**Research Background:**
"3D bioprinting, a branch of additive manufacturing (AM), creates three-dimensional biological structures by layering biomaterials and living cells [1 – 3]. Bioprinting has advanced bioengineering, offering avenues to improve transplantation methods by creating personalized tissues and organs [4, 5], facilitating advanced drug testing [6, 7], developing in vitro models for disease research and therapeutic screening [8–10], and producing meat alternatives. Yet, the objective of mass-producing customized biopr...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters (Page 2-5):**
   The central problem addressed in this paper is the integration of machine learning (ML) and artificial intelligence (AI) into 3D bioprinting to address both process-specific challenges and system-wide issues. This matters because it aims to enhance the scalability, automation, and overall efficiency of bioprinting technologies, which are crucial for advancing applications in tissue engineering, drug testing, disease modeling, and personalized medicine.

2. **Hardest Technical Difficulties (Pages 5-10):**
   The hardest technical dif...

---

### P119: Advancing 3D bioprinting through machine learning and artificial intelligence

**DOI**: 10.1016/j.bprint.2024.e00331
**Best distance**: 0.622
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P119 chunk_15, d=0.622]_

In  the  future,  combining  the  strengths  of  generative  adversarial networks (GANs) [164 -167], variational autoencoders (VAEs) [168 -170],  and  conditional  variational  autoencoders  (CVAEs)  [171, 172],  along  with  optimization  algorithms  [173 -175],  can  augment design for 3D bioprinting. For example, GANs have been employed in medical imaging to generate realistic textures and patterns [176 -178]. Integrating these technologies into bioprinting can involve generating realistic 3D models from medical imaging data, converting them into STL, AMF, 3MF, or other appropriate file types, and further tuning the design using optimization algorithms.

## 5.4. Selection and optimization of bioprinting parameters

Successful bioprinting relies on the geometric accuracy of material deposition (i.e., strand diameter, strand spacing, strand buckling, etc.) and  the  preservation  of  cell  viability,  both  influenced  by  numerous machine parameters [179,180]. This stage aims to identify the ' biofabrication  window ' for  repeatable  production  of  high-fidelity  structures with cell-containing bioinks [181]. Conventional approaches to identifying optimal design parameters invo...

**Background (from SOP metadata):**
Based on the provided text, here are the extracted sections:

**Research Background:**
The research background is encapsulated in the introduction and overview of bioprinting technologies. It highlights that 3D bioprinting, a branch of additive manufacturing (AM), creates three-dimensional biological structures by layering biomaterials and living cells [1-3]. Bioprinting has advanced bioengineering, offering avenues to improve transplantation methods by creating personalized tissues and organs [4,5], facilitating advanced drug testing [6,7], developing in vitro models for disease research and ...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters (Page 2-5):**
   The central problem addressed in this paper is the integration of machine learning (ML) and artificial intelligence (AI) into 3D bioprinting to enhance process efficiency, material selection, parameter optimization, real-time monitoring, and system-wide challenges. This matters because it aims to overcome current limitations in scalability, automation, and data management that hinder the widespread adoption of 3D bioprinting technologies for tissue engineering, drug testing, disease modeling, and other applications.

2. **Hardest Te...

---

### P1: The Role of Artificial Intelligence in Advancing Biofabrication Technology

**DOI**: _missing_
**Best distance**: 0.668
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P1 chunk_20, d=0.668]_

Bioprinting plays a significant role in biofabrication by enabling the precise deposition of biomaterials such as cells, growth factors, and bioinks to create complex 3D structures. The bioprinting process parameters must be combined with the selected printing technology and bioink performance. The ideal process parameters can achieve precise shaping fidelity, minimize cell damage during manufacturing, and enable the model to achieve its expected function. Parameter optimization throughout the biofabrication process is a complex and multidimensional research endeavor. Currently, researchers aim to utilize the learning capabilities of AI models to optimize and predict the parameter settings and corresponding printing outcomes for three common printing technologies: extrusion-, inkjet, and photopolymerization-based 3D bioprinting.

## 3.2.1. Extrusion-based 3D bioprinting

Extrusion-based 3D bioprinting is commonly used to fabricate cell-containing tissue models. The printing parameters that need to be considered and optimized in extrusion-based bioprinting include bioink reservoir temperature, printing pressure, printing speed, extrusion speed, nozzle geometry, nozzle diameter, plat...

**Background (from SOP metadata):**
The research paper titled "AI for Biofabrication" explores how artificial intelligence (AI) can enhance biofabrication, a technology aimed at constructing highly biomimetic three-dimensional human organs in vitro. The primary challenge addressed is the complexity involved in replicating organ structures and functions due to intricate biological data processing requirements.

Relevant concepts include machine learning (ML), deep learning (DL), and various AI models such as convolutional neural networks (CNNs) and generative adversarial networks (GANs). These technologies are crucial for handlin...

**Core problem & critique:**
The research paper "AI for Biofabrication" addresses a significant challenge in bioengineering: the creation of complex, functional tissues and organs through advanced manufacturing techniques. The central problem it tackles is how to integrate artificial intelligence (AI) into the intricate processes of biofabrication to enhance efficiency, precision, and automation. This integration aims to overcome limitations posed by traditional methods, such as manual data processing and pattern recognition, which are time-consuming and prone to human error.

One of the hardest technical difficulties lie...

---

### P27: Cell viability prediction and optimization in extrusion-based bioprinting via ne

**DOI**: 10.1088/1758-5090/ad17cf
**Best distance**: 0.670
**Chunks retrieved**: 3

**Retrieved chunks:**

_[P27 chunk_24, d=0.670]_

This study utilized a neural network-based Bayesian optimization model to optimize the bioprinting process to obtain the highest possible cell viability. Bayesian optimization is a powerful ML optimization tool that is applied to discover the optimal set of variables for a given objective function [24]. The Bayesian optimization model in this study allows us to quantify the uncertainty in cell viability prediction as well as predict the optimal bioprinting experimental features for maximizing cell viability. This method in extrusion-based bioprinting was used in the study by Ruberu et al [1] for the first time to optimize the printability of the bioink. The researchers utilized Bayesian optimization as a novel method for optimizing some of the printing variables while minimizing the necessary experiments. The study demonstrated the promising outcome of this method in speeding up the extrusion-based bioprinting process compared to conventional optimization.
Our current work aims to eliminate laborious trial-and-error steps in optimizing cell viability in extrusion-based bioprinting by integrating our built neural network with the Bayesian optimization technique. Inspired by the pion...

_[P27 chunk_25, d=0.681]_

To execute Bayesian optimization, we first defined the range space for 'Crosslinking (CaCl2)_Concentration' and 'Physical_crosslinking_ time' by determining the minimum and maximum values. We set the minimum value to be greater than zero because we intended to evaluate optical crosslinking parameters rather than zero for our particular bioprinting parameters. In addition, we defined the range's maximal value as the highest value observed in our dataset. The Bayesian optimization procedure relied on the neural network we developed for regression. During each iteration of the optimizer, the suggested 'Crosslinking (CaCl2)_Concentration' and 'Physical_crosslinking_time' with other predefined and desired variables were fed into the trained neural network to predict cell viability with good accuracy. This approach enabled us to rapidly investigate numerous unexplored parameter possibilities, ultimately identifying the most efficient parameter combination in printing. The Gaussian process in this process model the underlying patterns and correlations in the data, providing a probabilistic estimate of the behavior of cell viability for a set of printing parameters, and discovers the best ...

_[P27 chunk_12, d=0.690]_

The algorithm of this neural network-based Bayesian optimization model is depicted in figure 1. Here, the base Bayesian optimization framework started by constructing the Gaussian Process model using the created dataset of variables in the bioprinting process and their associated cell viability. The Gaussian Process model consists of mean and covariance functions. The Matern kernel, with a smoothness parameter equal to 2.5, is the covariance function in this study, which conveys the smoothness of the function and determines how the cell viability percentage in one spot affects the prediction of the nearby values [26]. Moreover, in the training of the Gaussian Process model, a small positive number, α = 10 -3 , was added to each element on the diagonal of the covariance matrix to modify the numerical stability of this method.
Using the Gaussian Process model's mean and covariance, we developed an acquisition function that suggests the next questioned bioprinting variables to probe. The suggested parameters were chosen to maximize the probability of achieving the highest cell viability while maintaining a balance between exploration and exploitation. In this study, the GP-UCB acquisi...

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
**Best distance**: 0.670
**Chunks retrieved**: 3

**Retrieved chunks:**

_[P111 chunk_24, d=0.670]_

This study utilized a neural network-based Bayesian optimization model to optimize the bioprinting process to obtain the highest possible cell viability. Bayesian optimization is a powerful ML optimization tool that is applied to discover the optimal set of variables for a given objective function [24]. The Bayesian optimization model in this study allows us to quantify the uncertainty in cell viability prediction as well as predict the optimal bioprinting experimental features for maximizing cell viability. This method in extrusion-based bioprinting was used in the study by Ruberu et al [1] for the first time to optimize the printability of the bioink. The researchers utilized Bayesian optimization as a novel method for optimizing some of the printing variables while minimizing the necessary experiments. The study demonstrated the promising outcome of this method in speeding up the extrusion-based bioprinting process compared to conventional optimization.
Our current work aims to eliminate laborious trial-and-error steps in optimizing cell viability in extrusion-based bioprinting by integrating our built neural network with the Bayesian optimization technique. Inspired by the pion...

_[P111 chunk_25, d=0.681]_

To execute Bayesian optimization, we first defined the range space for 'Crosslinking (CaCl2)_Concentration' and 'Physical_crosslinking_ time' by determining the minimum and maximum values. We set the minimum value to be greater than zero because we intended to evaluate optical crosslinking parameters rather than zero for our particular bioprinting parameters. In addition, we defined the range's maximal value as the highest value observed in our dataset. The Bayesian optimization procedure relied on the neural network we developed for regression. During each iteration of the optimizer, the suggested 'Crosslinking (CaCl2)_Concentration' and 'Physical_crosslinking_time' with other predefined and desired variables were fed into the trained neural network to predict cell viability with good accuracy. This approach enabled us to rapidly investigate numerous unexplored parameter possibilities, ultimately identifying the most efficient parameter combination in printing. The Gaussian process in this process model the underlying patterns and correlations in the data, providing a probabilistic estimate of the behavior of cell viability for a set of printing parameters, and discovers the best ...

_[P111 chunk_12, d=0.690]_

The algorithm of this neural network-based Bayesian optimization model is depicted in figure 1. Here, the base Bayesian optimization framework started by constructing the Gaussian Process model using the created dataset of variables in the bioprinting process and their associated cell viability. The Gaussian Process model consists of mean and covariance functions. The Matern kernel, with a smoothness parameter equal to 2.5, is the covariance function in this study, which conveys the smoothness of the function and determines how the cell viability percentage in one spot affects the prediction of the nearby values [26]. Moreover, in the training of the Gaussian Process model, a small positive number, α = 10 -3 , was added to each element on the diagonal of the covariance matrix to modify the numerical stability of this method.
Using the Gaussian Process model's mean and covariance, we developed an acquisition function that suggests the next questioned bioprinting variables to probe. The suggested parameters were chosen to maximize the probability of achieving the highest cell viability while maintaining a balance between exploration and exploitation. In this study, the GP-UCB acquisi...

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

### P11: Coupling machine learning with 3D bioprinting to fast track optimisation of extr 🎯 (also cited in outline)

**DOI**: 10.1016/j.apmt.2020.100914
**Best distance**: 0.702
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P11 chunk_14, d=0.702]_

In the experiment, the scoring of a print was manually conducted via a visual assessment by the experimenter. The process involved taking photos, like those shown in Table 3 , and comparing the images against the scale (shown in Fig. 4 ) to decide upon a score. As this is done by sight, much of the scoring is prone to human errors of judgements, and as such may not reflect a consistent objective measure of the print performance. Though the Gaussian Process model can handle errors in measurement (referred to as noise), this can impact the performance of the optimiser and result in more experiments being needed to find the optima. An additional factor contributing to an extension of the number of experiments needed to reach the optima is the experimental batch size. When a batch is recommended by the Bayesian optimiser, the confidence of achieving a good print is ranked down from the first recommendation of a batch (strongest confidence), with the least confident recommendation proposed at the end of the batch. In our experiments we initially started with a batch size of 10. With a large batch size, there is a chance that some experiments in the batch were recommended with far less c...

**Background (from SOP metadata):**
Certainly, here are the extracted sections from the research paper based on your request:

### 1. Research Background

**Page 2:**
"3D bioprinting continues to grow exponentially, gaining significant popularity within the fields of regenerative medicine and disease modelling [1]. The term 3D biofabrication has been used in parallel with the term 3D bioprinting and can be defined as a computer-guided additive manufacturing technique for creating highly precise and complex 3D structures with biologically relevant materials in a pre-designed geometry [2, 3]."

**Page 2:**
"Bioinks are a fundament...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters (Page 1-2)**

The central problem addressed in this paper is the optimization of printability for extrusion-based bioprinting, specifically focusing on GelMA and GelMA/HAMA bioinks. This matters because achieving optimal printing conditions can significantly enhance the reproducibility and quality of 3D printed constructs, which are crucial for applications in regenerative medicine and disease modeling.

2. **Hardest Technical Difficulties (Page 4-5)**

The hardest technical difficulties include fine-tuning numerous variables such as bioink composit...

---

### P33: Coupling machine learning with 3D bioprinting to fast track optimisation of extr

**DOI**: 10.1016/j.apmt.2020.100914
**Best distance**: 0.702
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P33 chunk_14, d=0.702]_

In the experiment, the scoring of a print was manually conducted via a visual assessment by the experimenter. The process involved taking photos, like those shown in Table 3 , and comparing the images against the scale (shown in Fig. 4 ) to decide upon a score. As this is done by sight, much of the scoring is prone to human errors of judgements, and as such may not reflect a consistent objective measure of the print performance. Though the Gaussian Process model can handle errors in measurement (referred to as noise), this can impact the performance of the optimiser and result in more experiments being needed to find the optima. An additional factor contributing to an extension of the number of experiments needed to reach the optima is the experimental batch size. When a batch is recommended by the Bayesian optimiser, the confidence of achieving a good print is ranked down from the first recommendation of a batch (strongest confidence), with the least confident recommendation proposed at the end of the batch. In our experiments we initially started with a batch size of 10. With a large batch size, there is a chance that some experiments in the batch were recommended with far less c...

**Background (from SOP metadata):**
Certainly, here are the extracted sections from the research paper based on your request:

### 1. Research Background

**Page 1:**
"3D bioprinting continues to grow exponentially, gaining significant popularity within the fields of regenerative medicine and disease modelling [1]. The term 3D biofabrication has been used in parallel with the term 3D bioprinting and can be defined as a computer-guided additive manufacturing technique for creating highly precise and complex 3D structures with biologically relevant materials in a pre-designed geometry [2, 3]."

**Page 1:**
"Bioinks are a fundament...

**Core problem & critique:**
1. **Most Central Problem and Why It Matters (Page 1-2)**

The central problem addressed in this paper is the optimization of printability for extrusion-based bioprinting, specifically focusing on GelMA and GelMA/HAMA bioinks. This matters because achieving optimal printing parameters can significantly enhance the reproducibility and quality of 3D printed constructs, which are crucial for applications in regenerative medicine and disease modeling.

2. **Hardest Technical Difficulties (Page 4-5)**

The hardest technical difficulties include fine-tuning numerous variables to achieve a reproducib...

---

### P5: Challenges and Advances in 3D Bioprinting for Tissue Engineering and Regenerativ

**DOI**: 10.1002/adfm.202509530
**Best distance**: 0.715
**Chunks retrieved**: 1

**Retrieved chunks:**

_[P5 chunk_54, d=0.715]_

Bayesian optimization (BO) and Gaussian process (GP) modeling have become essential tools in optimizing the complex and resource-demanding process of bioprinting. In EBB, where precise control over parameters like bioink composition, nozzle ge- ometry, and extrusion pressure is crucial, traditional trial-anderror methods can be inefficient and time-consuming. BO starts by testing a few initial parameter combinations and using a GP to create a model that predicts the system's behavior. It then uses an acquisition function to decide the next parameters to test, searching for a balance between exploring new possibilities and refining www.advancedsciencenews.com the most promising ones. Each new result updates the GP model, making predictions more accurate. The process repeats until a stopping condition is met, such as reaching a set number of iterations or finding a sufficient result. Finally, the approach identifies the best solution found [ 185] as shown in Figure 15C.
GP modeling, often used within BO, creates a probabilistic model of the system by predicting the outcomes of experiments based on limited data. It treats the relationship between input parameters and outputs as a cont...

**Background (from SOP metadata):**
The research paper examines the transformative role of artificial intelligence (AI) in 3D bioprinting and how advanced AI technologies enhance precision, functionality, and scalability. Key challenges in traditional bioprinting include achieving precise cell placement, real-time process monitoring, quality control, and managing bioink variability. These limitations hinder the production of complex tissues with high fidelity and consistency.

The paper aims to address these issues by integrating various branches of AI such as machine learning (ML), computer vision (CV), robotics, natural langua...

**Core problem & critique:**
The paper explores the transformative role of artificial intelligence (AI) in 3D bioprinting and its potential to enhance precision, functionality, and scalability. The central problem addressed is the technical challenge of achieving precise control over cell deposition and maintaining high-quality tissue fabrication despite biological variability and mechanical limitations inherent in current bioprinters. This issue is significant because it hinders the transition from laboratory settings to clinical applications where reproducibility and reliability are paramount.

One of the hardest techni...

---
