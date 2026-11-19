import json
d=json.load(open('study/nov10.json'))
R={0:'L',1:'V',2:'W',3:'W',4:'L',5:'L',6:'P',7:'P',8:'L',9:'L',10:'W',11:'W',12:'W',13:'L',14:'W',15:'P',
16:'W',17:'L',18:'W',19:'W',20:'W',21:'W',22:'W',23:'W',24:'W',25:'L',26:'L',27:'P',28:'P',29:'V',30:'V',31:'V',
32:'W',33:'L',34:'W',35:'L',36:'W',37:'P',38:'P',39:'P',40:'P',41:'P',42:'W',43:'L',44:'W',45:'L',46:'W',47:'L',
48:'V',49:'V',50:'L',51:'W',52:'W',53:'W',54:'W',55:'W',56:'P',57:'W',58:'W',59:'W',60:'W',61:'W',62:'L',63:'W',
64:'W',65:'W',66:'P',67:'P',68:'P',69:'L',70:'W',71:'L',72:'L',73:'W',74:'W',75:'P',76:'P',77:'W',78:'W',79:'W'}
A={0:'Brown under 15',2:'Maluach 6+',3:'RW3 4 reb',4:'KAT 2 threes',8:'Clingan 13',9:'Clingan 13',10:'Clingan 13 reb',11:'Caruso 1 ast',12:'Caruso 1 ast',
13:'KAT 2 threes',14:'KAT 2 threes',16:'Tatum 21',17:'Brown under 15',18:'Maxey 24',19:'Embiid 6 reb',20:'Brunson 23',21:'KAT 21',22:'MIA 115-109',23:'PHX 133-110',24:'ORL 107-100',25:'POR 123-103',26:'BOS 123-101',
32:'Bailey 15+',33:'Maxey 4 ast',34:'Acuff 4 reb',35:'Cain 3 reb',36:'Bam 8 reb',42:'TTU 84-78',43:'UTM 82-65',44:'FRES 95-92',45:'KU 89-69',46:'USF 63-58',47:'Tatum 6 reb',50:'Rui 13',51:'Rui 13',52:'Deni 2 threes',53:'Deni 2 threes',
54:'BGSU 33-28',55:'M-OH 34-17',57:'Peterson 25',58:'Peterson 25',59:'Acuff 4 threes',60:'Acuff 4 threes',61:'Acuff 4 threes',62:'LAC lost by 23',63:'SAC lost by 7',64:'KU 89-69',65:'158 total',69:'Franz 7 ast',70:'Acuff 6 ast',71:'Brunson 2 ast',72:'Giannis 4 ast',73:'Deni 8 ast',74:'Maluach 6+',77:'Bailey 15+',78:'Tatum 6 reb',79:'Franz 7 ast'}
for i,x in enumerate(d): x['r']=R[i]; x['act']=A.get(i,'')
json.dump(d,open('study/nov10_graded.json','w'))
g=[x for x in d if x['r'] in 'WL']
def tier(lo,hi):
  s=[x for x in g if lo<=x['pct']<hi]; w=sum(x['r']=='W' for x in s); return w,len(s)
for lo,hi in [(90,101),(80,90),(70,80),(60,70),(45,60),(0,45)]:
  print(lo,hi,tier(lo,hi))
w=sum(x['r']=='W' for x in g);print('all',w,len(g)); s=[x for x in g if x['pct']>=70];print('70+',sum(x['r']=='W' for x in s),len(s))
print('pending',[x['p'] for x in d if x['r']=='P'])
# fades: pct<45 losing = model right
print('misses 70+',[(x['p'],x['pct']) for x in s if x['r']=='L'])
