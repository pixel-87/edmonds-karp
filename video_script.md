# Edmonds-Karp Video Script

Here is a drafted script based on your outline and project files.

---

### **Time Slot: 0:00 - 0:30**
*   **Section Focus:** Introduction & Thesis
*   **Visuals:** Start with your `MaxFlowIntro` Manim animation. Show the graph, the "S" and "T" labels, and the conceptual path highlight. End with a title screen.
*   **Script:**
    > "(Upbeat, engaging music starts, then fades to background)
    > There are a handful of algorithms that truly changed the world, forming the bedrock of modern infrastructure. Today, we’re looking at one of them: the Edmonds-Karp algorithm.
    >
    > At its heart, it solves the 'maximum flow' problem. Imagine this graph is a data network, a supply chain, or a system of water pipes. The problem is: what is the absolute maximum amount of 'stuff' we can send from the source (S) to the sink (T) without exceeding the capacity of any single connection?
    >
    > The first solution to this, the Ford-Fulkerson method, had a critical flaw. Edmonds-Karp fixed it with a simple, elegant change that provided a guarantee of efficiency. This is the story of that fix."

---

### **Time Slot: 0:30 - 1:30**
*   **Section Focus:** The Problem & The BFS Fix
*   **Visuals:** Run your `FordFulkersonBadCase` animation. It perfectly shows the pathological case. When you mention the BFS fix, run the `EdmondsKarpSolution` animation.
*   **Script:**
    > "So what was the problem? The original Ford-Fulkerson method works by finding *any* path with available capacity—called an augmenting path—and pushing flow through it. It repeats this until no more paths can be found.
    >
    > But what if it makes bad choices?
    >
    > *(Show `FordFulkersonBadCase` animation)*
    >
    > Look at this classic pathological case. A naive search, like Depth-First Search, might choose the path right through the middle: S-U-V-T. The bottleneck here is the edge from U to V, with a capacity of just 1. After sending 1 unit of flow, the algorithm has to use a 'residual' graph to send flow back the other way... just to find another path that adds one more unit of flow. It would take twenty thousand steps to solve this. The algorithm's runtime is dependent on the amount of flow, written as O(E * f*), which is bad news.
    >
    > The fix? Edmonds-Karp mandates using Breadth-First Search (BFS) to find the augmenting path.
    >
    > *(Show `EdmondsKarpSolution` animation)*
    >
    > BFS doesn't just find *any* path; it finds the *shortest* path in terms of the number of edges. In the same graph, BFS immediately finds the two-edge path S-U-T, sending a million units of flow. Then it finds the other two-edge path, S-V-T, sending another million.
    >
    > Two augmentations, and it's done. Simple, efficient, and guaranteed to terminate quickly."

---

### **Time Slot: 1:30 - 2:30**
*   **Section Focus:** Complexity Proof (The Mechanism)
*   **Visuals:** Simple, clean slide or animation. Show the text `O(V * E^2)`. Animate an edge being "saturated" (turning red), and then show a simple layered graph diagram where the distance from S to a node 'u' `d(s, u)` increases.
*   **Script:**
    > "So why does using BFS give us this polynomial time guarantee of O(V * E squared)? It comes down to two key ideas.
    >
    > First, every time we find an augmenting path with BFS, we saturate at least one edge, making it a bottleneck.
    >
    > Second—and this is the crucial insight—the length of the shortest path from the source to any vertex in the residual graph can only increase or stay the same.
    >
    > When an edge `(u, v)` is saturated and removed from the residual graph, the shortest path to `v` might get longer. For that same edge `(u, v)` to become a bottleneck again, flow has to be pushed *backwards* through it. This can only happen if a new path to `u` is found, and it can be proven that this process forces the total path length to grow.
    >
    > Since the path length can't exceed the number of vertices (V), and each edge can only become a bottleneck a limited number of times, the total number of augmentations is bounded by V times E. Since each BFS takes O(E) time, we get our final complexity: O(V * E squared)."

---

### **Time Slot: 2:30 - 4:00**
*   **Section Focus:** Code Demonstration
*   **Visuals:** Screen recording of your terminal. First, have `src/edmonds_karp/edmonds_karp.py` open. Then, run `python src/edmonds_karp/edmonds_karp_tests.py`.
*   **Script:**
    > "Let's see this in code. Here is my Python implementation.
    >
    > *(Show `edmonds_karp.py` file, highlight the `bfs` function)*
    >
    > The whole process starts with the `bfs` function. Its only job is to find the shortest augmenting path from the source to the sink in the current residual graph. It uses a queue, just like a standard BFS, and keeps track of the path using this `parent` array. It returns `True` if a path is found, and `False` otherwise.
    >
    > *(In the same file, highlight the `edmonds_karp` main loop)*
    >
    > The main `edmonds_karp` function loops as long as BFS finds a path. Inside, it does three things. First, it walks backwards from the sink to find the bottleneck capacity—the minimum flow of the path we just found.
    >
    > *(Highlight the `path_flow` calculation)*
    >
    > Second, it adds that path's flow to our `max_flow` total.
    >
    > *(Highlight the residual graph update lines)*
    >
    > And third, it updates the residual graph. It subtracts the flow from the forward edges and, crucially, adds that capacity to the *backward* edges, allowing the algorithm to 'change its mind' about flow direction later if needed.
    >
    > *(Switch to terminal, run the tests)*
    >
    > Now, let's run it. Here are my tests. Test 3 shows a complex network where flow redirection is necessary. You can see it finds three different paths, including rerouting flow, to arrive at the correct maximum of 8.
    >
    > *(Let the output for Test 3 show clearly)*
    >
    > And here is Test 4, the pathological case we animated earlier. Just as we saw, it finds the two short, high-capacity paths immediately, solving for a max flow of two million in just two steps.
    >
    > *(Let the output for Test 4 show clearly)*"

---

### **Time Slot: 4:00 - 4:45**
*   **Section Focus:** Real-World Impact
*   **Visuals:** Diagram of a multi-server load balancing setup. Then transition to a medical image (like a brain scan MRI) showing a clear boundary, illustrating the min-cut concept.
*   **Script:**
    > "This isn't just theoretical. In DevOps and networking, max-flow algorithms are critical for capacity planning in Software-Defined Networks and data centers, ensuring that network traffic is routed as efficiently as possible to prevent congestion.
    >
    > The algorithm also has a fascinating connection to another problem. The Max-Flow Min-Cut theorem proves that the maximum flow through a network is equal to the minimum capacity of edges that, if cut, would separate the source from the sink. This 'min-cut' idea is used in applications like image segmentation, where it can find the optimal boundary between a foreground and background in a medical scan."

---

### **Time Slot: 4:45 - 5:00**
*   **Section Focus:** Conclusion
*   **Visuals:** Final slide with your name, student number, and the module title (ECM3428 - Algorithms that changed the world).
*   **Script:**
    > "By guaranteeing an efficient, polynomial runtime, the Edmonds-Karp algorithm turned the maximum flow problem from a theoretical curiosity into a reliable tool for building the robust, large-scale networks that power our digital world.
    >
    > (Music swells slightly)
    >
    > Thank you for watching."

---