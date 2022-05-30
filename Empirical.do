** For the do file to run, one needs to unzip the "cgss2017.dta.zip" file and feed the dta file into this do file
use "", clear
gen gender=a2
replace gender=0 if a2>=2
*汉=1，其他=0
gen ethnic=a4
replace ethnic=0 if a4==1
replace ethnic=1 if a4>=2
replace ethnic=1 if a4<=0
*从来没有参加宗教活动=0，一年不到一次～一年几次=1，以月计=2，以周记=3
gen religion=a51
replace religion=0 if a6<=1
replace religion=1 if a6>=2
replace religion=2 if a6>=5
replace religion=3 if a6>=7
*正规本科=15，成人高等教育本科=14，技校=职业高中=中专=高中=11，小学=5，初中=8，成人高等教育大专=12，研究生及以上=18，私塾/扫盲班=3，正规高等教育大专=13，未接受过教育=1
g edu=a7a
replace edu=150 if edu==12
replace edu=110 if edu==6
replace edu=50 if edu==3
replace edu=80 if edu==4
replace edu=110 if edu==7
replace edu=130 if edu==10
replace edu=1 if edu==1
replace edu=120 if edu==9
replace edu=180 if edu==13
replace edu=110 if edu==5
replace edu=140 if edu==11
replace edu=110 if edu==8
replace edu=3 if edu==2
replace edu=15 if edu==150
replace edu=11 if edu==110
replace edu=5 if edu==50
drop if edu==14
replace edu=8 if edu==80
replace edu=13 if edu==130
replace edu=12 if edu==120
replace edu=18 if edu==180
replace edu=14 if edu==140
replace edu=1 if edu==-8
*租房：有产权=1，无产权=0
g property=a128
replace property=1 if a128==0
replace property=0 if a128==1
*健康：很不健康=-2，比较不健康=-1，一般=0，比较健康=1，很健康=2
g health=a15
replace health=-2 if health==1
replace health=-1 if health==2
replace health=0 if health==3
replace health=1 if health==4
replace health=2 if health==5
replace health=0 if health>=98
*户口：农业户口=0，非农业户口=1
g hukou=a18
replace hukou=0 if hukou==1
replace hukou=1 if hukou>=0.1
replace hukou=1 if hukou<=-0.1
*户口1:农业户口=0，以前是农业户口=0，非农业户口=1，军籍/没有户口/蓝印户口=1
g hukou1=a18
replace hukou1=0 if a18==1
replace hukou1=0 if a18==4
replace hukou1=1 if a18==2
replace hukou1=1 if a18>=5
replace hukou1=1 if a18==3
*生活幸福：非常不幸福=-2，比较不幸福=-1，说不上=0，比较幸福=1，非常幸福=2
g happy=a36
replace happy=-2 if happy==1
replace happy=-1 if happy==2
replace happy=0 if happy==3
replace happy=1 if happy==4
replace happy=2 if happy==5
replace happy=0 if happy>=98
*养老：政府负责/老人自己负责=0.责任均摊=1
g support=a41
replace support=0 if support==1
replace support=0 if support==3
replace support=1 if support==4
replace support=1 if support>=98
proportion support
*男人事业女人家庭：完全不同意=-2～完全同意=2
g patriarchal=a421
replace patriarchal=-2 if patriarchal==1
replace patriarchal=-1 if patriarchal==2
replace patriarchal=0 if patriarchal==3
replace patriarchal=1 if patriarchal==4
replace patriarchal=2 if patriarchal==5
replace patriarchal=0 if patriarchal>=98
*您上一周是否为了取得收入而从事了一小时以上的劳动（包括参军）？未从事=停薪休假=0，带薪休假=工作=1
g work =a53
replace work=0 if a53==1
replace work=1 if a53==2
replace work=0 if a53==3
replace work=1 if a53==4
*工作时间：不工作=0，带薪休假=40，停薪休假=0，工作=a53a记载的工作时间
g worktime=a53
replace worktime=0 if a53==1
replace worktime=40 if a53==2
replace worktime=0 if a53==3
replace worktime=a53a if a53==4
*您目前是否参加了以下社会保障项目-城市/农村基本养老保险? 参加=1，没参加=0
g pension=a612
replace pension=1 if a612==1
replace pension=0 if a612==2
drop if pension >=7
*您目前是否参加了以下社会保障项目-商业性养老保险？参加=1，没参加=0
g compension=a614
replace compension=1 if a614==1
replace compension=0 if a614==2
*有几个儿子
g son=a681
drop if son==99
drop if son==21
*有几个女儿
g daughter=a682
replace son=0 if son==99
replace daughter=0 if daughter==99
drop if daughter >=9
g child=son+daughter
*婚姻：未婚=0，已婚=1
g marry=a69
replace marry=0 if a69==1
replace marry=1 if a69<=0.1
replace marry=1 if a69>=1.1
*配偶：初婚有配偶=再婚有配偶=同居=1，分居未离婚=未婚=丧偶=0
g partner=a69
replace partner=1 if a69==3
replace partner=1 if a69==4
replace partner=1 if a69==2
replace partner=0 if a69<=1
replace partner=0 if a69>=5
*工作经历：非农工作=1，目前没有工作,之前非农=1，目前务农,曾今非农=0,目前务农，没有过非农工作=0,目前没有工作，而且只务过农=0,从未工作过=0
g farm=a58
replace farm=1 if a58==1
replace farm=1 if a58==5
replace farm=0 if a58==2
replace farm=0 if a58==3
replace farm=0 if a58==4
replace farm=0 if a58==6
*您个人去年全年的总收入-您个人去年全年的职业/劳动收入
g nonincome=a8a-a8b
*您的出生日期-年
drop if a31>=1973
drop if a31<=1941
drop if pension<=-1
*drop收入为负数
replace a8b=0 if a8b<=0

codebook a54 if  a31==1967  & gender==0 & farm==1


drop if a31>=1968 & gender==1

logout, save(test2) tex replace: su work  child  pension  health gender ethnic edu property partner  happy support if farm==1

reg work   child pension health if farm==1,r
est store b1
reg work  child pension health gender ethnic edu property  partner  happy support   if farm==1,r
est store b2
logit work   child pension health if farm==1,r
est store b3
logit work  child pension health gender ethnic edu property  partner  happy support   if farm==1,r
est store b4
probit work  child pension health if farm==1,r
est store b5
probit work  child pension health gender ethnic edu property  partner  happy support   if farm==1,r
est store b6
outreg2 [b1 b2 b3 b4 b5 b6] using table6, tex dec(3) e(all)



