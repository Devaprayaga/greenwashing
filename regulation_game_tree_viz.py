# regulation_game_tree_viz.py
import matplotlib.pyplot as plt
import networkx as nx

# --- Game data ---
# Nodes: name, player, payoff (None for non-terminal)
nodes = {
    "FF": {"player": "Firm", "payoff": None},
    "R_A": {"player": "Regulator", "payoff": None},
    "R_B": {"player": "Regulator", "payoff": None},
    "C_A": {"player": "Terminal", "payoff": (60, 45)},
    "D_A": {"player": "Terminal", "payoff": (60, 50)},
    "C_B": {"player": "Terminal", "payoff": (35, 60)},
    "D_B": {"player": "Terminal", "payoff": (110, -20)},
}

# Edges: (from, to, label)
edges = [
    ("FF", "R_A", "A_Genuine"),
    ("FF", "R_B", "B_Greenwash"),
    ("R_A", "C_A", "C_Audit"),
    ("R_A", "D_A", "D_Ignore"),
    ("R_B", "C_B", "C_Audit"),
    ("R_B", "D_B", "D_Ignore"),
]

# SPNE path for highlighting
spne_path = [("FF", "R_A"), ("R_A", "D_A")]

# --- Build graph ---
G = nx.DiGraph()
for node, attr in nodes.items():
    G.add_node(node, **attr)
for u, v, label in edges:
    G.add_edge(u, v, action=label)

# --- Layout ---
pos = {
    "FF": (0, 2),
    "R_A": (-1, 1),
    "R_B": (1, 1),
    "C_A": (-1.5, 0),
    "D_A": (-0.5, 0),
    "C_B": (0.5, 0),
    "D_B": (1.5, 0),
}

# --- Draw nodes ---
node_colors = []
for n in G.nodes:
    if nodes[n]["player"] == "Terminal":
        node_colors.append("lightgreen")
    else:
        node_colors.append("lightblue")  # baby-blue for decision nodes

nx.draw_networkx_nodes(G, pos, node_size=2000, node_color=node_colors)
nx.draw_networkx_labels(
    G,
    pos,
    labels={n: n if nodes[n]["payoff"] is None else f"{n}\n{nodes[n]['payoff']}" for n in G.nodes},
    font_size=10,
)

# --- Draw edges ---
edge_colors = ["red" if (u, v) in spne_path else "black" for u, v in G.edges()]
nx.draw_networkx_edges(G, pos, arrows=True, edge_color=edge_colors, width=2)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d["action"] for u, v, d in G.edges(data=True)}, font_size=9)

# --- Display ---
plt.title("Regulation vs Greenwashing: Game Tree (SPNE in red)")
plt.axis("off")
plt.tight_layout()

# Save the figure as a PNG file
plt.savefig("game_tree.png", dpi=150)
print("Saved game tree to game_tree.png")
# plt.show()  # optional in Codespaces
