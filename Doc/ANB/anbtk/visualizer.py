import networkx as nx
import matplotlib.pyplot as plt

# Create a NetworkX graph
family_tree = nx.DiGraph()

# Add nodes to the graph
family_tree.add_node("John")
family_tree.add_node("Jane")
family_tree.add_node("Alice")
family_tree.add_node("Bob")

# Add edges to the graph
family_tree.add_edge("John", "Alice")
family_tree.add_edge("Jane", "Alice")
family_tree.add_edge("Alice", "Bob")

# Visualize the family tree
pos = nx.spring_layout(family_tree)  # Layout algorithm for graph visualization
nx.draw_networkx(family_tree, pos=pos, with_labels=True)
plt.axis("off")  # Turn off axes
plt.show()  # Display the graph
