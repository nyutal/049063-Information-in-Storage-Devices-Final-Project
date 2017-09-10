import sys, re
import numpy


def create_training_set(f):
    train_set = open('location_history_102014_v1_train_set.dat', 'wb')
    with open(f) as fp:

        for line in fp:
                line=line[:len(line)//10]
                print line
                train_set.write(line)
    train_set.close()


def create_training_set_columns(f):
    train_set = open('location_history_102014_v1_columns_train_set.dat', 'wb')
    with open(f) as fp:
        train_set_range = int(len(fp.readlines())*0.1)
        lines = fp.readline(train_set_range)
    fp.close()
    fp=open(f)
    for i in range(train_set_range):
            line=fp.readline()
            print line
            train_set.write(line)
    train_set.close()

def formating(str):
    str = str.replace("\"", "")
    if (str.endswith(',') == False):
        str = str + ","
    return str

def modified_file(file):
    f = open('location_history_102014_v1_columns.dat', 'wb')
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


#################################################################

create_training_set('location_history_102014_v1.json')
modified_file('strip_location_history_102014.json')
create_training_set_columns('location_history_102014_v1_columns.dat')


