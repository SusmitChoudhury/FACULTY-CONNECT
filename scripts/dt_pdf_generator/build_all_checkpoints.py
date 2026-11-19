import os
import sys

from generate_diagrams import generate_all_diagrams
from build_cp2 import build_cp2_pdf
from build_cp3 import build_cp3_pdf
from build_cp4 import build_cp4_pdf
from build_cp5 import build_cp5_pdf
from build_cp6 import build_cp6_pdf
from build_cp7 import build_cp7_pdf

def main():
    print("="*70)
    print("FACULTY CONNECT (P09) — INT335 DESIGN THINKING CHECKPOINTS BUILDER")
    print("Lovely Professional University (LPU) • Academic Session 2026–2027")
    print("="*70)

    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'INT335_P09_Checkpoints_PDFs'))
    os.makedirs(out_dir, exist_ok=True)

    print("\n[Stage 1/7] Generating visual diagram assets...")
    generate_all_diagrams()

    print("\n[Stage 2/7] Generating CP2: Empathy & User Research...")
    build_cp2_pdf(os.path.join(out_dir, 'CP2_Empathy_and_User_Research.pdf'))

    print("\n[Stage 3/7] Generating CP3: Problem Definition...")
    build_cp3_pdf(os.path.join(out_dir, 'CP3_Problem_Definition.pdf'))

    print("\n[Stage 4/7] Generating CP4: Ideation and Selection...")
    build_cp4_pdf(os.path.join(out_dir, 'CP4_Ideation_and_Selection.pdf'))

    print("\n[Stage 5/7] Generating CP5: Prototype Readiness...")
    build_cp5_pdf(os.path.join(out_dir, 'CP5_Prototype_Readiness.pdf'))

    print("\n[Stage 6/7] Generating CP6: Testing and Improvements...")
    build_cp6_pdf(os.path.join(out_dir, 'CP6_Testing_and_Improvements.pdf'))

    print("\n[Stage 7/7] Generating CP7: Final Showcase and Report...")
    build_cp7_pdf(os.path.join(out_dir, 'CP7_Final_Showcase_and_Report.pdf'))

    print("\n" + "="*70)
    print("ALL 6 CHECKPOINT PDF DOCUMENTS SUCCESSFULLY GENERATED!")
    print(f"Location: {out_dir}")
    print("="*70)

if __name__ == '__main__':
    main()
