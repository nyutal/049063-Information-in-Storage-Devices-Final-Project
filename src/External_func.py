import matplotlib.pyplot as plt
import os
import pandas as pd
plt.rcdefaults()
import numpy as np
import seaborn as sns
from IPython.display import display

###################################
#return data size in kB
###################################
def size_KB(x):
    return round(x / 8192.0, 2)
###################################
#convert csv/dat file to srting
###################################
def conv_file2str(f):
    str=''
    with open(f) as fp:
        for line in fp:
          str+=line
    return str

###################################
# create summary plot
#####################################
def plot(data_size_arr,title,labels,figure_i):

    fig = plt.figure(figure_i)
    fig.subplots_adjust(bottom=0.2)
    index = np.arange(len(data_size_arr))
    ax = sns.barplot()
    bar_width = 0.35

    rects = ax.bar(index, data_size_arr, bar_width, label=labels, align='center')
    ax.cla()

    for i in range(len(data_size_arr)):
        ax.bar(index[i], data_size_arr[i], bar_width, label=labels[i], align='center')
    plt.xticks([])
    #ax.set_xticklabels(['Original Data',"huffman- input alphabet1",\
    #                       "huffman- input alphabet2","huffman- input alphabet3"])

    bars_label(rects, ax)
    fig.set_size_inches(12.5, 8.5, forward=True)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True)
    plt.ylabel('Size[KB]')
    plt.title(title)
    fig_name=(title.replace(': ','_')).replace(' ','_')
    if not os.path.exists(".\..\output\Graphs"):
        os.makedirs(".\..\output\Graphs")
    plt.savefig("./../output/Graphs/"+fig_name+'.png')
    compress_ratio=[round(x/data_size_arr[0],2) for x in data_size_arr]
    print "Compression Ratio:",compress_ratio

###################################
#create labe to bars
###################################
def bars_label(rects, ax):
       # Get y-axis height to calculate label position from.
       (y_bottom, y_top) = ax.get_ylim()
       y_height = y_top - y_bottom

       for rect in rects:
           height = rect.get_height()
           label_position = height + (y_height * 0.01)
           ax.text(rect.get_x() + rect.get_width() / 2., label_position,
                   '%d' % int(height),
                   ha='center', va='bottom')

###################################
#Print dictionary
###################################

def pprint_code(dictionary):
    header = ['string','character']
    table = []
    for item in dictionary:

        table.append([item[0], item[1]])
    print_table(header, table)


def print_table(header, table):
    df = pd.DataFrame(table, columns=header)
    pd.options.display.max_columns = None
    display(df)

###################################
#create_training_set
###################################	
def create_training_set(f):
    train_set_name = f.rsplit('.', 1)[0]
    train_set = open(train_set_name+'_train_set.dat', 'wb')
    with open(f) as fp:
        train_set_range = int(len(fp.readlines())*0.1)
        lines = fp.readline(train_set_range)
    fp.close()
    fp=open(f)
    for i in range(train_set_range):
            line=fp.readline()
            train_set.write(line)
    train_set.close()



###################################
#create_training_set
###################################
def create_training_set_one_line(f):
    train_set_name = f.rsplit('.', 1)[0]
    train_set = open(train_set_name+"_train_set.dat", 'wb')
    with open(f) as fp:

        for line in fp:
                line=line[:len(line)//10]
                print line
                train_set.write(line)
    train_set.close()


def formating(str):
    str = str.replace("\"", "")
    if (str.endswith(',') == False):
        str = str + ","
    return str

def modified_mobile_location_history_file(file):
    output = (file.rsplit('.', 1)[0]).rsplit('\\', 1)[1]

    f = open("..\\modified_data_sets\\mobileLocationHistory102014\\"+ output +'_v1_columns.dat', 'wb')
    with open(file) as fp:
        for line in fp:
            sp_l = line.split()
            if sp_l[0] == "locations":
                print sp_l[0]
            if sp_l[0] in ("\"timestampMs\"", "\"latitudeE7\"", "\"longitudeE7\"", "\"accuracy\"","\"velocity\"" \
                           , "\"heading\"","\"altitude\""):
                sp_l[2] = formating(sp_l[2])
                f.write(sp_l[2])
            if sp_l[0] in ("\"activitys\""):
                sp_l = line.split()
                while not ((sp_l[0] == "},") and (line[:3] !='   ')):
                    line = fp.next()
                    sp_l = line.split()
                    print (line, "space number", line[:3])
                    print sp_l[0]
                    if sp_l[0] in ("\"timestampMs\"", "\"type\"", "\"confidence\""):
                        print sp_l[2]
                        sp_l[2] = formating(sp_l[2])
                        f.write(sp_l[2])
            if sp_l[0] == '},':
                f.write("\n")
        f.close()


# #Creating train_set (for csv file)
# create_training_set("..\modified_data_sets\\runOrWalk\\runOrWalk_v1.csv")
# create_training_set("'..\..\modified_data_sets\\nyc2016\\april2016_v1.csv")
#
# #Creating train_set to one line modified file(JSON)
# create_training_set_one_line("..\modified_data_sets\mobileLocationHistory102014\location_history_102014_v1.json")
# #Crating coulmns file from json -(work for specific data location_history_102014.json
# modified_mobile_location_history_file("..\data_sets\mobileLocationHistory102014\location_history_102014.json")
# create_training_set("..\modified_data_sets\mobileLocationHistory102014\location_history_102014_v1_columns.dat")
