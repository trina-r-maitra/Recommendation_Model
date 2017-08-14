import time
import numpy as np
import pandas as pd

class gst_item():
    
    def __init__(self):
        self.data = None
        self.nb_gst = 0
        self.nb_items = 0 
        self.probabilities = None
        self.top_n_recommendations_gsts = []
        self.nRec = 0
        
    def prepare_data(self, data):
        self.data = data
        self.data_np = np.array(data, dtype = 'int')
        self.nb_gst = len(np.unique(self.data_np[:,2]))
        self.nb_items = len(np.unique(self.data_np[:,1]))
        self.gst_lookup_table = np.unique(self.data_np[:,2])
        self.item_lookup_table = np.unique(self.data_np[:,1])
        self.item_item_similarity = np.zeros((self.nb_items, self.nb_items))
        self.counts = np.zeros((self.nb_gst, self.nb_items))
        
        #print "Number of Guests", self.nb_gst
        
        #self.probabilities = np.zeros(self.nb_gst, self.nb_items)
    
    def gst_item_matrix(self): 
        
        # Returns a np array that contains user: Item1 Item2 Item3 ... ItemN
        super_gst_item_list = []
        for i in self.gst_lookup_table:
        
            gst_item_list = []
            gst_item_list.append(i)
            items = self.data_np[np.where(self.data_np[:,2] == i)][:,1]
            
            for j in range(len(items)):
                gst_item_list.append(items[j])
            super_gst_item_list.append(gst_item_list)
        return super_gst_item_list   
        
    def load_matrix(self, collaborative):
        t0 = time.time()
        #counts = np.zeros((self.nb_gst, self.nb_items))
        total = 0.0
        num_zeros = self.nb_gst * self.nb_items

        for i, entry in enumerate(self.data_np): 
            
            gst = self.data_np[i][2]
            item = self.data_np[i][1]
            if self.data_np[i][0] <= 0:
                count = 0
            else:
                if (collaborative == 0):
                    count = 1 # self.data_np[i][0]
                else:
                    count = int(self.data_np[i][0])

            gst_id = int(np.where(self.gst_lookup_table == gst)[0][0])
            item_id = int(np.where(self.item_lookup_table == item)[0][0])
            
            #print gst_id, item_id
            self.counts[gst_id][item_id] = count
            total += count
            num_zeros -= 1
        alpha = num_zeros / total
        #print 'alpha %.2f' % alpha
        self.counts *= alpha
        t1 = time.time()
        #print 'Finished loading matrix in %f seconds' % (t1 - t0)
        return self.counts
    
    
        
    def get_probabilities(self, probabilities_data):
        self.probabilities = pd.DataFrame(data=probabilities_data, columns = self.item_lookup_table)
        self.probabilities.set_index(self.gst_lookup_table, drop=True, inplace=True)    

    
    # Get the top n recommendations for the gst
    def get_top_n_recommendations_gst(self, nRec):

        self.nRec = nRec
        for gst in self.gst_lookup_table:
            top_n_recommendations = self.probabilities.loc[gst,:].sort_values(ascending = False).iloc[0:self.nRec].keys()
            list_recommendations = []
            list_recommendations.append(gst)
            for i in range(nRec):
                list_recommendations.append(top_n_recommendations[i])   
            self.top_n_recommendations_gsts.append(list_recommendations)
    
        #self.top_n_recommendations_gsts    
    
    def get_top_n_popular_items(self, nTopItemsByOccurrence):
        popItems = self.data['item_i'].value_counts()
        array_indices = np.array(popItems.index.values)
        
        popItemsList = np.zeros((len(array_indices), 2))
        popItemsList[:,0] = array_indices
        popItemsList[:,1] = popItems
        
        #print popItemsList[0:nTopItemsByOccurrence,0]
        return popItemsList[0:nTopItemsByOccurrence,0]
     
    
    def item_item_collaborative_filtering(self):
        simvalue = 0.
        denom = 1.0
        simvalue = 0.0
        t0 = time.time()
        print self.nb_items
        for item_index_i in range(self.nb_items):
            for item_index_j in range(item_index_i, self.nb_items):
                
                item_vec_1 = np.array(self.counts[:, item_index_i])
                item_vec_2 = np.array(self.counts[:, item_index_j])
                
                dotProd = np.dot(item_vec_1, item_vec_2.T)
                #print dotProd
                denom = np.linalg.norm(item_vec_1, ord=2) * np.linalg.norm(item_vec_2, ord=2)
                #print denom
                
                simvalue = dotProd / denom
                #print simvalue
                self.item_item_similarity[item_index_i][item_index_j] = simvalue
                self.item_item_similarity[item_index_j][item_index_i] = simvalue
                #===============================================================
                # if (item_index_j % 1000 ==0):
                #     print item_index_j
                #===============================================================
            
            if (item_index_i % 1000 ==0):
                print item_index_i
        
        t1 = time.time()        
        df = pd.DataFrame(self.item_item_similarity)
        df.to_csv("Item-Item.csv")
        print "time: ", t1 - t0
                
                
                
                
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
