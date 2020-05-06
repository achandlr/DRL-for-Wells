package algo;
import java.util.*;

//ELogV implementation of dijkstra
public class DPQ {
	
	//runs a dijkstra algorithm on the given adjacency list
	//returns a 2d array of size 2 by N (N represents total nodes)
	//0 index of array shows distances
	//1 index of array shows prvious node of shortest path
	public int[][] dijkstra(List<List<Node>> adj, int src) {
		int[] dist = new int[adj.size()];
		int[] path = new int[adj.size()];
		PriorityQueue<Node> pq = new PriorityQueue<Node>(adj.size(), new Node());
		HashSet<Integer> settled = new HashSet<Integer>();

		for (int i = 0; i < adj.size(); i++) {
			dist[i] = Integer.MAX_VALUE;
			path[i] = -1;
		}

		pq.add(new Node(src, 0));

		dist[src] = 0;
		path[src] = src;
		while (!pq.isEmpty() && settled.size() != adj.size()) {
			int u = pq.remove().node;
			settled.add(u);
			e_Neighbours(u, adj, dist, path, settled, pq);
		}

		return new int[][] { dist, path };
	}

	//loops through neighbors and add them to queue
	private void e_Neighbours(int u, List<List<Node>> adj, int[] dist, int[] path, HashSet<Integer> settled, PriorityQueue<Node> pq) {
		int edgeDistance = -1;
		int newDistance = -1;

		for (int i = 0; i < adj.get(u).size(); i++) {
			Node v = adj.get(u).get(i);

			if (!settled.contains(v.node)) {
				edgeDistance = v.cost;
				newDistance = dist[u] + edgeDistance;

				if (newDistance < dist[v.node]) {
					dist[v.node] = newDistance;
					path[v.node] = u;
					pq.add(new Node(v.node, dist[v.node]));
				}
			}
		}
	}
}