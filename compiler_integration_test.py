import subprocess
import sys
import time
import pathlib
import dataclasses
from typing import List, Optional, Set, TextIO, Union
import re


@dataclasses.dataclass
class TestCase:
    filename: str
    harmony_args: List[str] = None
    lines_to_check: Union[List[int], str] = 'all'
    is_ephemeral: bool = False

@dataclasses.dataclass
class ExecutionResult:
    output: str
    average_duration: float

@dataclasses.dataclass
class TestResult:
    test_case: TestCase
    current: ExecutionResult
    baseline: ExecutionResult

@dataclasses.dataclass
class ComparisonResult:
    test_result: TestResult
    output_expected: bool
    duration_expected: bool

def load_test_cases() -> List[TestCase]:
    modules_dir = pathlib.Path("harmony_model_checker") / "modules"
    runall_script = pathlib.Path("runall.scr")
    code_dir = pathlib.Path("code")

    test_cases: List[TestCase] = []

    # Ensure our modules compile correctly
    tested_files: Set[str] = set()
    for f in modules_dir.glob("*.hny"):
        tested_files.add(str(f.resolve()))
        test_cases.append(TestCase(filename=str(f)))

    with runall_script.open("r") as f:
        # Exclude the first arg, i.e. the harmony script filename
        all_tc = [l.strip().split() for l in f.readlines() if l.startswith("./harmony")]
        for tc in all_tc:
            filename = pathlib.Path(tc[-1])
            if filename.exists():
                tested_files.add(str(filename.resolve()))
                test_cases.append(TestCase(
                    filename=str(filename),
                    harmony_args=tc[1:-1]
                ))

    for f in code_dir.glob("*.hny"):
        if str(f.resolve()) not in tested_files and f.exists():
            tested_files.add(str(f.resolve()))
            test_cases.append(TestCase(filename=str(f)))
    
    return test_cases

TEST_CASES = load_test_cases()
print(f"Number of tests: {len(TEST_CASES)}")

def dump_result(result: ComparisonResult, f: TextIO):
    test_case = result.test_result.test_case
    baseline = result.test_result.baseline
    current = result.test_result.current

    f.write('---')
    f.write('\n')
    f.write(f'## {" ".join(test_case.harmony_args or [])} {test_case.filename}\n')
    f.write('\n')
    f.write("### Summary\n\n")
    f.write(f"Duration is good: {'✅' if result.duration_expected else '❌'}\n\n")
    f.write(f"Output is good: {'✅' if result.output_expected else '❌'}\n\n")

    f.write("### Baseline Output\n\n")
    f.write(f"```\n{baseline.output}```\n\nDuration: {baseline.average_duration}\n\n")

    f.write("### Current Output\n\n")
    f.write(f"```\n{current.output}```\n\nDuration: {current.average_duration}\n\n")

def dump_results(results: List[ComparisonResult], f: TextIO):
    f.write('# Compiler Integration Test Results\n')
    f.write('\n')

    for r in results:
        dump_result(r, f)

    f.write('---')


def evaluate_test_case(test_case: TestCase, n: int) -> TestResult:
    harmony_args = ' '.join(test_case.harmony_args or [])
    filename = test_case.filename
    print(f'Evaluating `harmony {harmony_args} {filename}`')

    durations = []
    baseline_durations = []
    for _ in range(n):
        start_time = time.process_time()
        result = subprocess.run(
            f'harmony {harmony_args} {filename}'.split(),
            capture_output=True,
            encoding='utf8'
        )
        durations.append(time.process_time() - start_time)
        
        start_time = time.process_time()
        baseline_result = subprocess.run(
            f'python harmony.py {harmony_args or ""} {filename}'.split(),
            capture_output=True,
            encoding='utf8'
        )
        baseline_durations.append(time.process_time() - start_time)

    assert isinstance(result.stdout, str) and isinstance(baseline_result.stdout, str)

    average_duration = sum(durations) / len(durations)
    average_baseline_duration = sum(baseline_durations) / len(baseline_durations)

    stdout = result.stdout.strip()
    match = re.search("#states (\\d+) \\(time.*?\\)", stdout)
    if match is not None:
        states = match[1]
        stdout = stdout.replace(match[0], f"#states ({states})", 1)
    current_execution = ExecutionResult(stdout, average_duration)

    stdout = baseline_result.stdout.strip()
    match = re.search("#states (\\d+) \\(time.*?\\)", stdout)
    if match is not None:
        states = match[1]
        stdout = stdout.replace(match[0], f"#states ({states})", 1)
    baseline_execution = ExecutionResult(stdout, average_baseline_duration)

    return TestResult(
        test_case=test_case,
        current=current_execution,
        baseline=baseline_execution
    )


def evaluate_and_compare_test_cases(test_cases: List[TestCase], n: int) -> List[ComparisonResult]:
    curr_results = []

    for test_case in test_cases:
        tr = evaluate_test_case(test_case, n)
        curr_results.append(compare_result(tr))
    return curr_results


def expected_outputs_match(
    test_case: TestCase,
    prev_expected_output: str,
    curr_expected_output: str
) -> bool:

    if isinstance(test_case.lines_to_check, list):
        assert test_case.lines_to_check != []

        prev_split = prev_expected_output.splitlines()
        curr_split = curr_expected_output.splitlines()

        for line in test_case.lines_to_check:
            assert isinstance(line, int)

            if line >= len(prev_split) or line >= len(curr_split):
                return False
            if prev_split[line] != curr_split[line]:
                return False

        if prev_expected_output != curr_expected_output:
            print(
                f'{" ".join(test_case.harmony_args or [])}: Previous and current expected '
                f'outputs differ, but merge has been suppressed by '
                f'test_case.lines_to_check'
            )
            print()

        return True

    elif test_case.lines_to_check == 'all':
        return prev_expected_output == curr_expected_output

    else:
        assert False


def merge_expected_outputs(
    result: TestResult
) -> bool:

    test_case = result.test_case
    prev = result.baseline.output
    curr = result.current.output

    if expected_outputs_match(
        test_case,
        prev,
        curr
    ):
        return True

    print(f'{" ".join(test_case.harmony_args or [])}: difference on expected_output')
    print('Previous results expected output:')
    print('```')
    print(prev, end='')
    print('```')
    print('Current results expected output:', end='')
    print('```')
    print(curr)
    print('```')

    if input('Are the outputs satisfactory? [y/N]: ') == 'y':
        print('Accepting the current output')
        print()
        return True

    else:
        print('Output is not satisfactory')
        print()
        return False


def merge_average_durations(
    result: TestResult,
) -> bool:

    test_case = result.test_case
    prev = result.baseline.average_duration
    curr = result.current.average_duration

    if prev == curr:
        return True

    percent_difference = 2 * (abs(prev - curr) / (prev + curr))

    percent_difference = round(100 * percent_difference, 3)

    if percent_difference <= 100:
        return True

    print(f'{" ".join(test_case.harmony_args or [])}: difference on average duration by {percent_difference}% > 100%')
    print(f'Previous duration: {prev}')
    print(f'Current duration: {curr}')
    print()
    if input('Take current average duration? [y/N]: ') == 'y':
        print('Taking current average duration')
        print()
        return True

    else:
        print('Leaving previous average duration')
        print()
        return False


def compare_result(
    result: TestResult
) -> ComparisonResult:
    output_is_expected = merge_expected_outputs(result)
    duration_is_expected = merge_average_durations(result)

    return ComparisonResult(
        test_result=result,
        output_expected=output_is_expected,
        duration_expected=duration_is_expected
    )


def main():
    subprocess.run('make all'.split())
    print()

    if '--full' in sys.argv:
        final_results = evaluate_and_compare_test_cases(TEST_CASES, n=10)
    else:
        final_results = evaluate_and_compare_test_cases(TEST_CASES, n=1)
    print()

    with open('compiler_integration_results.md', 'w') as f:
        dump_results(final_results, f)


if __name__ == '__main__':
    main()
