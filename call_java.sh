#!/bin/bash
touch ./Weka/labeled.arff
javac -cp ".:/usr/share/java/weka.jar" classify.java
java -Xmx2000m -cp ".:/usr/share/java/weka.jar" classify
