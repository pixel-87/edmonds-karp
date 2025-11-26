from manim import *
import networkx as nx

class MaxFlowIntro(Scene):
    def construct(self):
        title = Text("Maximum Flow Problem").scale(0.8)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        
        # Define graph structure
        vertices = [1, 2, 3, 4, 5, 6]
        edges = [
            (1, 2), (1, 3),
            (2, 4), (2, 5),
            (3, 5), (3, 4),
            (4, 6), (5, 6)
        ]
        
        layout = {
            1: [-4, 0, 0],  # S
            2: [-1, 2, 0],
            3: [-1, -2, 0],
            4: [2, 2, 0],
            5: [2, -2, 0],
            6: [5, 0, 0],   # T
        }
        
        # Create the graph
        g = DiGraph(
            vertices,
            edges,
            layout=layout,
            vertex_config={
                1: {"color": BLUE, "radius": 0.4},
                6: {"color": BLUE, "radius": 0.4},
            }
        )
        
        # Add labels manually
        vertex_labels = VGroup()
        vertex_labels.add(Text("S", font_size=24).next_to(g.vertices[1], DOWN, buff=0.1))
        vertex_labels.add(Text("T", font_size=24).next_to(g.vertices[6], DOWN, buff=0.1))
        
        # Add capacities (labels on edges)
        capacities = {
            (1, 2): 10, (1, 3): 10,
            (2, 4): 4, (2, 5): 8,
            (3, 5): 9, (3, 4): 2,
            (4, 6): 10, (5, 6): 10
        }
        
        edge_labels = dict()
        for edge, capacity in capacities.items():
            # Find the edge mobject
            edge_mob = g.edges[edge]
            
            # Default direction
            direction = UP * 0.2
            
            # Adjust for crossing edges to avoid overlap
            if edge == (2, 5): # Crossing down-right
                direction = UP * 0.2 + RIGHT * 0.2
            elif edge == (3, 4): # Crossing up-right
                direction = UP * 0.2 + LEFT * 0.2
                
            label = Text(str(capacity), font_size=16).move_to(edge_mob.get_center() + direction)
            edge_labels[edge] = label
            
        self.play(Create(g))
        self.play(Write(vertex_labels))
        self.play(
            *[Write(label) for label in edge_labels.values()]
        )
        self.wait()
        
        # Explain Source and Sink
        source_text = Text("Source", color=BLUE).next_to(g.vertices[1], UP)
        sink_text = Text("Sink", color=BLUE).next_to(g.vertices[6], UP)
        
        self.play(Write(source_text), Write(sink_text))
        self.play(Indicate(g.vertices[1]), Indicate(g.vertices[6]))
        self.wait()
        
        self.play(FadeOut(source_text), FadeOut(sink_text))
        
        # Visualize flow (conceptually)
        # Just highlighting a path S -> 2 -> 5 -> T
        path_edges = [(1, 2), (2, 5), (5, 6)]
        self.play(
            *[g.edges[edge].animate.set_color(YELLOW) for edge in path_edges],
            run_time=2
        )
        self.wait()
        
        explanation = Text("Goal: Send max material from S to T", font_size=24).to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(2)

class FordFulkersonBadCase(Scene):
    def construct(self):
        title = Text("The Problem with Ford-Fulkerson").scale(0.8)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))

        # Define the "Bad Case" graph
        vertices = [1, 2, 3, 4] # S, U, V, T
        edges = [
            (1, 2), (1, 3), # S->U, S->V
            (2, 3),         # U->V (The bridge)
            (2, 4), (3, 4)  # U->T, V->T
        ]
        
        layout = {
            1: [-4, 0, 0],  # S
            2: [0, 2, 0],   # U
            3: [0, -2, 0],  # V
            4: [4, 0, 0],   # T
        }
        
        g = DiGraph(
            vertices,
            edges,
            layout=layout,
            vertex_config={
                1: {"color": BLUE, "radius": 0.4},
                4: {"color": BLUE, "radius": 0.4},
            }
        )
        
        # Add labels
        vertex_labels = VGroup()
        vertex_labels.add(Text("S", font_size=24).next_to(g.vertices[1], DOWN, buff=0.1))
        vertex_labels.add(Text("U", font_size=24).next_to(g.vertices[2], UP, buff=0.1))
        vertex_labels.add(Text("V", font_size=24).next_to(g.vertices[3], DOWN, buff=0.1))
        vertex_labels.add(Text("T", font_size=24).next_to(g.vertices[4], DOWN, buff=0.1))
        
        # Capacities
        # Using a large number M
        M = 1000
        capacities = {
            (1, 2): M, (1, 3): M,
            (2, 3): 1,
            (2, 4): M, (3, 4): M
        }
        
        edge_labels = {}
        for edge, capacity in capacities.items():
            edge_mob = g.edges[edge]
            # Adjust label position slightly
            direction = UP * 0.3
            if edge == (2, 3): direction = RIGHT * 0.3
            
            label = Text(str(capacity), font_size=20).move_to(edge_mob.get_center() + direction)
            edge_labels[edge] = label

        self.play(Create(g))
        self.play(Write(vertex_labels))
        self.play(*[Write(l) for l in edge_labels.values()])
        self.wait()
        
        # Explain the trap
        # DFS might choose S -> U -> V -> T
        path1 = [(1, 2), (2, 3), (3, 4)]
        
        self.play(
            *[g.edges[edge].animate.set_color(RED) for edge in path1],
            run_time=1.5
        )
        
        info = Text("Flow +1", color=RED).to_edge(UP)
        self.play(Write(info))
        self.wait()
        
        # Reset colors
        self.play(
            *[g.edges[edge].animate.set_color(WHITE) for edge in path1],
            FadeOut(info)
        )
        
        # Explain that now U->V is full, but V->U exists in residual
        # DFS might choose S -> V -> U -> T
        # Note: In the original graph, this path doesn't exist, but in residual it does.
        # For visualization, we can just show the path on the original graph but highlight the "backwards" flow on U->V
        
        path2_edges = [(1, 3), (3, 4)] # S->V, V->T
        # The middle part is tricky to visualize without changing the graph structure
        # We can just highlight the edges involved
        
        self.play(
            g.edges[(1, 3)].animate.set_color(RED), # S->V
            g.edges[(2, 3)].animate.set_color(RED), # U->V (traversed backwards)
            g.edges[(2, 4)].animate.set_color(RED), # U->T
            run_time=1.5
        )
        
        info2 = Text("Flow +1 (using residual edge V->U)", color=RED, font_size=24).to_edge(UP)
        self.play(Write(info2))
        self.wait()
        
        self.play(
            g.edges[(1, 3)].animate.set_color(WHITE),
            g.edges[(2, 3)].animate.set_color(WHITE),
            g.edges[(2, 4)].animate.set_color(WHITE),
            FadeOut(info2)
        )
        
        # Conclusion text
        conclusion = Text(f"Takes {2*M} steps!", color=RED).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)

class EdmondsKarpSolution(Scene):
    def construct(self):
        title = Text("Edmonds-Karp Algorithm").scale(0.8)
        subtitle = Text("Uses BFS to find shortest augmenting paths", font_size=24).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait()
        self.play(FadeOut(title), FadeOut(subtitle))

        # Same graph
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
        layout = {
            1: [-4, 0, 0], 2: [0, 2, 0],
            3: [0, -2, 0], 4: [4, 0, 0],
        }
        
        g = DiGraph(
            vertices, edges,
            layout=layout,
            vertex_config={1: {"color": BLUE, "radius": 0.4}, 4: {"color": BLUE, "radius": 0.4}}
        )
        
        # Add labels
        vertex_labels = VGroup()
        vertex_labels.add(Text("S", font_size=24).next_to(g.vertices[1], DOWN, buff=0.1))
        vertex_labels.add(Text("U", font_size=24).next_to(g.vertices[2], UP, buff=0.1))
        vertex_labels.add(Text("V", font_size=24).next_to(g.vertices[3], DOWN, buff=0.1))
        vertex_labels.add(Text("T", font_size=24).next_to(g.vertices[4], DOWN, buff=0.1))
        
        M = 1000
        capacities = {
            (1, 2): M, (1, 3): M, (2, 3): 1,
            (2, 4): M, (3, 4): M
        }
        
        edge_labels = {}
        for edge, capacity in capacities.items():
            edge_mob = g.edges[edge]
            direction = UP * 0.3
            if edge == (2, 3): direction = RIGHT * 0.3
            label = Text(str(capacity), font_size=20).move_to(edge_mob.get_center() + direction)
            edge_labels[edge] = label

        self.play(Create(g))
        self.play(Write(vertex_labels))
        self.play(*[Write(l) for l in edge_labels.values()])
        self.wait()
        
        # BFS Step 1: Find shortest path
        # S -> U -> T (Length 2)
        path1 = [(1, 2), (2, 4)]
        
        self.play(
            *[g.edges[edge].animate.set_color(GREEN) for edge in path1],
            run_time=1.5
        )
        
        info1 = Text("BFS Path 1: S -> U -> T (Length 2)", color=GREEN, font_size=24).to_edge(UP)
        self.play(Write(info1))
        self.wait()
        
        # Show flow added
        flow_text = Text(f"Flow += {M}", color=GREEN).next_to(info1, DOWN)
        self.play(Write(flow_text))
        self.wait()
        
        self.play(
            *[g.edges[edge].animate.set_color(WHITE) for edge in path1],
            FadeOut(info1), FadeOut(flow_text)
        )
        
        # BFS Step 2: Find shortest path in residual
        # S -> V -> T (Length 2)
        # Note: S->U is full, U->T is full.
        # But wait, S->U->T pushed 1000.
        # S->U cap is 1000, so it's full.
        # U->T cap is 1000, so it's full.
        # So S->U and U->T are removed from residual graph.
        # Remaining path: S -> V -> T.
        
        path2 = [(1, 3), (3, 4)]
        self.play(
            *[g.edges[edge].animate.set_color(GREEN) for edge in path2],
            run_time=1.5
        )
        
        info2 = Text("BFS Path 2: S -> V -> T (Length 2)", color=GREEN, font_size=24).to_edge(UP)
        self.play(Write(info2))
        self.wait()
        
        flow_text2 = Text(f"Flow += {M}", color=GREEN).next_to(info2, DOWN)
        self.play(Write(flow_text2))
        self.wait()
        
        self.play(
            *[g.edges[edge].animate.set_color(WHITE) for edge in path2],
            FadeOut(info2), FadeOut(flow_text2)
        )
        
        # Conclusion
        final_text = Text("Solved in 2 steps!", color=GREEN).scale(1.2)
        self.play(Write(final_text))
        self.wait(2)
