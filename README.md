##tmongo
### tmongo是什么?
> 模拟来实现mongodb的事务，暂时只支持insert, update, remove

### 拿两账号转账写个简单的例子，如果在转账过程中有异常，则会将更新的数据回滚回去, 代码如下

>        with db:
>            db.account.update({'user': 'a1'}, {"$inc": {'balance': -500}})
>            db.account.update({'user': 'a2'}, {"$inc": {'balance': 500}})
>            raise Exception