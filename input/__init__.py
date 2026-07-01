import json
import subprocess
import tempfile
import os

APP = "app.py"
RESUME = "input/resume.pdf"


TEST_CASES = [
    {
        "name": "Happy Path",
        "csv": """name,email,phone,current_company,title
Shaik Mohammad Azaruddin,mohammadazaruddinsk@gmail.com,+919100312008,GDOT Contractor,RAG Data Intern
""",
        "checks": [
            ("full_name", "Shaik Mohammad Azaruddin"),
            ("emails", "mohammadazaruddinsk@gmail.com"),
            ("phones", "+919100312008"),
        ],
    },
    {
        "name": "Missing Company",
        "csv": """name,email,phone,current_company,title
Shaik Mohammad Azaruddin,mohammadazaruddinsk@gmail.com,+919100312008,,RAG Data Intern
""",
        "checks": [
            ("full_name", "Shaik Mohammad Azaruddin"),
            ("emails", "mohammadazaruddinsk@gmail.com"),
        ],
    },
    {
        "name": "Email Case Normalization",
        "csv": """name,email,phone,current_company,title
Shaik Mohammad Azaruddin,MOHAMMADAZARUDDINSK@GMAIL.COM,+919100312008,GDOT Contractor,RAG Data Intern
""",
        "checks": [
            ("emails", "mohammadazaruddinsk@gmail.com"),
        ],
    },
    {
        "name": "Phone Formatting",
        "csv": """name,email,phone,current_company,title
Shaik Mohammad Azaruddin,mohammadazaruddinsk@gmail.com,919100312008,GDOT Contractor,RAG Data Intern
""",
        "checks": [
            ("phones", "+919100312008"),
        ],
    },
    {
        "name": "Wrong Company Should Prefer Resume",
        "csv": """name,email,phone,current_company,title
Shaik Mohammad Azaruddin,mohammadazaruddinsk@gmail.com,+919100312008,Microsoft,RAG Data Intern
""",
        "checks": [
            ("experience_company", "GDOT Contractor"),
        ],
    },
]


def get_value(data, key):
    if key == "emails":
        return data["emails"][0]

    if key == "phones":
        return data["phones"][0]

    if key == "experience_company":
        return data["experience"][0]["company"]

    return data.get(key)


passed = 0

print("=" * 70)
print("Candidate Transformation Pipeline Tests")
print("=" * 70)

for test in TEST_CASES:

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
    ) as csv_file:

        csv_file.write(test["csv"])
        csv_path = csv_file.name

    output_path = tempfile.NamedTemporaryFile(
        suffix=".json",
        delete=False,
    ).name

    cmd = [
        "python",
        APP,
        "--resume",
        RESUME,
        "--csv",
        csv_path,
        "--output",
        output_path,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"❌ {test['name']} FAILED")
        print(result.stderr)
        continue

    with open(output_path) as f:
        data = json.load(f)

    success = True

    for field, expected in test["checks"]:

        actual = get_value(data, field)

        if actual != expected:
            success = False
            print(
                f"    {field}: expected={expected} got={actual}"
            )

    if success:
        passed += 1
        print(f"✅ {test['name']}")
    else:
        print(f"❌ {test['name']}")

    os.remove(csv_path)
    os.remove(output_path)

print()
print(f"{passed}/{len(TEST_CASES)} tests passed.")