"""
LUNAR-FUSION-OPEN-SOURCE v0.5
Coaxial Regolith Recuperator — Corrected Physical Model
"""
import numpy as np

# ---------- CONSTANTS ----------
g_moon   = 1.62          # m/s²
sigma_SB = 5.67e-8       # W/(m²·K⁴)

# ---------- REGOLITH ----------
rho_p        = 1500.0    # kg/m³ (solid)
rho_bulk     = 900.0     # kg/m³ (packed, ε = 0.40)
c_p          = 800.0     # J/(kg·K)
d_p          = 70e-6     # m  (mean particle)
eps_bed      = 0.40      # void fraction, packed
e_rest       = 0.70      # coefficient of restitution

# ---------- GEOMETRY ----------
D_core   = 0.10          # m, inner core (cold rising)
D_sleeve = 0.20          # m, outer annulus (hot falling)
t_wall   = 0.004         # m, C/SiC composite wall
L_tube   = 2.5           # m
A_core   = np.pi/4 * D_core**2
A_ann    = np.pi/4 * (D_sleeve**2 - D_core**2)

# ---------- OPERATING POINT ----------
T_hot_top = 973.0        # K  (700 °C, laser flash point)
T_cold_in = 250.0        # K  (-23 °C, ambient regolith)
eta_recup = 0.60         # recuperator effectiveness (target)

# ---------- VIBRATION ----------
f       = 30.0           # Hz  ← NOT 22 kHz 
A_amp   = 1.5e-3         # m   (1.5 mm)
omega   = 2 * np.pi * f

print("=" * 70)
print("  LUNAR-FUSION-OPEN-SOURCE v0.5 — VKGR FLUIDIZATION MODULE")
print("=" * 70)

# =====================================================================
#  1. VIBRATION REGIME
# =====================================================================
a_max = A_amp * omega**2
Gamma = a_max / g_moon

if   Gamma < 1:    regime, ok = "PACKED",       False
elif Gamma < 5:    regime, ok = "ONSET",        False
elif Gamma < 50:   regime, ok = "FLUIDIZED",    True
elif Gamma < 500:  regime, ok = "BOUNCING",     False
else:              regime, ok = "CHURNING",     False

print(f"[VIB] Frequency                : {f:>10.1f} Hz")
print(f"[VIB] Amplitude                : {A_amp*1e3:>10.2f} mm")
print(f"[VIB] Peak accel.              : {a_max:>10.1f} m/s²  ({a_max/g_moon:.1f} g_moon)")
print(f"[VIB] Froude number Γ          : {Gamma:>10.1f}")
print(f"[VIB] Regime                   : {regime}")
print(f"[VIB] Target window (5–50)     : {'PASS ✓' if ok else 'FAIL ✗ — retune f, A'}")
print("-" * 70)

# =====================================================================
#  2. GRANULAR VISCOSITY (kinetic theory, dilute/vibrated)
# =====================================================================
if ok:
    v_fluct = 0.20 * A_amp * omega
    T_gran  = v_fluct**2 / 3.0     
    mu_eff  = rho_p * d_p * np.sqrt(T_gran)   
else:
    v_fluct = 0.0
    T_gran  = 0.0
    mu_eff  = 10.0                 # packed-bed value (Pa·s)

print(f"[GRA] Fluct. velocity v'       : {v_fluct*1e3:>10.2f} mm/s")
print(f"[GRA] Granular temp. T_g       : {T_gran:>10.3e} m²/s²")
print(f"[GRA] Effective viscosity μ_eff: {mu_eff:>10.3f} Pa·s")
print("-" * 70)

# =====================================================================
#  3. MINIMUM FLUIDIZATION VELOCITY (gas-assisted, Ergun)
# =====================================================================
mu_g    = 2.0e-5         # Pa·s (kinetic theory, ~constant vs P)
rho_g   = 0.016          # kg/m³ (He at 0.1 bar, 300 K)
eps3    = eps_bed**3
one_eps = 1 - eps_bed
u_mf    = (g_moon * (rho_p - rho_g) * d_p**2 * eps3) / (150 * mu_g * one_eps)

print(f"[FLW] Gas                  : He @ 0.1 bar, 300 K")
print(f"[FLW] u_mf (Ergun)         : {u_mf*1e3:>10.3f} mm/s")
print("-" * 70)

# =====================================================================
#  4. PRODUCTION RATE — the honest calculation
# =====================================================================
m_dot_target = 10.0 / 3600.0     # kg/s = 0.00278 kg/s (pilot scale)
v_solid_needed = m_dot_target / (rho_bulk * A_ann)
t_residence = L_tube / v_solid_needed if v_solid_needed > 0 else float('inf')
annual_kg = m_dot_target * 3600 * 24 * 365 * (3 / 12)  # 25% duty cycle
annual_t  = annual_kg / 1000.0

print(f"[PRD] Target m_dot         : {m_dot_target*1000:>10.2f} g/s   ({m_dot_target*3600:.1f} kg/h)")
print(f"[PRD] Required v_solid     : {v_solid_needed*1e3:>10.3f} mm/s")
print(f"[PRD] Residence time       : {t_residence/60:>10.1f} min")
print(f"[PRD] Annual output (25% DC): {annual_t:>8.1f} t/year  ← PILOT SCALE")
print("-" * 70)

# =====================================================================
#  5. THERMAL BALANCE — recuperator reality check
# =====================================================================
T_cold_out = T_cold_in + eta_recup * (T_hot_top - T_cold_in)
T_hot_out  = T_hot_top - eta_recup * (T_hot_top - T_cold_in)

print(f"[THM] Cold in              : {T_cold_in-273.15:>10.1f} °C")
print(f"[THM] Cold out (preheated) : {T_cold_out-273.15:>10.1f} °C")
print(f"[THM] Hot in (laser flash) : {T_hot_top-273.15:>10.1f} °C")
print(f"[THM] Hot out (waste)      : {T_hot_out-273.15:>10.1f} °C")
print(f"[THM] Laser heat required  : {m_dot_target*c_p*(T_hot_top-T_cold_out)/1e3:>8.2f} kW")
print(f"[THM] Recuperated heat     : {m_dot_target*c_p*(T_cold_out-T_cold_in)/1e3:>8.2f} kW")
print("-" * 70)

# =====================================================================
#  6. ACTUATOR POWER — piezo is the wrong tool here
# =====================================================================
m_active = 50.0          # kg, active vibrating wall section
Q_factor = 20.0          # low-Q mechanical system
P_peak   = m_active * A_amp**2 * omega**3
P_active = P_peak / Q_factor

print(f"[ACT] Wall mass (active)   : {m_active:>10.1f} kg")
print(f"[ACT] P_reactive (peak)    : {P_peak/1e3:>10.2f} kW")
print(f"[ACT] P_dissipated (Q=20)  : {P_active/1e3:>10.2f} kW")
print(f"[ACT] Actuator type        : Electromagnetic shaker (30 Hz)")
print("=" * 70)

# =====================================================================
#  7. SANITY ASSERTIONS
# =====================================================================
assert ok, "Vibration regime must be FLUIDIZED (5 < Γ < 50)"
assert u_mf < v_solid_needed * 10, "Gas velocity too low for transport"
assert T_hot_out > T_cold_in, "Recuperator violates 2nd law"
assert P_active < 5000, "Actuator power exceeds pilot-class budget"
print("ALL CHECKS PASSED — v0.5 model is physically consistent.")
print("=" * 70)
