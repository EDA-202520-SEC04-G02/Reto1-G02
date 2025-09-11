def new_list():
    newlist = {
        'elements': [],
        'size': 0
    }
    return newlist

def get_element(my_list, index):

    return my_list["elements"][index]

def is_present(my_list,element,cmp_function):

    size = my_list["size"]
    if size > 0:
        keyexist = False
        for keypos in range(0,size):
            info = my_list["elements"][keypos]
            if cmp_function(element, info)== 0:
                keyexist = True
                break
        if keyexist:
            return keypos
    return -1

def add_first(my_list, element):
    my_list["elements"].insert(0, element)
    my_list["size"] += 1

def add_last(my_list, element):
    my_list["elements"].append(element)
    my_list["size"] += 1
    
def size(my_list):
    return my_list["size"]

def first_element(my_list):
    if my_list["size"] == 0:
        raise IndexError("list index out of range")
    return my_list["elements"][0]

def is_empty(my_list):
    if my_list["size"]== 0:
        return True
    return False

def last_element(my_list):
    if my_list["size"]== 0:
        raise IndexError("list index out of range")
    
    return my_list["elements"][-1]

def delete_element(my_list,pos):
    
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    
    remove = my_list["elements"].pop(pos)
    
    my_list["size"]-=1
    
    return my_list

def remove_first(my_list):
    if my_list["size"]==0:
        raise IndexError("list index out of range")
    
    remove= my_list["elements"].pop(0)
    my_list["size"]-=1
    
    return remove

def remove_last(my_list):
    if my_list["size"]== 0:
        raise IndexError("list index out of range")
    
    remove = my_list["elements"].pop()
    my_list["size"]-=1
    
    return remove

def insert_element(my_list,element,pos):
    
    my_list["elements"].insert(pos,element)
    
    my_list["size"]+=1
    
    return my_list

def change_info(my_list,pos,new_info):
    
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("list index out of range")
    
    my_list["elements"][pos]= new_info
    
    return my_list

def exchange(my_list,pos_1,pos_2):
    
    if pos_1 < 0 or pos_1 >= my_list["size"]:
        raise IndexError("list index out of range")
    
    if pos_2 < 0 or pos_2 >= my_list["size"]:
        raise IndexError("list index out of range")
    
    elemento1= my_list["elements"][pos_1]
    elemento2= my_list["elements"][pos_2]
    
    my_list["elements"][pos_1]=elemento2
    my_list["elements"][pos_2]=elemento1
    
    return my_list

def sub_list(my_list,pos_i,num_elements):
    
    if pos_i < 0 or pos_i >= my_list["size"]:
        raise IndexError("list index out of range")
    
    final= min(pos_i+num_elements, my_list["size"])
    
    new_list={"elements":[],"size":0}
    
    for i in range(pos_i,final):
        new_list["elements"].append(my_list["elements"][i])
        new_list["size"]+=1
    
    
    return new_list