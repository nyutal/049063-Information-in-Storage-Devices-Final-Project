#creating train set from f (taking only 10% of the line)
def create_training_set(f):
    train_set = open('runOrWalk_v1_train_set.dat', 'wb')
    with open(f) as fp:
        train_set_range = int(len(fp.readlines())*0.1)
        lines = fp.readline(train_set_range)
    fp.close()
    fp=open(f)
    for i in range(train_set_range):
            line=fp.readline()
            train_set.write(line)
    train_set.close()

create_training_set('runOrWalk_v1.csv')
