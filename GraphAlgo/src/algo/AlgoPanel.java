package algo;

import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.IOException;

import javax.swing.JPanel;
import javax.swing.Timer;


//Modified JPanel that shows the map and path of the drill
public class AlgoPanel extends JPanel implements ActionListener, KeyListener {
	private int w, h;
	private String fName;
	private boolean auto;
	
	private int[][] map;
	private Field f;
	private int[][] path;
	private int loc;
	
	private Timer t;
	private int fps = 10; 
	
	public AlgoPanel(String fName, int w, int h, boolean auto) throws IOException {
		this.auto = auto;
		this.fName = fName;
		this.w = w;
		this.h = h;
		run();
	}
	
	//initializes the runner
	private void run() throws IOException {
		Runner r = new Runner();
		int[][][] output = r.runFile("field.txt");
		map = output[0];
		f = new Field(map, w, h, 250);
		path = output[1];
		loc = 0;
		t = new Timer(1000/fps, this);
	}
	
	public void start() {
		t.start();
	}

	@Override
	public void keyTyped(KeyEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void keyPressed(KeyEvent e) {
		// TODO Auto-generated method stub
		if(t == null) return;
		
		if(e.getKeyCode() == KeyEvent.VK_RIGHT) {
			fps = Math.min(60,  fps+2);
			if(t.isRunning()) {
				t.stop();
				t = new Timer(1000/fps, this);
				t.start();
			} else {
				t = new Timer(1000/fps, this);
			}
		} else if (e.getKeyCode() == KeyEvent.VK_LEFT) {
			fps = Math.max(2,  fps-2);
			if(t.isRunning()) {
				t.stop();
				t = new Timer(1000/fps, this);
				t.start();
			} else {
				t = new Timer(1000/fps, this);
			}
		} else if(e.getKeyCode() == KeyEvent.VK_SPACE) {
			if(t.isRunning()) t.stop();
			else t.start();
		}
	}

	@Override
	public void keyReleased(KeyEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		// TODO Auto-generated method stub
		if(loc==path.length) {
			loc = 0;
			f.reset(map);
			if(!auto)
				t.stop();
		} else {
			f.process(path[loc]);
			loc++;
			repaint();
		}
	}
	
	public void paint(Graphics g) {
		f.draw(g);
	}
}
