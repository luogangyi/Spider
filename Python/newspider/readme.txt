BaseBBS是所有bbs论坛的基类，该基类的实现是用于处理“凤凰山下论坛”，对于其他的论坛，可通过继承该基类实现。
根据论坛情况，重写相应的函数。

目前用“凤凰山下论坛”和“开县乡情论坛 ”作为例子，见bbs_dz19.py,bbs_cqkx.py。

BaseTimeLimit 是在BaseBBS的基础上增加了“根据时间比较来退出循环的功能”，通常如果查找出来的结果是按时间排序的，请继承BaseTimeLimit而不是BaseBBS。如果不是按时间排序的，请直接继承BaseBBS。


已完成网站，请看数据库info_sources表



