           org      0
A          0        
B          0        
X          0        
PC         4        
           load     A,INPUT
           jmk      LAB133
           store    A,LAB094
           halt     
           load     A,INPUT
           jmk      LAB133
           store    A,LAB095
           halt     
           load     A,INPUT
           jmk      LAB133
           sub      A,1
           store    A,LAB096
           halt     
           load     A,INPUT
           jmk      LAB133
           store    A,LAB097
           load     A,128
           store    A,LAB111
           load     A,LAB095
           sft      A,R,2
           store    A,B
           add      B,LAB097
           load     X,LAB096
           add      B,LAB098+X
           jmk      LAB156
           jmk      LAB112
           sub      B,A
           jmk      LAB189
           jmk      LAB112
           add      B,A
           add      B,LAB095
LAB062     load     A,B
           and      A,248
           jmp      A,EQ,LAB074
           sub      B,7
           jmk      LAB112
           jmp      LAB062
LAB074     load     A,B
           sub      A,7
           jmp      A,LT,LAB082
           load     B,0
LAB082     load     X,B
           load     A,LAB243+X
           store    A,OUTPUT
           halt     
LAB089     load     A,255
           store    A,OUTPUT
           halt     
LAB094     0        
LAB095     0        
LAB096     0        
LAB097     0        
LAB098     1        
           4        
           4        
           0        
           2        
           5        
           0        
           3        
           6        
           1        
           4        
           6        
LAB110     0        
LAB111     0        
LAB112     0        
           store    A,LAB110
           load     A,LAB111
           store    A,OUTPUT
           rot      A,R,1
           store    A,LAB111
           load     A,LAB110
           jmp      (LAB112)
           0        
           0        
OUTPUT     0        
OCA        0        
OCB        0        
OCX        0        
           0        
LAB133     0        
           store    A,X
           sft      A,R,4
           jmk      LAB228
           store    A,B
           add      B,B
           sft      A,L,3
           add      B,A
           store    X,A
           and      A,15
           jmk      LAB228
           add      A,B
           jmp      (LAB133)
LAB156     0        
           load     A,LAB096
           and      A,254
           jmp      A,NE,LAB185
           load     A,LAB095
           jmp      A,NE,LAB175
           load     A,LAB094
           and      A,3
           jmp      A,EQ,LAB181
           jmp      LAB185
LAB175     load     A,LAB095
           and      A,3
           jmp      A,NE,LAB185
LAB181     load     A,1
           jmp      (LAB156)
LAB185     load     A,0
           jmp      (LAB156)
LAB189     0        
           load     A,LAB094
LAB192     sub      A,17
           jmp      A,GE,LAB204
           load     A,LAB094
           add      A,4
           store    A,LAB094
           jmp      LAB192
LAB204     load     A,LAB094
LAB206     sub      A,20
           jmp      A,LT,LAB220
           jmp      A,EQ,LAB220
           load     A,LAB094
           sub      A,4
           store    A,LAB094
           jmp      LAB206
LAB220     load     X,LAB094
           sub      X,17
           load     A,LAB250+X
           jmp      (LAB189)
LAB228     0        
           store    A,LAB110
           load     A,9
           sub      A,LAB110
           and      A,128
           jmp      A,NE,LAB089
           load     A,LAB110
           jmp      (LAB228)
LAB243     2        
           128      
           64       
           32       
           16       
           8        
           4        
LAB250     4        
           2        
           0        
           6        
           0        
INPUT      0        
