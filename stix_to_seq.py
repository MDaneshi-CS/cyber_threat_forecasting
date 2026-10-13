import networkx as nx
import numpy as np

def build_attack_graph(edges):
    """
    Constructs a directed graph representation of multi-source attack paths using NetworkX.
    """
    G = nx.DiGraph()
    for source, target, timestamp in edges:
        G.add_edge(source, target, timestamp=timestamp)
    
    print(f"[+] Built directed attack graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

def tokenize_attack_sequence(attack_path, context_attrs):
    """
    Converts attack graphs into linearized token sequences mapped to MITRE ATT&CK techniques.
    Includes special tokens: [SOS], [EOS], [TACTIC_SEP], [UNK], and initial condition attributes.
    """
    host_os = context_attrs.get("host_os", "Windows")
    access_level = context_attrs.get("privilege_level", "Initial")
    
    tokens = [
        "[SOS]",
        f"[OS: {host_os}]",
        f"[ACCESS: {access_level}]"
    ]
    
    for idx, technique in enumerate(attack_path):
        if idx > 0:
            tokens.append("[TACTIC_SEP]")
        tokens.append(technique)
        
    tokens.append("[EOS]")
    return tokens

if __name__ == "__main__":
    simulated_edges = [
        ("T1190", "T1059.001", "2026-09-01T10:00:00Z"),
        ("T1059.001", "T1003.001", "2026-09-01T10:15:00Z"),
        ("T1003.001", "T1021", "2026-09-01T10:30:00Z")
    ]
    
    graph = build_attack_graph(simulated_edges)
    path_sequence = ["T1190", "T1059.001", "T1003.001", "T1021"]
    context = {"host_os": "Windows", "privilege_level": "Initial"}
    
    token_stream = tokenize_attack_sequence(path_sequence, context)
    print("\n[+] Final Generated Token Sequence:")
    print(" ".join(token_stream))

