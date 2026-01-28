from coding.code_runner import run_code

def evaluate_code(code, test_cases, max_marks):
    passed = 0

    for tc in test_cases:
        output = run_code(code, tc.input_data)
        if output == tc.expected_output.strip():
            passed += 1

    total = len(test_cases)
    marks = round((passed / total) * max_marks)

    return passed, total, marks
