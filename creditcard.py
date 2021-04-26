# -*- coding: utf-8 -*-
"""simrancolab.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UAxB711HfuKWp3UYkf6JQn7esLW2shcA
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import platform; print(platform.platform())
import sys; print("Python", sys.version)
import numpy; print("NumPy", numpy.__version__)
import scipy; print("SciPy", scipy.__version__)
import sklearn; print("Scikit-Learn", sklearn.__version__)
import imblearn; print("Imbalanced-Learn", imblearn.__version__)

from google.colab import drive
drive.mount('/content/drive')



df=pd.read_csv('/content/drive/MyDrive/creditcard.csv')
df.head()

# determine the number of records in the dataset
print('The dataset contains {0} rows and {1} columns.'.format(df.shape[0], df.shape[1]))

#explore the dataset
print(df.columns)

"""# check for missing values and data types of the columns

"""

df.info()

"""# Explore label class"""

print('Normal transactions count: ', df['Class'].value_counts().values[0])
print('Fraudulent transactions count: ', df['Class'].value_counts().values[1])

print('Normal transactions', round(df['Class'].value_counts()[0]/len(df) * 100,2), '% of the dataset')
print('Frauds', round(df['Class'].value_counts()[1]/len(df) * 100,2), '% of the dataset')

# Count the occurrences of fraud and no fraud cases
LABELS = ["Normal", "Fraud"]
fnf = df["Class"].value_counts()

# Plottingg your data
fnf.plot(kind = 'bar',title = 'Frequency by observation number',rot=0)
plt.xticks(range(2),LABELS)
plt.xlabel("Class (0:Normal, 1:Fraud)")
plt.ylabel("Number of Observations")

# Plot how fraud and non-fraud cases are scattered 
plt.scatter(df.loc[df['Class'] == 0]['V1'], df.loc[df['Class'] == 0]['V2'], label="Class #0", alpha=0.5, linewidth=0.15,c='b')
plt.scatter(df.loc[df['Class'] == 1]['V1'], df.loc[df['Class'] == 1]['V2'], label="Class #1", alpha=0.5, linewidth=0.15,c='r')
plt.show()

"""# Distribution of 2 Features : Time and Amount

"""

import seaborn as sns

fig, ax = plt.subplots(1, 2, figsize=(18,4))

# Plot the distribution of 'Time' feature 
sns.distplot(df['Time'].values/(60*60), ax=ax[0], color='r')
ax[0].set_title('Distribution of Transaction Time', fontsize=14)
ax[0].set_xlim([min(df['Time'].values/(60*60)), max(df['Time'].values/(60*60))])

sns.distplot(df['Amount'].values, ax=ax[1], color='b')
ax[1].set_title('Distribution of Transaction Amount', fontsize=14)
ax[1].set_xlim([min(df['Amount'].values), max(df['Amount'].values)])

plt.show()

"""# Cut Up the Dataset into Two Datasets and Summarize


"""

# Seperate total data into non-fraud and fraud cases
df_nonfraud = df[df.Class == 0] #save non-fraud df observations into a separate df
df_fraud = df[df.Class == 1] #do the same for frauds

"""# Compare the Amount of transactions in two separate datasets"""

# Summarize statistics and see differences between fraud and normal transactions
print(df_nonfraud.Amount.describe())
print('_'*25)
print(df_fraud.Amount.describe())

# Import the module
from scipy import stats
F, p = stats.f_oneway(df['Amount'][df['Class'] == 0], df['Amount'][df['Class'] == 1])
print("F:", F)
print("p:",p)

"""# Transaction Amount Visualization"""

# Plot of high value transactions($200-$2000)
bins = np.linspace(200, 2000, 100)
plt.hist(df_nonfraud.Amount, bins, alpha=1, density=True, label='Non-Fraud')
plt.hist(df_fraud.Amount, bins, alpha=1, density=True, label='Fraud')
plt.legend(loc='upper right')
plt.title("Amount by percentage of transactions (transactions \$200-$2000)")
plt.xlabel("Transaction amount (USD)")
plt.ylabel("Percentage of transactions (%)")
plt.show()

"""# Transaction Hour"""

# Plot of transactions in 48 hours
bins = np.linspace(0, 48, 48) #48 hours
plt.hist((df_nonfraud.Time/(60*60)), bins, alpha=1, density=True, label='Non-Fraud')
plt.hist((df_fraud.Time/(60*60)), bins, alpha=0.6, density=True, label='Fraud')
plt.legend(loc='upper right')
plt.title("Percentage of transactions by hour")
plt.xlabel("Transaction time from first transaction in the dataset (hours)")
plt.ylabel("Percentage of transactions (%)")
plt.show()

"""# Transaction Amount vs. Hour

"""

# Plot of transactions in 48 hours
plt.scatter((df_nonfraud.Time/(60*60)), df_nonfraud.Amount, alpha=0.6, label='Non-Fraud')
plt.scatter((df_fraud.Time/(60*60)), df_fraud.Amount, alpha=0.9, label='Fraud')
plt.title("Amount of transaction by hour")
plt.xlabel("Transaction time as measured from first transaction in the dataset (hours)")
plt.ylabel('Amount (USD)')
plt.legend(loc='upper right')
plt.show()

"""# Feature Scaling"""

# Scale "Time" and "Amount"
from sklearn.preprocessing import StandardScaler, RobustScaler
df['scaled_amount'] = RobustScaler().fit_transform(df['Amount'].values.reshape(-1,1))
df['scaled_time'] = RobustScaler().fit_transform(df['Time'].values.reshape(-1,1))

# Make a new dataset named "df_scaled" dropping out original "Time" and "Amount"
df_scaled = df.drop(['Time','Amount'],axis = 1,inplace=False)
df_scaled.head()

"""# Extract features from our scaled dataset "df_scaled"

"""

# Define the prep_data function to extrac features 
def prep_data(df):
    X = df.drop(['Class'],axis=1, inplace=False) #  
    X = np.array(X).astype(np.float)
    y = df[['Class']]  
    y = np.array(y).astype(np.float)
    return X,y

# Create X and y from the prep_data function 
X, y = prep_data(df_scaled)

"""# Resample data with RUS, ROS and SMOTE"""

from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import BorderlineSMOTE
from imblearn.pipeline import Pipeline
from imblearn.metrics import classification_report_imbalanced

"""# Create the training and testing sets"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=0)
X_train.shape,X_test.shape

"""# Define the resampling method"""

undersam = RandomUnderSampler(random_state=0)
oversam = RandomOverSampler(random_state=0)
smote = SMOTE(random_state=0)
borderlinesmote = BorderlineSMOTE(kind='borderline-2',random_state=0)

"""# resample the training data"""

X_undersam, y_undersam = undersam.fit_sample(X_train,y_train)
X_oversam, y_oversam = oversam.fit_sample(X_train,y_train)
X_smote, y_smote = smote.fit_sample(X_train,y_train)
X_borderlinesmote, y_borderlinesmote = borderlinesmote.fit_sample(X_train,y_train)

"""# Module 3: Logistic Regression

"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
x = np.array(df.iloc[:, df.columns != 'Class'])
y = np.array(df.iloc[:, df.columns == 'Class'])


# Create the training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=0)

# Fit a logistic regression model to our data
model = LogisticRegression()
model.fit(X_train, y_train)

# Obtain model predictions
y_predicted = model.predict(X_test)

from sklearn.metrics import roc_curve,roc_auc_score, precision_recall_curve, average_precision_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
cnf_matrix = confusion_matrix(y_true = y_test, y_pred = y_predicted)
labels = ['Non-fraud', 'Fraud']
sns.heatmap(pd.DataFrame(cnf_matrix),xticklabels = labels, yticklabels = labels, annot=True, cmap="Reds", fmt='g')
plt.ylabel('Actual Label',size = 15)
plt.xlabel('Predicted Label',size = 15)
plt.title("Confusion Matrix Plotting for Logistic Regression model", size = 20)

# Create true and false positive rates
false_positive_rate, true_positive_rate, threshold = roc_curve(y_test, y_predicted)

# Calculate Area Under the Receiver Operating Characteristic Curve 
probs = model.predict_proba(X_test)
roc_auc = roc_auc_score(y_test, probs[:, 1])
print('ROC AUC Score:',roc_auc)

# Obtain precision and recall 
precision, recall, thresholds = precision_recall_curve(y_test, y_predicted)

# Calculate average precision 
average_precision = average_precision_score(y_test, y_predicted)

# Define a roc_curve function
def plot_roc_curve(false_positive_rate,true_positive_rate,roc_auc):
    plt.plot(false_positive_rate, true_positive_rate, linewidth=5, label='AUC = %0.3f'% roc_auc)
    plt.plot([0,1],[0,1], linewidth=5)
    plt.xlim([-0.01, 1])
    plt.ylim([0, 1.01])
    plt.legend(loc='upper right')
    plt.title('Receiver operating characteristic curve (ROC)')
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()

# Define a precision_recall_curve function
def plot_pr_curve(recall, precision, average_precision):
    plt.step(recall, precision, color='b', alpha=0.2, where='post')
    plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(average_precision))
    plt.show()
    
# Print the classifcation report and confusion matrix
print('Classification report:\n', classification_report(y_test, y_predicted))
#print('Confusion matrix:\n',confusion_matrix(y_true = y_test, y_pred = y_predicted))
print('accuracy :\n',accuracy_score(y_test,y_predicted))

# Plot the roc curve 
plot_roc_curve(false_positive_rate,true_positive_rate,roc_auc)

# Plot recall precision curve
plot_pr_curve(recall, precision, average_precision)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import BorderlineSMOTE

# Create the training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=0)

# Resample your training data
rus = RandomUnderSampler()
ros = RandomOverSampler()
smote = SMOTE(random_state=5)
blsmote = BorderlineSMOTE(kind='borderline-2',random_state=5)

X_train_rus, y_train_rus = rus.fit_sample(X_train,y_train)
X_train_ros, y_train_ros = ros.fit_sample(X_train,y_train)
X_train_smote, y_train_smote = smote.fit_sample(X_train,y_train)
X_train_blsmote, y_train_blsmote = blsmote.fit_sample(X_train,y_train)

print("Transaction Number x_train dataset: ", X_train.shape)
print("Transaction Number y_train dataset: ", y_train.shape)
print("Transaction Number x_test dataset: ", X_test.shape)
print("Transaction Number y_test dataset: ", y_test.shape)

print("Before OverSampling, counts of label '1': {}".format(sum(y_train==1)))
print("Before OverSampling, counts of label '0': {} \n".format(sum(y_train==0)))
#ROS
print('After OverSampling, the shape of train_x: {}'.format(X_train_ros.shape))
print('After OverSampling, the shape of train_y: {} \n'.format(y_train_ros.shape))
print("After OverSampling, counts of label '1', %: {}".format(sum(y_train_ros==1)/len(y_train_ros)*100.0,2))
print("After OverSampling, counts of label '0', %: {}".format(sum(y_train_ros==0)/len(y_train_ros)*100.0,2))
sns.countplot(x=y_train_ros, data=df, palette='CMRmap')

"""#RUS"""

print('After Sampling using undersample, the shape of train_x: {}'.format(X_train_rus.shape))
print('After Sampling using undersample, the shape of train_y: {} \n'.format(y_train_rus.shape))
print("After Sampling using undersample, counts of label '1', %: {}".format(sum(y_train_rus==1)/len(y_train_rus)*100.0,2))
print("After Sampling using undersample, counts of label '0', %: {}".format(sum(y_train_rus==0)/len(y_train_rus)*100.0,2))

"""#SMOTE"""

print('After OverSampling using smomte, the shape of train_x: {}'.format(X_train_smote.shape))
print('After OverSampling using smomte, the shape of train_y: {} \n'.format(y_train_smote.shape))
print("After OverSampling using smomte, counts of label '1', %: {}".format(sum(y_train_smote==1)/len(y_train_smote)*100.0,2))
print("After OverSampling using smomte, counts of label '0', %: {}".format(sum(y_train_smote==0)/len(y_train_smote)*100.0,2))
sns.countplot(x=y_train_smote, data=df, palette='CMRmap')

"""# Logistic Regression with Resampled Data"""

# Fit a logistic regression model to our data
rus_model = LogisticRegression().fit(X_train_rus, y_train_rus)
ros_model = LogisticRegression().fit(X_train_ros, y_train_ros)
smote_model = LogisticRegression().fit(X_train_smote, y_train_smote)
blsmote_model = LogisticRegression().fit(X_train_blsmote, y_train_blsmote)

y_rus = rus_model.predict(X_test)
y_ros = ros_model.predict(X_test)
y_smote = smote_model.predict(X_test)
y_blsmote = blsmote_model.predict(X_test)

print('')
print('Classifcation report:\n', classification_report(y_test, y_rus))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_rus))
print('accuracyy :\n',accuracy_score(y_test,y_rus))

print('*'*25)

print('Classifcation report:\n', classification_report(y_test, y_ros))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_ros))
print('accuracyy :\n',accuracy_score(y_test,y_ros))

print('*'*25)

print('Classifcation report:\n', classification_report(y_test, y_smote))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_smote))
print('accuracyy :\n',accuracy_score(y_test,y_smote))
print('*'*25)

print('Classifcation report:\n', classification_report(y_test, y_blsmote))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_blsmote))
print('accuracyy :\n',accuracy_score(y_test,y_blsmote))
print('*'*25)

"""# Module 4: Decision Tree Classifier

"""

# Import the decision tree model from sklearn
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# Create the training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=0)

# Fit a logistic regression model to our data
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Obtain model predictions
y_predicted = model.predict(X_test)

# Calculate average precision 
average_precision = average_precision_score(y_test, y_predicted)

# Obtain precision and recall 
precision, recall, _ = precision_recall_curve(y_test, y_predicted)

# Plot the recall precision tradeoff
plot_pr_curve(recall, precision, average_precision)

# Print the classifcation report and confusion matrix
print('Classification report:\n', classification_report(y_test, y_predicted))
print('Confusion matrix:\n',confusion_matrix(y_true = y_test, y_pred = y_predicted))
print('accuracy :\n',accuracy_score(y_test,y_predicted))

"""#Decision Tree with RUS"""

rus_model = DecisionTreeClassifier().fit(X_train_rus, y_train_rus)
y_rus = rus_model.predict(X_test)
print('')
print('Classifcation report:\n', classification_report(y_test, y_rus))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_rus))
print('accuracyy :\n',accuracy_score(y_test,y_rus))

"""#Decision Tree with ROS"""

ros_model = DecisionTreeClassifier().fit(X_train_ros, y_train_ros)
y_ros = ros_model.predict(X_test)
print('Classifcation report:\n', classification_report(y_test, y_ros))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_ros))
print('accuracyy :\n',accuracy_score(y_test,y_ros))

"""#Decision Tree with SMOTE"""

smote_model = DecisionTreeClassifier().fit(X_train_smote, y_train_smote)
y_smote = smote_model.predict(X_test)
print('Classifcation report:\n', classification_report(y_test, y_smote))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_smote))
print('accuracyy :\n',accuracy_score(y_test,y_smote))

"""# Decision Tree Classifier with BLSMOTE Data"""

# Import the pipeline module we need for this from imblearn
from imblearn.pipeline import Pipeline 
from imblearn.over_sampling import BorderlineSMOTE

# Define which resampling method and which ML model to use in the pipeline
resampling = BorderlineSMOTE(kind='borderline-2',random_state=0) # instead SMOTE(kind='borderline2') 
model = DecisionTreeClassifier() 

# Define the pipeline, tell it to combine SMOTE with the Logistic Regression model
pipeline = Pipeline([('SMOTE', resampling), ('Decision Tree Classifier', model)])

# Fit your pipeline onto your training set and obtain predictions by fitting the model onto the test data 
pipeline.fit(X_train,y_train) 
y_predicted = pipeline.predict(X_test)

# Obtain the results from the classification report and confusion matrix 
print('Classifcation report:\n', classification_report(y_test, y_predicted))
print('Confusion matrix:\n',  confusion_matrix(y_true = y_test, y_pred = y_predicted))
print('accuracyy :\n',accuracy_score(y_test,y_predicted))

"""# Module 5: Random Forest Classifier"""

# Import the Random Forest Classifier model from sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,roc_auc_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# Create the training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=0)

# Fit a logistic regression model to our data
model = RandomForestClassifier(random_state=5)
model.fit(X_train, y_train)

# Obtain model predictions
y_predicted = model.predict(X_test)

# Predict probabilities
probs = model.predict_proba(X_test)

# Calculate average precision 
average_precision = average_precision_score(y_test, y_predicted)

# Obtain precision and recall 
precision, recall, _ = precision_recall_curve(y_test, y_predicted)

# Plot the recall precision tradeoff
plot_pr_curve(recall, precision, average_precision)

# Print the classifcation report and confusion matrix
print(accuracy_score(y_test, y_predicted))
print("AUC ROC score: ", roc_auc_score(y_test, probs[:,1]))

print('Classification report:\n', classification_report(y_test, y_predicted))
print('Confusion matrix:\n',confusion_matrix(y_true = y_test, y_pred = y_predicted))
print('accuracyy :\n',accuracy_score(y_test,y_predicted))

"""#Random Forest Classifier with RUS """

rus_model = RandomForestClassifier().fit(X_train_rus, y_train_rus)
y_rus = rus_model.predict(X_test)
print('')
print('Classifcation report:\n', classification_report(y_test, y_rus))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_rus))
print('accuracyy :\n',accuracy_score(y_test,y_rus))

"""#Random Forest Classifier with ROS"""

ros_model = RandomForestClassifier().fit(X_train_ros, y_train_ros)
y_ros = ros_model.predict(X_test)
print('Classifcation report:\n', classification_report(y_test, y_ros))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_ros))
print('accuracyy :\n',accuracy_score(y_test,y_ros))

"""#Random Forest Classifier with SMOTE """

smote_model = RandomForestClassifier().fit(X_train_smote, y_train_smote)
y_smote = smote_model.predict(X_test)
print('Classifcation report:\n', classification_report(y_test, y_smote))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_smote))
print('accuracyy :\n',accuracy_score(y_test,y_smote))

"""# Random Forest Classifier with BLSMOTE Data Catch Fraud"""

# Import the pipeline module we need for this from imblearn
from imblearn.pipeline import Pipeline 
from imblearn.over_sampling import BorderlineSMOTE

# Define which resampling method and which ML model to use in the pipeline

resampling = BorderlineSMOTE(kind='borderline-2',random_state=0) # instead SMOTE(kind='borderline2') 
model = RandomForestClassifier() 

# Define the pipeline, tell it to combine SMOTE with the Logistic Regression model
pipeline = Pipeline([('SMOTE', resampling), ('Random Forest Classifier', model)])

# Fit your pipeline onto your training set and obtain predictions by fitting the model onto the test data 
pipeline.fit(X_train, y_train) 
y_predicted = pipeline.predict(X_test)

# Predict probabilities
probs = model.predict_proba(X_test)

print(accuracy_score(y_test, y_predicted))
print("AUC ROC score: ", roc_auc_score(y_test, probs[:,1]))
# Obtain the results from the classification report and confusion matrix 

print('Classifcation report:\n', classification_report(y_test, y_predicted))
print('Confusion matrix:\n',  confusion_matrix(y_true = y_test, y_pred = y_predicted))
print('accuracy :\n',accuracy_score(y_test,y_predicted))

"""# Module 7: KMeans Clustering

## Prepare unlabeled train and test dataset
"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize

# Split the data into train set and test set
train,test = train_test_split(df,test_size=0.3,random_state=0)

# Get the arrays of features and labels in train dataset
features_train = train.drop(['Time','Class'],axis=1)
features_train = features_train.values
labels_train = pd.DataFrame(train[['Class']])
labels_train = labels_train.values

# Get the arrays of features and labels in test dataset
features_test = test.drop(['Time','Class'],axis=1)
features_test = features_test.values
labels_test = pd.DataFrame(test[["Class"]])
labels_test = labels_test.values

# Normalize the features in both train and test dataset
features_train = normalize(features_train)
features_test = normalize(features_test)

"""# Build the model"""

from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix

model = KMeans(n_clusters=2,random_state=0)
model.fit(features_train)
labels_train_predicted = model.predict(features_train)
labels_test_predicted = model.predict(features_test)

# Decide if model predicted label is aligned with true label 
true_negative,false_positive,false_negative,true_positive = confusion_matrix(labels_train,labels_train_predicted).ravel()
reassignflag = true_negative + true_positive < false_positive + false_negative
print(reassignflag)


labels_test_predicted = 1- labels_test_predicted

"""# Model Evaluation"""

from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score,f1_score
# Calculating confusion matrix for kmeans
print('Confusion Matrix:\n',confusion_matrix(labels_test,labels_test_predicted))

# Scoring kmeans

print('kmeans_precison_score:', precision_score(labels_test,labels_test_predicted))
print('kmeans_recall_score:', recall_score(labels_test,labels_test_predicted))
print('kmeans_accuracy_score:', accuracy_score(labels_test,labels_test_predicted))
print('kmeans_f1_score:',f1_score(labels_test,labels_test_predicted))

"""#K-Mean with RUS """

rus_model = KMeans(n_clusters=2).fit(X_train_rus, y_train_rus)
y_rus = rus_model.predict(X_test)
print('')
print('Classifcation report:\n', classification_report(y_test, y_rus))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_rus))
print('accuracyy :\n',accuracy_score(y_test,y_rus))

"""#K-Mean with ROS"""

ros_model = KMeans(n_clusters=2).fit(X_train_ros, y_train_ros)
y_ros = ros_model.predict(X_test)
print('Classifcation report:\n', classification_report(y_test, y_ros))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_ros))
print('accuracyy :\n',accuracy_score(y_test,y_ros))

"""#K-Mean with SMOTE"""

smote_model = KMeans(n_clusters=2).fit(X_train_smote, y_train_smote)
y_smote = smote_model.predict(X_test)
print('Classifcation report:\n', classification_report(y_test, y_smote))
print('Confusion matrix:\n', confusion_matrix(y_true = y_test, y_pred = y_smote))
print('accuracyy :\n',accuracy_score(y_test,y_smote))

"""# Module 8: MiniBatchKMeans Clustering"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize

# Split the data into train set and test set
train,test = train_test_split(df,test_size=0.3,random_state=0)

# Get the arrays of features and labels in train dataset
features_train = train.drop(['Time','Class'],axis=1)
features_train = features_train.values
labels_train = pd.DataFrame(train[['Class']])
labels_train = labels_train.values

# Get the arrays of features and labels in test dataset
features_test = test.drop(['Time','Class'],axis=1)
features_test = features_test.values
labels_test = pd.DataFrame(test[["Class"]])
labels_test = labels_test.values

# Normalize the features in both train and test dataset
features_train = normalize(features_train)
features_test = normalize(features_test)
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import confusion_matrix

model = MiniBatchKMeans(n_clusters=2,random_state=0)
model.fit(features_train)
labels_train_predicted = model.predict(features_train)
labels_test_predicted = model.predict(features_test)

# Decide if model predicted label is aligned with true label 
true_negative,false_positive,false_negative,true_positive = confusion_matrix(labels_train,labels_train_predicted).ravel()
reassignflag = true_negative + true_positive < false_positive + false_negative
print(reassignflag)

from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score,f1_score
# Calculating confusion matrix for kmeans
print('Confusion Matrix:\n',confusion_matrix(labels_test,labels_test_predicted))

# Scoring kmeans

print('kmeans_precison_score:', precision_score(labels_test,labels_test_predicted))
print('kmeans_recall_score:', recall_score(labels_test,labels_test_predicted))
print('kmeans_accuracy_score:', accuracy_score(labels_test,labels_test_predicted))
print('kmeans_f1_score:',f1_score(labels_test,labels_test_predicted))

"""# NEURAL NETWORK """

#Using neural networks 
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense,Activation,Flatten
from tensorflow.keras import Sequential
from keras.models import  Sequential
from keras.layers import Dense
from keras.layers import Dropout

classifier = Sequential([
    Dense(units =16,input_dim=30,activation='relu'),
    Dense(units =24,activation='relu'),
    Dense(units =20,activation='relu'),
    Dropout(0.5),
    Dense(units =21,activation='relu'),
    Dense(units =24,activation='relu'),
    Dense(1,activation='sigmoid')
])

classifier.summary()

"""#Training"""

y_train.shape

classifier.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
history=classifier.fit(X_train,y_train,batch_size=30,epochs=5,validation_data = (X_test,y_test))

score = classifier.evaluate(X_test,y_test)

print(score)

y_predicted = classifier.predict(X_test)

cnf_matrix = confusion_matrix(y_true = y_test, y_pred = y_predicted.round())
labels = ['Non-fraud', 'Fraud']
sns.heatmap(pd.DataFrame(cnf_matrix),xticklabels = labels, yticklabels = labels, annot=True, cmap="Reds", fmt='g')
plt.ylabel('Actual Label',size = 15)
plt.xlabel('Predicted Label',size = 15)
plt.title("Confusion Matrix Plotting for Neural Network", size = 20)

print('Classification report:\n', classification_report(y_test, y_predicted.round()))
print('accuracy :\n',accuracy_score(y_test,y_predicted.round()))

print(roc_auc_score(y_test, y_predicted))

fpr, tpr, thresholds = roc_curve(y_test,y_predicted)
plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.show()

"""#Neural Network Using RUS"""

classifier.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
history=classifier.fit(X_train_rus,y_train_rus,batch_size=30,epochs=5,validation_data = (X_test,y_test))

score = classifier.evaluate(X_test,y_test)
print(score)

y_predicted_rus = classifier.predict(X_test)

cnf_matrix = confusion_matrix(y_true = y_test, y_pred = y_predicted_rus.round())
labels = ['Non-fraud', 'Fraud']
sns.heatmap(pd.DataFrame(cnf_matrix),xticklabels = labels, yticklabels = labels, annot=True, cmap="Reds", fmt='g')
plt.ylabel('Actual Label',size = 15)
plt.xlabel('Predicted Label',size = 15)
plt.title("Confusion Matrix Plotting for Neural Network", size = 20)

print('Classification report:\n', classification_report(y_test, y_predicted_rus.round()))
print('accuracy :\n',accuracy_score(y_test,y_predicted_rus.round()))

print(roc_auc_score(y_test, y_predicted_rus))

fpr, tpr, thresholds = roc_curve(y_test,y_predicted_rus)
plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.show()

"""#Neural Network using ROS"""

classifier.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
history=classifier.fit(X_train_ros,y_train_ros,batch_size=30,epochs=5,validation_data = (X_test,y_test))

score = classifier.evaluate(X_test,y_test)
print(score)

y_predicted_ros = classifier.predict(X_test)

cnf_matrix = confusion_matrix(y_true = y_test, y_pred = y_predicted_ros.round())
labels = ['Non-fraud', 'Fraud']
sns.heatmap(pd.DataFrame(cnf_matrix),xticklabels = labels, yticklabels = labels, annot=True, cmap="Reds", fmt='g')
plt.ylabel('Actual Label',size = 15)
plt.xlabel('Predicted Label',size = 15)
plt.title("Confusion Matrix Plotting for Neural Network", size = 20)

print('Classification report:\n', classification_report(y_test, y_predicted_ros.round()))
print('accuracy :\n',accuracy_score(y_test,y_predicted_ros.round()))

print(roc_auc_score(y_test, y_predicted_ros))

fpr, tpr, thresholds = roc_curve(y_test,y_predicted_ros)
plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.show()

"""#Neural Network using SMOTE"""

classifier = Sequential([
    Dense(units =16,input_dim=30,activation='relu'),
    Dense(units =24,activation='relu'),
    Dense(units =20,activation='relu'),
    Dropout(0.5),
    Dense(units =21,activation='relu'),
    Dense(units =24,activation='relu'),
    Dense(1,activation='sigmoid')
])

classifier.summary()

classifier.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
history=classifier.fit(X_train_smote,y_train_smote,batch_size=30,epochs=5,validation_data = (X_test,y_test))

score = classifier.evaluate(X_test,y_test)

print(score)

y_predicted_smote = classifier.predict(X_test)

cnf_matrix = confusion_matrix(y_true = y_test, y_pred = y_predicted_smote.round())
labels = ['Non-fraud', 'Fraud']
sns.heatmap(pd.DataFrame(cnf_matrix),xticklabels = labels, yticklabels = labels, annot=True, cmap="Reds", fmt='g')
plt.ylabel('Actual Label',size = 15)
plt.xlabel('Predicted Label',size = 15)
plt.title("Confusion Matrix Plotting for Neural Network", size = 20)

print('Classification report:\n', classification_report(y_test, y_predicted_smote.round()))
print('accuracy :\n',accuracy_score(y_test,y_predicted_smote.round()))

print(roc_auc_score(y_test, y_predicted_smote))

fpr, tpr, thresholds = roc_curve(y_test,y_predicted_smote)
plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.show()

"""#Neural Network with BLSMOTE"""

classifier.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
history=classifier.fit(X_train_blsmote,y_train_blsmote,batch_size=30,epochs=5,validation_data = (X_test,y_test))

score = classifier.evaluate(X_test,y_test)
print(score)

y_predicted_blsmote = classifier.predict(X_test)

cnf_matrix = confusion_matrix(y_true = y_test, y_pred = y_predicted_blsmote.round())
labels = ['Non-fraud', 'Fraud']
sns.heatmap(pd.DataFrame(cnf_matrix),xticklabels = labels, yticklabels = labels, annot=True, cmap="Reds", fmt='g')
plt.ylabel('Actual Label',size = 15)
plt.xlabel('Predicted Label',size = 15)
plt.title("Confusion Matrix Plotting for Neural Network", size = 20)

print('Classification report:\n', classification_report(y_test, y_predicted_blsmote.round()))
print('accuracy :\n',accuracy_score(y_test,y_predicted_blsmote.round()))

print(roc_auc_score(y_test, y_predicted_blsmote))

fpr, tpr, thresholds = roc_curve(y_test,y_predicted_blsmote)
plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.show()

"""# naive bayes"""

# Naive Bayes
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
Model = GaussianNB()
Model.fit(X_train, y_train)
y_pred = Model.predict(X_test)

# Summary of the predictions made by the classifier
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
# Accuracy score

print('accuracy is',accuracy_score(y_pred,y_test))

"""#Naive Bayes with RUS"""

Model = GaussianNB()
Model.fit(X_train_rus, y_train_rus)
y_pred_rus = Model.predict(X_test)

# Summary of the predictions made by the classifier
print(classification_report(y_test, y_pred_rus))
print(confusion_matrix(y_test, y_pred_rus))
# Accuracy score

print('accuracy is',accuracy_score(y_pred_rus,y_test))

"""#Naive Bayes with ROS"""

Model = GaussianNB()
Model.fit(X_train_ros, y_train_ros)
y_pred_ros = Model.predict(X_test)

# Summary of the predictions made by the classifier
print(classification_report(y_test, y_pred_ros))
print(confusion_matrix(y_test, y_pred_ros))
# Accuracy score

print('accuracy is',accuracy_score(y_pred_ros,y_test))

"""# naive bayes smote"""

Model = GaussianNB()
Model.fit(X_train_smote, y_train_smote)
y_pred_smote = Model.predict(X_test)

# Summary of the predictions made by the classifier
print(classification_report(y_test, y_pred_smote))
print(confusion_matrix(y_test, y_pred_smote))
# Accuracy score

print('accuracy is',accuracy_score(y_pred_smote,y_test))

"""#Naive Bayes with BLSMOTE"""

Model = GaussianNB()
Model.fit(X_train_blsmote, y_train_blsmote)
y_pred_blsmote = Model.predict(X_test)

# Summary of the predictions made by the classifier
print(classification_report(y_test, y_pred_blsmote))
print(confusion_matrix(y_test, y_pred_blsmote))
# Accuracy score

print('accuracy is',accuracy_score(y_pred_blsmote,y_test))

"""# support vector machine"""

Model = SVC()
Model.fit(X_train, y_train)
y_pred = Model.predict(X_test)

# Summary of the predictions made by the classifier
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
# Accuracy score

print('accuracy is',accuracy_score(y_pred,y_test))

"""#Support Vector with RUS"""

Model = SVC()
Model.fit(X_train_rus, y_train_rus)
y_pred = Model.predict(X_test)

# Summary of the predictions made by the classifier
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
# Accuracy score

print('accuracy is',accuracy_score(y_pred,y_test))

"""#Support Vector with ROS"""

Model = SVC()
Model.fit(X_train_ros, y_train_ros)
y_pred = Model.predict(X_test)

# Summary of the predictions made by the classifier
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
# Accuracy score

print('accuracy is',accuracy_score(y_pred,y_test))

"""#Support Vector using SMOTE"""

Model = SVC()
Model.fit(X_train_smote, y_train_smote)
y_pred = Model.predict(X_test)

# Summary of the predictions made by the classifier
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
# Accuracy score

print('accuracy is',accuracy_score(y_pred,y_test))

"""#SVM with BLSMOTE"""

Model = SVC()
Model.fit(X_train_blsmote, y_train_blsmote)
y_pred = Model.predict(X_test)

# Summary of the predictions made by the classifier
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
# Accuracy score

print('accuracy is',accuracy_score(y_pred,y_test))

"""# Autoencoder """

from keras.layers import Input, Dense
from keras import regularizers
from keras.models import Model, load_model
from keras.callbacks import ModelCheckpoint, TensorBoard



input_dim = 30
encoding_dim = 14

input_layer = Input(shape=(input_dim))
encoder = Dense(encoding_dim, activation="tanh", 
                activity_regularizer=regularizers.l1(10e-5))(input_layer)
encoder = Dense(int(encoding_dim / 2), activation="relu")(encoder)

decoder = Dense(int(encoding_dim / 2), activation='tanh')(encoder)
decoder = Dense(input_dim, activation='relu')(decoder)

autoencoder = Model(inputs=input_layer, outputs=decoder)

autoencoder.compile(optimizer='adam',loss='mean_squared_error')

history = autoencoder.fit(X_train, X_train, epochs = 50, batch_size=16,
validation_data=(X_test,X_test)).history



plt.figure(figsize = (10,5))
plt.plot(history['loss'], label = 'Training Loss')
plt.plot(history['val_loss'], label = 'CV Loss')
plt.title("Model Loss")
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.grid()
plt.legend()
plt.show()

predictions = autoencoder.predict(X_test)

mse = np.mean(np.power(X_test - predictions,2), axis=1)
error = pd.DataFrame({'reconstruction_error': mse, 'actual_class': y_test.ravel()})

without_fraud = error[error.actual_class==0]
with_fraud = error[error.actual_class==1]

plt.figure(figsize=(16,5))

plt.subplot(1,2,1)
sns.distplot(without_fraud["reconstruction_error"])
plt.title("Reconstruction error without fraud")

plt.subplot(1,2,2)
sns.distplot(with_fraud["reconstruction_error"])
plt.title("Reconstruction error with fraud")

plt.show()

from sklearn.metrics import confusion_matrix
y_pred = [1 if e > 3 else 0 for e in error.reconstruction_error.values]
print('Confusion Matrix\n' + str(confusion_matrix(y_test, y_pred)))
print(classification_report(y_test, y_pred))
# Accuracy score
print('accuracy is',accuracy_score(y_pred,y_test))