#!/usr/bin/env python3
"""End-to-end test runner for the stage compiler.

Each NAME.py in the tests directory is both the test input and its own
oracle: the expected output is what CPython prints for it, the actual output
is what the compiled binary prints.  A test passes when the two agree.

NAME.in, when present, is fed to both runs as stdin.

The tests directory is tests/ unless --tests-dir names another one, so that a
compiler for a larger language (loops.py) can have its own programs.
"""
import argparse
import os
import subprocess
import sys

DEFAULT_TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(DEFAULT_TESTS_DIR)
RUNTIME = os.path.join(PROJECT_DIR, 'runtime.c')

# Not test cases: the input_int shim CPython needs, and this runner.
EXCLUDED = {'runtime.py', 'run_tests.py'}

TIMEOUT = 30


class Failure(Exception):
    """A test did not pass; the message says why."""


def discover(tests_dir: str, pattern: str | None) -> list[str]:
    names = sorted(f[:-3] for f in os.listdir(tests_dir)
                   if f.endswith('.py') and f not in EXCLUDED)
    if pattern:
        names = [n for n in names if pattern in n]
    return names


def stdin_for(tests_dir: str, name: str) -> bytes:
    path = os.path.join(tests_dir, name + '.in')
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f.read()
    return b''


def run(cmd: list[str], stdin: bytes, cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, input=stdin, cwd=cwd, timeout=TIMEOUT,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def expected_output(tests_dir: str, name: str, stdin: bytes) -> str:
    """Run the test program under CPython.  Run from the tests directory so
    that 'from runtime import input_int' resolves to its runtime.py."""
    proc = run([sys.executable, name + '.py'], stdin, tests_dir)
    if proc.returncode != 0:
        raise Failure(f"CPython could not run the test program:\n"
                      f"{proc.stderr.decode(errors='replace').strip()}")
    return proc.stdout.decode()


def interpreted_output(tests_dir: str, name: str, stdin: bytes, compiler: str,
                       after: str | None) -> str:
    """Compile, then run the result under the x86 interpreter.

    No gcc, no linker, no binary -- and with --interp-after it runs a program
    from the middle of the back end, where the operands may still be
    Variables.  That is what localises a miscompilation to one pass."""
    source = os.path.join(tests_dir, name + '.py')
    cmd = [sys.executable, compiler, source, '--interp']
    if after:
        cmd = [sys.executable, compiler, source, '--interp-after', after]
    proc = run(cmd, stdin, PROJECT_DIR)
    if proc.returncode != 0:
        raise Failure(f"interpreter failed:\n{tail(proc.stderr)}")
    return proc.stdout.decode()


def actual_output(tests_dir: str, name: str, stdin: bytes, compiler: str) -> str:
    """Compile, assemble, link and run the test program."""
    source = os.path.join(tests_dir, name + '.py')
    asm = os.path.join(build_dir(tests_dir), name + '.s')
    binary = os.path.join(build_dir(tests_dir), name)

    proc = run([sys.executable, compiler, source, '-o', asm], b'', PROJECT_DIR)
    if proc.returncode != 0:
        raise Failure(f"compiler failed:\n{tail(proc.stderr)}")

    proc = run(['gcc', '-g', '-o', binary, asm, RUNTIME,
                '-Wl,-z,noexecstack'], b'', PROJECT_DIR)
    if proc.returncode != 0:
        raise Failure(f"assembler/linker failed:\n{tail(proc.stderr)}")

    proc = run([binary], stdin, tests_dir)
    if proc.returncode != 0:
        raise Failure(f"compiled program exited with {proc.returncode}\n"
                      f"{tail(proc.stderr)}")
    return proc.stdout.decode()


def tail(stderr: bytes, lines: int = 4) -> str:
    text = stderr.decode(errors='replace').strip().splitlines()
    return '\n'.join('    ' + line for line in text[-lines:])


def build_dir(tests_dir: str) -> str:
    return os.path.join(tests_dir, 'build')


def check(tests_dir: str, name: str, compiler: str, args) -> None:
    stdin = stdin_for(tests_dir, name)
    expected = expected_output(tests_dir, name, stdin)
    if args.interp or args.interp_after:
        actual = interpreted_output(tests_dir, name, stdin, compiler,
                                    args.interp_after)
    else:
        actual = actual_output(tests_dir, name, stdin, compiler)
    if expected != actual:
        raise Failure(f"expected {expected.split()!r}, got {actual.split()!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-k', dest='pattern', default=None,
                        help="only run tests whose name contains PATTERN")
    parser.add_argument('--compiler', default='if1.py',
                        help="compiler script relative to the project directory")
    parser.add_argument('--tests-dir', default=DEFAULT_TESTS_DIR,
                        help="directory of test programs (default: tests/)")
    parser.add_argument('--interp', action='store_true',
                        help="run the compiled program under the x86 "
                             "interpreter instead of assembling and linking")
    parser.add_argument('--interp-after', metavar='PASS', default=None,
                        help="interpret each program as it stands after PASS "
                             "(implies --interp)")
    args = parser.parse_args()

    tests_dir = os.path.abspath(args.tests_dir)
    if not (args.interp or args.interp_after):
        os.makedirs(build_dir(tests_dir), exist_ok=True)
    names = discover(tests_dir, args.pattern)
    if not names:
        print("no tests matched")
        return 1

    failed = []
    width = max(len(n) for n in names)
    for name in names:
        try:
            check(tests_dir, name, args.compiler, args)
        except Failure as e:
            failed.append(name)
            print(f"FAIL {name:<{width}}  {e}")
        except subprocess.TimeoutExpired:
            failed.append(name)
            print(f"FAIL {name:<{width}}  timed out after {TIMEOUT}s")
        else:
            print(f"pass {name}")

    print(f"\n{len(names) - len(failed)}/{len(names)} passed")
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
