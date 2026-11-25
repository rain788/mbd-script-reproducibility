# Task specifications

Development tasks T1–T6 were used while the stage rules, prompts and diagnosis patterns were written. Held-out tasks H1–H6 were written after the rule library was fixed and were never used to add or edit a rule.

| Task | Set | Model parameters | Acceptance check |
|---|---|---|---|
| T1 | Dev. | SI; m = 1.0 kg, r = 0.05 m, g = (0, −9.81, 0), end = 2.0 s | Terminal position −19.62 m, abs. tol. 1e−4 m |
| T2 | Dev. | SI; m = 1.0 kg, CM at (0.12, 0, 0), Icm = 0.00036 kg·m², pivot at origin, τz = 0.02 N·m, end = 2.0 s | Terminal angle 0.02·2²/(2·0.01476) = 2.710 rad, abs. tol. 0.002 rad |
| T3 | Dev. | SI; m = 0.2 kg, r = 0.03 m, F = (0, 0, 5.0) N, end = 5.0 s | Terminal backward-difference speed 125 m/s, abs. tol. 0.02 m/s |
| T4 | Dev. | SI; m = 1.0 kg, k = 100 N/m, c = 2.0 N·s/m, F = 1.0 N, end = 2.0 s | Max. relative trace error ≤ 0.5% |
| T5 | Dev. | mm-kg-s-N; stage masses 80/35 kg, interstage 140 N/mm + 0.6 N·s/mm, isolator 220 N/mm + 2.2 N·s/mm, F = 3500 N, end = 4.0 s | Max. relative trace error ≤ 0.5% |
| T6 | Dev. | SI; m = [2.0, 1.0] kg, interstage 50 N/m + 1.0 N·s/m, to ground 100 N/m + 2.0 N·s/m, F = [10, 0] N, end = 2.0 s | Max. relative trace error ≤ 0.5% |
| H1 | Held-out | SI; pendulum m = 1.0 kg, l = 0.5 m, θ0 = 20°, Icm = 0.00036 kg·m², end = 2.0 s | Max. relative trace error ≤ 0.5% |
| H2 | Held-out | SI; double pendulum m = [1.0, 0.8] kg, l = [0.6, 0.4] m, θ0 = [20, −10]°, end = 2.0 s | Max. relative trace error ≤ 1.0% |
| H3 | Held-out | SI; m = [1.0, 2.0, 1.5] kg, ground k = [10, 20, 30] N/m, c = [1.0, 1.5, 2.0] N·s/m, couplings 0–1 (15, 0.5), 0–2 (12, 0.4), F = [3, 0, −1] N, end = 2.0 s | Max. relative trace error ≤ 0.5% |
| H4 | Held-out | SI; m = 1.0 kg, F = 1.0 N, k = 20 N/m, k3 = 200 N/m³, c = 2.0 N·s/m, end = 2.0 s | Max. relative trace error ≤ 0.5% |
| H5 | Held-out | SI; m = [1.0, 1.5, 2.0] kg, ground k = [0, 0, 60] N/m, c = [0, 0, 1.5] N·s/m, couplings 0–1 (30, 0.8), 1–2 (40, 1.0), load F = [3, 0, 0] N for 0–0.5 s and [−2, 0, 0] N for 0.5–1.0 s | Max. relative trace error ≤ 1.0% |
| H6 | Held-out | SI; four-bar, ground span 1.0 m, links [0.3, 0.8, 0.7] m, masses [0.3, 0.8, 0.7] kg, crank 30°, upper branch, τ = 0.01 N·m, end = 1.0 s | Max. relative trace error ≤ 1.0%; loop closure ≤ 1e−5 m |

Trace error = max_t |y(t) − y_ref(t)| / max_t |y_ref(t)| per channel. Reference histories are in `reference_traces/`. A run is a complete success only if it executes, passes the numerical check, preserves every task parameter (fidelity) and exports every requested history.
