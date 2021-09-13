import subprocess
import timeit
from tqdm import tqdm

benchmark_filenames = [
    ('choose', 10),
    ('diners', 10)
]


def build_harmony():
    subprocess.run(['make', 'all'], cwd='..')
    print()


def compile_programs():
    for (filename, _) in tqdm(benchmark_filenames, leave=False, desc='Compile Programs'):
        tqdm.write(f'Compiling {filename}')
        subprocess.run(['../harmony', f'{filename}.hny'], stdout=subprocess.DEVNULL)

    print()


def run_benchmarks():
    for (filename, num_iters) in tqdm(benchmark_filenames, position=0, desc='Run Benchmarks', leave=False):
        setup = '''
import subprocess
        '''
        stmt = f'''
subprocess.run(['../charm.exe', '{filename}.hvm'], stdout=subprocess.DEVNULL)
        '''

        times = []
        for i in tqdm(range(num_iters), desc=filename, leave=False):
            time = timeit.timeit(stmt, setup, number=1)
            times.append(time)

        mean = sum(times) / num_iters
        variance = sum([(time - mean) ** 2 for time in times]) / num_iters

        tqdm.write(','.join([filename, str(mean), str(variance)]))

if __name__ == '__main__':
    build_harmony()
    compile_programs()
    run_benchmarks()
            
    
