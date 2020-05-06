package algo;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class PathFinder {
	public int[][] findPath(int[][] map, int rs, int cs, int len) {
		int[][] vmap = new int[map.length][map[0].length];
		populate2D(vmap, -1);

		int[][] pools = pool(map, vmap);
		ArrayList<int[][][]> circs = circ(pools, vmap);
		int[][][][] paths = poolPath(circs, pools, map);
		int[][][] dSolve = dijkstraSolve(map, paths);
		
		int start = rs * map[0].length + cs;
		ArrayList<Integer> out = poolsDFS(start, map, paths, dSolve, new boolean[paths.length], len);
		int val = out.remove(out.size()-1);
		System.out.println(val);
		int[][] fPath = reverseHash(out, map[0].length);
		
		return fPath;
	}
	
	//uses flood fill to find pools of high-value locations
	private int[][] pool(int[][] map, int[][] vmap) {
		ArrayList<int[]> pools = new ArrayList<int[]>();

		for (int i = 0; i < map.length; i++) {
			for (int j = 0; j < map[0].length; j++) {
				if (map[i][j] > 0 && vmap[i][j] < 0) {
					int[] dim = new int[] { i, i, j, j };
					floodFill(i, j, map, vmap, dim, pools.size() * 4);
					pools.add(dim);
				}
			}
		}

		int[][] ret = new int[pools.size()][4];
		for (int i = 0; i < pools.size(); i++) {
			for (int j = 0; j < 4; j++) {
				ret[i][j] = pools.get(i)[j];
			}
		}

		return ret;
	}

	private void floodFill(int r, int c, int[][] map, int[][] vmap, int[] dim, int val) {
		if (!isValid(r, c, map.length, map[0].length) || vmap[r][c] >= 0 || map[r][c] <= 0)
			return;
		vmap[r][c] = val;

		dim[0] = Math.min(dim[0], r);
		dim[1] = Math.max(dim[1], r);
		dim[2] = Math.min(dim[2], c);
		dim[3] = Math.max(dim[3], c);

		for (int i = 0; i < 4; i++) {
			floodFill(r + (2 - i) % 2, c + (i - 1) % 2, map, vmap, dim, val);
		}
	}
	
	//finds the 8 corner points of each pool
	private ArrayList<int[][][]> circ(int[][] pools, int[][] vmap) {
		ArrayList<int[][][]> circs = new ArrayList<int[][][]>();
		for (int i = 0; i < pools.length; i++) {
			int u = pools[i][0], d = pools[i][1], l = pools[i][2], r = pools[i][3];
			int[][] horz = new int[d - u + 1][2];
			int[][] vert = new int[r - l + 1][2];

			for (int j = 0; j < horz.length; j++)
				horz[j][0] = -1;
			for (int j = 0; j < vert.length; j++)
				vert[j][0] = -1;

			for (int j = u; j <= d; j++) {
				for (int k = l; k <= r; k++) {
					if (vmap[j][k] == i * 4) {
						if (horz[j - u][0] < 0)
							horz[j - u][0] = k - l;
						horz[j - u][1] = k - l;
						if (vert[k - l][0] < 0)
							vert[k - l][0] = j - u;
						vert[k - l][1] = j - u;
					}
				}
			}

			int[][][] add = new int[][][] { horz, vert };
			circs.add(add);
		}
		return circs;
	}
	
	//finds the optimal path through each pool
	private int[][][][] poolPath(ArrayList<int[][][]> circs, int[][] pools, int[][] map) {
		int[][][][] ret = new int[circs.size()][4][1][1];
		for (int i = 0; i < circs.size(); i++) {
			int[][][] cloc = new int[4][1][1];
			for (int j = 0; j < 2; j++) {
				int[][] dirv = circs.get(i)[j];
				for (int k = 0; k < 2; k++) {
					ArrayList<int[]> locs = new ArrayList<int[]>();
					for (int l = 0; l < dirv.length; l++) {
						int clo = l + 2 * ((l + k) % 2) - 1;
						int chi = l - 2 * ((l + k) % 2) + 1;

						if (clo < 0 || clo >= dirv.length)
							clo = l;
						if (chi < 0 || chi >= dirv.length)
							chi = l;

						int lo = Math.min(dirv[l][0], dirv[clo][0]);
						int hi = Math.max(dirv[l][1], dirv[chi][1]);

						int s = ((l + k) % 2 == 0) ? lo : hi;
						int f = ((l + k) % 2 == 0) ? hi : lo;
						int inc = ((l + k) % 2 == 0) ? 1 : -1;

						for (int m = s; (m <= f && inc > 0) || (m >= f && inc < 0); m += inc) {
							int r = pools[i][0] + ((j == 0) ? l : m);
							int c = pools[i][2] + ((j == 0) ? m : l);
							locs.add(new int[] { r, c });
						}
					}

					int[][] add = new int[locs.size()][2];
					for (int l = 0; l < add.length; l++) {
						add[l][0] = locs.get(l)[0];
						add[l][1] = locs.get(l)[1];
					}
					cloc[j * 2 + k] = add;
				}
			}
			ret[i] = cloc;
		}

		return ret;
	}

	//converts map into adjacency list with rewards as vertices
	private List<List<Node>> makeGraph(int[][] map) {
		List<List<Node>> adj = new ArrayList<List<Node>>();
		for (int i = 0; i < map.length * map[0].length; i++) {
			List<Node> item = new ArrayList<Node>();
			adj.add(item);
		}

		for (int i = 0; i < map.length; i++) {
			for (int j = 0; j < map[i].length; j++) {
				for (int k = 0; k < 4; k++) {
					int r = i + (2 - k) % 2, c = j + (k - 1) % 2;
					if (isValid(r, c, map.length, map[i].length)) {
						adj.get(i * map[0].length + j).add(new Node(r * map[0].length + c, Math.abs(map[r][c])+1));
					}
				}
			}
		}

		return adj;
	}
	
	//runs dijkstra on all corner points
	private int[][][] dijkstraSolve(int[][] map, int[][][][] paths) {
		int[][][] dSolve = new int[map.length*map[0].length][2][1];
		List<List<Node>> graph = makeGraph(map);
		for(int i = 0; i<paths.length; i++) {
			for(int j = 0; j<4; j++) {
				int[][] p = paths[i][j];
				int v = p[0][0]*map[0].length+p[0][1];
				if(dSolve[v][0].length==1) dSolve[v] = new DPQ().dijkstra(graph, v);
				v = p[p.length-1][0]*map[0].length+p[p.length-1][1];
				if(dSolve[v][0].length==1) dSolve[v] = new DPQ().dijkstra(graph, v);
			}
		}
		return dSolve;
	}

	//runs a dfs between all of the pools
	private ArrayList<Integer> poolsDFS(int loc, int[][] map, int[][][][] paths, int[][][] dSolve, boolean[] vis, int len) {
		if(len<=0) {
			ArrayList<Integer> ret = new ArrayList<Integer>();
			ret.add(0);
			return ret;
		}
		
		int[][] cmap = new int[map.length][1];
		for(int i = 0; i<map.length; i++) cmap[i] = map[i].clone();
		
		boolean f = false;
		ArrayList<ArrayList<Integer>> allPaths = new ArrayList<ArrayList<Integer>>();
		
		if(dSolve[loc][0].length == 1) {
			f = true;
			dSolve[loc] = new DPQ().dijkstra(makeGraph(map), loc);
		}
		int[][] ds = dSolve[loc];

		for (int i = 0; i < paths.length; i++) {
			if(vis[i]) continue;
			vis[i] = true;
			
			for (int j = 0; j < 4; j++) {
				int[][] pPath = paths[i][j%4];
				ArrayList<Integer> subPath = new ArrayList<Integer>();
				int value = 0;
				
				int l1 = ds[0][pPath[0][0]*map[0].length+pPath[0][1]];
				int l2 = ds[0][pPath[pPath.length-1][0]*map[0].length+pPath[pPath.length-1][1]];
				j = (l1<l2) ? j : j+4;
				
				int t = pPath[(j/4)*(pPath.length-1)][0]*map[0].length + pPath[(j/4)*(pPath.length-1)][1];
				while(t != ds[1][t] && subPath.size()<len) {
					value+=map[t/map[0].length][t%map[0].length];
					subPath.add(0, t);
					map[t/map[0].length][t%map[0].length] = 0;
					t = ds[1][t];
				}
				
				if(subPath.size()==len) {
					for(int k = 1; k<map.length; k++) map[k] = cmap[k].clone();
					continue;
				}
				
				if(f) {
					value+=map[loc/map[0].length][loc%map[0].length];
					subPath.add(0, loc);
				}
				
				for(int k = 1; k<pPath.length && subPath.size()<len; k++) {
					int ind = (j>=4) ? pPath.length-1-k : k;
					value+=map[pPath[ind][0]][pPath[ind][1]];
					subPath.add(pPath[ind][0]*map[0].length + pPath[ind][1]);
					map[pPath[ind][0]][pPath[ind][1]] = 0;
				}
				
				int nloc = pPath[((j+4)%8)/4*(pPath.length-1)][0]*map[0].length + pPath[((j+4)%8)/4*(pPath.length-1)][1];
				ArrayList<Integer> mPath = poolsDFS(nloc, map, paths, dSolve, vis, len-subPath.size());
				value+=mPath.remove(mPath.size()-1);
				
				subPath.addAll(mPath);
				subPath.add(value);
				allPaths.add(subPath);
				
				for(int k = 0; k<map.length; k++) map[k] = cmap[k].clone();
				j = j%4;
			}
			vis[i] = false;
		}
		
		int maxVal = 0, minLen = Integer.MAX_VALUE;
		ArrayList<Integer> ret = new ArrayList<Integer>();
		ret.add(0);
		
		for(int i = 0; i<allPaths.size(); i++) {
			ArrayList<Integer> a = allPaths.get(i);
			if(a.get(a.size()-1) > maxVal) {
				maxVal = a.get(a.size()-1);
				minLen = a.size()-1;
				ret = a;
			} else if(a.get(a.size()-1) == maxVal && a.size()-1<minLen) {
				minLen = a.size()-1;
				ret = a;
			}
		}
		
		//if(f) ret.remove(ret.size()-1);
		return ret;
	}
	
	//find the location given the hash
	private int[][] reverseHash(ArrayList<Integer> arr, int d) {
		int[][] ret = new int[arr.size()][2];
		for(int i = 0; i<arr.size(); i++) {
			ret[i][0] = arr.get(i)/d;
			ret[i][1] = arr.get(i)%d;
		}
		return ret;
	}

	private void populate2D(int[][] arr, int v) {
		for (int i = 0; i < arr.length; i++) {
			for (int j = 0; j < arr[0].length; j++) {
				arr[i][j] = -1;
			}
		}
	}
	
	private boolean isValid(int r, int c, int l, int w) {
		if (r >= 0 && r < l && c >= 0 && c < w)
			return true;
		else
			return false;
	}
}