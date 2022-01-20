import subprocess
import sys
import time
from typing import List, TextIO, Optional, Union


class TestCase:

    def __init__(
        self,
        harmony_args: str,
        lines_to_check: Union[List[int], str] = 'all',
        is_ephemeral: bool = False
    ):
        self.harmony_args = harmony_args
        self.lines_to_check = lines_to_check
        self.is_ephemeral = is_ephemeral


class ExecutionResult:

    def __init__(
        self,
        test_case: TestCase,
        expected_output: str,
        average_duration: Optional[float] = None
    ):
        self.test_case = test_case
        self.expected_output = expected_output
        self.average_duration = average_duration


# negative values in lines_to_check index lines from the end of the expected
# output
TEST_CASES: List[TestCase] = [
    TestCase('code/prog1.hny'),
    TestCase('code/prog2.hny', lines_to_check=[0, 1]),
    TestCase('code/Up.hny'),
    TestCase('code/UpEnter.hny'),
    TestCase('code/csbarebones.hny'),
    TestCase('code/cs.hny'),
    TestCase('code/naiveLock.hny'),
    TestCase('code/naiveFlags.hny'),
    TestCase('code/naiveTurn.hny'),
    TestCase('code/Peterson.hny'),
    TestCase('code/PetersonInductive.hny'),
    TestCase('code/csonebit.hny'),
    TestCase('code/PetersonMethod.hny'),
    TestCase('code/spinlock.hny'),
    TestCase('code/csTAS.hny'),
    TestCase('code/UpLock.hny'),
    TestCase('-msynch=synchS code/UpLock.hny'),
    TestCase('code/xy.hny', lines_to_check=[0, 1, -1]),
    TestCase('code/atm.hny', lines_to_check=[0, 1]),
    TestCase('code/queuedemo.hny'),
    TestCase('-msynch=synchS code/queuedemo.hny'),
    TestCase('code/qtestseq.hny'),
    TestCase('code/qtest1.hny'),
    TestCase('-msynch=synchS code/qtest1.hny'),
    TestCase('code/qtest2.hny'),
    TestCase('-msynch=synchS code/qtest2.hny'),
    TestCase('code/qtest4.hny'),
    TestCase('-mqueue=queueMS code/queuedemo.hny', lines_to_check=[0, 1, 2]),
    TestCase('-mqueue=queueMS -msynch=synchS code/queuedemo.hny', lines_to_check=[0, 1, 2]),
    TestCase('code/lltest.hny'),
    TestCase('-msynch=synchS code/lltest.hny'),
    TestCase('code/RWtest.hny'),
    TestCase('-msynch=synchS code/RWtest.hny'),
    TestCase('-mRW=RWsbs code/RWtest.hny'),
    TestCase('-mRW=RWsbs -msynch=synchS code/RWtest.hny'),
    TestCase('-mRW=RWfair code/RWtest.hny'),
    TestCase('-mRW=RWfair -msynch=synchS code/RWtest.hny'),
    TestCase('code/BBhoaretest.hny'),
    TestCase('-msynch=synchS code/BBhoaretest.hny'),
    TestCase('-mRW=RWcv code/RWtest.hny'),
    TestCase('-mRW=RWcv -msynch=synchS code/RWtest.hny'),
    TestCase('code/qsorttest.hny'),
    TestCase('code/Diners.hny'),
    TestCase('-msynch=synchS code/Diners.hny'),
    TestCase('code/DinersAvoid.hny'),
    TestCase('code/bank.hny'),
    TestCase('code/counter.hny'),
    TestCase('code/qbarrier.hny'),
    TestCase('-msynch=synchS code/qbarrier.hny'),
    TestCase('code/barriertest.hny'),
    TestCase('-msynch=synchS code/barriertest.hny'),
    TestCase('code/trap.hny'),
    TestCase('code/trap2.hny'),
    TestCase('code/trap3.hny'),
    TestCase('code/trap4.hny'),
    TestCase('code/trap5.hny'),
    TestCase('code/trap6.hny'),
    TestCase('-msynch=synchS code/trap6.hny'),
    TestCase('code/hw.hny'),
    TestCase('code/abptest.hny'),
    TestCase('test/DinersVar.hny'),
]


def find_test_case(harmony_args: str) -> Optional[TestCase]:
    for test_case in TEST_CASES:
        if test_case.harmony_args == harmony_args:
            return test_case
    return None


def find_execution_result(
    execution_results: List[ExecutionResult],
    harmony_args: str
) -> Optional[ExecutionResult]:

    for execution_result in execution_results:
        if execution_result.test_case.harmony_args == harmony_args:
            return execution_result
    return None


def load_results(f: TextIO) -> List[ExecutionResult]:
    state = 'header'
    results: List[ExecutionResult] = []

    average_duration: Optional[float] = None
    expected_output: str = ''
    harmony_args: str = ''

    def init_execution_result():
        nonlocal average_duration, expected_output, harmony_args

        average_duration = None
        expected_output = ''
        harmony_args = ''

    init_execution_result()

    for line in f:
        invalid_line = False

        if state == 'header':
            line = line.strip()
            if not line:
                continue

            if line == '# Integration Test Results':
                state = 'top level'
            else:
                invalid_line = True

        elif state == 'top level':
            line = line.strip()
            if not line:
                continue

            if line == '---':
                if harmony_args and expected_output:
                    test_case = find_test_case(harmony_args) \
                        or TestCase(harmony_args=harmony_args, is_ephemeral=True)

                    if test_case.is_ephemeral:
                        print(f'Found ephemeral test case while parsing: {harmony_args}')

                    results.append(ExecutionResult(
                        test_case,
                        expected_output,
                        average_duration
                    ))

                init_execution_result()

            elif line.startswith('###'):
                harmony_args = line[3:].strip()

            elif line.startswith('Average duration:'):
                try:
                    average_duration = float(line[len('Average duration:'):].strip())
                except ValueError:
                    invalid_line = True

            elif line == 'Expected output:':
                state = 'expected output quote start'

            else:
                invalid_line = True

        elif state == 'expected output quote start':
            line = line.strip()
            if not line:
                continue

            if line == '```':
                expected_output = ''
                state = 'expected output body'
            else:
                invalid_line = True

        elif state == 'expected output body':
            if line == '```\n':
                state = 'top level'
            else:
                expected_output += line

        else:
            raise ValueError(f'Invalid parser state: {state}')

        if invalid_line:
            raise ValueError(f'Unexpected line: "{line}". Parser state: {state}')

    return results


def dump_result(result: ExecutionResult, f: TextIO):
    f.write('---')
    f.write('\n')
    f.write(f'### {result.test_case.harmony_args}\n')
    f.write('\n')
    f.write(f'Average duration: {result.average_duration}\n')
    f.write('\n')
    f.write('Expected output:\n')
    f.write('```\n')
    for line in result.expected_output.splitlines():
        line = line.strip()
        f.write(line + '\n')
    f.write('```\n')
    f.write('\n')


def dump_results(results: List[ExecutionResult], f: TextIO):
    f.write('# Integration Test Results\n')
    f.write('\n')

    process_after = []

    for test_case in TEST_CASES:
        execution_result = find_execution_result(results, test_case.harmony_args)
        if execution_result:
            dump_result(execution_result, f)

        else:
            process_after.append(execution_result)

    process_after.sort(key=lambda r: r.test_case.harmony_args)

    for execution_result in process_after:
        dump_result(execution_result, f)

    f.write('---')


def evaluate_test_case(test_case: TestCase, n: int) -> ExecutionResult:
    print(f'Evaluating `harmony {test_case.harmony_args}`')

    durations = []
    for _ in range(n):
        start_time = time.time()
        result = subprocess.run(
            f'harmony {test_case.harmony_args}'.split(),
            capture_output=True,
            encoding='utf8'
        )
        durations.append(time.time() - start_time)

    assert type(result.stdout) == str

    average_duration = sum(durations) / len(durations)

    return ExecutionResult(
        test_case,
        expected_output=result.stdout,
        average_duration=average_duration
    )


def evaluate_test_cases(test_cases: List[TestCase], n: int) -> List[ExecutionResult]:
    curr_results = []

    for test_case in test_cases:
        curr_results.append(evaluate_test_case(test_case, n))

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
                f'{test_case.harmony_args}: Previous and current expected '
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
    test_case: TestCase,
    prev: str,
    curr: str
) -> str:

    if expected_outputs_match(
        test_case,
        prev,
        curr
    ):
        return prev

    print(f'{test_case.harmony_args}: difference on expected_output')
    print('Previous results expected output:')
    print('```')
    print(prev, end='')
    print('```')
    print('Current results expected output:', end='')
    print('```')
    print(curr)
    print('```')

    if input('Take current expected output? [y/N]: ') == 'y':
        print('Taking current expected output')
        print()
        return curr

    else:
        print('Leaving previous expected output')
        print()
        return prev


def merge_average_durations(
    test_case: TestCase,
    prev: Optional[float],
    curr: Optional[float]
) -> Optional[float]:

    if prev == curr:
        return prev

    if prev and curr:
        percent_difference = 2 * (abs(prev - curr) / (prev + curr))

        percent_difference = round(100 * percent_difference, 3)

        if percent_difference <= 100:
            return prev

        print(f'{test_case.harmony_args}: difference on average duration by {percent_difference}% > 100%')
        print(f'Previous duration: {prev}')
        print(f'Current duration: {curr}')
        print()
        if input('Take current average duration? [y/N]: ') == 'y':
            print('Taking current average duration')
            print()
            return curr

        else:
            print('Leaving previous average duration')
            print()
            return prev

    elif prev and not curr:
        return prev

    else:
        return None


def merge_results(
    prev_results: List[ExecutionResult],
    curr_results: List[ExecutionResult]
) -> List[ExecutionResult]:

    # The merge process biases towards keeping the final results equal to the
    # prev results, except where noted.
    #
    # The merge process should not depend on the list of all test cases, since
    # it may be useful to merge two arbitrary results lists in the future.

    final_results: List[ExecutionResult] = []

    for prev_result in prev_results:
        harmony_args = prev_result.test_case.harmony_args

        if not find_execution_result(curr_results, harmony_args):
            print(f'"{harmony_args}" is missing from current results.')

            # This is one of the situations where we need to bias against prev
            # results, since this may occur if a test case is deleted from the
            # list above.
            if input('Include in final results? [y/N]: ') == 'y':
                final_results.append(prev_result)

            print()

    for curr_result in curr_results:
        harmony_args = curr_result.test_case.harmony_args

        prev_result = find_execution_result(prev_results, harmony_args)
        if not prev_result:
            print(f'"{harmony_args}" is new in current results.')

            if input('Include in final results? [y/N]: ') == 'y':
                final_results.append(curr_result)

            print()
            continue

        assert prev_result.test_case == curr_result.test_case
        test_case = prev_result.test_case

        final_expected_outputs = merge_expected_outputs(
            test_case,
            prev_result.expected_output,
            curr_result.expected_output
        )

        final_average_duration = merge_average_durations(
            test_case,
            prev_result.average_duration,
            curr_result.average_duration
        )

        final_results.append(ExecutionResult(
            test_case,
            final_expected_outputs,
            final_average_duration
        ))

    return final_results


def main():
    subprocess.run('make all'.split())
    print()

    if '--full' in sys.argv:
        curr_results = evaluate_test_cases(TEST_CASES, n=10)
    else:
        curr_results = evaluate_test_cases(TEST_CASES, n=1)
    print()

    try:
        with open('hintegration_results.md') as f:
            prev_results = load_results(f)
    except FileNotFoundError:
        with open('hintegration_results.md', 'w') as f:
            dump_results(curr_results, f)
        return

    final_results = merge_results(prev_results, curr_results)

    with open('hintegration_results.md', 'w') as f:
        dump_results(final_results, f)


if __name__ == '__main__':
    main()
