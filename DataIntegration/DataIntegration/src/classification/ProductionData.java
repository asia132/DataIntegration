package classification;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.FileNotFoundException;

import weka.classifiers.trees.J48;
import weka.clusterers.Canopy;
import weka.classifiers.functions.SimpleLinearRegression;
import weka.classifiers.Evaluation;
import weka.core.Instances;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;

class ProductionData {
	Instances trainData;
	
	public ProductionData() {
	}
	
	private Integer [] sortedIndexes(double [] array) {
		Double [] conv_attr_cl = new Double[array.length];
		for (int ind = 0; ind < array.length; ind++)
			conv_attr_cl[ind] = Double.valueOf(array[ind]);
		ArrayIndexComparator comparator = new ArrayIndexComparator(conv_attr_cl);
		Integer[] indexes = comparator.createIndexArray();
		Arrays.sort(indexes, comparator);
		return indexes;
	}
	
	private int mostCommon(Integer [] array, int maxVal) {
		int [] statistic = new int [maxVal + 1];
		int max = 0;
		for (int i = 0; i < array.length; ++i) {
			statistic[array[i]]++;
			max = statistic[max] > statistic[array[i]] ? max : array[i];
		}
		return max;
	}
	
	public void stats(String path) {
			Instances testData;
			try {
				testData = new Instances(new BufferedReader(new FileReader(path)));
//				System.out.println(testData.toString());
				System.out.println("Average:");
				System.out.println("\tused_energy_kWh " + testData.attributeStats(0).numericStats.sum / 1000);
				System.out.println("\tused_gas_m3 " + testData.attributeStats(1).numericStats.sum / 1000);
				System.out.println("\tduration_time_s " + testData.attributeStats(2).numericStats.sum / 1000);
				System.out.println("Min:");
				System.out.println("\tused_energy_kWh " + testData.attributeStats(0).numericStats.min);
				System.out.println("\tused_gas_m3 " + testData.attributeStats(1).numericStats.min);
				System.out.println("\tduration_time_s " + testData.attributeStats(2).numericStats.min);
				System.out.println("Max:");
				System.out.println("\tused_energy_kWh " + testData.attributeStats(0).numericStats.max);
				System.out.println("\tused_gas_m3 " + testData.attributeStats(1).numericStats.max);
				System.out.println("\tduration_time_s " + testData.attributeStats(2).numericStats.max);
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	}
	
	public double [] clustering(String path) {
		double [] temp = new double [5];
		try {
			Instances testData = new Instances(new BufferedReader(new FileReader(path)));
			// new clusterer instance, default options
			Canopy cluster = new Canopy();   
			
			double pipesTemp = 0;
			double blurringTemp = 0;
			double lastBreakTemp = 0;
			double mashTemp = 0;
			double boilTemp = 0;

			// proceed regression for all numeric attributes
			for (int i = 3; i < testData.numAttributes(); ++i) {
				testData.setClassIndex(i);
				// build clusterer
				cluster.buildClusterer(testData);
				
				Instances clusters_inst = cluster.getCanopies();
				ArrayList <Integer> minIndx = new ArrayList<>();
				int maxVal = 0;
				for (int j = 0; j < 3; ++j) {
					double [] attr_cl = clusters_inst.attributeToDoubleArray(j);
					Integer [] ind = sortedIndexes(attr_cl);
					minIndx.add(ind[0]);
					maxVal = maxVal > ind[0] ? maxVal : ind[0];
				}
				Integer [] array = (Integer[]) minIndx.toArray(new Integer[minIndx.size()]);
				int mostComIndx = mostCommon(array, maxVal);
				
				double [] attr_cl3 = clusters_inst.attributeToDoubleArray(3);
				pipesTemp += attr_cl3[mostComIndx];
				
				double [] attr_cl4 = clusters_inst.attributeToDoubleArray(4);
				blurringTemp += attr_cl4[mostComIndx];
				
				double [] attr_cl5 = clusters_inst.attributeToDoubleArray(5);
				lastBreakTemp += attr_cl5[mostComIndx];
				
				double [] attr_cl6 = clusters_inst.attributeToDoubleArray(6);
				mashTemp += attr_cl6[mostComIndx];
				
				double [] attr_cl7 = clusters_inst.attributeToDoubleArray(7);
				boilTemp += attr_cl7[mostComIndx];
			}
			
			temp[0] = pipesTemp/(testData.numAttributes() - 3);
			temp[1] = blurringTemp/(testData.numAttributes() - 3);
			temp[2] = lastBreakTemp/(testData.numAttributes() - 3);
			temp[3] = mashTemp/(testData.numAttributes() - 3);
			temp[4] = boilTemp/(testData.numAttributes() - 3);
			
		} catch (Exception e) {
			System.out.println("WEKA: " + e.toString());	
		}
		return temp;
	}
	
	// Applies Regression to ARFF file, using all available numeric attributes
	public void regression(String path) {
		try {
			// load data from path
			Instances testData = new Instances(new BufferedReader(new FileReader(path)));
			testData.setClassIndex(testData.numAttributes() - 1);
			
			// removing nominal classes
			String[] options = new String[2];
			options[0] = "-R";                                    // "range"
			options[1] = "6, 7";                                     // first attribute
			Remove remove = new Remove();                         // new instance of filter
			remove.setOptions(options);                           // set options
			remove.setInputFormat(testData);                          // inform filter about dataset **AFTER** setting options
			Instances newData = Filter.useFilter(testData, remove);   // apply filter
			
			SimpleLinearRegression reg = new SimpleLinearRegression();
			
			newData.setClassIndex(0);
			reg.buildClassifier(newData);
			System.out.println("=================================");
			System.out.println(newData.classAttribute());
			System.out.println(reg.getSlope() + " * " + newData.attribute(reg.getAttributeIndex()) + " + " + reg.getIntercept());

			newData.setClassIndex(1);
			reg.buildClassifier(newData);
			System.out.println("=================================");
			System.out.println(newData.classAttribute());
			System.out.println(reg.getSlope() + " * " + newData.attribute(reg.getAttributeIndex()) + " + " + reg.getIntercept());

			newData.setClassIndex(2);
			reg.buildClassifier(newData);
			System.out.println("=================================");
			System.out.println(newData.classAttribute());
			System.out.println(reg.getSlope() + " * " + newData.attribute(reg.getAttributeIndex()) + " + " + reg.getIntercept());

		} catch (Exception e) {
			System.out.println("WEKA: " + e.getMessage());	
		}
	}
	
	public void clasification(String path) {
		try {
			J48 cls = new J48();
			cls.buildClassifier(trainData);
			System.out.println(cls.toString());
			
			Instances testData = new Instances(new BufferedReader(new FileReader(path)));
			testData.setClassIndex(testData.numAttributes() - 2);
			
			Evaluation eval = new Evaluation(trainData);
			
			eval.evaluateModel(cls, testData);
			System.out.println(eval.toMatrixString("\n================\n"));
			eval.crossValidateModel(cls, trainData, 10, new Random(1));
			System.out.println(eval.toMatrixString("\n================\n"));
			eval.evaluateModelOnce(cls, testData.firstInstance());
			System.out.println(eval.toMatrixString("\n================\n"));
		} catch (Exception e) {
			System.out.println("Problem z eval" + e.getMessage());	
		}
	}
}
