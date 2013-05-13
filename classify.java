import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.functions.SMO;
import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import java.util.Random;
import java.io.*;

public class classify 
{
 
    public static void main(String[] args) throws Exception
    {
        // DataSource source = new DataSource("./Dataset/trainingset_corp.arff");
        // Instances data = source.getDataSet();
        // if (data.classIndex() == -1)
        //     data.setClassIndex(data.numAttributes() - 1);

        // data.setClassIndex(data.numAttributes() - 1);

        //create a classifier and set options.
        /* Classifier svm =(Classifier) new SMO();
        svm.buildClassifier(data);
        svm.setOptions(weka.core.Utils.splitOptions("weka.classifiers.functions.SMO -C 4.0 -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K \"weka.classifiers.functions.supportVector.RBFKernel -C 250007 -G 0.5\""));
        */

        Classifier svm = (Classifier) weka.core.SerializationHelper.read(new FileInputStream("./Weka/SMO_final.model"));

        DataSource testSource = new DataSource("./Weka/toClassify.arff");
        Instances unlabeled = testSource.getDataSet();
        //set class attribute
        unlabeled.setClassIndex(unlabeled.numAttributes() - 1);
        
        //create copy
        Instances labeled = new Instances(unlabeled);

        //label instances
        for (int i = 0; i < unlabeled.numInstances(); i++) 
        {
            double clsLabel = svm.classifyInstance(unlabeled.instance(i));
            labeled.instance(i).setClassValue(clsLabel);
        }

        BufferedWriter writer = new BufferedWriter(
                           new FileWriter("./Weka/labeled.arff"));
        writer.write(labeled.toString());
        writer.newLine();
        writer.flush();
        writer.close();
        System.out.println("Classification complete.");
        /*Evaluation eval = new Evaluation(data);
        Random rand = new Random(1);  // using seed = 1
        int folds = 10;
        eval.crossValidateModel(svm, data, folds, rand);
        System.out.println(eval.toClassDetailsString());
                
        // Get the confusion matrix
        double[][] cmMatrix = eval.confusionMatrix();
        for(int row_i=0; row_i<cmMatrix.length; row_i++)
        {
            for(int col_i=0; col_i<cmMatrix.length; col_i++){
                System.out.print(cmMatrix[row_i][col_i]);
                System.out.print("|");
            }
            System.out.println();
        }*/
    }
}
