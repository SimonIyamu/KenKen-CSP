# KenKen-CSP
For information about the puzzle: http://en.wikipedia.org/wiki/KenKen

##### CSP Problem modeling:  
Variables: Cages  
Domain: Each cage's domain contains the values that can be given to it's cells.(e.x. a cage with goal sum=4 has {(1,3),(3,1),(2,2)} as a domain).  
Contraints: On any pair of variables A,B, there must not be a cell of cage A that is in the same row or column as a cell of cage B that has the same value as the cells of cage A.  

##### Notes:  
A puzzle is given as a tupple of strings.
The first string of the tupple, indicates the cage of each cell. The second and the third string show the goal number and the operation of each cage respectively. 

The csp class, which is imported, is from the aimacode project and can be found here: https://github.com/aimacode/aima-python/blob/master/csp.py  
It is required in order to run kenken.py.
