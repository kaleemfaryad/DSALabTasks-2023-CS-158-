import tkinter as tk
from tkinter import messagebox
import heapq

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, source, destination, distance, travel_time, cost):
        if source not in self.graph:
            self.graph[source] = []
        if destination not in self.graph:
            self.graph[destination] = []
        
        self.graph[source].append((destination, {'distance': distance, 'travel_time': travel_time, 'cost': cost}))
        self.graph[destination].append((source, {'distance': distance, 'travel_time': travel_time, 'cost': cost}))

    def dijkstra(self, start, end, weight_type):
        if start not in self.graph or end not in self.graph:
            return None, None

        priority_queue = [(0, start)]  # (cumulative weight, current node)
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        previous_nodes = {node: None for node in self.graph}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_node == end:
                break

            for neighbor, weights in self.graph[current_node]:
                weight = weights[weight_type]
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path, total_weight = self._reconstruct_path(previous_nodes, start, end), distances[end]
        return path, total_weight

    def _reconstruct_path(self, previous_nodes, start, end):
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        path.reverse()
        return path if path[0] == start else []

class TravelPlannerGUI:
    def __init__(self):
        self.graph = Graph()
        self.root = tk.Tk()
        self.root.title("Travel Planner")

        self.create_widgets()

    def create_widgets(self):
        # Input fields for adding a route
        tk.Label(self.root, text="Source:").grid(row=0, column=0, padx=5, pady=5)
        self.source_entry = tk.Entry(self.root)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Destination:").grid(row=1, column=0, padx=5, pady=5)
        self.destination_entry = tk.Entry(self.root)
        self.destination_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Distance:").grid(row=2, column=0, padx=5, pady=5)
        self.distance_entry = tk.Entry(self.root)
        self.distance_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Travel Time:").grid(row=3, column=0, padx=5, pady=5)
        self.travel_time_entry = tk.Entry(self.root)
        self.travel_time_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Cost:").grid(row=4, column=0, padx=5, pady=5)
        self.cost_entry = tk.Entry(self.root)
        self.cost_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Add Route", command=self.add_route).grid(row=5, column=0, columnspan=2, pady=10)

        # Input fields for finding the shortest path
        tk.Label(self.root, text="Start:").grid(row=6, column=0, padx=5, pady=5)
        self.start_entry = tk.Entry(self.root)
        self.start_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.root, text="End:").grid(row=7, column=0, padx=5, pady=5)
        self.end_entry = tk.Entry(self.root)
        self.end_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Weight Type:").grid(row=8, column=0, padx=5, pady=5)
        self.weight_type_var = tk.StringVar(value="distance")
        tk.OptionMenu(self.root, self.weight_type_var, "distance", "travel_time", "cost").grid(row=8, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Find Shortest Path", command=self.find_shortest_path).grid(row=9, column=0, columnspan=2, pady=10)

    def add_route(self):
        source = self.source_entry.get()
        destination = self.destination_entry.get()
        try:
            distance = float(self.distance_entry.get())
            travel_time = float(self.travel_time_entry.get())
            cost = float(self.cost_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter numeric values for distance, travel time, and cost.")
            return

        self.graph.add_edge(source, destination, distance, travel_time, cost)
        messagebox.showinfo("Success", f"Route added between {source} and {destination}.")

        # Clear the input fields
        self.source_entry.delete(0, tk.END)
        self.destination_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)
        self.travel_time_entry.delete(0, tk.END)
        self.cost_entry.delete(0, tk.END)

    def find_shortest_path(self):
        start = self.start_entry.get()
        end = self.end_entry.get()
        weight_type = self.weight_type_var.get()

        path, total_weight = self.graph.dijkstra(start, end, weight_type)

        if path:
            messagebox.showinfo("Shortest Path", f"Path: {' -> '.join(path)}\nTotal {weight_type}: {total_weight:.2f}")
        else:
            messagebox.showerror("Error", "No path found between the specified locations.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = TravelPlannerGUI()
    gui.run()
