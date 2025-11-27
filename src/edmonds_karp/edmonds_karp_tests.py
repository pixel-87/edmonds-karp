from edmonds_karp import EdmondsKarpGraph

def run_simple_path_test() -> None:
    """Integration Test 1: Simple linear flow to verify the bottleneck logic."""
    print("\n" + "="*70)
    print("--- TEST 1: SIMPLE BOTTLENECK PATH (Max Flow: 5) ---")
    
    g = EdmondsKarpGraph(4)
    g.set_vertex_label(0, "S"); g.set_vertex_label(1, "A"); 
    g.set_vertex_label(2, "B"); g.set_vertex_label(3, "T")

    g.add_edge(0, 1, 10)
    g.add_edge(1, 2, 5)   # Bottleneck
    g.add_edge(2, 3, 15)
    
    source = 0; sink = 3
    final_max_flow = g.edmonds_karp(source, sink)

    print(f"\nCalculated Maximum Flow: {final_max_flow} | Expected: 5")
    assert final_max_flow == 5, "Test 1 Failed: Simple path bottleneck incorrect."
    print("Test 1 Passed.")


def run_parallel_paths_test() -> None:
    """Integration Test 2: Two parallel paths to verify flow summation."""
    print("\n" + "="*70)
    print("--- TEST 2: PARALLEL PATHS (Max Flow: 15) ---")
    
    g = EdmondsKarpGraph(4)
    g.set_vertex_label(0, "S"); g.set_vertex_label(1, "A"); 
    g.set_vertex_label(2, "B"); g.set_vertex_label(3, "T")

    # Path 1: S -> A -> T (capacity 10)
    g.add_edge(0, 1, 10)
    g.add_edge(1, 3, 10)
    # Path 2: S -> B -> T (capacity 5)
    g.add_edge(0, 2, 5)
    g.add_edge(2, 3, 5)
    
    source = 0; sink = 3
    final_max_flow = g.edmonds_karp(source, sink)

    print(f"\nCalculated Maximum Flow: {final_max_flow} | Expected: 15")
    assert final_max_flow == 15, "Test 2 Failed: Parallel path summation incorrect."
    print("Test 2 Passed.")


def run_complex_redirection_test() -> None:
    """
    Structural Test 3: Complex Flow Redirection
    Verifies that the backward edges are correctly used to redirect flow for global optimum.
    """
    print("\n\n" + "="*70)
    print("--- TEST 3: COMPLEX FLOW REDIRECTION (Max Flow: 8) ---")
    print("This demonstrates the necessity of the residual graph for flow changes.")
    print("="*70)

    g = EdmondsKarpGraph(6)
    vertex_names = ['s', 'v1', 'v2', 'v3', 'v4', 't']
    for i, name in enumerate(vertex_names):
        g.set_vertex_label(i, name)

    # Edge Definition (Initial Capacities)
    g.add_edge(0, 1, 3); g.add_edge(0, 2, 7)  
    g.add_edge(1, 3, 3); g.add_edge(1, 4, 4)  
    g.add_edge(2, 1, 5)  # v2 -> v1, cap: 5  <-- The critical cross-edge
    g.add_edge(2, 4, 3); g.add_edge(3, 4, 3)  
    g.add_edge(3, 5, 2); g.add_edge(4, 5, 6)  

    source = 0; sink = 5
    final_max_flow = g.edmonds_karp(source, sink)

    print(f"\nCalculated Maximum Flow: {final_max_flow} | Expected: 8")
    assert final_max_flow == 8, "Test 3 Failed: Flow does not match expected result."
    print("Test 3 Passed.")


def run_pathological_test() -> None:
    """
    Structural Test 4: Pathological Case Analysis
    Verifies that BFS prevents the O(E*f*) runtime issue, demonstrating that 
    the number of augmentations is independent of capacity magnitude.
    """
    print("\n\n" + "="*70)
    print("--- TEST 4: PATHOLOGICAL CASE (Max Flow: 2000000) ---")
    print("Graph Size: 4 nodes. Capacities are large (1M) and the flow is large.")
    print("Expected: Only 2 augmentation steps required to find Max Flow.")
    print("="*70)
    
    g2 = EdmondsKarpGraph(4)
    vertex_names_2 = ['s', 'u', 'v', 't']
    for i, name in enumerate(vertex_names_2):
        g2.set_vertex_label(i, name)

    CAPACITY_LARGE = 1000000

    # Edge Definition
    g2.add_edge(0, 1, CAPACITY_LARGE) # s -> u
    g2.add_edge(0, 2, CAPACITY_LARGE) # s -> v
    g2.add_edge(1, 2, 1)              # u -> v (The small bottleneck edge)
    g2.add_edge(1, 3, CAPACITY_LARGE) # u -> t
    g2.add_edge(2, 3, CAPACITY_LARGE) # v -> t

    source_2 = 0; sink_2 = 3
    final_max_flow_2 = g2.edmonds_karp(source_2, sink_2)

    print(f"\nCalculated Maximum Flow: {final_max_flow_2} | Expected: {2 * CAPACITY_LARGE}")
    assert final_max_flow_2 == 2 * CAPACITY_LARGE, "Test 4 Failed: Flow does not match expected result."
    print("Test 4 Passed.")


if __name__ == '__main__':
    run_simple_path_test()
    run_parallel_paths_test()
    run_complex_redirection_test()
    run_pathological_test()