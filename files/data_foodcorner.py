import os

relative_path = 'foodcorner_recipedata/' # Adds relative path for recipe data

with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'A1.txt'),'r') as data_a1:
    a1 = data_a1.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'A2.txt'),'r') as data_a2:
    a2 = data_a2.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'A3.txt'),'r') as data_a3:
    a3 = data_a3.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'A4.txt'),'r') as data_a4:
    a4 = data_a4.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'A5.txt'),'r') as data_a5:
    a5 = data_a5.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'A6.txt'),'r') as data_a6:
    a6 = data_a6.read()
# ---------------------------------------------------------------- #
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'B1.txt'),'r') as data_b1:
    b1 = data_b1.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'B2.txt'),'r') as data_b2:
    b2 = data_b2.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'B3.txt'),'r') as data_b3:
    b3 = data_b3.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'B4.txt'),'r') as data_b4:
    b4 = data_b4.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'B5.txt'),'r') as data_b5:
    b5 = data_b5.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'B6.txt'),'r') as data_b6:
    b6 = data_b6.read()
# ---------------------------------------------------------------- #
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'C1.txt'),'r') as data_c1:
    c1 = data_c1.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'C2.txt'),'r') as data_c2:
    c2 = data_c2.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'C3.txt'),'r') as data_c3:
    c3 = data_c3.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'C4.txt'),'r') as data_c4:
    c4 = data_c4.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'C5.txt'),'r') as data_c5:
    c5 = data_c5.read()
with open(os.path.join(os.path.dirname(__file__),relative_path,\
    'C6.txt'),'r') as data_c6:
    c6 = data_c6.read()

food_dict = {'a1':a1,'a2':a2,'a3':a3,'a4':a4,'a5':a5,'a6':a6,
            'b1':b1,'b2':b2,'b3':b3,'b4':b4,'b5':b5,'b6':b6,
            'c1':c1,'c2':c2,'c3':c3,'c4':c4,'c5':c5,'c6':c6}
