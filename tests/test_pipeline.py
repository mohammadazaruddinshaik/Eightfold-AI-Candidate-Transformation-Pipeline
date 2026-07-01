import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

APP = "app.py"
RESUME = "input/resume.pdf"

CSV_HEADER = "name,email,phone,current_company,title\n"

TEST_CASES = [

    {
        "name": "Happy Path",
        "expect_success": True,
        "csv": CSV_HEADER +
               "Shaik Mohammad Azaruddin,"
               "mohammadazaruddinsk@gmail.com,"
               "+919100312008,"
               "GDOT Contractor,"
               "RAG Data Intern\n",
        "checks": [
            ("full_name", "Shaik Mohammad Azaruddin"),
            ("emails", "mohammadazaruddinsk@gmail.com"),
            ("phones", "+919100312008"),
        ],
    },

    {
        "name": "Missing Company",
        "expect_success": True,
        "csv": CSV_HEADER +
               "Shaik Mohammad Azaruddin,"
               "mohammadazaruddinsk@gmail.com,"
               "+919100312008,,"
               "RAG Data Intern\n",
        "checks": [
            ("full_name", "Shaik Mohammad Azaruddin"),
        ],
    },

    {
        "name": "Email Normalization",
        "expect_success": True,
        "csv": CSV_HEADER +
               "Shaik Mohammad Azaruddin,"
               "MOHAMMADAZARUDDINSK@GMAIL.COM,"
               "+919100312008,"
               "GDOT Contractor,"
               "RAG Data Intern\n",
        "checks": [
            ("emails", "mohammadazaruddinsk@gmail.com"),
        ],
    },

    {
        "name": "Phone Normalization",
        "expect_success": True,
        "csv": CSV_HEADER +
               "Shaik Mohammad Azaruddin,"
               "mohammadazaruddinsk@gmail.com,"
               "919100312008,"
               "GDOT Contractor,"
               "RAG Data Intern\n",
        "checks": [
            ("phones", "+919100312008"),
        ],
    },

    {
        "name": "Wrong Company (CSV Priority)",
        "expect_success": True,
        "csv": CSV_HEADER +
               "Shaik Mohammad Azaruddin,"
               "mohammadazaruddinsk@gmail.com,"
               "+919100312008,"
               "Microsoft,"
               "RAG Data Intern\n",
        "checks": [
            ("experience_company", "Microsoft"),
        ],
    },

    {
        "name": "Missing Email",
        "expect_success": True,
        "csv": CSV_HEADER +
               "Shaik Mohammad Azaruddin,,"
               "+919100312008,"
               "GDOT Contractor,"
               "RAG Data Intern\n",
        "checks": [],
    },

    {
        "name": "Missing Phone",
        "expect_success": True,
        "csv": CSV_HEADER +
               "Shaik Mohammad Azaruddin,"
               "mohammadazaruddinsk@gmail.com,,"
               "GDOT Contractor,"
               "RAG Data Intern\n",
        "checks": [],
    },

    {
        "name": "Wrong Name Same Email",
        "expect_success": True,
        "csv": CSV_HEADER +
               "Random Person,"
               "mohammadazaruddinsk@gmail.com,"
               "+919100312008,"
               "GDOT Contractor,"
               "RAG Data Intern\n",
        "checks": [
            ("emails", "mohammadazaruddinsk@gmail.com"),
        ],
    },

    {
        "name": "Completely Different Candidate",
        "expect_success": False,
        "csv": CSV_HEADER +
               "John Doe,"
               "john@example.com,"
               "+15551234567,"
               "Google,"
               "Software Engineer\n",
        "checks": [],
    },
]


def get_value(data, field):

    if field == "emails":
        return data.get("emails", [None])[0]

    if field == "phones":
        return data.get("phones", [None])[0]

    if field == "experience_company":
        exp = data.get("experience", [])
        if exp:
            return exp[0].get("company")
        return None

    return data.get(field)


def run_pipeline(csv_content):
    """
    Execute the pipeline with a temporary CSV and return
    (success, parsed_json, stderr)
    """

    # -------------------------------
    # Temporary CSV
    # -------------------------------

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
        encoding="utf-8",
    ) as csv_file:

        csv_file.write(csv_content)
        csv_path = csv_file.name

    # -------------------------------
    # Temporary Output JSON
    # -------------------------------

    with tempfile.NamedTemporaryFile(
        suffix=".json",
        delete=False,
    ) as output_file:

        output_path = output_file.name

    command = [
        "python",
        APP,
        "--resume",
        RESUME,
        "--csv",
        csv_path,
        "--output",
        output_path,
        "--pretty",
    ]

    start = time.perf_counter()

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    elapsed = time.perf_counter() - start

    # -------------------------------
    # Cleanup CSV
    # -------------------------------

    if os.path.exists(csv_path):
        os.remove(csv_path)

    # -------------------------------
    # Pipeline failed
    # -------------------------------

    if result.returncode != 0:

        if os.path.exists(output_path):
            os.remove(output_path)

        return False, None, result.stderr, elapsed

    # -------------------------------
    # Output missing
    # -------------------------------

    if not os.path.exists(output_path):
        return False, None, "Output JSON not created.", elapsed

    if os.path.getsize(output_path) == 0:

        os.remove(output_path)

        return False, None, "Output JSON is empty.", elapsed

    # -------------------------------
    # Read JSON
    # -------------------------------

    try:

        with open(
            output_path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

    except json.JSONDecodeError:

        if os.path.exists(output_path):
            os.remove(output_path)

        return False, None, "Invalid JSON produced.", elapsed

    # -------------------------------
    # Cleanup
    # -------------------------------

    if os.path.exists(output_path):
        os.remove(output_path)

    return True, data, "", elapsed


def run_tests():

    print("=" * 70)
    print("Candidate Transformation Pipeline Test Suite")
    print("=" * 70)

    passed = 0
    failed = 0

    suite_start = time.perf_counter()

    for test in TEST_CASES:

        print(f"\n▶ Running: {test['name']}")

        success, data, error, elapsed = run_pipeline(
            test["csv"]
        )

        # ----------------------------------------------------
        # Expected Failure
        # ----------------------------------------------------

        if not test["expect_success"]:

            if success:
                print("   ❌ FAILED")
                print("   Expected pipeline to reject candidate.")
                failed += 1

            else:
                print("   ✅ PASSED")
                print("   Identity mismatch handled correctly.")
                print(f"   Time: {elapsed:.3f}s")
                passed += 1

            continue

        # ----------------------------------------------------
        # Unexpected Failure
        # ----------------------------------------------------

        if not success:

            print("   ❌ FAILED")
            print(f"   Error: {error}")

            failed += 1
            continue

        # ----------------------------------------------------
        # Validate Fields
        # ----------------------------------------------------

        case_passed = True

        for field, expected in test["checks"]:

            actual = get_value(data, field)

            if actual != expected:

                case_passed = False

                print(f"\n      Field : {field}")
                print(f"      Expected : {expected}")
                print(f"      Actual   : {actual}")

        if case_passed:

            print("   ✅ PASSED")
            print(f"   Time: {elapsed:.3f}s")

            passed += 1

        else:

            print("   ❌ FAILED")

            failed += 1

    total_time = time.perf_counter() - suite_start

    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    print(f"Total Tests : {len(TEST_CASES)}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print(f"Success Rate: {(passed/len(TEST_CASES))*100:.1f}%")
    print(f"Total Time  : {total_time:.3f}s")

    print("=" * 70)

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED")
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")


if __name__ == "__main__":
    run_tests()