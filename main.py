from manim import *
import networkx as nx

class MaxFlowIntro(Scene):
    def construct(self):
        title = Text("Maximum Flow Problem").scale(0.8)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        
        # TODO: Visualize a flow network
        # TODO: Explain Source and Sink

class FordFulkersonBadCase(Scene):
    def construct(self):
        title = Text("The Problem with Ford-Fulkerson").scale(0.8)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))

        # TODO: Show the graph with a small bottleneck
        # TODO: Animate the slow convergence

class EdmondsKarpSolution(Scene):
    def construct(self):
        title = Text("Edmonds-Karp Algorithm").scale(0.8)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))

        # TODO: Show how BFS solves the bottleneck issue
