import random
# variable: (kalshi p for each threshold label), nested lines share a latent U
K={ # var:{line:kalshi_p}
'DET':{'ml':.80,'-1.5':.78},'PHI':{'ml':.71},'PHX':{'ml':.67},'WAS':{'ml':.46},
'Ayo':{'10':.90,'15':.72},'AyoA':{'2':.89},'Sarr':{'4':.84},'Wade':{'2':.88,'4':.70},
'NabR':{'3':.91,'4':.84},'Daniels':{'15':.84},'Naz':{'15':.81,'20':.54},'Gaff':{'10':.37},
'CP_u':{'220':.62},'NoInt':{'x':.55},'NabY':{'50':.71},'Tot':{'38.5':.59,'32.5':.77},
'Flagg':{'20':.75},'Kyrie':{'15':.87},'Cade':{'15':.95,'20':.76},'AD':{'15':.87},
'MINm':{'8.5':.61,'12.5':.73},'NYGm':{'6.5':.68,'7.5':.75},'Gob':{'8':.80},'AusA':{'2':.87},
'Sion':{'10':.38},'Fields':{'2':.67},'Skat':{'30':.90},'Maxey':{'15':.92},'AW':{'15':.82}}
# our grades where we have them (else Kalshi)
O={('DET','ml'):.80,('PHI','ml'):.72,('PHX','ml'):.75,('WAS','ml'):.47,('Ayo','10'):.85,('Ayo','15'):.56,('Sarr','4'):.80,('Wade','4'):.80,('Wade','2'):.93,
('NabR','3'):.74,('NabR','4'):.66,('Daniels','15'):.84,('Naz','15'):.72,('Naz','20'):.48,('Gaff','10'):.62,('CP_u','220'):.55,('NoInt','x'):.64,('NabY','50'):.50,
('Tot','38.5'):.62,('Tot','32.5'):.79,('Cade','20'):.82,('MINm','12.5'):.78,('NYGm','7.5'):.72,('Gob','8'):.80,('Sion','10'):.60,('Fields','2'):.78,('Skat','30'):.66,('AW','15'):.75}
T=[ # stake, payout, legs
(19.99,36.86,[('DET','ml'),('Ayo','10'),('Sarr','4'),('Wade','2'),('NabR','3'),('Daniels','15')]),
(19.95,1333.33,[('Naz','20'),('Gaff','10'),('Ayo','15'),('CP_u','220'),('WAS','ml'),('NoInt','x'),('NabY','50'),('Tot','38.5')]),
(34.98,365.34,[('PHX','ml'),('DET','ml'),('PHI','ml'),('Flagg','20'),('Kyrie','15'),('Cade','15'),('AD','15'),('MINm','8.5'),('NabR','3'),('NYGm','6.5')]),
(41.99,204.87,[('DET','ml'),('PHI','ml'),('Ayo','10'),('Wade','4'),('MINm','12.5'),('NabR','4'),('Daniels','15')]),
(79.98,175.70,[('PHI','ml'),('Naz','15'),('Sarr','4'),('AW','15')]),
(59.97,331.49,[('AusA','2'),('Sion','10'),('DET','-1.5'),('Fields','2'),('Skat','30')]),
(119.99,255.10,[('DET','ml'),('Ayo','10'),('Wade','4'),('Daniels','15')]),
(119.97,265.31,[('PHX','ml'),('Cade','20'),('Gob','8')]),
(100,381.53,[('AyoA','2'),('DET','ml'),('Naz','15'),('Ayo','10'),('Cade','20'),('Sarr','4'),('MINm','12.5'),('Daniels','15')]),
(123.76,305.10,[('DET','ml'),('PHI','ml'),('Ayo','10'),('Cade','20'),('Maxey','15'),('Wade','2')]),
(99.97,730.46,[('AusA','2'),('PHX','ml'),('DET','ml'),('PHI','ml'),('MINm','12.5'),('Daniels','15'),('NYGm','7.5'),('Tot','32.5')]),
]
def run(src,N=200000):
  stake=sum(t[0] for t in T); pos=0; tot=0; big=0; res=[]
  for _ in range(N):
    U={v:random.random() for v in K}
    pay=0
    for st,po,legs in T:
      if all(U[v]< (O.get((v,l),K[v][l]) if src=='ours' else K[v][l]) for v,l in legs): pay+=po
    net=pay-stake; tot+=net; pos+=net>0; res.append(net)
  res.sort()
  return stake, pos/N, tot/N, res[N//2], res[N//10], res[9*N//10]
for s in ('kalshi','ours'): print(s, [round(x,3) for x in run(s)])
def rec(p): return .93 if p>=.9 else .85 if p>=.7 else .67 if p>=.6 else p
O2={}
for v in K:
  for l in K[v]: O2[(v,l)]=rec(O.get((v,l),K[v][l]))
O.clear(); O.update(O2)
print('record', [round(x,3) for x in run('ours')])
# Pistons exposure
import collections
c=collections.Counter(); s=collections.Counter()
for st,po,legs in T:
  for v,l in set(legs): c[v]+=1; s[v]+=st
print(sorted(((s[v],c[v],v) for v in c),reverse=True)[:6])
