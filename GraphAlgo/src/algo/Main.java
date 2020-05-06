package algo;

import java.io.IOException;
import javax.swing.JFrame;

public class Main {

	JFrame frame;
	AlgoPanel panel;
	int width = 800;
	int height = 800;

	public static void main(String args[]) throws IOException {
		Main main = new Main();
		main.Jsetup();
	}

	private void Jsetup() {
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(width, height);
		frame.setLocation(0, 0);
		frame.setVisible(true);
		panel.start();
	}

	public Main() throws IOException {
		frame = new JFrame();
		panel = new AlgoPanel("field.txt", width, height, false);
		frame.add(panel);
		frame.addKeyListener(panel);
	}
}

