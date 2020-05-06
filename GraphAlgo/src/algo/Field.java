package algo;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;

public class Field {
	private int[][] map;
	private int[][] locs;
	private int w, h, len;
	private int max, min;
	private int score;
	
	public Field(int[][] map, int w, int h, int len) {
		cloneIn(map);
		this.w = w;
		this.h = h;
		this.len = len;
		
		getEnds();
		initLocs();
	}
	
	private void cloneIn(int[][] nmap) {
		map = new int[nmap.length][1];
		for(int i = 0; i<map.length; i++) {
			map[i] = nmap[i].clone();
		}
	}
	
	//finds the min and max values of the map
	private void getEnds() {
		max = Integer.MIN_VALUE;
		min = Integer.MAX_VALUE;
		for(int i = 0; i<map.length; i++) {
			for(int j = 0; j<map[0].length; j++) {
				max = Math.max(max, map[i][j]);
				min = Math.min(min,  map[i][j]);
			}
		}
	}
	
	private void initLocs() {
		locs = new int[len][2];
		for(int i = 0; i<locs.length; i++) {
			locs[i][0] = -1;
			locs[i][1] = -1;
		}
	}
	
	public void process(int[] in) {
		for(int i = 0; i<locs.length-1; i++) {
			locs[i][0] = locs[i+1][0];
			locs[i][1] = locs[i+1][1];
		}
		
		locs[locs.length-1][0] = in[0];
		locs[locs.length-1][1] = in[1];		
	}
	
	public void reset(int[][] map) {
		cloneIn(map);
		initLocs();
		getEnds();
	}
	
	//draws the map and current path
	public void draw(Graphics g) {
		if(map == null) return;
		
		double d = Math.min((double)h/map.length, (double)w/map[0].length);
		int xs = (int)((w-d*map[0].length)/2);
		int ys = (int)((h-d*map.length)/2);
		
		for(int i = 0; i<map.length; i++) {
			for(int j = 0; j<map[i].length; j++) {
				int r = (map[i][j]<0) ? 255-(int)(255.0*map[i][j]/min) : 255;
				int b = (map[i][j]>0) ? 255-(int)(255.0*map[i][j]/max) : 255;
				if(map[i][j]==0) {
					r=0;
					b=0;
				}
				
				g.setColor(new Color(r, Math.min(r, b), b));
				g.fillRect((int)(j*d+xs), (int)(i*d+ys), (int)d, (int)d);
				g.setColor(Color.DARK_GRAY);
				g.drawRect((int)(j*d+xs), (int)(i*d+ys), (int)d, (int)d);
			}
		}
		
		Graphics2D g2 = (Graphics2D) g;
	    g2.setStroke(new BasicStroke(4));
		
		for(int i = 0; i<locs.length; i++) {
			if(locs[i][0] == -1) continue;
//			int dif = (int)(255.0*(i+1)/locs.length);
//			dif = Math.min(255,  dif);
//			g.setColor(new Color(0, 255, 0));
//			g.fillRect((int)(locs[i][1]*d+xs), (int)(locs[i][0]*d+ys), (int)d, (int)d);
//			g.setColor(Color.BLACK);
//			g.drawRect((int)(locs[i][1]*d+xs), (int)(locs[i][0]*d+ys), (int)d, (int)d);
			
			if(i>0 && Math.abs(locs[i][0]-locs[i-1][0])<2 && Math.abs(locs[i][1]-locs[i-1][1])<2) {
				g2.setColor(Color.GREEN);
				g2.drawLine((int)(locs[i][1]*d+xs+d/2), (int)(locs[i][0]*d+ys+d/2), (int)(locs[i-1][1]*d+xs+d/2), (int)(locs[i-1][0]*d+ys+d/2));
			}
		}
	}
}
