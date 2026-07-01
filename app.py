"""
Entry point for the Candidate Transformer.
"""

import json
import argparse
from pathlib import Path
from src.utils.file_validator import FileValidator
from src.parsers.csv_parser import CSVParser
from src.parsers.resume_parser import ResumeParser
from src.normalizers.candidate_normalizer import CandidateNormalizer
from src.merger.identity_resolver import IdentityResolver
from src.merger.candidate_merger import CandidateMerger
from src.merger.provenance_builder import ProvenanceBuilder
from src.confidence.confidence_calculator import ConfidenceCalculator
from src.projection.config_loader import ConfigLoader
from src.projection.projection_engine import ProjectionEngine
from src.validation.projection_validator import ProjectionValidator

def build_parser() -> argparse.ArgumentParser:
    """
    Build CLI argument parser.
    """

    parser = argparse.ArgumentParser(
        prog="Candidate Transformer",
        description="Multi-Source Candidate Data Transformer",
    )

    parser.add_argument(
        "--resume",
        type=Path,
        default=Path("input/resume.pdf"),
        help="Resume PDF path",
    )

    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("input/t1.csv"),
        help="Recruiter CSV path",
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "src/projection/sample_configs/default.json"
        ),
        help="Projection configuration JSON",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "output/candidate.json"
        ),
        help="Output JSON",
    )

    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print projected output",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show pipeline stages",
    )

    parser.add_argument(
        "--explain",
        action="store_true",
        help="Show provenance explanation",
    )

    return parser


def main():
    """
    Application entry point.
    """

    parser = build_parser()

    args = parser.parse_args()

    # --------------------------------------------------
    # Validate CLI Inputs
    # --------------------------------------------------

    try:

        FileValidator.validate_file(
            args.resume,
            "Resume",
        )

        FileValidator.validate_file(
            args.csv,
            "Recruiter CSV",
        )

        FileValidator.validate_file(
            args.config,
            "Projection Config",
        )

        FileValidator.prepare_output(
            args.output,
        )

    except Exception as error:

        print(f"\n❌ {error}")

        return

    # --------------------------------------------------
    # Show Configuration
    # --------------------------------------------------

    if args.verbose:

        print("\n" + "=" * 60)
        print("Candidate Transformation Pipeline")
        print("=" * 60)

        print(f"Resume : {args.resume}")
        print(f"CSV    : {args.csv}")
        print(f"Config : {args.config}")
        print(f"Output : {args.output}")

        print(f"Pretty : {args.pretty}")
        print(f"Verbose: {args.verbose}")
        print(f"Explain: {args.explain}")

        print("=" * 60)

    # --------------------------------------------------
    # Parse Sources
    # --------------------------------------------------

    if args.verbose:
        print("\n📄 Parsing input sources...")

    try:

        csv_candidate = CSVParser().parse(
            args.csv,
        )

        resume_candidate = ResumeParser().parse(
            args.resume,
        )

    except Exception as error:

        print(f"\n❌ Parsing failed: {error}")

        return

    if args.verbose:

        print("✅ Resume parsed successfully.")

        print("✅ Recruiter CSV parsed successfully.")
    
    
    # --------------------------------------------------
    # Normalize Candidates
    # --------------------------------------------------

    if args.verbose:
        print("\n🔄 Normalizing candidates...")

    try:

        normalizer = CandidateNormalizer()

        csv_candidate = normalizer.normalize(
            csv_candidate,
        )

        resume_candidate = normalizer.normalize(
            resume_candidate,
        )

    except Exception as error:

        print(f"\n❌ Normalization failed: {error}")

        return

    if args.verbose:

        print("✅ CSV candidate normalized.")

        print("✅ Resume candidate normalized.")

    # --------------------------------------------------
    # Identity Resolution
    # --------------------------------------------------

    if args.verbose:
        print("\n🔍 Resolving candidate identity...")

    try:

        resolver = IdentityResolver()

        identity_result = resolver.match(
            csv_candidate,
            resume_candidate,
        )

    except Exception as error:

        print(f"\n❌ Identity resolution failed: {error}")

        return

    if args.verbose:

        print(
            f"Identity Score : {identity_result.score:.2f}"
        )

        print(
            f"Matched        : {identity_result.matched}"
        )

        if identity_result.matched_on:

            print("Matched On     :")

            for field in identity_result.matched_on:

                print(f"   ✓ {field}")

        else:

            print("Matched On     : None")


    # --------------------------------------------------
    # Stop if candidates don't match
    # --------------------------------------------------

    if not identity_result.matched:

        print(
            "\n❌ The provided Resume and CSV "
            "do not belong to the same candidate."
        )

        return


    # --------------------------------------------------
    # Merge Candidates
    # --------------------------------------------------

    if args.verbose:
        print("\n🔀 Merging candidate profiles...")

    try:

        merger = CandidateMerger()

        canonical_candidate = merger.merge(
            [
                csv_candidate,
                resume_candidate,
            ]
        )

    except Exception as error:

        print(f"\n❌ Candidate merge failed: {error}")

        return

    if args.verbose:

        print("✅ Canonical candidate created.")

        print(
            f"Candidate ID : {canonical_candidate.candidate_id}"
        )

    # --------------------------------------------------
    # Build Provenance
    # --------------------------------------------------

    if args.verbose:
        print("\n📍 Building provenance...")

    try:

        builder = ProvenanceBuilder()

        canonical_candidate = builder.build(
            canonical_candidate,
            [
                csv_candidate,
                resume_candidate,
            ],
        )

    except Exception as error:

        print(f"\n❌ Provenance generation failed: {error}")

        return

    if args.verbose:

        print("✅ Provenance generated.")

        print(
            f"Tracked Fields : {len(canonical_candidate.provenance)}"
        )

    # --------------------------------------------------
    # Calculate Confidence
    # --------------------------------------------------

    if args.verbose:
        print("\n📊 Calculating confidence...")

    try:

        calculator = ConfidenceCalculator()

        canonical_candidate = calculator.calculate(
            canonical_candidate,
            identity_result,
        )

    except Exception as error:

        print(f"\n❌ Confidence calculation failed: {error}")

        return

    if args.verbose:

        confidence = canonical_candidate.overall_confidence

        if confidence:

            print(
                f"Overall Confidence : {confidence.score:.2f}"
            )

            print(
                f"Reason             : {confidence.reason}"
            )

        else:

            print("Overall Confidence : Not Available")
     
    # --------------------------------------------------
    # Load Projection Configuration
    # --------------------------------------------------

    if args.verbose:
        print("\n📦 Loading projection configuration...")

    try:

        config = ConfigLoader.load(
            args.config,
        )

    except Exception as error:

        print(f"\n❌ Failed to load configuration: {error}")

        return

    if args.verbose:

        print("✅ Projection configuration loaded.")       
    
        


    
    # --------------------------------------------------
    # Apply Projection
    # --------------------------------------------------

    if args.verbose:
        print("\n📤 Applying projection...")

    try:

        engine = ProjectionEngine()

        projected_candidate = engine.project(
            canonical_candidate,
            config,
        )

    except Exception as error:

        print(f"\n❌ Projection failed: {error}")

        return

    if args.verbose:

        print("✅ Projection completed.")
        
    
    # --------------------------------------------------
    # Validate Projection
    # --------------------------------------------------

    if args.verbose:
        print("\n✔ Validating projected output...")

    try:

        validator = ProjectionValidator()

        validation = validator.validate(
            projected_candidate,
            config,
        )

    except Exception as error:

        print(f"\n❌ Validation failed: {error}")

        return

    if not validation.valid:

        print("\n❌ Projection validation failed.")

        for error in validation.errors:

            print(f"   • {error}")

        return

    if args.verbose:

        print("✅ Validation passed.")
        
    # --------------------------------------------------
    # Write Output
    # --------------------------------------------------

    if args.verbose:
        print("\n💾 Writing output...")

    try:

        with args.output.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                projected_candidate,
                file,
                indent=4,
                ensure_ascii=False,
                default=str,
            )

    except Exception as error:

        print(f"\n❌ Failed to write output: {error}")

        return

    if args.verbose:

        print(f"✅ Output written to: {args.output}")
if __name__ == "__main__":
    main()