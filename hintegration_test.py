import subprocess
import sys
from typing import TextIO, Optional

import time

from tqdm import tqdm

all_test_programs = {
    'code/prog1.hny': {},
    'code/prog2.hny': {
        'lines_to_check': [0, 1, -2]
    },
    'code/Up.hny': {},
    'code/UpEnter.hny': {
        'lines_to_check': [0, 1, 2]
    },
    'code/csbarebones.hny': {},
    'code/cs.hny': {},
    'code/naiveLock.hny': {},
    'code/naiveFlags.hny': {},
    'code/naiveTurn.hny': {},
    'code/Peterson.hny': {},
    'code/PetersonInductive.hny': {},
    'code/csonebit.hny': {},
    'code/PetersonMethod.hny': {},
    'code/spinlock.hny': {},
    'code/csTAS.hny': {},
    'code/UpLock.hny': {},
    '-msynch=synchS code/UpLock.hny': {},
    'code/xy.hny': {
        'lines_to_check': [0, 1]
    },
    'code/atm.hny': {
        'lines_to_check': [0, 1]
    },
    'code/queuedemo.hny': {
        'lines_to_check': [0, 1, 2]
    },
    '-msynch=synchS code/queuedemo.hny': {
        'lines_to_check': [0, 1, 2]
    },
    'code/qtestseq.hny': {},
    'code/qtest1.hny': {},
    '-msynch=synchS code/qtest1.hny': {},
    'code/qtest2.hny': {},
    '-msynch=synchS code/qtest2.hny': {},
    'code/qtest4.hny': {},
    '-mqueue=queueMS code/queuedemo.hny': {
        'lines_to_check': [0, 1, 2]
    },
    '-mqueue=queueMS -msynch=synchS code/queuedemo.hny': {
        'lines_to_check': [0, 1, 2]
    },
    'code/lltest.hny': {},
    '-msynch=synchS code/lltest.hny': {},
    'code/RWtest.hny': {},
    '-msynch=synchS code/RWtest.hny': {},
    '-mRW=RWsbs code/RWtest.hny': {},
    '-mRW=RWsbs -msynch=synchS code/RWtest.hny': {},
    '-mRW=RWfair code/RWtest.hny': {},
    '-mRW=RWfair -msynch=synchS code/RWtest.hny': {},
    'code/BBhoaretest.hny': {},
    '-msynch=synchS code/BBhoaretest.hny': {},
    '-mRW=RWcv code/RWtest.hny': {},
    '-mRW=RWcv -msynch=synchS code/RWtest.hny': {},
    'code/qsorttest.hny': {},
    'code/Diners.hny': {},
    '-msynch=synchS code/Diners.hny': {},
    'code/DinersAvoid.hny': {},
    'code/bank.hny': {},
    'code/counter.hny': {},
    'code/qbarrier.hny': {},
    '-msynch=synchS code/qbarrier.hny': {},
    'code/barriertest.hny': {},
    '-msynch=synchS code/barriertest.hny': {},
    'code/trap.hny': {},
    'code/trap2.hny': {},
    'code/trap3.hny': {},
    'code/trap4.hny': {},
    'code/trap5.hny': {},
    'code/trap6.hny': {},
    '-msynch=synchS code/trap6.hny': {},
    'code/hw.hny': {},
    'code/abptest.hny': {},
}

def load_results(f: TextIO):
    state = 'header'
    results = {}
    average_duration = None
    expected_output = None
    harmony_args = None

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
                    results[harmony_args] = {
                        'expected_output': expected_output,
                        'average_duration': average_duration
                    }

                harmony_args = None
                expected_output = None

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


def dump_results(results, f: TextIO):
    f.write('# Integration Test Results\n')
    f.write('\n')

    for (args_name, entry) in results.items():
        f.write('---')
        f.write('\n')
        f.write(f'### {args_name}\n')
        f.write('\n')
        f.write(f'Average duration: {entry["average_duration"]}\n')
        f.write('\n')
        f.write('Expected output:\n')
        f.write('```\n')
        for line in entry['expected_output'].splitlines():
            line = line.strip()
            f.write(line + '\n')
        f.write('```\n')
        f.write('\n')

    f.write('---')


def evaluate_current_results(n=1):
    curr_results = {}

    for args in tqdm(all_test_programs, leave=False, ncols=70):
        durations = []
        for _ in range(n):
            start_time = time.time()
            subprocess.run(f'harmony {args}'.split(), capture_output=True)
            durations.append(time.time() - start_time)
        average_duration = sum(durations) / len(durations)

        result = subprocess.run(
            f'harmony {args}'.split(),
            capture_output=True,
            encoding='utf8')

        assert type(result.stdout) == str

        curr_results[args] = {
            'expected_output': result.stdout,
            'average_duration': average_duration
        }

    return curr_results


def match_expected_output(prev, curr, lines_to_check:Optional[list[int]]=None, **kwargs):
    if lines_to_check:
        prev_split = prev['expected_output'].splitlines()
        curr_split = curr['expected_output'].splitlines()

        # print(f'Checking: {lines_to_check}')
        for line in lines_to_check:
            if line >= len(prev_split) or line >= len(curr_split):
                return False
            if prev_split[line] != curr_split[line]:
                return False

        return True

    else:
        return prev['expected_output'] == curr['expected_output']


def merge_results(prev_results, curr_results):
    # The merge process biases towards keeping the final results equal to the
    # prev results.

    final_results = {}
    for harmony_args in prev_results:
        if harmony_args not in curr_results:
            print(f'"{harmony_args}" is missing from current results.')
            if input('Include in final results? [Y/n]') != 'n':
                final_results[harmony_args] = prev_results[harmony_args]
            print()

    for harmony_args in curr_results:
        if harmony_args not in prev_results:
            print(f'"{harmony_args}" is new in current results.')
            if input('Include in final results? [y/N]') == 'y':
                final_results[harmony_args] = curr_results[harmony_args]
            print()

    # merge expected output
    for harmony_args in curr_results.keys() | prev_results.keys():
        if harmony_args not in curr_results or harmony_args not in prev_results:
            continue

        prev = prev_results[harmony_args]
        curr = curr_results[harmony_args]
        final = {
            'expected_output': prev['expected_output'],
            'average_duration': prev['average_duration']
        }

        # merge expected output
        if not match_expected_output(prev, curr, **all_test_programs[harmony_args]):
            print(f'{harmony_args}: difference on expected_output')
            print('Previous results expected output:')
            print('```')
            print(prev['expected_output'])
            print('```')
            print('Current results expected output:')
            print('```')
            print(curr['expected_output'])
            print('```')
            if input('Take current expected output? [y/N]: ') == 'y':
                final['expected_output'] = curr['expected_output']
                print('Taking current expected output')
            else:
                print('Leaving previous expected output')
            print()

        # notify of any differences in average duration
        if prev['average_duration'] and curr['average_duration']:
            percent_difference = 2 * (abs(prev['average_duration'] - curr['average_duration'])
                                       / (prev['average_duration'] + curr['average_duration']))

            if percent_difference > 100:
                print(f'{harmony_args}: difference on average duration by {round(100 * percent_difference, 3)}% > 100%')
                print(f'Previous duration: {prev["average_duration"]}')
                print(f'Current duration: {curr["average_duration"]}')
                print()

        elif not prev['average_duration'] and curr['average_duration']:
            final['average_duration'] = curr['average_duration']

        final_results[harmony_args] = final

    return final_results


def main():
    subprocess.run('make all'.split())
    print()

    if '--full' in sys.argv:
        curr_results = evaluate_current_results(n=10)
    else:
        curr_results = evaluate_current_results(n=1)

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
