	org 0
A           0      
B           0      
X           0      
PC          0      
            load   A,0
            store  A,LAB030
            load   A,1
            store  A,LAB031
            store  X,0
LAB014      load   A,LAB030+X
            add    A,LAB031+X
            skp    1,0,OCA
            nop    
            halt   
            store  A,LAB032+X
            store  A,OUTPUT
            add    X,1
            jmp    LAB014
LAB030      0      
LAB031      0      
LAB032      0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
OUTPUT      0      
OCA         0      
OCB         0      
OCX         0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
            0      
INPUT       0      
