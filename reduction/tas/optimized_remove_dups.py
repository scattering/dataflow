import numpy as np

from .data_abstraction import Detector


def remove_duplicates_optimized(tas, distinct, not_distinct):
    """Removes the duplicate data rows from TripleAxis object tas whose distinct fields (columns)
    are in the list distinct, and nondistinct fields are in the list nondistinct"""

    numrows = tas.detectors.primary_detector.dimension[0]
    newtas = tas
    tuples = []
    indices = [] # list of lists of all duplicate indices to check
    first = True

    for field in distinct:
        if first:  # will only go in here the first time 
            for i in range(numrows):
                tuples.append((field.measurement[i].x, i)) #appending tuples pairing value with index

            tuples.sort()  #sorting by value

            samelist = False #signifies whether or not a different duplicate values were found
            index = -1

            for i in range(0, len(tuples)-1):
                if tuples[i+1][0] == tuples[i][0]:
                    if not samelist:
                        indices.append([tuples[i][1], tuples[i+1][1]]) #add array of duplicate indices
                        samelist = True
                        index += 1 #increment the index
                    else:
                        indices[index].append(tuples[i+1][1])
                else:
                    samelist = False
            first = False
        else:
            j = 0
            while j < len(indices):
                indexlist = indices.pop(j) #pop off the indices list at j
                tuples = []

                for index in indexlist: # O(n)
                    tuples.append((field.measurement[index].x, index))
                tuples.sort() # O(nlogn) hopefully

                samelist = False     
                dups = []
                for i in range(0, len(tuples)-1):
                    if tuples[i+1][0] == tuples[i][0]: # if values are same (duplicates)
                        if not samelist: 
                            #create dups --> list of duplicate indices
                            dups.append(tuples[i][1])
                            dups.append(tuples[i+1][1]) 
                            samelist = True
                        else:
                            dups.append(tuples[i+1][1])
                    else:
                        if len(dups) > 0: # if there is a list of duplicates, add them to indices
                            indices.insert(j, dups)
                            j += 1 # increment j
                            dups = [] # reset dups to be empty
                        samelist = False                            

    print len(indices)
    print indices
    if not first and len(indices) < 1:
        print "done"
        return newtas  # if there are no duplicates left, then every row is unique so we're done

    for field in not_distinct:
        if not type(field) == Detector: #don't check Detectors
            if first:
                # In the event that there are no distinct fields (ie only not_distinct fields)
                # This is the first segment, and will only run first.
                for i in range(numrows):
                    tuples.append((field.measurement[i].x, i)) #appending tuples pairing value with index
                tuples.sort() 

                samelist = False 
                index = -1

                for i in range(0, len(tuples)-1):
                    if tuples[i][0] == None or tuples[i+1][0] == None or (type(tuples[i][0]) == str or type(tuples[i][0]) == np.string_ or not hasattr(field, 'window')): 
                        # if no tolerance is specified or needed, directly compare:
                        if tuples[i+1][0] == tuples[i][0]:
                            if not samelist:
                                indices.append([tuples[i][1], tuples[i+1][1]]) #add array of duplicate indices
                                samelist = True
                                index += 1 #increment the index
                            else:
                                indices[index].append(tuples[i+1][1])
                        else:
                            samelist = False
                    else: # else use specified tolerance
                        if tuples[i+1][0] - tuples[i][0] <= field.window:
                            if not samelist:
                                indices.append([tuples[i][1], tuples[i+1][1]]) #add array of duplicate indices
                                samelist = True
                                index += 1 #increment the index
                            else:
                                indices[index].append(tuples[i+1][1])
                        else:
                            samelist = False
                first = False
            else:
                j = 0
                while j < len(indices):
                    indexlist = indices.pop(j)
                    tuples = []
                    for index in indexlist: # O(n)
                        tuples.append((field.measurement[index].x, index))
                    tuples.sort() # O(nlogn) hopefully

                    samelist = False
                    dups = []
                    for i in range(0, len(tuples)-1):
                        if tuples[i][0] == None or tuples[i+1][0] == None or type(tuples[i][0]) == str \
                           or type(tuples[i][0]) == np.string_ or not hasattr(field, 'window'):
                            if tuples[i+1][0] == tuples[i][0]: # if values are same (duplicates)
                                if not samelist:
                                    #create dups --> list of duplicate indices
                                    dups.append(tuples[i][1])
                                    dups.append(tuples[i+1][1])
                                    samelist = True
                                else:
                                    dups.append(tuples[i+1][1])
                            else:
                                if len(dups) > 0: # if there is a list of duplicates, add them to indices
                                    indices.insert(j, dups)
                                    j += 1 # increment j
                                    dups = [] # reset dups to be empty
                                samelist = False
                        else:
                            if tuples[i+1][0] - tuples[i][0] > field.window: # if values are different enough
                                if not samelist:
                                    #create dups --> list of duplicate indices
                                    dups.append(tuples[i][1])
                                    dups.append(tuples[i+1][1])
                                    samelist = True
                                else:
                                    dups.append(tuples[i+1][1])
                            else:
                                if len(dups) > 0: # if there is a list of duplicates, add them to indices
                                    indices.insert(j, dups)
                                    j += 1 # increment j
                                    dups = [] # reset dups to be empty
                                samelist = False


    # AVERAGING DETECTORS
    rows_to_be_removed = []
    for indexlist in indices:
        if len(indexlist) > 1: #if there are more than one rows that are duplicates
            for k in range(1, len(indexlist)):
                for detector in newtas.detectors:
                    # Average the first (0th) duplicate row's detectors with every other (kth) duplicate row's 
                    # detectors and save the result into the first duplicate row.
                    detector.measurement[indexlist[0]] = (detector.measurement[indexlist[0]] + detector.measurement[indexlist[k]]) / 2.0

                rows_to_be_removed.append(indexlist[k])
    # DONE AVERAGING DETECTORS

    rows_to_be_removed.sort() #duplicate rows to be removed indices in order now
    rows_to_be_removed.reverse() #duplicate rows to be removed indices in reverse order now

    for key, value in newtas.__dict__.iteritems():
        if key == 'data' or key == 'meta_data' or key == 'sample' or key == 'sample_environment':
            #ignoring metadata for now
            pass
        elif key.find('blade') >= 0:
            for blade in value.blades:
                for k in rows_to_be_removed:
                    blade.measurement.__delitem__(k) #removes duplicate row from this field (column)
        else:
            for field in value:
                for k in rows_to_be_removed:
                    print field.name
                    field.measurement.__delitem__(k) #removes duplicate row from this field (column)

    #update primary detector dimension
    newtas.detectors.primary_detector.dimension = [len(newtas.detectors.primary_detector.measurement.x), 1]
    return newtas




def remove_2D_duplicates(ex, ey, x, y):
    """ Removes dupcliate points (x,y) given lists of corresponding x and y values.
    Values considered equal if within a given epilson (ex, ey) range. """
    xtuples = []
    indices = []    # list of lists of all duplicate indices based on x values
    duplicateindices = []

    for i in range(0, len(x)):
        xtuples.append((x[i], i)) #appending tuples pairing value with index 
        #duplicateindices.append(i) # will be a list [0,1,2,...,len(x)-1]
    xtuples.sort()  #sorting by xvalue

    samelist = False #signifies if the index list is continuing or a set of different duplicate x's was found
    index = -1
    for i in range(0, len(xtuples)-1):
        if (xtuples[i+1][0] - xtuples[i][0]) <= ex: #if xvalues close enough
            if not samelist:
                indices.append([xtuples[i][1], xtuples[i+1][1]]) #add array of duplicate indices
                samelist = True
                index += 1 #increment the index
            else:
                indices[index].append(xtuples[i+1][1])
        else:
            samelist = False


    if y == None: # if 1D
        print indices
        for indexlist in indices:
            for i in range(1, len(indexlist)): #remove all indices except first in list
                duplicateindices.append(indexlist[i])

        duplicateindices.sort() #TODO find faster way then getting indices then sorting?

        for i in reversed(duplicateindices): #iterate through indices backwards
            del x[i]
    else:
        #handling y values
        for indexlist in indices:
            ytuples = []
            for index in indexlist:
                ytuples.append((y[index], index)) # tuples of y values with their associated index
            ytuples.sort()
            for i in range(0, len(ytuples)-1):
                if (ytuples[i+1][0] - ytuples[i][0]) <= ey: #if yvalues close enough
                    duplicateindices.append(ytuples[i+1][1]) # add index of next value (i+1)

        duplicateindices.sort() #TODO find faster way then getting indices then sorting?
        for i in reversed(duplicateindices):
            del x[i]
            del y[i]



if __name__ == "__main__":

    x = [4, 4, 6, 7, 8, 4, 9, 9, 9, 4]
    y = [3, 6, 4 ,1, 7, 3, 2, 1, 2, 3]
    #x = np.array([4, 4, 6, 7, 8, 4, 9, 9, 9])
    #y = np.array([3, 6, 4 ,1, 7, 3, 2, 1, 2])
    #y = None

    remove_2D_duplicates(.1, .1, x, y)
    print x
    print y
    _ = ''' testing code

    x = [[1, 2, 3], [4, 5, 6]]
    for a in x:
        try:
            a.remove(1)
            a.remove(7)
        except:
            pass
    print x
    '''


