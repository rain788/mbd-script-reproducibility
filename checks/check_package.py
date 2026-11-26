"""Recompute the reported statistics and buffer checks from the public files.

Usage:  python checks/check_package.py      (requires numpy)
"""
import csv, json, math, os, random
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
TASKS = ['T1','T2','T3','T4','T5','T6','H1','H2','H3','H4','H5','H6']

def gate(exec_, num, fid, exp):
    """Complete success requires all four acceptance gates."""
    return int(exec_ and num and fid and exp)

def trace_error(y, yref):
    """Maximum absolute deviation normalised by the peak absolute reference value."""
    return float(np.max(np.abs(y - yref)) / np.max(np.abs(yref)))

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (c - h), 100 * (c + h)

def task_weighted_diff(rows, model, a, b, n_boot=10000, seed=20261103):
    rate = lambda m: {t: np.mean([int(r['complete_success']) for r in rows if r['model'] == model and r['method'] == m and r['task'] == t]) for t in TASKS}
    ra, rb = rate(a), rate(b); per = {t: ra[t] - rb[t] for t in TASKS}
    est = 100 * np.mean(list(per.values()))
    rnd = random.Random(seed); bs = sorted(100 * np.mean([per[rnd.choice(TASKS)] for _ in TASKS]) for _ in range(n_boot))
    return est, bs[int(0.025 * n_boot)], bs[int(0.975 * n_boot)]

def check_gates():
    tests = list(csv.DictReader(open(P('results', 'controlled_study', 'checker_test_results.csv'), encoding='utf-8-sig')))
    for t in tests:
        if t['check'] == 'gate_truth_table':
            assert gate(*[int(c) for c in t['input']]) == int(t['expected'])
    print('gate truth table: %d cases consistent' % sum(t['check'] == 'gate_truth_table' for t in tests))

def check_tables():
    rows = list(csv.DictReader(open(P('results', 'controlled_study', 'runs_summary.csv'), encoding='utf-8')))
    F = [r for r in rows if r['study'] == 'formal']
    for r in F:
        assert int(r['complete_success']) == gate(*(int(r[g]) for g in ('gate_exec', 'gate_num', 'gate_fid', 'gate_exp')))
    print('formal runs:', len(F), ' ablation runs:', sum(r['study'] == 'ablation' for r in rows))
    print('calls hitting the per-call output cap:', sum(int(r['truncated_calls']) for r in rows))
    for m in ['qwen3:8b', 'qwen3:30b', 'llama3.1:8b', 'gemma3:4b']:
        k = sum(int(r['complete_success']) for r in F if r['model'] == m and r['method'] == 'proposed')
        lo, hi = wilson(k, 120)
        est, blo, bhi = task_weighted_diff(F, m, 'proposed', 'full_api_rules')
        print(f'{m:12s} proposed {k}/120 [{lo:.1f}, {hi:.1f}]  vs Full-API+Rules {est:+.1f} pp [{blo:+.1f}, {bhi:+.1f}]')

def buffer_reference(k, c, h=5e-4, T=4.0, m1=80., m2=35., kg=220e3, cg=2.2e3, F=3500.):
    """Two-DOF buffer model (SI). Returns peak stroke [mm], peak a2 [m/s2], z at T [mm], RK4 vs expm error."""
    k, c = k * 1e3, c * 1e3
    A = np.array([[0, 0, 1, 0], [0, 0, 0, 1],
                  [-k / m1, k / m1, -c / m1, c / m1],
                  [k / m2, -(k + kg) / m2, c / m2, -(c + cg) / m2]])
    b = np.array([0, 0, F / m1, 0])
    f = lambda x: A @ x + b
    n = int(round(T / h)); x = np.zeros(4); xs = [x]
    for _ in range(n):
        k1 = f(x); k2 = f(x + h / 2 * k1); k3 = f(x + h / 2 * k2); k4 = f(x + h * k3)
        x = x + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); xs.append(x)
    xs = np.array(xs); t = np.arange(n + 1) * h
    w, V = np.linalg.eig(A); xeq = -np.linalg.solve(A, b); Vi = np.linalg.inv(V)
    ex = np.array([(V @ np.diag(np.exp(w * ti)) @ Vi).real @ (-xeq) + xeq for ti in t])
    acc = np.array([f(xi) for xi in xs])
    err = np.max(np.abs(xs[:, 0] - ex[:, 0])) / np.max(np.abs(ex[:, 0]))
    return 1e3 * xs[:, 0].max(), np.abs(acc[:, 3]).max(), 1e3 * xs[-1, :2], err

def check_buffer():
    ref = {(float(r['k_N_per_mm']), float(r['c_Ns_per_mm'])): r for r in csv.DictReader(open(P('results', 'buffer_case', 'reference_solutions.csv'))) if r['output_intervals'] == '8000'}
    feas = []
    for (k, c), r in sorted(ref.items()):
        s, a2, zend, err = buffer_reference(k, c)
        zs2 = 3500 / 220; zs1 = zs2 + 3500 / k
        assert abs(s - float(r['peak_stroke_mm'])) < 1e-3, (k, c, s)
        ok = s <= 70 and a2 <= 17 and float(r['peak_force_N']) <= 6000 and 3500 / 80 <= 45
        if ok: feas.append((k, c))
        print(f'k={k:5.0f} c={c:.1f}: stroke {s:7.3f} mm, a2 {a2:6.3f} m/s2, static dev {max(abs(zend[0]-zs1), abs(zend[1]-zs2)):.1e} mm, RK4-expm {err:.1e}, feasible {ok}')
    print('reference feasible candidates (declared limits):', feas)
    adams = list(csv.DictReader(open(P('results', 'buffer_case', 'adams_nine_case_screen.csv'))))
    def feasible(stroke_lim):
        ad = [(float(r['coupling_stiffness_N_per_mm']), float(r['coupling_damping_N_s_per_mm'])) for r in adams
              if float(r['first_stage_peak_dz_mm']) <= stroke_lim and float(r['first_stage_peak_az_mm_per_s2']) / 1e3 <= 45
              and float(r['second_stage_peak_az_mm_per_s2']) / 1e3 <= 17 and float(r['peak_coupling_force_N']) <= 6000]
        rf = [key for key, r in sorted(ref.items()) if float(r['peak_stroke_mm']) <= stroke_lim and float(r['peak_a1_m_s2']) <= 45
              and float(r['peak_a2_m_s2']) <= 17 and float(r['peak_force_N']) <= 6000]
        return ad, rf
    for lim in (70, 75):
        ad, rf = feasible(lim)
        sel = lambda c: min(c, key=lambda kc: float(ref[kc]['peak_stroke_mm'])) if c else None
        print(f'stroke limit {lim} mm: Adams feasible {ad}, reference feasible {rf}, selected {sel(ad)} / {sel(rf)}')
    print('note: k=140, c=0.4 has a2 = 16.97 (Adams) vs 17.02 (reference) m/s2, on opposite sides of the 17 m/s2 limit')

if __name__ == '__main__':
    check_gates(); check_tables(); check_buffer()
