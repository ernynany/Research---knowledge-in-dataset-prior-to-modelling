"""Writes references.tex (IEEE style, numbered in order of first citation) from the entries below.

Only works published 2010-2026 are cited. Scans the paper's .tex files for \\cite{...} keys in order.
"""
import re, os

E = {
"grinsztajn2022": r"L.~Grinsztajn, E.~Oyallon, and G.~Varoquaux, ``Why do tree-based models still outperform deep learning on typical tabular data?,'' in \emph{Adv. Neural Inf. Process. Syst. (NeurIPS), Datasets and Benchmarks Track}, vol.~35, 2022.",
"erickson2025": r"N.~Erickson \emph{et al.}, ``TabArena: A living benchmark for machine learning on tabular data,'' in \emph{Adv. Neural Inf. Process. Syst. (NeurIPS), Datasets and Benchmarks Track}, 2025, arXiv:2506.16791.",
"hollmann2025": r"N.~Hollmann \emph{et al.}, ``Accurate predictions on small data with a tabular foundation model,'' \emph{Nature}, vol.~637, no.~8045, pp.~319--326, 2025, doi: 10.1038/s41586-024-08328-6.",
"renggli2020snoopy": r"C.~Renggli \emph{et al.}, ``Ease.ml/snoopy in action: Towards automatic feasibility analysis for machine learning application development,'' \emph{Proc. VLDB Endow.}, vol.~13, no.~12, pp.~2837--2840, 2020.",
"renggli2023feasibility": r"C.~Renggli \emph{et al.}, ``Automatic feasibility study via data quality analysis for ML: A case-study on label noise,'' in \emph{Proc. IEEE Int. Conf. Data Eng. (ICDE)}, 2023, arXiv:2010.08410.",
"lorena2019": r"A.~C. Lorena, L.~P.~F. Garcia, J.~Lehmann, M.~C.~P. Souto, and T.~K. Ho, ``How complex is your classification problem? A survey on measuring classification complexity,'' \emph{ACM Comput. Surv.}, vol.~52, no.~5, Art. no.~107, 2019.",
"ross2014": r"B.~C. Ross, ``Mutual information between discrete and continuous data sets,'' \emph{PLoS ONE}, vol.~9, no.~2, Art. no.~e87357, 2014.",
"ojala2010": r"M.~Ojala and G.~C. Garriga, ``Permutation tests for studying classifier performance,'' \emph{J. Mach. Learn. Res.}, vol.~11, pp.~1833--1863, 2010.",
"varoquaux2018": r"G.~Varoquaux, ``Cross-validation failure: Small sample sizes lead to large error bars,'' \emph{NeuroImage}, vol.~180, pp.~68--77, 2018.",
"korthauer2019": r"K.~Korthauer \emph{et al.}, ``A practical guide to methods controlling false discoveries in computational biology,'' \emph{Genome Biol.}, vol.~20, Art. no.~118, 2019, doi: 10.1186/s13059-019-1716-1.",
"renggli2021feebee": r"C.~Renggli, L.~Rimanic, N.~Hollenstein, and C.~Zhang, ``Evaluating Bayes error estimators on real-world datasets with FeeBee,'' in \emph{Adv. Neural Inf. Process. Syst. (NeurIPS), Datasets and Benchmarks Track}, 2021, arXiv:2108.13034.",
"theisen2021": r"R.~Theisen, H.~Wang, L.~R. Varshney, C.~Xiong, and R.~Socher, ``Evaluating state-of-the-art classification models against Bayes optimality,'' in \emph{Adv. Neural Inf. Process. Syst. (NeurIPS)}, vol.~34, 2021.",
"ishida2023": r"T.~Ishida, I.~Yamane, N.~Charoenphakdee, G.~Niu, and M.~Sugiyama, ``Is the performance of my deep network too good to be true? A direct approach to estimating the Bayes error in binary classification,'' in \emph{Proc. Int. Conf. Learn. Represent. (ICLR)}, 2023.",
"smith2014": r"M.~R. Smith, T.~Martinez, and C.~Giraud-Carrier, ``An instance level analysis of data complexity,'' \emph{Mach. Learn.}, vol.~95, no.~2, pp.~225--256, 2014.",
"munoz2018": r"M.~A. Mu\~{n}oz, L.~Villanova, D.~Baatar, and K.~Smith-Miles, ``Instance spaces for machine learning classification,'' \emph{Mach. Learn.}, vol.~107, 2018.",
"rivolli2022": r"A.~Rivolli, L.~P.~F. Garcia, C.~Soares, J.~Vanschoren, and A.~C.~P.~L.~F. de~Carvalho, ``Meta-features for meta-learning,'' \emph{Knowl.-Based Syst.}, vol.~240, Art. no.~108101, 2022.",
"komorniczak2022": r"J.~Komorniczak and P.~Ksieniewicz, ``problexity -- An open-source Python library for binary classification problem complexity assessment,'' 2022, arXiv:2207.06709.",
"pedregosa2011": r"F.~Pedregosa \emph{et al.}, ``Scikit-learn: Machine learning in Python,'' \emph{J. Mach. Learn. Res.}, vol.~12, pp.~2825--2830, 2011.",
"gao2017": r"W.~Gao, S.~Kannan, S.~Oh, and P.~Viswanath, ``Estimating mutual information for discrete-continuous mixtures,'' in \emph{Adv. Neural Inf. Process. Syst. (NeurIPS)}, vol.~30, 2017.",
"mcallester2020": r"D.~McAllester and K.~Stratos, ``Formal limitations on the measurement of mutual information,'' in \emph{Proc. Int. Conf. Artif. Intell. Stat. (AISTATS)}, PMLR vol.~108, 2020.",
"czyz2023": r"P.~Czy\.{z}, F.~Grabowski, J.~E. Vogt, N.~Beerenwinkel, and A.~Marx, ``Beyond normal: On the evaluation of mutual information estimators,'' in \emph{Adv. Neural Inf. Process. Syst. (NeurIPS)}, vol.~36, 2023.",
"szekely2013": r"G.~J. Sz\'{e}kely and M.~L. Rizzo, ``Energy statistics: A class of statistics based on distances,'' \emph{J. Stat. Plan. Inference}, vol.~143, no.~8, pp.~1249--1272, 2013.",
"ramoscarreno2023": r"C.~Ramos-Carre\~{n}o and J.~L. Torrecilla, ``dcor: Distance correlation and energy statistics in Python,'' \emph{SoftwareX}, vol.~22, Art. no.~101326, 2023.",
"sejdinovic2013": r"D.~Sejdinovic, B.~Sriperumbudur, A.~Gretton, and K.~Fukumizu, ``Equivalence of distance-based and RKHS-based statistics in hypothesis testing,'' \emph{Ann. Stat.}, vol.~41, no.~5, pp.~2263--2291, 2013.",
"ramdas2015": r"A.~Ramdas, S.~J. Reddi, B.~P\'{o}czos, A.~Singh, and L.~Wasserman, ``On the decreasing power of kernel and distance based nonparametric hypothesis tests in high dimensions,'' in \emph{Proc. AAAI Conf. Artif. Intell.}, vol.~29, 2015.",
"vergara2014": r"J.~R. Vergara and P.~A. Est\'{e}vez, ``A review of feature selection methods based on mutual information,'' \emph{Neural Comput. Appl.}, vol.~24, no.~1, pp.~175--186, 2014.",
"li2017": r"J.~Li \emph{et al.}, ``Feature selection: A data perspective,'' \emph{ACM Comput. Surv.}, vol.~50, no.~6, Art. no.~94, 2017.",
"lopezpaz2017": r"D.~Lopez-Paz and M.~Oquab, ``Revisiting classifier two-sample tests,'' in \emph{Proc. Int. Conf. Learn. Represent. (ICLR)}, 2017.",
"kim2021": r"I.~Kim, A.~Ramdas, A.~Singh, and L.~Wasserman, ``Classification accuracy as a proxy for two-sample testing,'' \emph{Ann. Stat.}, vol.~49, no.~1, 2021, doi: 10.1214/20-AOS1962.",
"hemerik2018": r"J.~Hemerik and J.~Goeman, ``Exact testing with random permutations,'' \emph{TEST}, vol.~27, 2018.",
"phipson2010": r"B.~Phipson and G.~K. Smyth, ``Permutation p-values should never be zero: Calculating exact p-values when permutations are randomly drawn,'' \emph{Stat. Appl. Genet. Mol. Biol.}, vol.~9, no.~1, Art. no.~39, 2010.",
"hollmann2023": r"N.~Hollmann, S.~M{\"u}ller, K.~Eggensperger, and F.~Hutter, ``TabPFN: A transformer that solves small tabular classification problems in a second,'' in \emph{Proc. Int. Conf. Learn. Represent. (ICLR)}, 2023.",
"qu2025": r"J.~Qu, D.~Holzm{\"u}ller, G.~Varoquaux, and M.~Le~Morvan, ``TabICL: A tabular foundation model for in-context learning on large data,'' in \emph{Proc. Int. Conf. Mach. Learn. (ICML)}, PMLR vol.~267, 2025.",
"hegselmann2023": r"S.~Hegselmann, A.~Buendia, H.~Lang, M.~Agrawal, X.~Jiang, and D.~Sontag, ``TabLLM: Few-shot classification of tabular data with large language models,'' in \emph{Proc. Int. Conf. Artif. Intell. Stat. (AISTATS)}, 2023.",
"bordt2024": r"S.~Bordt, H.~Nori, V.~Rodrigues, B.~Nushi, and R.~Caruana, ``Elephants never forget: Memorization and learning of tabular data in large language models,'' in \emph{Proc. Conf. Lang. Model. (COLM)}, 2024.",
"bates2024": r"S.~Bates, T.~Hastie, and R.~Tibshirani, ``Cross-validation: What does it estimate and how well does it do it?,'' \emph{J. Amer. Statist. Assoc.}, vol.~119, no.~546, pp.~1434--1445, 2024.",
"bouthillier2021": r"X.~Bouthillier \emph{et al.}, ``Accounting for variance in machine learning benchmarks,'' in \emph{Proc. Mach. Learn. Syst. (MLSys)}, vol.~3, 2021.",
"mohr2024": r"F.~Mohr and J.~N. van~Rijn, ``Learning curves for decision making in supervised machine learning: A survey,'' \emph{Mach. Learn.}, 2024.",
"viering2023": r"T.~Viering and M.~Loog, ``The shape of learning curves: A review,'' \emph{IEEE Trans. Pattern Anal. Mach. Intell.}, 2023.",
"kaufman2012": r"S.~Kaufman, S.~Rosset, C.~Perlich, and O.~Stitelman, ``Leakage in data mining: Formulation, detection, and avoidance,'' \emph{ACM Trans. Knowl. Discov. Data}, vol.~6, no.~4, Art. no.~15, 2012.",
"kapoor2023": r"S.~Kapoor and A.~Narayanan, ``Leakage and the reproducibility crisis in machine-learning-based science,'' \emph{Patterns}, vol.~4, no.~9, 2023.",
"frenay2014": r"B.~Fr\'{e}nay and M.~Verleysen, ``Classification in the presence of label noise: A survey,'' \emph{IEEE Trans. Neural Netw. Learn. Syst.}, vol.~25, no.~5, pp.~845--869, 2014.",
"xu2020": r"Y.~Xu, S.~Zhao, J.~Song, R.~Stewart, and S.~Ermon, ``A theory of usable information under computational constraints,'' in \emph{Proc. Int. Conf. Learn. Represent. (ICLR)}, 2020.",
"ethayarajh2022": r"K.~Ethayarajh, Y.~Choi, and S.~Swayamdipta, ``Understanding dataset difficulty with $\mathcal{V}$-usable information,'' in \emph{Proc. Int. Conf. Mach. Learn. (ICML)}, PMLR vol.~162, 2022.",
"dua2019": r"D.~Dua and C.~Graff, ``UCI Machine Learning Repository,'' Univ. California, Irvine, School Inf. Comput. Sci., 2019. [Online]. Available: http://archive.ics.uci.edu/ml",
"imbens2015": r"G.~W. Imbens, ``Matching methods in practice: Three examples,'' \emph{J. Hum. Resour.}, vol.~50, no.~2, pp.~373--419, 2015.",
"cunningham2021": r"S.~Cunningham, \emph{Causal Inference: The Mixtape}. New Haven, CT, USA: Yale Univ. Press, 2021.",
"benavoli2016": r"A.~Benavoli, G.~Corani, and F.~Mangili, ``Should we really use post-hoc tests based on mean-ranks?,'' \emph{J. Mach. Learn. Res.}, vol.~17, no.~5, pp.~1--10, 2016.",
}

def main(paper_dir):
    order = []
    files = ["paper.tex", "sections/front.tex", "sections/setup.tex", "sections/results.tex"]
    text = ""
    for f in files:
        p = os.path.join(paper_dir, f)
        if os.path.exists(p):
            text += open(p).read()
    # follow \input order: paper.tex inputs sections in order; simple approach: process in file order above
    for m in re.finditer(r"\\cite\{([^}]*)\}", text):
        for k in m.group(1).split(","):
            k = k.strip()
            if k and k not in order:
                order.append(k)
    missing = [k for k in order if k not in E]
    if missing:
        raise SystemExit(f"missing bib entries: {missing}")
    unused = [k for k in E if k not in order]
    out = ["\\begin{thebibliography}{%d}" % len(order)]
    for k in order:
        out.append(f"\\bibitem{{{k}}}\n{E[k]}\n")
    out.append("\\end{thebibliography}")
    open(os.path.join(paper_dir, "sections", "references.tex"), "w").write("\n".join(out))
    print(f"{len(order)} references written; unused entries: {unused}")

if __name__ == "__main__":
    main(os.path.dirname(os.path.abspath(__file__)))
