import pickle

def read_list(dump_file):
    with open(dump_file, "rb") as fp:
        pay_list = pickle.load(fp)
        return pay_list

dump_file = input("Type dump file:\t")
special_payload_list = read_list(dump_file)
print(len(special_payload_list))
