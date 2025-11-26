# regulation_game_spne.py
# Simple, dependency-free construction of the two-stage regulation game
# and computation of SPNE by backward induction.

from dataclasses import dataclass

@dataclass
class Outcome:
    firm: float
    regulator: float
    label: str

# Define payoffs for terminal outcomes
# Naming: (FirmChoice, RegulatorChoice)
outcomes = {
    ("A", "C"): Outcome(firm=60,  regulator=45,  label="A_then_C"),
    ("A", "D"): Outcome(firm=60,  regulator=50,  label="A_then_D"),
    ("B", "C"): Outcome(firm=35,  regulator=60,  label="B_then_C"),
    ("B", "D"): Outcome(firm=110, regulator=-20, label="B_then_D"),
}

# Regulator's decision at each information set:
# For each firm action, regulator chooses the action with higher regulator payoff.
reg_actions = {}
for firm_action in ["A", "B"]:
    # possible regulator moves
    candidates = [("C", outcomes[(firm_action, "C")].regulator),
                  ("D", outcomes[(firm_action, "D")].regulator)]
    # pick regulator action maximizing regulator payoff (break ties by choosing 'C' first)
    best = max(candidates, key=lambda x: (x[1], x[0]))
    reg_actions[firm_action] = best[0]

# Firm anticipates regulator response and picks action maximizing firm payoff
firm_payoffs_if = {}
for firm_action in ["A", "B"]:
    reg_choice = reg_actions[firm_action]
    firm_payoffs_if[firm_action] = outcomes[(firm_action, reg_choice)].firm

best_firm_action = max(firm_payoffs_if.items(), key=lambda x: (x[1], x[0]))[0]
best_reg_action = reg_actions[best_firm_action]
spne_outcome = outcomes[(best_firm_action, best_reg_action)]

# Print results
print("Regulator strategies (best responses by subgame):")
for fa, ra in reg_actions.items():
    print(f"  If Firm chooses {fa}: Regulator chooses {ra}")

print("\nFirm's anticipated payoffs (given regulator responses):")
for fa, pf in firm_payoffs_if.items():
    print(f"  If Firm chooses {fa}: Firm payoff = {pf} (Regulator will choose {reg_actions[fa]})")

print("\nSPNE (subgame perfect equilibrium):")
print(f"  Firm action: {best_firm_action}")
print(f"  Regulator action (after that firm action): {best_reg_action}")
print(f"  Outcome: {spne_outcome.label}, Payoffs (Firm, Regulator) = ({spne_outcome.firm}, {spne_outcome.regulator})")
