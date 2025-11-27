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

        # Graph setup - shifted down to leave room for text at top
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
        layout = {1: [-3, -0.5, 0], 2: [0, 1.5, 0], 3: [0, -2.5, 0], 4: [3, -0.5, 0]}
        g = DiGraph(vertices, edges, layout=layout, vertex_config={1: {"color": BLUE, "radius": 0.4}, 4: {"color": BLUE, "radius": 0.4}})
        
        vertex_labels = VGroup()
        vertex_labels.add(Text("S", font_size=24).next_to(g.vertices[1], LEFT, buff=0.1))
        vertex_labels.add(Text("U", font_size=24).next_to(g.vertices[2], UP, buff=0.1))
        vertex_labels.add(Text("V", font_size=24).next_to(g.vertices[3], DOWN, buff=0.1))
        vertex_labels.add(Text("T", font_size=24).next_to(g.vertices[4], RIGHT, buff=0.1))
        
        # Use 10,000 as the large-capacity value so on-screen numbers match labels
        M = 10_000
        
        # Create edge labels - show actual numbers, highlight bottleneck specially
        edge_labels = VGroup()
        for edge in edges:
            mob = g.edges[edge]
            if edge == (2, 3):  # Bottleneck edge
                label = Text("1", font_size=20, color=RED).move_to(mob.get_center() + RIGHT * 0.3)
            else:
                # Position labels to avoid overlap
                if edge == (1, 2):
                    direction = LEFT * 0.5 + UP * 0.2
                elif edge == (1, 3):
                    direction = LEFT * 0.5 + DOWN * 0.2
                elif edge == (2, 4):
                    direction = RIGHT * 0.5 + UP * 0.2
                elif edge == (3, 4):
                    direction = RIGHT * 0.5 + DOWN * 0.2
                else:
                    direction = UP * 0.5
                label = Text("10000", font_size=18).move_to(mob.get_center() + direction)
            edge_labels.add(label)

        self.play(Create(g), Write(vertex_labels))
        self.play(Write(edge_labels))
        
        # Highlight the bottleneck
        bottleneck_highlight = Text("Bottleneck = 1", font_size=22, color=RED).to_corner(UL)
        self.play(Write(bottleneck_highlight))
        self.play(Indicate(g.edges[(2,3)], color=RED))
        self.wait()

        # --- Augmentation 1: S -> U -> V -> T ---
        path1 = [(1, 2), (2, 3), (3, 4)]
        
        # Show flow counter in bottom right
        flow_box = VGroup()
        flow_label = Text("Total Flow:", font_size=24)
        flow_value = Text("0", font_size=32, color=YELLOW)
        flow_box.add(flow_label, flow_value).arrange(RIGHT, buff=0.2)
        # Place the flow box to the right of the graph to avoid overlap
        flow_box.next_to(g, RIGHT, buff=0.6)
        self.play(Write(flow_box))
        
        # Show path info at top
        aug1_text = Text("DFS finds path: S → U → V → T", color=RED, font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(aug1_text))
        self.play(*[g.edges[e].animate.set_color(RED) for e in path1])
        self.play(Indicate(g.edges[(2,3)], color=RED, scale_factor=1.5)) # Indicate bottleneck
        self.wait(0.5)
        
        # Show the flow being pushed with +1
        plus_one = Text("+1", color=GREEN, font_size=40).next_to(flow_value, UP)
        new_flow = Text("1", font_size=32, color=YELLOW).move_to(flow_value)
        self.play(Write(plus_one))
        self.play(Transform(flow_value, new_flow), FadeOut(plus_one))
        self.wait(0.5)
        
        # Reset path colors
        self.play(*[g.edges[e].animate.set_color(WHITE) for e in path1], FadeOut(aug1_text))

        # --- Augmentation 2: S -> V -> U -> T (uses residual edge) ---
        path2_forward = [(1, 3), (2, 4)]
        path2_backward = g.edges[(2, 3)]
        
        aug2_text = Text("DFS finds path: S → V → U → T", color="#FF00FF", font_size=26).to_edge(UP, buff=0.3)
        residual_note = Text("(uses residual capacity)", color="#FF00FF", font_size=20).next_to(aug2_text, DOWN)
        self.play(Write(aug2_text), Write(residual_note))

        # Animate path - show backward traversal on the bottleneck edge
        self.play(
            g.edges[(1, 3)].animate.set_color("#FF00FF"),
            g.edges[(2, 4)].animate.set_color("#FF00FF"),
        )
        # Show the residual edge going backwards with a dashed style hint
        self.play(Indicate(path2_backward, color="#FF00FF", scale_factor=1.5))
        self.wait(0.5)
        
        # Show the flow being pushed with +1
        plus_one_2 = Text("+1", color=GREEN, font_size=40).next_to(flow_value, UP)
        new_flow_2 = Text("2", font_size=32, color=YELLOW).move_to(flow_value)
        self.play(Write(plus_one_2))
        self.play(Transform(flow_value, new_flow_2), FadeOut(plus_one_2))
        self.wait(0.5)
        
        # Reset
        self.play(
            g.edges[(1, 3)].animate.set_color(WHITE),
            g.edges[(2, 4)].animate.set_color(WHITE),
            FadeOut(aug2_text), FadeOut(residual_note)
        )

        # --- Conclusion ---
        self.play(FadeOut(bottleneck_highlight))
        
        # Top conclusion text
        top_conclusion = VGroup()
        line1 = Text("Each augmentation only adds +1 flow", color=YELLOW, font_size=26)
        line2 = Text("because of the tiny bottleneck!", color=YELLOW, font_size=26)
        top_conclusion.add(line1, line2).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.4)
        
        # Bottom conclusion text (spaced away from graph)
        line3 = Text(f"This alternating pattern repeats {M:,} times per side,", font_size=24)
        line4 = Text(f"≈{2*M:,} augmentations total.", color=RED, font_size=32)
        # place the bottom text slightly above the bottom edge so it stays visible
        line3.to_edge(DOWN, buff=0.6)
        line4.next_to(line3, DOWN, buff=0.15)

        self.play(Write(line1))
        self.play(Write(line2))
        self.wait(0.5)
        self.play(Write(line3))
        self.play(Write(line4))
        self.wait(2)


class EdmondsKarpSolution(Scene):
    def construct(self):
        title = Text("Edmonds-Karp: The BFS Fix").scale(0.8)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))

        # Same graph setup
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
        layout = {1: [-4, 0, 0], 2: [0, 2, 0], 3: [0, -2, 0], 4: [4, 0, 0]}
        g = DiGraph(vertices, edges, layout=layout, vertex_config={1: {"color": BLUE, "radius": 0.4}, 4: {"color": BLUE, "radius": 0.4}})
        
        vertex_labels = VGroup()
        vertex_labels.add(Text("S", font_size=24).next_to(g.vertices[1], DOWN, buff=0.1))
        vertex_labels.add(Text("U", font_size=24).next_to(g.vertices[2], UP, buff=0.1))
        vertex_labels.add(Text("V", font_size=24).next_to(g.vertices[3], DOWN, buff=0.1))
        vertex_labels.add(Text("T", font_size=24).next_to(g.vertices[4], DOWN, buff=0.1))
        
        M = 1_000_000
        capacities = {(1, 2): M, (1, 3): M, (2, 3): 1, (2, 4): M, (3, 4): M}
        
        edge_labels = VGroup()
        label_mobjects = {}
        for edge, capacity in capacities.items():
            mob = g.edges[edge]
            direction = RIGHT * 0.6 if edge == (2,3) else UP * 0.6
            label = Text(str(capacity), font_size=20).move_to(mob.get_center() + direction)
            edge_labels.add(label)
            label_mobjects[edge] = label

        self.play(Create(g), Write(vertex_labels), Write(edge_labels))
        self.wait()
        
        # --- Augmentation 1: S -> U -> T ---
        path1 = [(1, 2), (2, 4)]
        
        aug1_text = Text("BFS finds shortest path (2 edges): S → U → T", color=GREEN, font_size=28).to_edge(UP)
        self.play(Write(aug1_text))
        self.play(*[g.edges[edge].animate.set_color(GREEN) for edge in path1], run_time=1.5)
        
        flow_text = Text(f"Flow += {M}", color=GREEN, font_size=28).next_to(aug1_text, DOWN)
        self.play(Write(flow_text))
        self.wait()
        
        # Visually saturate the path
        self.play(
            *[g.edges[edge].animate.set_color(WHITE) for edge in path1],
            FadeOut(aug1_text), FadeOut(flow_text),
            # Fade labels of saturated edges
            label_mobjects[(1,2)].animate.set_opacity(0.3),
            label_mobjects[(2,4)].animate.set_opacity(0.3)
        )
        self.wait()
        
        # --- Augmentation 2: S -> V -> T ---
        path2 = [(1, 3), (3, 4)]
        
        aug2_text = Text("Next shortest path: S → V → T", color=GREEN, font_size=28).to_edge(UP)
        self.play(Write(aug2_text))
        self.play(*[g.edges[edge].animate.set_color(GREEN) for edge in path2], run_time=1.5)
        
        flow_text2 = Text(f"Flow += {M}", color=GREEN, font_size=28).next_to(aug2_text, DOWN)
        self.play(Write(flow_text2))
        self.wait()
        
        self.play(
            *[g.edges[edge].animate.set_color(WHITE) for edge in path2],
            FadeOut(aug2_text), FadeOut(flow_text2),
            label_mobjects[(1,3)].animate.set_opacity(0.3),
            label_mobjects[(3,4)].animate.set_opacity(0.3)
        )
        
        # --- Conclusion ---
        final_text = Text("Max Flow Found in 2 Steps!", color=GREEN).scale(1.2)
        self.play(Write(final_text))
        self.wait(2)
