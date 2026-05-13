# SOP_v3 prompts - clean output (per ADR-0007)
#
# Changes from v2:
#   - No "page numbers" requested (LLM can't see pages)
#   - No "1) 2) 3)" enumerate (triggers markdown)
#   - No "A) B) C)" heading (triggers markdown bold)
#   - Plain prose paragraphs only
#   - Explicit RULES block prohibiting markdown / fake pages / filler
#   - Verbatim quote field reserved (ADR-0010, not yet enforced)

GLOBAL_RULES = """
CRITICAL OUTPUT RULES (must obey):
1. Plain prose paragraphs only. NO markdown.
2. NO bold (**text**), NO headers (### / ##), NO bullets (* / -), NO numbered lists (1. / 1) / A) ).
3. NO page references. You do not have page information. Do not write "page 5", "(p.2)", "pages 4-5", etc.
4. NO preamble like "Based on the provided text" or "Here are the methods". Start directly with substantive content.
5. NO repeating the question phrasing. Start with information, not "This paper addresses...".
6. Separate paragraphs with single newline. No section labels.
"""

SOP_V3_PROMPTS = {
    "L1_factual_background": (
        "Extract the factual background of this research paper.\n\n"
        + GLOBAL_RULES + "\n"
        + "Cover in one continuous narrative: what problem the paper studies, what concepts are relevant, "
        + "what failure modes prior work has, what the paper aims to achieve, and how it measures success.\n\n"
        + "Paper text:\n{text}\n\n"
        + "Output:"
    ),
    
    "L1_factual_methods": (
        "Extract the methods used in this research paper.\n\n"
        + GLOBAL_RULES + "\n"
        + "Describe in continuous prose all experimental procedures, analytical or modeling techniques, "
        + "and validation approaches. Do not group them with labels. Just describe each method as a "
        + "self-contained sentence or two of prose.\n\n"
        + "Paper text:\n{text}\n\n"
        + "Output:"
    ),
    
    "L2_interpretive_problem": (
        "Critically analyze this research paper.\n\n"
        + GLOBAL_RULES + "\n"
        + "Write a continuous prose analysis covering: the central problem and its significance, "
        + "the hardest technical difficulties, the gap between authors' claims and supporting evidence, "
        + "and a one-sentence overall judgment of intellectual contribution. "
        + "Do not label these as separate questions; weave into flowing analysis.\n\n"
        + "Paper text:\n{text}\n\n"
        + "Output:"
    ),
    
    "L2_interpretive_scoring": (
        "Score this paper on 10 dimensions. For EACH dimension, write exactly one line:\n"
        "    dimension_name: SCORE/10. One-sentence justification.\n\n"
        "Example:\n"
        "    novelty: 7/10. Combines existing ML methods in a new application domain but no new algorithm.\n"
        "    clarity: 8/10. Figures are clean and the math is well-explained.\n\n"
        "This one-line-per-dimension format is the ONLY structured list allowed; "
        "everywhere else in your output, use plain prose.\n\n"
        + GLOBAL_RULES + "\n"
        + "Use lowercase dimension names. No bold. No quotes around dimension names.\n\n"
        + "Dimensions: novelty, clarity, methodological rigor, empirical strength, reproducibility, "
        + "theoretical contribution, practical impact, scope appropriateness, writing quality, citation use.\n\n"
        + "Paper text:\n{text}\n\n"
        + "Output:"
    ),
    
    "L3_personal_relevance": (
        "Identify the top 3 sections of the review outline this paper best supports.\n\n"
        + GLOBAL_RULES + "\n"
        + "For each section, write a single prose paragraph (3-5 sentences) explaining: "
        + "which section, what specific arguments the paper supports, and what evidence type "
        + "(empirical / theoretical / review / methodology). Do not number the sections in output; "
        + "separate them with blank lines.\n\n"
        + "Review outline:\n{outline}\n\n"
        + "Paper text:\n{text}\n\n"
        + "Output:"
    ),
}
