package algo;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;

public class Runner {
	
	public int[][][] runFile(String inName) throws IOException {
		int[][] map = read(inName);
		/*int[][] map = new int[][] { 
			{ 1, 1, 1, 0, 0, 0 }, 
			{ 1, 0, 1, 1, 0, 0 }, 
			{ 0, 1, 1, 0, 0, 0 },
			{ 0, 0, 0, Integer.MIN_VALUE, 1, 0 }, 
			{ 0, 0, 1, 1, 1, 0 }, 
			{ 0, 1, 1, 1, 0, 0 }
		};*/
		int[] p = getPump(map);
		
		PathFinder pf = new PathFinder();
		int[][] out = pf.findPath(map, p[0], p[1], 150);
		
		return new int[][][] {map, out};
	}
	
	//reads in file as 2D array (map)
	private int[][] read(String inName) throws IOException {
		File file = new File(inName); 
		BufferedReader br = new BufferedReader(new FileReader(file)); 
		  
		String[] sta = br.readLine().split(" "); 
		int r = Integer.parseInt(sta[0]);
		int c = Integer.parseInt(sta[1]);
		int[][] out = new int[r][c];
		
		for(int i = 0; i<r; i++) {
			String st = br.readLine();
			for(int j = 0; j<c; j++) {
			 	int rand = (int)(Math.random()*10+1);
				if(st.charAt(j) == 'O') out[i][j] = 1;
				else if(st.charAt(j) == 'W') out[i][j] = -1;
				else if(st.charAt(j) == 'P') out[i][j] = Integer.MIN_VALUE;
			}
		}
		
		return out;
	}
	
	//gets the location of the pump
	public int[] getPump(int[][] map) {
		for(int i = 0; i<map.length; i++) {
			for(int j = 0; j<map[0].length; j++) {
				if(map[i][j] == Integer.MIN_VALUE) {
					map[i][j] = 0;
					return new int[] {i, j};
				}
			}
		}
		return new int[] {-1, -1};
	}
}
