package classification;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Hashtable;

public class ProcessOptymalization {		
	String basicPath = "C:\\Users\\Asia\\PycharmProjects\\DataIntegration\\outputs\\";
	
	String communicateOutput = "C:\\Users\\Asia\\PycharmProjects\\DataIntegration\\input\\message";
	String communicateInput = "C:\\Users\\Asia\\PycharmProjects\\DataIntegration\\input\\settings.conf";
	
	ProductionData productionDataTrain;
	
	ArrayList <String> paths;
	
	// settings
	String date;
	Double [] tempPipes;
	Double [] tempMaltoseBreak;
	Double [] tempDextrinizationBreak;
	Double [] tempMashOut;
	Double [] tempBoiling;
	
	public ProcessOptymalization() {		
		productionDataTrain = new ProductionData();
		
		paths = new ArrayList<>();
		
		File [] dirs = new File(basicPath).listFiles(File::isDirectory);
		for (int i = 0; i < dirs.length; ++i) {
			File [] dirsOfDate = new File(dirs[i].toString()).listFiles();
			String seq = dirsOfDate[0].toString();
			if (!seq.contains("archive")) {
				paths.add(seq);
			}
		}
		
		tempPipes = new Double [2];
		tempMaltoseBreak = new Double [2];
		tempDextrinizationBreak = new Double [2];
		tempMashOut = new Double [2];
		tempBoiling = new Double [2];
		
		readSettings();
	}
	
	public void readSettings() {
		try {
			BufferedReader file = new BufferedReader(new FileReader(communicateInput));
			date = file.readLine();
			String [] pipes = file.readLine().split(" ");
			String [] maltoseBreak = file.readLine().split(" ");
			String [] dextrinizationBreak = file.readLine().split(" ");
			String [] mashOut = file.readLine().split(" ");
			String [] boiling = file.readLine().split(" ");
			for(int i = 0; i < maltoseBreak.length; ++i) {
				tempPipes[0] = Double.parseDouble(pipes[0]);
				tempPipes[1] = Double.parseDouble(pipes[1]);
				tempMaltoseBreak[0] = Double.parseDouble(maltoseBreak[0]);
				tempMaltoseBreak[1] = Double.parseDouble(maltoseBreak[1]);
				tempDextrinizationBreak[0] = Double.parseDouble(dextrinizationBreak[0]);
				tempDextrinizationBreak[1] = Double.parseDouble(dextrinizationBreak[1]);
				tempMashOut[0] = Double.parseDouble(mashOut[0]);
				tempMashOut[1] = Double.parseDouble(mashOut[1]);
				tempBoiling[0] = Double.parseDouble(boiling[0]);
				tempBoiling[1] = Double.parseDouble(boiling[1]);
			}
			file.close();
		}catch(FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	private String getTagFromPath(String path) {
		return path.substring(63, path.length() - 8);
	}
	
	public String getDateFromPath(String path) {
		return path.substring(54, 61);
	}
	
	public void runOpt() {
		
		System.out.println("-----------------------------------------");
		for (int i = 0; i < paths.size(); ++i) {
			productionDataTrain.stats(paths.get(i));
			String tag = getTagFromPath(paths.get(i));
			double [] clustTemp = productionDataTrain.clustering(paths.get(i));
			System.out.println("CLUSTERING " + tag + " " + clustTemp[0] + ", " + clustTemp[1] + ", " + clustTemp[2] + ", " + clustTemp[3] + ", " + clustTemp[4]);
			System.out.println("-----------------------------------------");
			prepareMessage(clustTemp);
		}
	}
	
	private void prepareMessage(double [] clustTemp) {
		try (Writer writer = new BufferedWriter(new OutputStreamWriter(
	              new FileOutputStream(communicateOutput)))) {
			int change = clustTemp[0] - tempPipes[0] < tempPipes[1] - clustTemp[0] ? 0 : 1;
			writer.write(change + " " + clustTemp[0] + "\n");
			change = clustTemp[0] - tempMaltoseBreak[0] < tempMaltoseBreak[1] - clustTemp[0] ? 0 : 1;
			writer.write(change + " " + clustTemp[1] + "\n");
			change = clustTemp[0] - tempDextrinizationBreak[0] < tempDextrinizationBreak[1] - clustTemp[0] ? 0 : 1;
			writer.write(change + " " + clustTemp[2] + "\n");
			change = clustTemp[0] - tempMashOut[0] < tempMashOut[1] - clustTemp[0] ? 0 : 1;
			writer.write(change + " " + clustTemp[3] + "\n");
			change = clustTemp[0] - tempBoiling[0] < tempBoiling[1] - clustTemp[0] ? 0 : 1;
			writer.write(change + " " + clustTemp[4] + "\n");
	} catch (FileNotFoundException e) {
		e.printStackTrace();
	} catch (IOException e) {
		e.printStackTrace();
	}
	}
	
	public void archivize() {
		for (int i = 0; i < paths.size(); ++i) {
			File file = new File(paths.get(i));
			renameDir(file.getParent());
		}
	}
	
	private void renameDir(String path) {
		File dir = new File(path);
		File parentdir = new File(dir.getParent());
		if (!dir.isDirectory()) {
			System.err.println("There is no directory @ given path");
		} else {
			StringBuilder sb = new StringBuilder (String.valueOf("archive_"));
			sb.append(parentdir.listFiles().length);
			String newDirName = sb.toString();
			File newDir = new File(dir.getParent() + "\\" + newDirName);
					dir.renameTo(newDir);
		}
	}
}
