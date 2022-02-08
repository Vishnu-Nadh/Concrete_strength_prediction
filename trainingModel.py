"""This is the entry point to training the model """

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from Data_Ingestion.train_data_loader import Data_Loader_Train
from Data_Preprocessing.preprocessTraindata import Preprocessor
from clustering.clustering import Data_Clustering
import logging
from application_logger.loggerConfigure import configure_logger


logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Training_Logs/trainingModel.log")

class Train_Model:
    """this class is used to train the model using the exported data from database"""
    def __init__(self):
        self.logger = logger
    
    def trainModel(self):
        """this function train and tune the model and saves models"""
        try:
            dataloader = Data_Loader_Train()
            data = dataloader.get_train_data()
            
            # data preprocessing
            preprocessor = Preprocessor(data)
            
            is_null_present, columns_with_nan = preprocessor.getColsWithNullValues()
            
            data = preprocessor.fillAllNanValues()
            self.logger.info("imputed all missing values in data")
            
            X, y = preprocessor.splitFeatureAndLabels(data)
            self.logger.info("data features and labels saperated")

            # clustering of data 
            kmeans = Data_Clustering()
            number_of_clusters = kmeans.createElbowPlot(X)
            self.logger.info(f"optimum number of clusters found as {number_of_clusters}")
            
            X = kmeans.createCluster(X, number_of_clusters)
            self.logger.info("Created clusters")
            
            #create a new column in the dataset consisting of the corresponding cluster assignments.
            X['Labels']=y

            # getting the unique clusters from our dataset
            list_of_clusters=X['Cluster'].unique()

            """parsing all the clusters and looking for the best ML algorithm to fit on individual cluster"""

            for i in list_of_clusters:
                cluster_data=X[X['Cluster']==i] # filter the data for one cluster
                
                # Prepare the feature and Label columns
                cluster_features=cluster_data.drop(['Labels','Cluster'],axis=1)
                cluster_label= cluster_data['Labels']
                
                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=0.2, random_state=36)

                x_train_scaled = preprocessor.standeredScalingData(x_train, f"scaler_{i}")
                x_test_scaled = preprocessor.standeredScalingData(x_train)
                
                
                
        except Exception as e:
            logger.exception(f"ERROR occured: {e}")
            raise e
        