from pylab import *

def getColumn(fileName, column):
    f = open(fileName)
    content = f.read()
    content =  [i.strip().split(',') for i in content.split('\n') if len(i) > 1 and i[0] != "#"]
    content = [array(i[0:], float) for i in content]

    toReturn = [i[column] for i in content if len(i) > column]
    return toReturn
    
epoch = getColumn('cell_type_count.dat', 0)
empty = getColumn('cell_type_count.dat', 1)
uninfected_sensitive =  getColumn('cell_type_count.dat', 2)
uninfected_resistant = getColumn('cell_type_count.dat', 3)
infected_sensitive = getColumn('cell_type_count.dat', 4)
infected_resistant = getColumn('cell_type_count.dat', 5)

plot(empty, label="Empty")
plot(uninfected_sensitive, label="Uninfected Susceptible")
plot(uninfected_resistant, label="Uninfected Unsusceptible")
plot(infected_sensitive, label="Infected Sensitive")
plot(infected_resistant, label= "Infected Resistant")
legend()
show()

