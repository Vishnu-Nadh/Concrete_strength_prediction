from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from kneed import KneeLocator
from File_Operations.fileOperations import File_Operations

import logging
from application_logger.loggerConfigure import configure_logger

logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Training_Logs/clusteringTrainData.log")


class Data_Clustering:
    """this class used to cluster the data set using k means clustering and return the clusters"""

    def __init__(self):
        self.logger = logger

    def createCluster(self, data, number_of_clusters):
        """this method create the clusters of data based the number of clusters provided

        Args:
            data (dataframe): input data for clustering
            number_of_clusters (integer): number of clusters to be formed
        """
        self.data = data
        try:
            kmeans = KMeans(
                n_clusters=number_of_clusters, init="k-means++", random_state=42
            )
            self.y_kmeans = kmeans.fit_predict(self.data)

            fileop = File_Operations()
            fileop.saveModel(kmeans, "KMeans")
            self.data["Cluster"] = self.y_kmeans
            self.logger.info(
                f"Created {self.kn.knee} clusters. model saved to model directory"
            )

            return self.data

        except Exception as e:
            self.logger.info(f"{e}")
            raise e

    def createElbowPlot(self, data):
        """this method create elbow plot for the given data and saves the plot in local directory
        also outputs optiminum number of clusters

        Args:
            data (dataframe): data to be clusterd

        Returns:
            number`: optimum number of cluster for given data
        """
        wcss = []
        try:
            for i in range(1, 11):
                kmeans = KMeans(
                    n_clusters=i, init="k-means++", random_state=42
                )  # initializing the KMeans object
                kmeans.fit(data)  # fitting the data to the KMeans Algorithm
                wcss.append(kmeans.inertia_)

            plt.plot(
                range(1, 11), wcss
            )  # creating the graph between WCSS and the number of clusters
            plt.title("The Elbow Method")
            plt.xlabel("Number of clusters")
            plt.ylabel("WCSS")
            # plt.show()
            plt.savefig("clustering/K-Means_Elbow.PNG")  # saving the elbow plot locally
            # finding the value of the optimum cluster programmatically
            self.kn = KneeLocator(
                range(1, 11), wcss, curve="convex", direction="decreasing"
            )
            self.logger.info(
                f"optimum number of clusters found as {self.kn.knee} and elbow curve plotted"
            )

            return self.kn.knee

        except Exception as e:
            self.logger.exception(f"{e}")
            raise e
