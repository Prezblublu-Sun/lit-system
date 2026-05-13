# Bioprinting Golden Set (5 papers)

5 representative papers chosen for benchmarking SOP extraction quality
across the bioprinting library timeline.

Selection rationale:
- P1, P5  : Early SOP_v2 ingest (Week 2)
- P44     : Mid-period research paper, manually audited (CV-aided bone)
- P77     : Post-restart ingest (Week 2 Day 4 evening)
- P117    : Latest ingest, RSC review's target topic (self-driving bioprinting)

| paper_id | doc_id            | title                                                       | DOI                          |
|----------|-------------------|-------------------------------------------------------------|------------------------------|
| P1       | 5f23b7834bcd9638  | AI for biofabrication                                       | MISSING (review)             |
| P5       | 63a0f39f8e576219  | The Synergy of Artificial Intelligence and 3D Bioprinting   | MISSING                      |
| P44      | 59efff5fa9ec3a3d  | Computer vision-aided bioprinting for bone research         | 10.1038/s41413-022-00192-2   |
| P77      | 3a5e1b0de5a85ee3  | On the reproducibility of extrusion-based bioprinting       | 10.1088/1758-5090/acfe3b     |
| P117     | a6741da02cfc40ba  | Self-driving bioprinting laboratories                       | 10.1088/1758-5090/ae3645     |

PDFs themselves live in inbox/<doc_id>.pdf (gitignored). To recreate
symlinks on a fresh clone:

    for pair in "P1:5f23b7834bcd9638" "P5:63a0f39f8e576219" \
                "P44:59efff5fa9ec3a3d" "P77:3a5e1b0de5a85ee3" \
                "P117:a6741da02cfc40ba"; do
        pid="${pair%:*}"
        did="${pair#*:}"
        ln -sf "$(realpath inbox/${did}.pdf)" "golden_set/bioprinting_5/${pid}.pdf"
    done
