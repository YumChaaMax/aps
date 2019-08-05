# aps
本项目的目标：根据不同产线生产不同型号的不同速度，安排n(3)条产线的生产，减少整体工作时间（cost)

变量：
  x[i][(i,j,t)]  订单j (型号i) 在t时间完成生产（下线时间）-类型：binary  <br />
  h[i][(i,t)]    型号i 在t时间完成生产（下线时间）-类型：binary  <br />
  k[i][(i,l,m)]  辅佐变量，用于计算可变的生产速度 ，连续变量【0，1】  <br />
  f[i][(i,l)]    型号i在不同产线生产的比例  类型：continuous[0,1]  <br />
  ft[i][(i,l,t)]  型号i 在产线l 在t 时间完成    <br />
  z[i1][(i1,i2,t)]  辅佐变量，用来解决生产占用     <br />
  wt[i][(i,l,m)]   辅佐变量，用于表示ft 与 f的关系， 当f=0,ft必为0，f不为0，f=1   <br />
 
分3部分：
1. 处理数据（423行以前）：<br />
    将订单的信息按照型号与交付时间重新划分了新的型号，三个月内的相同型号的点订单放在一起生产。<br />
     以上同时做了一个维，用于计算每个型号在产线的速度（每天都不一样，指数增长）<br />
     num_by_day 是每天该产线该型号生产的产量，连续生产，速度会提高，所以每天产量不是恒定的，是指数增加的 （day_process 是连续生产的天数）<br />
     
     ![Image text](https://raw.githubusercontent.com/YumChaaMax/aps/master/img/productionSp.jpg)
2. Mixed Integer模型部分: 423行-598行    <br />
   速度计算使用了piecewise linear     <br />
    

3. 结果处理
  
