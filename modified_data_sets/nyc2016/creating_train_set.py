import os.path

def convert_csv_to_dat(file):
    dat_file=os.path.splitext(file)[0]+".dat"
    print dat_file
    dat_file = open(dat_file, 'wb')
    with open(file) as f:
        for line in f:
            dat_file.write(line)
    dat_file.close()

def create_training_set(file):
    train_set_name=os.path.splitext(file)[0]+"_train_set.dat"
    train_set = open(train_set_name, 'wb')
    with open(file) as fp:
        train_set_range = int(len(fp.readlines())*0.1)
        lines = fp.readline(train_set_range)
    fp.close()
    fp=open(file)
    for i in range(train_set_range):
            line=fp.readline()
            train_set.write(line)
    train_set.close()


################################################################
convert_csv_to_dat('april2016_v1.csv')
create_training_set('april2016_v1.csv')



